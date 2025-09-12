import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

function PopulationChart({ prediction }) {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartInstance.current) chartInstance.current.destroy();

    chartInstance.current = new Chart(chartRef.current, {
      type: "line",
      data: {
        labels: ["2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"],
        datasets: [
          {
            label: "Dân số (triệu)",
            data: [97.3,97.5,97.7,97.8,98.0,98.3,98.7,99.2,99.8,100.5,101.2],
            borderColor: "#667eea",
            backgroundColor: "rgba(102,126,234,0.1)",
            borderWidth: 3,
            fill: true,
            tension: 0.4,
          },
          {
            label: "Dự đoán AI",
            data: [null,null,null,null,98.0,98.4,98.9,99.5,100.2,101.0,101.8],
            borderColor: "#764ba2",
            backgroundColor: "rgba(118,75,162,0.1)",
            borderWidth: 3,
            borderDash: [5,5],
            fill: true,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { position: "top" } },
        scales: { y: { min: 95, max: 105 } },
      },
    });
  }, [prediction]);

  return (
    <div className="chart-container">
      <h3 className="chart-title">📊 Biểu đồ Dự đoán Dân số</h3>
      <canvas ref={chartRef}></canvas>
    </div>
  );
}

export default PopulationChart;
