import os
from fastapi import FastAPI, File, UploadFile
from faster_whisper import WhisperModel
from rag.AIVoiceAssisstant import AIVoiceAssistant
from googletrans import Translator  # pip install googletrans==4.0.0-rc1

# Initialize Whisper model, AI assistant, and translator
DEFAULT_MODEL_SIZE = "medium"  # Whisper model
model = WhisperModel(DEFAULT_MODEL_SIZE, device="cpu")
ai_assistant = AIVoiceAssistant()
translator = Translator()

app = FastAPI()


def transcribe_audio(file_path: str) -> str:
    """Transcribe audio file using WhisperModel."""
    segments, _ = model.transcribe(file_path, beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription


@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    """
    Receive audio from frontend in Hindi, convert to English for AI assistant,
    then translate AI response back to Hindi and return.
    """
    try:
        # Save uploaded audio temporarily
        temp_file = "uploaded_audio.wav"
        with open(temp_file, "wb") as f:
            f.write(await file.read())

        # Step 1: Transcribe audio (in Hindi)
        hindi_text = transcribe_audio(temp_file)

        # Step 2: Translate Hindi -> English
        english_text = translator.translate(hindi_text, src="hi", dest="en").text

        # Step 3: Get AI assistant response (in English)
        ai_response_en = ai_assistant.interact_with_llm(english_text)
        ai_response_en = ai_response_en.strip() if ai_response_en else ""

        # Step 4: Translate AI response back to Hindi
        ai_response_hi = translator.translate(ai_response_en, src="en", dest="hi").text

        # Cleanup temp file
        os.remove(temp_file)

        return {"text_response": ai_response_hi}

    except Exception as e:
        return {"error": str(e)}
