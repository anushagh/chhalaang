import  { useState, useRef } from "react";
import { sendVoiceQuery } from "./services/api";
import "./App.css";

function App() {
  const [recording, setRecording] = useState(false);
  const [responseText, setResponseText] = useState("");
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      chunks.current = [];

      mediaRecorder.current.ondataavailable = (e) => chunks.current.push(e.data);
      mediaRecorder.current.start();
      setRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Microphone access is required!");
    }
  };

  const stopRecording = () => {
    if (!mediaRecorder.current) return;

    mediaRecorder.current.onstop = async () => {
      const blob = new Blob(chunks.current, { type: "audio/webm" });
      await handleSendAudio(blob);
    };

    mediaRecorder.current.stop();
    setRecording(false);
  };

  const handleSendAudio = async (blob) => {
    try {
      const data = await sendVoiceQuery(blob);
      const text = data.text_response || "No response from backend";
      setResponseText(text);
      speakText(text);
    } catch (err) {
      alert("Backend not reachable. Make sure your backend is running on port 8000.");
    }
  };

  const speakText = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US"; // You can make this dynamic for multi-lingual support
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Porter Saathi Voice Prototype</h1>
        <button onClick={recording ? stopRecording : startRecording}>
          {recording ? "Stop Recording" : "Start Recording"}
        </button>
        {responseText && (
          <p>
            <strong>AI Response:</strong> {responseText}
          </p>
        )}
      </header>
    </div>
  );
}

export default App;
