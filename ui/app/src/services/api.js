import axios from "axios";

const API_BASE = "http://localhost:8000"; // backend URL

export const sendAudio = async (audioBlob) => {
  const formData = new FormData();
  formData.append("file", audioBlob, "voice.webm");

  const res = await axios.post(`${API_BASE}/voice-query`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data; // backend returns { text: "recognized text", audio_url: "tts file" }
};
