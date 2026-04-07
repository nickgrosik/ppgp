import { useEffect, useMemo, useState } from "react";
import {
  export_encrypted_private_key,
  get_health,
  get_public_key_fingerprint,
  import_encrypted_private_key,
  inspect_public_key,
  list_files
} from "../api/crypto";
import { useApi } from "../hooks/useApi";

import AesGcmPanel from "../components/AesGcmPanel";
import ConnectionStatus from "../components/ConnectionStatus";
import DecryptMessagePanel from "../components/DecryptMessagePanel";
import EncryptMessagePanel from "../components/EncryptMessagePanel";
import KeygenPanel from "../components/KeygenPanel";
import LogPanel from "../components/LogPanel";
import PathField from "../components/PathField";
import SignFilePanel from "../components/SignFilePanel";
import VerifySignaturePanel from "../components/VerifySignaturePanel";

function Home({ activeTab }) {
  const [healthy, setHealthy] = useState(false);
  const [statusMessage, setStatusMessage] = useState("Backend: being inspected.");
  const [statusLoading, setStatusLoading] = useState(false);

  const [fileLists, setFileLists] = useState({
    keys: [],
    encrypted: [],
    signatures: []
  });

  const [logs, setLogs] = useState([]);

  const [exportForm, setExportForm] = useState({
    source_path: "",
    output_name: "mykey_encrypted.priv",
    passphrase: ""
  });

  const [importForm, setImportForm] = useState({
    path: "",
    passphrase: ""
  });

  const [inspectPath, setInspectPath] = useState("");
  const [fingerprintPath, setFingerprintPath] = useState("");

  // API wrappers
  const exportApi = useApi({
    onSuccess: (data, message) =>
      handleOperation("Export Encrypted Private Key", "success", message, data),
    onError: (_error, message) =>
      handleOperation("Export Encrypted Private Key", "error", message)
  });

  const importApi = useApi({
    onSuccess: (data, message) =>
      handleOperation("Import Encrypted Private Key", "success", message, data),
    onError: (_error, message) =>
      handleOperation("Import Encrypted Private Key", "error", message)
  });

  const inspectApi = useApi({
    onSuccess: (data, message) =>
      handleOperation("Inspect Public Key", "success", message, data),
    onError: (_error, message) =>
      handleOperation("Inspect Public Key", "error", message)
  });

  const fingerprintApi = useApi({
    onSuccess: (data, message) =>
      handleOperation("Public Key Fingerprint", "success", message, data),
    onError: (_error, message) =>
      handleOperation("Public Key Fingerprint", "error", message)
  });

  // Initial load
  useEffect(() => {
    refreshWorkspace();
  }, []);

  async function refreshWorkspace() {
    setStatusLoading(true);
    try {
      const [health, keys, encrypted, signatures] = await Promise.all([
        get_health(),
        list_files("keys"),
        list_files("encrypted"),
        list_files("signatures")
      ]);

      setHealthy(health.status === "ok");
      setStatusMessage(
        health.status === "ok"
          ? "Backend: awake."
          : "Backend: not responding. Rude."
      );

      setFileLists({
        keys: keys.items || [],
        encrypted: encrypted.items || [],
        signatures: signatures.items || []
      });
    } catch (_error) {
      setHealthy(false);
      setStatusMessage("Backend: not responding. Rude.");
    } finally {
      setStatusLoading(false);
    }
  }

  function handleOperation(type, status, message, data = null) {
    setLogs((current) =>
      [
        {
          id: `${Date.now()}-${Math.random()}`,
          type,
          status,
          message,
          timestamp: new Date().toLocaleTimeString()
        },
        ...current
      ].slice(0, 12)
    );

    refreshWorkspace();
    return data;
  }

  const fileSummary = useMemo(
    () => [
      { title: "Keys", items: fileLists.keys },
      { title: "Encrypted", items: fileLists.encrypted },
      { title: "Signatures", items: fileLists.signatures }
    ],
    [fileLists]
  );

  return (
    <div className="home-layout">

      {/* LEFT SIDEBAR */}
      <aside className="workspace-sidebar">
        <p className="tagline">PPGP Desktop - local crypto, no drama.</p>

        <ConnectionStatus
          healthy={healthy}
          loading={statusLoading}
          message={statusMessage}
          onRefresh={refreshWorkspace}
        />

        {fileSummary.map((group) => (
          <section className="panel compact-panel" key={group.title}>
            <div className="panel-heading">
              <h3>{group.title}</h3>
            </div>

            {group.items.length === 0 ? (
              <p className="panel-message">Nothing here yet. Nature is healing.</p>
            ) : (
              <div className="file-list">
                {group.items.map((item) => (
                  <div className="file-item" key={item.path}>
                    <strong>{item.name}</strong>
                    <span>{item.path}</span>
                  </div>
                ))}
              </div>
            )}
          </section>
        ))}
      </aside>

      {/* RIGHT COLUMN — THIS FIXES YOUR ENTIRE LAYOUT */}
      <section className="view-stack">

        {/* KEYS TAB */}
        {activeTab === "Keys" && (
          <>
            <KeygenPanel onOperation={handleOperation} />

            <section className="panel">
              <div className="panel-heading">
                <h3>Encrypted Private Key</h3>
              </div>

              <div className="split-panels">

                {/* EXPORT */}
                <form
                  className="panel-form grouped-form"
                  onSubmit={(event) => {
                    event.preventDefault();
                    exportApi.run(() =>
                      export_encrypted_private_key(exportForm)
                    );
                  }}
                >
                  <h4>Export</h4>

                  <PathField
                    label="Source private key"
                    value={exportForm.source_path}
                    onChange={(value) =>
                      setExportForm({ ...exportForm, source_path: value })
                    }
                  />

                  <label className="field">
                    <span>Output file</span>
                    <input
                      value={exportForm.output_name}
                      onChange={(event) =>
                        setExportForm({
                          ...exportForm,
                          output_name: event.target.value
                        })
                      }
                    />
                  </label>

                  <label className="field">
                    <span>Passphrase</span>
                    <input
                      type="password"
                      value={exportForm.passphrase}
                      onChange={(event) =>
                        setExportForm({
                          ...exportForm,
                          passphrase: event.target.value
                        })
                      }
                    />
                  </label>

                  <button type="submit" disabled={exportApi.loading}>
                    {exportApi.loading ? "Working..." : "Export it"}
                  </button>

                  <p className="panel-message">{exportApi.message}</p>
                  {exportApi.error && (
                    <p className="panel-error">{exportApi.error}</p>
                  )}

                  <pre className="result-box">
                    {exportApi.result
                      ? JSON.stringify(exportApi.result, null, 2)
                      : "Nothing yet. The key remains exposed."}
                  </pre>
                </form>

                {/* IMPORT */}
                <form
                  className="panel-form grouped-form"
                  onSubmit={(event) => {
                    event.preventDefault();
                    importApi.run(() =>
                      import_encrypted_private_key(importForm)
                    );
                  }}
                >
                  <h4>Import</h4>

                  <PathField
                    label="Encrypted private key"
                    value={importForm.path}
                    onChange={(value) =>
                      setImportForm({ ...importForm, path: value })
                    }
                  />

                  <label className="field">
                    <span>Passphrase</span>
                    <input
                      type="password"
                      value={importForm.passphrase}
                      onChange={(event) =>
                        setImportForm({
                          ...importForm,
                          passphrase: event.target.value
                        })
                      }
                    />
                  </label>

                  <button type="submit" disabled={importApi.loading}>
                    {importApi.loading ? "Working..." : "Import it"}
                  </button>

                  <p className="panel-message">{importApi.message}</p>
                  {importApi.error && (
                    <p className="panel-error">{importApi.error}</p>
                  )}

                  <pre className="result-box">
                    {importApi.result
                      ? JSON.stringify(importApi.result, null, 2)
                      : "Nothing yet. The file sits there, smug."}
                  </pre>
                </form>
              </div>
            </section>
          </>
        )}

        {/* MESSAGES TAB */}
        {activeTab === "Messages" && (
          <>
            <EncryptMessagePanel onOperation={handleOperation} />
            <DecryptMessagePanel onOperation={handleOperation} />
          </>
        )}

        {/* FILES TAB */}
        {activeTab === "Files" && (
          <>
            <SignFilePanel onOperation={handleOperation} />
            <VerifySignaturePanel onOperation={handleOperation} />
            <AesGcmPanel onOperation={handleOperation} />
          </>
        )}

        {/* ADVANCED TAB */}
        {activeTab === "Advanced" && (
          <>
            <section className="panel">
              <div className="panel-heading">
                <h3>Key Inspection</h3>
              </div>

              <div className="split-panels">

                {/* INSPECT */}
                <form
                  className="panel-form grouped-form"
                  onSubmit={(event) => {
                    event.preventDefault();
                    inspectApi.run(() =>
                      inspect_public_key({ path: inspectPath })
                    );
                  }}
                >
                  <h4>Inspect Public Key</h4>

                  <PathField
                    label="Public key path"
                    value={inspectPath}
                    onChange={setInspectPath}
                  />

                  <button type="submit" disabled={inspectApi.loading}>
                    {inspectApi.loading ? "Working..." : "Inspect it"}
                  </button>

                  <p className="panel-message">{inspectApi.message}</p>
                  {inspectApi.error && (
                    <p className="panel-error">{inspectApi.error}</p>
                  )}

                  <pre className="result-box">
                    {inspectApi.result
                      ? JSON.stringify(inspectApi.result, null, 2)
                      : "Nothing yet. The key keeps its secrets."}
                  </pre>
                </form>

                {/* FINGERPRINT */}
                <form
                  className="panel-form grouped-form"
                  onSubmit={(event) => {
                    event.preventDefault();
                    fingerprintApi.run(() =>
                      get_public_key_fingerprint(fingerprintPath)
                    );
                  }}
                >
                  <h4>Fingerprint</h4>

                  <PathField
                    label="Public key path"
                    value={fingerprintPath}
                    onChange={setFingerprintPath}
                  />

                  <button type="submit" disabled={fingerprintApi.loading}>
                    {fingerprintApi.loading ? "Working..." : "Get print"}
                  </button>

                  <p className="panel-message">{fingerprintApi.message}</p>
                  {fingerprintApi.error && (
                    <p className="panel-error">{fingerprintApi.error}</p>
                  )}

                  <pre className="result-box">
                    {fingerprintApi.result
                      ? JSON.stringify(fingerprintApi.result, null, 2)
                      : "Nothing yet. Apparently identity is hard."}
                  </pre>
                </form>
              </div>
            </section>

            <LogPanel items={logs} />
          </>
        )}

        {/* SETTINGS TAB */}
        {activeTab === "Settings" && (
          <section className="panel">
            <div className="panel-heading">
              <h3>Settings</h3>
            </div>

            <div className="panel-form grouped-form">
              <label className="field">
                <span>Default key directory</span>
                <input value="keys/" readOnly />
              </label>

              <label className="field">
                <span>Default encrypted directory</span>
                <input value="encrypted/" readOnly />
              </label>

              <label className="field">
                <span>Theme</span>
                <select defaultValue="dark">
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                </select>
              </label>

              <label className="field">
                <span>Narrator intensity</span>
                <select defaultValue="normal">
                  <option value="mild">Mild</option>
                  <option value="normal">Normal</option>
                  <option value="aggressive">Aggressive</option>
                </select>
              </label>

              <p className="panel-message">
                Settings coming soon. Try to contain yourself.
              </p>
            </div>
          </section>
        )}

      </section>
    </div>
  );
}

export default Home;