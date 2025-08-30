import { useState } from "react";
import { predict } from "./services/api";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");

  const handlePredict = async () => {
    try {
      const res = await predict(Number(input));
      setResult(res.data.status);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>TideGuard Alerter 🌊</h1>
      <input
        type="number"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter a value"
      />
      <button onClick={handlePredict}>Check</button>
      {result && <p>Prediction: {result}</p>}
    </div>
  );
}

export default App;
