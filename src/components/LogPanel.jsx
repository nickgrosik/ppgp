function LogPanel({ items }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <h3>Recent Operations</h3>
      </div>
      {items.length === 0 ? (
        <p className="panel-message">Nothing to report. Miraculous, really.</p>
      ) : (
        <div className="log-list">
          {items.map((item) => (
            <article key={item.id} className="log-item">
              <div>
                <strong>{item.type}</strong>
                <p>{item.message}</p>
              </div>
              <div className={`log-status ${item.status}`}>
                <span>{item.status}</span>
                <time>{item.timestamp}</time>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default LogPanel;
