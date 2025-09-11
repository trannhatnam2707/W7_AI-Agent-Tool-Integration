function LogBox({ logs }) {
  if (!logs || logs.length === 0) return null;

  return (
    <div
      style={{
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "12px",
        background: "#fafafa",
        boxShadow: "0 4px 8px rgba(0,0,0,0.05)",
      }}
    >
      <h2 style={{ marginBottom: "10px" }}>📜 Log thực hiện</h2>
      <ul style={{ fontFamily: "monospace", fontSize: "14px" }}>
        {logs.map((step, idx) => (
          <li key={idx} style={{ margin: "5px 0" }}>
            <strong>Bước {step.step}:</strong> {step.action} → {step.result}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default LogBox;
