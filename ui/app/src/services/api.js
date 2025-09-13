import axios from "axios";

const API_BASE = "http://localhost:8000"; // Change if backend is hosted elsewhere

export const sendVoiceQuery = async (audioBlob) => {
  try {
    const formData = new FormData();
    formData.append("file", audioBlob, "voice.webm");

    const res = await axios.post(`${API_BASE}/voice-query`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return res.data;
  } catch (err) {
    console.error("Error sending audio:", err);
    throw err;
  }
};

export const fetchHistory = async () => {
  try {
    const res = await axios.get(`${API_BASE}/history`);
    return res.data;
  } catch (err) {
    console.error("Error fetching history:", err);
    throw err;
  }
};
