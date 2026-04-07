import { useState } from "react";
import { aes_gcm_decrypt_file, aes_gcm_encrypt_file } from "../api/crypto";
import { useApi } from "../hooks/useApi";
import PathField from "./PathField";

function AesGcmPanel({ onOperation }) {
  const [encryptForm, setEncryptForm] = useState({ input_path: "", key_hex: "", output_path: "" });
  const [decryptForm, setDecryptForm] = useState({ input_path: "", key_hex: "", output_path: "" });
  const encryptApi = useApi({
    onSuccess: (data, statusMessage) => onOperation("AES Encrypt File", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("AES Encrypt File", "error", statusMessage)
  });
  const decryptApi = useApi({
    onSuccess: (data, statusMessage) => onOperation("AES Decrypt File", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("AES Decrypt File", "error", statusMessage)
  });

  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>AES-GCM</h3>
      </div>

      <form className="panel-form grouped-form" onSubmit={(event) => {
        event.preventDefault();
        encryptApi.run(() => aes_gcm_encrypt_file(encryptForm)).catch(() => {});
      }}>
        <h4>Encrypt File</h4>
        <PathField label="Input file" value={encryptForm.input_path} onChange={(value) => setEncryptForm({ ...encryptForm, input_path: value })} />
        <label className="field">
          <span>Key hex</span>
          <input value={encryptForm.key_hex} onChange={(event) => setEncryptForm({ ...encryptForm, key_hex: event.target.value })} />
        </label>
        <label className="field">
          <span>Output path</span>
          <input value={encryptForm.output_path} onChange={(event) => setEncryptForm({ ...encryptForm, output_path: event.target.value })} />
        </label>
        <button type="submit" disabled={encryptApi.loading}>{encryptApi.loading ? "Working..." : "Encrypt file"}</button>
        <p className="panel-message">{encryptApi.message}</p>
        {encryptApi.error ? <p className="panel-error">{encryptApi.error}</p> : null}
        <pre className="result-box">{encryptApi.result ? JSON.stringify(encryptApi.result, null, 2) : "Nothing yet. File remains embarrassingly readable."}</pre>
      </form>

      <form className="panel-form grouped-form" onSubmit={(event) => {
        event.preventDefault();
        decryptApi.run(() => aes_gcm_decrypt_file(decryptForm)).catch(() => {});
      }}>
        <h4>Decrypt File</h4>
        <PathField label="Input file" value={decryptForm.input_path} onChange={(value) => setDecryptForm({ ...decryptForm, input_path: value })} />
        <label className="field">
          <span>Key hex</span>
          <input value={decryptForm.key_hex} onChange={(event) => setDecryptForm({ ...decryptForm, key_hex: event.target.value })} />
        </label>
        <label className="field">
          <span>Output path</span>
          <input value={decryptForm.output_path} onChange={(event) => setDecryptForm({ ...decryptForm, output_path: event.target.value })} />
        </label>
        <button type="submit" disabled={decryptApi.loading}>{decryptApi.loading ? "Working..." : "Decrypt file"}</button>
        <p className="panel-message">{decryptApi.message}</p>
        {decryptApi.error ? <p className="panel-error">{decryptApi.error}</p> : null}
        <pre className="result-box">{decryptApi.result ? JSON.stringify(decryptApi.result, null, 2) : "Nothing yet. File stays locked up."}</pre>
      </form>
    </section>
  );
}

export default AesGcmPanel;
