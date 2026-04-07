import { useState } from "react";
import { verify_signature } from "../api/crypto";
import { useApi } from "../hooks/useApi";
import PathField from "./PathField";

function VerifySignaturePanel({ onOperation }) {
  const [form, setForm] = useState({ input_path: "", signature_path: "", public_key_path: "" });
  const { run, loading, result, error, message } = useApi({
    onSuccess: (data, statusMessage) => onOperation("Verify Signature", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("Verify Signature", "error", statusMessage)
  });

  async function handleSubmit(event) {
    event.preventDefault();
    await run(() => verify_signature(form)).catch(() => {});
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>Verify Signature</h3>
        {loading ? <span className="working-chip">Working...</span> : null}
      </div>
      <form className="panel-form" onSubmit={handleSubmit}>
        <PathField label="Input file" value={form.input_path} onChange={(value) => setForm({ ...form, input_path: value })} />
        <PathField label="Signature path" value={form.signature_path} onChange={(value) => setForm({ ...form, signature_path: value })} />
        <PathField
          label="Public key path"
          value={form.public_key_path}
          onChange={(value) => setForm({ ...form, public_key_path: value })}
          placeholder="Optional. It defaults to keys/mykey.pub."
        />
        <button type="submit" disabled={loading}>{loading ? "Working..." : "Check it"}</button>
      </form>
      <p className="panel-message">{message}</p>
      {error ? <p className="panel-error">{error}</p> : null}
      <pre className="result-box">{result ? JSON.stringify(result, null, 2) : "Nothing yet. Still waiting on your evidence."}</pre>
    </section>
  );
}

export default VerifySignaturePanel;
