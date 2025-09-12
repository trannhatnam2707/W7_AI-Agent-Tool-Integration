import { useState } from "react";
import Header from "./components/Header";
import StatsGrid from "./components/StartGrid";
import PopulationChart from "./components/Populationchat";
import Controls from "./components/Controls";
import PredictionResult from "./components/PredictionResult";

function App() {
  const [stats, setStats] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async (startYear, endYear, predictYear, region) => {
    setLoading(true);
    try {
      // 🔹 Tạo query text để gửi cho BE (BE sẽ tự detect country & years)
      const query = `Dân số ${region} năm ${startYear} và ${endYear}, từ đó đưa ra tỉ lệ tăng giảm và dự đoán đến năm ${predictYear}`;

      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      if (data.success) {
        // Update stats cho StatsGrid
        setStats({
          region: data.country,
          currentYear: data.year_start,
          currentPop: data.population_start,
          endYear: data.year_end,
          endPop: data.population_end,
          growthPercent: (data.growth_rate * 100).toFixed(2),
          predictYear: data.future_year,
          futurePop: data.predicted_population,
        });

        // Update prediction cho PredictionResult + Chart
        setPrediction({
          year: data.future_year,
          population: data.predicted_population,
          year_start: data.year_start,
          population_start: data.population_start,
          year_end: data.year_end,
          population_end: data.population_end,
        });
      } else {
        alert("❌ Lỗi BE: " + data.error);
      }
    } catch (err) {
      alert("❌ Lỗi FE gọi API: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <Header />

      {stats && <StatsGrid stats={stats} />}

      {prediction && <PopulationChart prediction={prediction} />}

      <Controls onPredict={handlePredict} />

      {loading && <p>⏳ Đang tính toán...</p>}

      <PredictionResult prediction={prediction} />
    </div>
  );
}

export default App;
