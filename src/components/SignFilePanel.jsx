import { useState } from "react";
import { sign_file } from "../api/crypto";
import { useApi } from "../hooks/useApi";
import PathField from "./PathField";

function SignFilePanel({ onOperation }) {
  const [form, setForm] = useState({ input_path: "", private_key_path: "" });
  const { run, loading, result, error, message } = useApi({
    onSuccess: (data, statusMessage) => onOperation("Sign File", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("Sign File", "error", statusMessage)
  });

  async function handleSubmit(event) {
    event.preventDefault();
    await run(() => sign_file(form)).catch(() => {});
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>Sign File</h3>
        {loading ? <span className="working-chip">Working...</span> : null}
      </div>
      <form className="panel-form" onSubmit={handleSubmit}>
        <PathField label="Input file" value={form.input_path} onChange={(value) => setForm({ ...form, input_path: value })} />
        <PathField
          label="Private key path"
          value={form.private_key_path}
          onChange={(value) => setForm({ ...form, private_key_path: value })}
          placeholder="Optional. It uses keys/mykey.priv if you do nothing."
        />
        <button type="submit" disabled={loading}>{loading ? "Working..." : "Sign it"}</button>
      </form>
      <p className="panel-message">{message}</p>
      {error ? <p className="panel-error">{error}</p> : null}
      <pre className="result-box">{result ? JSON.stringify(result, null, 2) : "Nothing yet. Sign nothing, get nothing."}</pre>
    </section>
  );
}

export default SignFilePanel;
