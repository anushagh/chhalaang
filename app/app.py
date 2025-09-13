import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from faster_whisper import WhisperModel
from rag.AIVoiceAssisstant import AIVoiceAssistant

# Initialize Whisper model and AI assistant
DEFAULT_MODEL_SIZE = "medium.en"
model = WhisperModel(DEFAULT_MODEL_SIZE, device="cpu")
ai_assistant = AIVoiceAssistant()

app = FastAPI()


def transcribe_audio(file_path: str) -> str:
    """Transcribe audio file using WhisperModel."""
    segments, _ = model.transcribe(file_path, beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription


@app.post("/voice-query")
async def process_audio(file: UploadFile = File(...)):
    """
    Receive audio from frontend, transcribe it, and get AI assistant response.
    Returns JSON: { "text_response": "<AI assistant response>" }
    """
    try:
        # Save uploaded audio temporarily
        temp_file = "uploaded_audio.wav"
        with open(temp_file, "wb") as f:
            f.write(await file.read())

        # Transcribe audio
        transcription = transcribe_audio(temp_file)

        # Get AI assistant response
        ai_response = ai_assistant.interact_with_llm(transcription)

        # Clean up temp file
        os.remove(temp_file)

        return {"text_response": ai_response.strip() if ai_response else ""}

    except Exception as e:
        return {"error": str(e)}



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)