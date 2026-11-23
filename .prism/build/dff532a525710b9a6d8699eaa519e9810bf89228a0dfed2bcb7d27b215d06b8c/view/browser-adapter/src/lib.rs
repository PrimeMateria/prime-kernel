use wasm_bindgen::prelude::*;

// Transport copies allocate only after their byte limits are checked.
// The core's own allocation bound remains an application-model obligation.
#[wasm_bindgen]
pub fn invoke_bytes(input: JsValue) -> Result<js_sys::Uint8Array, JsValue> {
    let input = input.dyn_into::<js_sys::Uint8Array>().map_err(|_| JsValue::from_str("expected Uint8Array"))?;
    if input.length() > 64 { return Err(JsValue::from_str("input byte limit")); }
    let bytes = input.to_vec();
    core::str::from_utf8(&bytes).map_err(|_| JsValue::from_str("invalid input UTF-8"))?;
    let output = prism_text_request::dispatch(bytes);
    if output.len() > 256 { return Err(JsValue::from_str("output byte limit")); }
    core::str::from_utf8(&output).map_err(|_| JsValue::from_str("invalid output UTF-8"))?;
    Ok(js_sys::Uint8Array::from(output.as_slice()))
}
