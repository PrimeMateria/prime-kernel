#!/usr/bin/env node
/**
 * Core Hologram WebAssembly Runtime Microbenchmark
 * High-resolution V8 microbenchmark engine for holo_alloc and holo_run.
 */

import fs from 'node:fs';
import path from 'node:path';

function computeStats(samplesNs) {
  if (samplesNs.length === 0) return null;
  // Sort for percentile calculation
  const sorted = Float64Array.from(samplesNs).sort();
  const n = sorted.length;
  const minNs = sorted[0];
  const maxNs = sorted[n - 1];

  let sumNs = 0;
  for (let i = 0; i < n; i++) {
    sumNs += sorted[i];
  }
  const meanNs = sumNs / n;

  let varianceSum = 0;
  for (let i = 0; i < n; i++) {
    const diff = sorted[i] - meanNs;
    varianceSum += diff * diff;
  }
  const stddevNs = Math.sqrt(varianceSum / n);

  const p50Ns = sorted[Math.floor(n * 0.50)];
  const p90Ns = sorted[Math.floor(n * 0.90)];
  const p99Ns = sorted[Math.floor(n * 0.99)];
  const totalSec = sumNs / 1e9;
  const opsPerSec = totalSec > 0 ? n / totalSec : 0;

  return {
    samples: n,
    min_us: +(minNs / 1000).toFixed(3),
    max_us: +(maxNs / 1000).toFixed(3),
    mean_us: +(meanNs / 1000).toFixed(3),
    stddev_us: +(stddevNs / 1000).toFixed(3),
    p50_us: +(p50Ns / 1000).toFixed(3),
    p90_us: +(p90Ns / 1000).toFixed(3),
    p99_us: +(p99Ns / 1000).toFixed(3),
    ops_per_sec: +opsPerSec.toFixed(0),
    total_duration_ms: +(sumNs / 1e6).toFixed(2)
  };
}

async function runBenchmarks() {
  const wasmPath = process.argv[2];
  const modelPath = process.argv[3];
  const iterations = parseInt(process.argv[4] || '10000', 10);
  const warmup = parseInt(process.argv[5] || '1000', 10);

  if (!wasmPath || !fs.existsSync(wasmPath)) {
    console.error(`Error: WASM file not found at: ${wasmPath}`);
    process.exit(1);
  }
  if (!modelPath || !fs.existsSync(modelPath)) {
    console.error(`Error: Model JSON not found at: ${modelPath}`);
    process.exit(1);
  }

  const wasmBuffer = fs.readFileSync(wasmPath);
  const wasmModule = new WebAssembly.Module(wasmBuffer);
  const model = JSON.parse(fs.readFileSync(modelPath, 'utf8'));
  const vectors = model.application.acceptance_vectors;

  // 1. Cold Instantiation Benchmark (Module -> Instance + run)
  const coldSamples = 100;
  const coldDurationsNs = new Float64Array(coldSamples);
  const v0Req = Buffer.from(vectors[0].request);

  for (let i = 0; i < coldSamples; i++) {
    const t0 = process.hrtime.bigint();
    const inst = new WebAssembly.Instance(wasmModule, {});
    const { memory, holo_alloc, holo_run } = inst.exports;
    const offset = holo_alloc(v0Req.length);
    new Uint8Array(memory.buffer).set(v0Req, offset);
    holo_run(offset, v0Req.length);
    const t1 = process.hrtime.bigint();
    coldDurationsNs[i] = Number(t1 - t0);
  }
  const coldStats = computeStats(coldDurationsNs);

  // 2. Memory Allocation Microbenchmark (holo_alloc)
  // Note: Prism guest allocator is bump-only with a 128B pool limit; each allocation
  // is measured on a fresh instance to avoid pool exhaustion.
  const allocSizes = [0, 3, 32, 64, 128];
  const allocBenchmarks = {};

  for (const size of allocSizes) {
    const allocSamples = new Float64Array(Math.min(iterations, 2000));
    for (let i = 0; i < allocSamples.length; i++) {
      const inst = new WebAssembly.Instance(wasmModule, {});
      const t0 = process.hrtime.bigint();
      inst.exports.holo_alloc(size);
      const t1 = process.hrtime.bigint();
      allocSamples[i] = Number(t1 - t0);
    }
    allocBenchmarks[`alloc_${size}B`] = computeStats(allocSamples);
  }

  // 3. Vector Invocation Microbenchmarks
  // Every request executes against a fresh isolated guest instance per the Prism contract.
  const vectorBenchmarks = [];
  const testIterations = Math.min(iterations, 5000);

  for (let idx = 0; idx < vectors.length; idx++) {
    const v = vectors[idx];
    const req = Buffer.from(v.request);
    const expected = Buffer.from(v.response);

    // Warmup
    for (let w = 0; w < Math.min(warmup, 200); w++) {
      const inst = new WebAssembly.Instance(wasmModule, {});
      const off = inst.exports.holo_alloc(req.length);
      new Uint8Array(inst.exports.memory.buffer).set(req, off);
      inst.exports.holo_run(off, req.length);
    }

    const samplesNs = new Float64Array(testIterations);
    let verifiedExact = true;

    for (let i = 0; i < testIterations; i++) {
      const t0 = process.hrtime.bigint();
      const inst = new WebAssembly.Instance(wasmModule, {});
      const off = inst.exports.holo_alloc(req.length);
      new Uint8Array(inst.exports.memory.buffer).set(req, off);
      const packed = BigInt.asUintN(64, inst.exports.holo_run(off, req.length));
      const resOff = Number(packed >> 32n);
      const resLen = Number(packed & 0xffffffffn);
      const actual = Buffer.from(inst.exports.memory.buffer, resOff, resLen);
      const t1 = process.hrtime.bigint();
      samplesNs[i] = Number(t1 - t0);

      if (i === 0 && !actual.equals(expected)) {
        verifiedExact = false;
      }
    }

    const stats = computeStats(samplesNs);
    vectorBenchmarks.push({
      vector_index: idx + 1,
      name: `vector_${idx + 1}_req_${req.length}B`,
      request_len: req.length,
      response_len: expected.length,
      verified_exact: verifiedExact,
      stats
    });
  }

  const results = {
    iterations,
    warmup,
    wasm_size_bytes: wasmBuffer.length,
    cold_instantiation: coldStats,
    allocation: allocBenchmarks,
    vectors: vectorBenchmarks
  };

  console.log(JSON.stringify(results, null, 2));
}

runBenchmarks().catch(err => {
  console.error(err);
  process.exit(1);
});
