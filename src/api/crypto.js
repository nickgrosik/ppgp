const API_BASE_URL = window.ppgpDesktop?.getBackendBaseUrl?.() || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Request failed.");
  }

  return data;
}

export function get_health() {
  return request("/health");
}

export function list_files(group) {
  return request(`/api/files/${group}`);
}

export function generate_keys(payload) {
  return request("/api/keys/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function encrypt_message(payload) {
  return request("/api/rsa/encrypt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function decrypt_message(payload) {
  return request("/api/rsa/decrypt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function sign_file(payload) {
  return request("/api/signatures/sign", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function verify_signature(payload) {
  return request("/api/signatures/verify", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function aes_gcm_encrypt_file(payload) {
  return request("/api/aes/encrypt-file", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function aes_gcm_decrypt_file(payload) {
  return request("/api/aes/decrypt-file", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function export_encrypted_private_key(payload) {
  return request("/api/keys/private/export-encrypted", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function import_encrypted_private_key(payload) {
  return request("/api/keys/private/import-encrypted", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function inspect_public_key(payload) {
  return request("/api/keys/public/inspect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
}

export function get_public_key_fingerprint(path = "") {
  const query = path ? `?path=${encodeURIComponent(path)}` : "";
  return request(`/api/keys/public/fingerprint${query}`);
}
