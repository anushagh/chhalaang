import React, { useState, useEffect } from "react";
import { useRecorder } from "./hooks/useRecorder";
import { sendAudio } from "./services/api";

function App() {
  const { recording, audioBlob, startRecording, stopRecording } = useRecorder();
  const [responseText, setResponseText] = useState("");
  const [ttsAudio, setTtsAudio] = useState(null);

  useEffect(() => {
    if (audioBlob) handleSendAudio();
  }, [audioBlob]);

  const handleSendAudio = async () => {
    const res = await sendAudio(audioBlob);
    setResponseText(res.text);

    
    if (res.audio_url) {
      const audio = new Audio(res.audio_url);
      audio.play();
      setTtsAudio(audio);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Porter Saathi</h1>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {responseText && (
        <div style={{ marginTop: "1rem" }}>
          <h3>AI Response:</h3>
          <p>{responseText}</p>
        </div>
      )}
    </div>
  );
}

export default App;
