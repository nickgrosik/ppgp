import { useState } from "react";
import { encrypt_message } from "../api/crypto";
import { useApi } from "../hooks/useApi";
import PathField from "./PathField";

function EncryptMessagePanel({ onOperation }) {
  const [form, setForm] = useState({ message: "", public_key_path: "" });
  const { run, loading, result, error, message } = useApi({
    onSuccess: (data, statusMessage) => onOperation("Encrypt Message", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("Encrypt Message", "error", statusMessage)
  });

  async function handleSubmit(event) {
    event.preventDefault();
    await run(() => encrypt_message(form)).catch(() => {});
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>Encrypt Message</h3>
        {loading ? <span className="working-chip">Working...</span> : null}
      </div>
      <form className="panel-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Message</span>
          <textarea rows={5} value={form.message} onChange={(event) => setForm({ ...form, message: event.target.value })} />
        </label>
        <PathField
          label="Public key path"
          value={form.public_key_path}
          onChange={(value) => setForm({ ...form, public_key_path: value })}
          placeholder="Optional. It uses keys/mykey.pub if you leave it alone."
        />
        <button type="submit" disabled={loading}>{loading ? "Working..." : "Encrypt it"}</button>
      </form>
      <p className="panel-message">{message}</p>
      {error ? <p className="panel-error">{error}</p> : null}
      <pre className="result-box">{result ? JSON.stringify(result, null, 2) : "Nothing yet. As expected."}</pre>
    </section>
  );
}

export default EncryptMessagePanel;
