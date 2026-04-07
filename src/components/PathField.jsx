async function browsePath(setter, directory = false) {
  if (window.ppgpDesktop?.browseFile) {
    const selected = await window.ppgpDesktop.browseFile({ directory });
    if (selected) {
      setter(selected);
    }
    return;
  }

  // TODO: Wire Electron file picker for this input if preload support is unavailable.
}

function PathField({ label, value, onChange, placeholder = "" }) {
  return (
    <label className="field">
      <span>{label}</span>
      <div className="path-row">
        <input value={value} placeholder={placeholder} onChange={(event) => onChange(event.target.value)} />
        <button type="button" className="secondary-button" onClick={() => browsePath(onChange)}>Browse</button>
      </div>
    </label>
  );
}

export default PathField;
