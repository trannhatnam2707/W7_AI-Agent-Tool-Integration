function PredictionResult({ prediction }) {
    if (!prediction) return null;
  
    return (
      <div className="prediction-result show">
        <h3>Kết quả Dự đoán</h3>
        <p>
          Dân số dự kiến năm <span>{prediction.year}</span>:{" "}
          <strong>{prediction.population} triệu người</strong>
        </p>
      </div>
    );
  }
  
  export default PredictionResult;
  