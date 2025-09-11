function ResultBox({ result }) {
  if (!result) return null;

  return (
    <div
      style={{
        marginBottom: "20px",
        padding: "20px",
        border: "1px solid #4caf50",
        borderRadius: "12px",
        background: "#f6fff6",
        boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
      }}
    >
      <h2 style={{ marginBottom: "10px" }}>📊 Kết quả</h2>
      {result.success ? (
        <>
          <p style={{ fontWeight: "bold" }}>{result.answer}</p>
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li>🌍 Quốc gia: {result.country}</li>
            <li>📅 Năm bắt đầu: {result.year_start}</li>
            <li>📅 Năm kết thúc: {result.year_end}</li>
            <li>🔮 Năm dự đoán: {result.future_year}</li>
            <li>
              🏙️ Dân số {result.year_start}:{" "}
              {result.population_start?.toLocaleString()}
            </li>
            <li>
              🏙️ Dân số {result.year_end}:{" "}
              {result.population_end?.toLocaleString()}
            </li>
            <li>
              📈 Tăng trưởng: {(result.growth_rate * 100).toFixed(3)}%/năm
            </li>
            <li>
              🔮 Dự đoán:{" "}
              {result.predicted_population?.toLocaleString()}
            </li>
          </ul>
        </>
      ) : (
        <p style={{ color: "red" }}>{result.error}</p>
      )}
    </div>
  );
}

export default ResultBox;
  