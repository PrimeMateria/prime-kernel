const INPUT_LIMIT=64;
const OUTPUT_LIMIT=256;
const INPUT_ERROR="Invalid request";
const RESPONSE_ERROR="Invalid response";
const form = document.getElementById('application-form');
const request = document.getElementById('request');
const submit = document.getElementById('submit');
const result = document.getElementById('result');
const encoder = new TextEncoder();
// Preserve a leading U+FEFF: it is application data, not a transport BOM.
const decoder = new TextDecoder('utf-8', {fatal: true, ignoreBOM: true});
let busy = false;
let displayed = false;

// Validate before TextEncoder allocates; never replace malformed UTF-16.
function boundedText(value, limit) {
  if (typeof value !== 'string' || value.length > limit) return false;
  let bytes = 0;
  for (let index = 0; index < value.length; index++) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      if (++index >= value.length) return false;
      const low = value.charCodeAt(index);
      if (low < 0xdc00 || low > 0xdfff) return false;
      bytes += 4;
    } else if (unit >= 0xdc00 && unit <= 0xdfff) {
      return false;
    } else {
      bytes += unit < 0x80 ? 1 : unit < 0x800 ? 2 : 3;
    }
    if (bytes > limit) return false;
  }
  return true;
}

function show(value) { displayed = true; result.textContent = value; }
// A delayed initialization must not erase a validation error already shown.
function clearInitialStatus() { if (!displayed) result.textContent = ''; }

function attach(invoke) {
  // Install cancellation before any path can submit. HTML stays disabled if
  // this module never executes; CSP independently denies native navigation.
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    const value = request.value;
    if (!boundedText(value, INPUT_LIMIT)) {
      request.setAttribute('aria-invalid', 'true');
      show(INPUT_ERROR);
      request.focus();
      return;
    }
    request.removeAttribute('aria-invalid');
    busy = true;
    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    try {
      const answer = await invoke(value);
      if (!boundedText(answer, OUTPUT_LIMIT)) throw new Error('response text');
      show(answer);
    } catch (_) {
      show(RESPONSE_ERROR);
    } finally {
      busy = false;
      submit.disabled = false;
      form.removeAttribute('aria-busy');
    }
  });
  request.addEventListener('keydown', event => {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey) && !event.isComposing) {
      event.preventDefault();
      if (!busy) form.requestSubmit();
    }
  });
  submit.disabled = false;
}

// Only the Hologram transport envelope is parsed, never application payloads.
// JSON can escape each payload byte as six ASCII bytes. Bound its envelope
// before decoding/parsing; streaming also handles absent Content-Length.
async function envelope(response) {
  if (!response.ok || !response.body) throw new Error('intent response');
  const maximum = OUTPUT_LIMIT * 6 + 256;
  const length = response.headers.get('content-length');
  if (length !== null && (!/^[0-9]+$/.test(length) || Number(length) > maximum)) {
    await response.body.cancel();
    throw new Error('intent size');
  }
  const reader = response.body.getReader();
  const decode = new TextDecoder('utf-8', {fatal: true, ignoreBOM: true});
  let total = 0;
  let text = '';
  try {
    for (;;) {
      const {done, value} = await reader.read();
      if (done) break;
      if (!(value instanceof Uint8Array) || value.byteLength > maximum - total) {
        throw new Error('intent size');
      }
      total += value.byteLength;
      text += decode.decode(value, {stream: true});
    }
    text += decode.decode();
    return JSON.parse(text);
  } catch (error) {
    await reader.cancel();
    throw error;
  } finally {
    reader.releaseLock();
  }
}
attach(async value => {
  const response = await fetch('/_hologram/intent', {
    method: 'POST',
    headers: {'content-type': 'application/json'},
    body: JSON.stringify({version: 1, name: 'application.invoke', payload: value})
  });
  const answer = await envelope(response);
  if (answer === null || answer.version !== 1 || !Array.isArray(answer.outputs) || answer.outputs.length !== 1) {
    throw new Error('intent envelope');
  }
  return answer.outputs[0];
});
clearInitialStatus();
