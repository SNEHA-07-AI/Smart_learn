import subprocess
from deep_translator import GoogleTranslator
from gtts import gTTS
import streamlit as st
import os

# Ensure a directory for temporary audio files exists
if not os.path.exists("temp_audio"):
    os.makedirs("temp_audio")

@st.cache_data(show_spinner="Asking the AI model...")
def generate_ollama_response(prompt):
    """
    Runs the Ollama command to get a response from the Llama3 model.
    This function is cached to prevent re-running for the same topic.
    """
    try:
        # The command to run the Ollama model
        command = ["ollama", "run", "llama3:8b-instruct-q2_K", prompt]
        result = subprocess.run(
            command, capture_output=True, text=True, check=True, encoding='utf-8'
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        # Provide a much more helpful error message to the user
        st.error(f"Ollama command failed: {e}. Please ensure the Ollama application is running on your computer.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

@st.cache_data(show_spinner="Translating text...")
def translate_text(text, target_lang):
    """Translates text to the specified target language."""
    if not text or target_lang == "en":
        return text
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        st.warning(f"Translation failed: {e}")
        return f"{text}\n\n(Translation to '{target_lang}' failed.)"

def text_to_audio(text, lang):
    """Converts text to an audio file and returns the file path."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_path = os.path.join("temp_audio", "lesson_audio.mp3")
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        st.error(f"Failed to generate audio: {e}")
        return None

def generate_lesson(topic, lang, format_type):
    """Generates all lesson materials (text, audio, video link)."""
    # A more detailed prompt for a higher-quality response from the AI
    prompt = f"Act as a university professor. Explain the topic '{topic}' in a clear, structured, and detailed way. Start with a simple introduction, explain the core concepts with real-world examples, and finish with a concise summary."

    content_en = generate_ollama_response(prompt)
    if content_en is None: # Handle error from Ollama
        return None

    final_content = translate_text(content_en, lang)
    lesson_data = {"content": final_content}

    if format_type == "audio":
        with st.spinner("Generating audio track..."):
            lesson_data["audio_path"] = text_to_audio(final_content, lang)
    elif format_type == "video":
        search_query = topic.replace(" ", "+")
        lesson_data["video_url"] = f"https://www.youtube.com/results?search_query={search_query}"

    return lesson_data

@st.cache_data(show_spinner="Preparing your quiz...")
def generate_quiz(topic, lang):
    """Generates quiz questions and answers."""
    # Prompts designed for better quiz questions
    questions_en = [
        f"Based on '{topic}', what is its most fundamental concept?",
        f"Describe a primary real-world application of '{topic}'.",
        f"What is a significant challenge or limitation when working with '{topic}'?",
        f"How does '{topic}' influence or interact with a related field of study?",
        f"Explain a specific component or process within '{topic}'."
    ]

    quiz_data = []
    for q_en in questions_en:
        answer_en = generate_ollama_response(q_en)
        if answer_en is None: continue # Skip if question generation fails

        question_display = translate_text(q_en, lang)
        answer_display = translate_text(answer_en, lang)

        quiz_data.append({
            'question': question_display,
            'correct_answer': answer_display
        })

    return quiz_data