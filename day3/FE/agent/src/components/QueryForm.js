import { useState } from "react";
import countries from "../country";

function QueryForm({ onSubmit, loading }) {
  const [country, setCountry] = useState("vietnam");
  const [yearStart, setYearStart] = useState("");
  const [yearEnd, setYearEnd] = useState("");
  const [futureYear, setFutureYear] = useState("");

  const years = Array.from({ length: 2035 - 1950 + 1 }, (_, i) => 1950 + i);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!yearStart || !yearEnd) {
      return alert("Vui lòng chọn năm bắt đầu và kết thúc!");
    }

    let query = `Lấy dân số ${country} năm ${yearStart} và ${yearEnd}, từ đó tính tỷ lệ tăng trưởng dân số hàng năm`;
    if (futureYear) {
      query += `, dự đoán ${futureYear}`;
    }
    onSubmit(query);
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        marginBottom: "20px",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "12px",
        background: "#ffffff",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
      }}
    >
      <h2 style={{ marginBottom: "15px", color: "#333" }}>🌍 Tra cứu dân số</h2>

      {/* Quốc gia */}
      <div style={{ margin: "10px 0" }}>
        <label>Quốc gia: </label>
        <select value={country} onChange={(e) => setCountry(e.target.value)}>
          {countries.map((c) => (
            <option key={c.code} value={c.code}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {/* Năm bắt đầu */}
      <div style={{ margin: "10px 0" }}>
        <label>Năm bắt đầu: </label>
        <select value={yearStart} onChange={(e) => setYearStart(e.target.value)}>
          <option value="">-- Chọn năm --</option>
          {years.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      {/* Năm kết thúc */}
      <div style={{ margin: "10px 0" }}>
        <label>Năm kết thúc: </label>
        <select value={yearEnd} onChange={(e) => setYearEnd(e.target.value)}>
          <option value="">-- Chọn năm --</option>
          {years.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      {/* Năm dự đoán */}
      <div style={{ margin: "10px 0" }}>
        <label>Năm dự đoán (tương lai): </label>
        <input
          type="number"
          placeholder="Ví dụ: 2030"
          value={futureYear}
          onChange={(e) => setFutureYear(e.target.value)}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        style={{
          padding: "10px 20px",
          background: "#4caf50",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        {loading ? "⏳ Đang xử lý..." : "🚀 Gửi yêu cầu"}
      </button>
    </form>
  );
}

export default QueryForm;
