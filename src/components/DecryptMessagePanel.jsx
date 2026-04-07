import { useState } from "react";
import { decrypt_message } from "../api/crypto";
import { useApi } from "../hooks/useApi";
import PathField from "./PathField";

function DecryptMessagePanel({ onOperation }) {
  const [form, setForm] = useState({ ciphertext_path: "", ciphertext_base64: "", private_key_path: "" });
  const { run, loading, result, error, message } = useApi({
    onSuccess: (data, statusMessage) => onOperation("Decrypt Message", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("Decrypt Message", "error", statusMessage)
  });

  async function handleSubmit(event) {
    event.preventDefault();
    await run(() => decrypt_message(form)).catch(() => {});
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>Decrypt Message</h3>
        {loading ? <span className="working-chip">Working...</span> : null}
      </div>
      <form className="panel-form" onSubmit={handleSubmit}>
        <PathField
          label="Ciphertext path"
          value={form.ciphertext_path}
          onChange={(value) => setForm({ ...form, ciphertext_path: value })}
          placeholder="Optional if you insist on pasting base64 instead."
        />
        <label className="field">
          <span>Ciphertext base64</span>
          <textarea rows={5} value={form.ciphertext_base64} onChange={(event) => setForm({ ...form, ciphertext_base64: event.target.value })} />
        </label>
        <PathField
          label="Private key path"
          value={form.private_key_path}
          onChange={(value) => setForm({ ...form, private_key_path: value })}
          placeholder="Optional. It falls back to keys/mykey.priv."
        />
        <button type="submit" disabled={loading}>{loading ? "Working..." : "Decrypt it"}</button>
      </form>
      <p className="panel-message">{message}</p>
      {error ? <p className="panel-error">{error}</p> : null}
      <pre className="result-box">{result ? JSON.stringify(result, null, 2) : "Nothing yet. The suspense is mild."}</pre>
    </section>
  );
}

export default DecryptMessagePanel;
