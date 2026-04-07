function ConnectionStatus({ healthy, loading, message, onRefresh }) {
  return (
    <section className="panel compact-panel">
      <div className="panel-heading">
        <h3>Connection</h3>
        <button type="button" onClick={onRefresh}>Check again</button>
      </div>
      <p>{healthy ? "Backend: awake." : "Backend: not responding. Rude."}</p>
      <p className={loading ? "status-working" : "status-idle"}>{message || "Backend: being inspected."}</p>
    </section>
  );
}

export default ConnectionStatus;
