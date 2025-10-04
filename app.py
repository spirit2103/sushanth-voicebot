import streamlit as st
import tempfile
import base64
import time
from streamlit_mic_recorder import mic_recorder

from modules.rag_engine import RAGPipeline
from modules.stt_engine import speech_to_text
from modules.llm_engine import query_groq_stream
from modules.tts_engine import text_to_speech

# ---------------- Page Config ----------------
st.set_page_config(page_title="🎤 Sushanth's Voicebot", page_icon="🤖", layout="wide")

# ---------------- Force Full Width ----------------
st.markdown(
    """
    <style>
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stApp {
        padding-bottom: 120px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Title ----------------
st.markdown(
    """
    <div style="margin-bottom:70px;">
        <h1 style="margin:0; font-size:30px;">🤖 Welcome to Sushanth's Voice Assistant Bot 🎤</h1>
        <p style="margin:0; font-size:16px;">Ask your questions using your voice</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- RAG Pipeline ----------------
if "rag" not in st.session_state:
    with st.spinner("🔄 Loading RAG pipeline..."):
        st.session_state["rag"] = RAGPipeline("data/my_details.txt")
rag = st.session_state["rag"]

# ---------------- Chat History ----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------- Display Chat Messages ----------------
def display_messages():
    chat_area = st.container()
    with chat_area:
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                st.markdown(
                    f"""
                    <div style="text-align:right; background-color:#DCF8C6; 
                                padding:10px; border-radius:12px; 
                                margin:6px 0; max-width:70%; float:right; clear:both;
                                font-family: Arial, sans-serif; font-size:16px;">
                        {message['content']}
                    </div><div style="clear:both"></div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="text-align:left; background-color:#F1F0F0; 
                                padding:10px; border-radius:12px; 
                                margin:6px 0; max-width:70%; float:left; clear:both;
                                font-family: Arial, sans-serif; font-size:16px;">
                        {message['content']}
                    </div><div style="clear:both"></div>
                    """,
                    unsafe_allow_html=True,
                )

# ---------------- Voice Input (Floating Overlay) ----------------
def voice_input_ui():
    st.markdown(
        """
        <style>
        .bottom-container {
            position: fixed !important;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10000;
            background: rgba(255, 255, 255, 0.95);
            padding: 14px 28px;
            border-radius: 40px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.2);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(0,0,0,0.1);
        }

        .bottom-container:hover {
            box-shadow: 0 8px 30px rgba(0,0,0,0.25);
            transform: translateX(-50%) scale(1.02);
        }

        .bottom-container button {
            background-color: #007BFF;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 30px;
            border: none;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }

        .bottom-container button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="bottom-container">', unsafe_allow_html=True)
    audio = mic_recorder(
        start_prompt="🎙 Speak Now",
        stop_prompt="⏹️ Stop",
        just_once=True,
        use_container_width=False,
        key="mic_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return audio

# ---------------- Main ----------------
display_messages()
st.markdown("<br><br><br><br>", unsafe_allow_html=True)  # spacing for bottom bar

audio = voice_input_ui()
user_query = None

# ---------------- Handle Mic Input ----------------
if audio:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio["bytes"])
        audio_path = tmp.name
    try:
        user_query = speech_to_text(audio_path)
        st.session_state["messages"].append({"role": "user", "content": user_query})
    except Exception as e:
        st.error(f"⚠️ Error converting speech to text: {e}")
        user_query = None

# ---------------- Process Query ----------------
if user_query:
    with st.spinner("⏳ Processing your question..."):
        try:
            context = rag.retrieve(user_query)

            # Streaming bot response
            answer_container = st.empty()
            partial_answer = ""

            for chunk in query_groq_stream(user_query, context):
                partial_answer += chunk
                answer_container.markdown(
                    f"""
                    <div style="text-align:left; background-color:#F1F0F0; 
                                padding:10px; border-radius:12px; 
                                margin:6px 0; max-width:70%; float:left; clear:both;
                                font-family: Arial, sans-serif; font-size:16px;">
                        {partial_answer}
                    </div><div style="clear:both"></div>
                    """,
                    unsafe_allow_html=True,
                )
                time.sleep(0.02)

            # Save to history
            st.session_state["messages"].append({"role": "bot", "content": partial_answer})

            # Auto-speak answer
            audio_file = text_to_speech(partial_answer)
            if isinstance(audio_file, str):
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
            else:
                audio_bytes = audio_file

            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            st.markdown(
                f"""
                <audio autoplay="true" style="display:none">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"⚠️ Error generating answer: {e}")