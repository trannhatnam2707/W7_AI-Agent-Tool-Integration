import { useState } from "react";
import axios from "axios";
import QueryForm from "./components/QueryForm";
import ResultBox from "./components/ResultBox";
import LogBox from "./components/LogBox";

function App() {
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async (query) => {
    setLoading(true);
    setResult(null);
    setLogs([]);

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", { query });
      setResult(res.data);
      setLogs(res.data.history || []);
    } catch (err) {
      setResult({ success: false, error: "❌ Lỗi kết nối server." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <h1 style={{ textAlign: "center" }}>Population Assistant</h1>
      <QueryForm onSubmit={handleAsk} loading={loading} />
      <ResultBox result={result} />
      <LogBox logs={logs} />
    </div>
  );
}

export default App;
