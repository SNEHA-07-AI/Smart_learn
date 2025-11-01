import streamlit as st
from services import generate_lesson, generate_quiz
from ui import apply_custom_css, show_header

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Learn AI Tutor", page_icon="🎓", layout="centered")

def main():
    """Main function to run the app."""
    apply_custom_css()
    show_header()

    # --- SESSION STATE INITIALIZATION ---
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "topic" not in st.session_state:
        st.session_state.topic = ""
    if "lesson" not in st.session_state:
        st.session_state.lesson = None
    if "quiz" not in st.session_state:
        st.session_state.quiz = None

    # --- PAGE ROUTING ---
    if st.session_state.page == "home":
        render_home_page()
    elif st.session_state.page == "lesson":
        render_lesson_page()
    elif st.session_state.page == "quiz":
        render_quiz_page()
    elif st.session_state.page == "results":
        render_results_page()

def render_home_page():
    """Renders the main input page."""
    with st.container():
        st.subheader("Start Your Learning Journey")
        st.session_state.topic = st.text_input(
            "What subject would you like to master today?",
            placeholder="e.g., 'Machine Learning' or 'Astrophysics'",
        )

        col1, col2 = st.columns(2)
        with col1:
            lang_options = {"English": "en", "Japanese": "ja", "Korean": "ko", "Hindi": "hi", "Kannada": "kn"}
            selected_lang_name = st.selectbox("Language:", options=list(lang_options.keys()))
            st.session_state.lang = lang_options[selected_lang_name]

        with col2:
            st.session_state.format_type = st.radio("Format:", ["Text", "Audio", "Video"], horizontal=True)

        if st.button("Generate My Lesson", use_container_width=True, type="primary"):
            if st.session_state.topic:
                st.session_state.page = "lesson"
                st.rerun()
            else:
                st.warning("Please enter a topic to begin.")

def render_lesson_page():
    """Generates and displays the lesson."""
    st.header(f"Lesson: {st.session_state.topic}", divider="rainbow")

    if st.session_state.lesson is None:
        with st.spinner("Your personal AI tutor is crafting your lesson... This may take a moment."):
            st.session_state.lesson = generate_lesson(
                st.session_state.topic, st.session_state.lang, st.session_state.format_type.lower()
            )

    if st.session_state.lesson:
        lesson_data = st.session_state.lesson
        st.markdown(lesson_data.get("content", "Could not generate lesson content."))

        if lesson_data.get("audio_path"):
            st.audio(lesson_data["audio_path"])
        if lesson_data.get("video_url"):
            st.info(f"For a video-based lesson, check out these results on YouTube: [Search for {st.session_state.topic}]({lesson_data['video_url']})")

        if st.button("I'm Ready! Let's Start the Quiz", use_container_width=True):
            st.session_state.page = "quiz"
            st.rerun()
    else:
        st.error("There was a problem generating your lesson. Please make sure Ollama is running and try again.")
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()

def render_quiz_page():
    """Renders the quiz form."""
    st.header(f"Quiz: {st.session_state.topic}", divider="rainbow")

    if st.session_state.quiz is None:
        st.session_state.quiz = generate_quiz(st.session_state.topic, st.session_state.lang)

    if st.session_state.quiz:
        with st.form("quiz_form"):
            user_answers = [st.text_area(f"**Question {i+1}:** {q['question']}", key=f"q_{i}") for i, q in enumerate(st.session_state.quiz)]

            if st.form_submit_button("Submit My Answers", use_container_width=True, type="primary"):
                st.session_state.user_answers = user_answers
                st.session_state.page = "results"
                st.rerun()
    else:
        st.error("Could not generate the quiz. Please try again.")

def render_results_page():
    """Renders the quiz results."""
    st.header("Quiz Results", divider="rainbow")
    score = 0
    total = len(st.session_state.quiz)

    for i, q_data in enumerate(st.session_state.quiz):
        user_ans = st.session_state.user_answers[i].lower().strip()
        correct_ans = q_data["correct_answer"].lower().strip()

        if user_ans and all(keyword in user_ans for keyword in correct_ans.split()[:4]):
            score += 1

        with st.container(border=True):
            st.write(f"**Question:** {q_data['question']}")
            st.markdown(f"**Your Answer:** <span style='color: #0068FF;'>{st.session_state.user_answers[i]}</span>", unsafe_allow_html=True)
            st.markdown(f"**Suggested Answer:** <span style='color: #28a745;'>{q_data['correct_answer']}</span>", unsafe_allow_html=True)

    st.subheader(f"Your Final Score: {score}/{total}", divider="rainbow")

    if score == total:
        st.balloons()
        st.success("Flawless Victory! You have mastered this topic. Incredible work!")
    elif score >= total * 0.7:
        st.info("Excellent work! You have a strong grasp of the subject.")
    else:
        st.warning("Good effort! Review the suggested answers to strengthen your understanding.")

    if st.button("Start a New Topic", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()