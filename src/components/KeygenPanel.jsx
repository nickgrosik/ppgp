import { useState } from "react";
import { generate_keys } from "../api/crypto";
import { useApi } from "../hooks/useApi";

function KeygenPanel({ onOperation }) {
  const [form, setForm] = useState({
    key_size: "2048",
    private_key_name: "mykey.priv",
    public_key_name: "mykey.pub"
  });
  const { run, loading, result, error, message } = useApi({
    onSuccess: (data, statusMessage) => onOperation("Generate RSA Keys", "success", statusMessage, data),
    onError: (_error, statusMessage) => onOperation("Generate RSA Keys", "error", statusMessage)
  });

  async function handleSubmit(event) {
    event.preventDefault();
    await run(
      () => generate_keys({ ...form, key_size: Number(form.key_size) }),
      { successMessage: "Keys made. Humanity survives another day." }
    ).catch(() => {});
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>Generate RSA Keys</h3>
        {loading ? <span className="working-chip">Working...</span> : null}
      </div>
      <form className="panel-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Key size</span>
          <input value={form.key_size} onChange={(event) => setForm({ ...form, key_size: event.target.value })} />
        </label>
        <label className="field">
          <span>Private key file</span>
          <input value={form.private_key_name} onChange={(event) => setForm({ ...form, private_key_name: event.target.value })} />
        </label>
        <label className="field">
          <span>Public key file</span>
          <input value={form.public_key_name} onChange={(event) => setForm({ ...form, public_key_name: event.target.value })} />
        </label>
        <button type="submit" disabled={loading}>{loading ? "Working..." : "Make keys"}</button>
      </form>
      <p className="panel-message">{message}</p>
      {error ? <p className="panel-error">{error}</p> : null}
      <pre className="result-box">{result ? JSON.stringify(result, null, 2) : "Nothing yet. Tragic."}</pre>
    </section>
  );
}

export default KeygenPanel;
