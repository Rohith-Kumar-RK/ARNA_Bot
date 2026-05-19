import { useState, useRef, useEffect } from "react";

const API = "http://localhost:8000";

const Spinner = () => (
  <span style={{
    width: 16,
    height: 16,
    border: "2px solid #ccc",
    borderTop: "2px solid #1D9E75",
    borderRadius: "50%",
    animation: "spin 0.2s linear infinite"
  }} />
);

export default function App() {

  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ✅ HANDLE FILE
  const handleFile = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please upload an image");
      return;
    }

    setImageFile(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  // ✅ ANALYZE IMAGE
  const analyze = async () => {
    if (!imageFile) return;

    setAnalyzing(true);

    const fd = new FormData();
    fd.append("file", imageFile);

    try {
      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        body: fd
      });

      const data = await res.json();
      setResult(data);
    } catch {
      alert("Backend not running");
    }

    setAnalyzing(false);
  };

  // ✅ CHAT
  const sendChat = async () => {
    if (!input.trim()) return;

    const userMsg = input;
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setInput("");
    setChatLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: userMsg,
          disease_context: result?.disease || ""
        })
      });

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { role: "assistant", content: data.reply }
      ]);

    } catch {
      setMessages(prev => [
        ...prev,
        { role: "assistant", content: "Backend error" }
      ]);
    }

    setChatLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 20 }}>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>

      <h2>🌿 Crop Disease Analyzer</h2>

      {/* ✅ IMAGE UPLOAD */}
      <div style={{
        border: "2px dashed #ccc",
        padding: 20,
        textAlign: "center",
        marginBottom: 20
      }}>

        <label htmlFor="fileUpload" style={{ cursor: "pointer" }}>
          {preview ? (
            <img src={preview} style={{ maxWidth: "100%", height: 200 }} />
          ) : (
            <p>📷 Click here to upload image</p>
          )}
        </label>

        <input
          id="fileUpload"
          type="file"
          accept="image/*"
          onChange={handleFile}
          style={{ display: "none" }}
        />

        <br /><br />

        <button onClick={analyze} disabled={!imageFile || analyzing}>
          {analyzing ? "Analyzing..." : "Analyze"}
        </button>

        {result && (
          <div style={{ marginTop: 10 }}>
            <p><b>Disease:</b> {result.disease}</p>
            <p><b>Confidence:</b> {result.confidence}</p>
            <p><b>Fertilizer:</b> {result.fertilizer}</p>
          </div>
        )}
      </div>

      {/* ✅ CHAT */}
      <h2>💬 Chat Assistant</h2>

      <div style={{ border: "1px solid #ccc", padding: 20 }}>

        <div style={{ height: 250, overflowY: "auto" }}>
          {messages.map((m, i) => (
            <div key={i} style={{
              textAlign: m.role === "user" ? "right" : "left"
            }}>
              <p>{m.content}</p>
            </div>
          ))}

          {chatLoading && <Spinner />}

          <div ref={bottomRef} />
        </div>

        <div style={{
          display: "flex",
          gap: "10px",
          marginTop: "10px"
        }}>

          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendChat()}
            placeholder="Ask about disease, treatment, prevention..."
            style={{
              flex: 1,                 // 🔥 makes it expand full width
              padding: "10px",
              fontSize: "14px",
              borderRadius: "6px",
              border: "1px solid #ccc"
            }}
          />

          <button
            onClick={sendChat}
            style={{
              padding: "10px 16px",
              background: "#1D9E75",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer"
            }}
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}