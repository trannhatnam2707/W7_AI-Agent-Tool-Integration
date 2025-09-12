import { useState } from "react";

// Mapping giống như BE
const countries = [
  { label: "Việt Nam", value: "vietnam" },
  { label: "China", value: "china" },
  { label: "Japan", value: "japan" },
  { label: "South Korea", value: "south-korea" },
  { label: "Thailand", value: "thailand" },
  { label: "Singapore", value: "singapore" },
  { label: "Malaysia", value: "malaysia" },
  { label: "Philippines", value: "philippines" },
  { label: "Indonesia", value: "indonesia" },
  { label: "India", value: "india" },
];

function Controls({ onPredict }) {
  const [startYear, setStartYear] = useState(2024);
  const [endYear, setEndYear] = useState(2030);
  const [predictYear, setPredictYear] = useState(2035);
  const [region, setRegion] = useState("vietnam");

  const handleClick = () => {
    onPredict(Number(startYear), Number(endYear), Number(predictYear), region);
  };

  return (
    <div className="controls">
      <div className="control-group">
        <div className="input-group">
          <label>Năm bắt đầu</label>
          <input
            type="number"
            value={startYear}
            onChange={(e) => setStartYear(e.target.value)}
            min="2020"
            max="2030"
          />
        </div>
        <div className="input-group">
          <label>Năm kết thúc</label>
          <input
            type="number"
            value={endYear}
            onChange={(e) => setEndYear(e.target.value)}
            min="2025"
            max="2050"
          />
        </div>
        <div className="input-group">
          <label>Năm dự đoán</label>
          <input
            type="number"
            value={predictYear}
            onChange={(e) => setPredictYear(e.target.value)}
            min="2025"
            max="2050"
          />
        </div>
        <div className="input-group">
          <label>Khu vực</label>
          <select value={region} onChange={(e) => setRegion(e.target.value)}>
            {countries.map((c) => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </select>
        </div>
        <button className="btn-predict" onClick={handleClick}>
          🔮 Dự đoán
        </button>
      </div>
    </div>
  );
}

export default Controls;
