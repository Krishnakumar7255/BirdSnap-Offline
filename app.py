import os
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st

from birdnet_service import identify_bird
from history import add_observation, load_history

st.set_page_config(
    page_title="BirdSnap Offline",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(61,120,83,.18), transparent 30rem),
        #07120e;
}
.block-container { max-width: 1150px; padding-top: 2rem; }
h1 { letter-spacing: -0.05em; }
.hero {
    padding: 2.2rem 2rem;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(21,48,35,.95), rgba(10,26,19,.9));
    margin-bottom: 1.2rem;
}
.hero-tag {
    color: #c8f36c;
    font-size: .75rem;
    letter-spacing: .12em;
    font-weight: 700;
}
.muted { color: #91a79a; }
.result {
    border: 1px solid #365642;
    border-radius: 18px;
    padding: 1.2rem;
    background: #10241a;
}
.big-bird { font-size: 2.2rem; font-weight: 800; }
.conf { color: #c8f36c; font-size: 1.8rem; font-weight: 800; }
.local {
    border: 1px solid #294536;
    background: #0b1912;
    padding: .8rem 1rem;
    border-radius: 12px;
    color: #91a79a;
}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None

st.markdown("""
<div class="hero">
    <div class="hero-tag">HACKTOBERFEST 2026 · TOUCH GRASS</div>
    <h1>🐦 BirdSnap Offline</h1>
    <p class="muted">
        Hear a bird. Identify it locally. Then put the screen down and keep exploring.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🌿 Field Mode")
    st.write("Record or upload a bird call, then run local BirdNET inference.")
    st.divider()
    st.markdown("**Open AI principles**")
    st.write("🔒 Audio stays on your machine")
    st.write("📡 No closed AI API")
    st.write("🧠 Local model inference")
    st.write("🔧 Replaceable model layer")

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("🎙️ Capture a bird call")
    st.caption("Best results: a clear recording with the bird call above heavy wind/noise.")

    recording = st.audio_input("Record from microphone")
    uploaded = st.file_uploader(
        "Or upload an audio recording",
        type=["wav", "mp3", "m4a", "ogg", "flac", "webm", "aac"],
    )

    audio = recording or uploaded

    if audio:
        st.audio(audio)

    col1, col2 = st.columns(2)
    with col1:
        min_conf = st.slider(
            "Minimum confidence",
            min_value=0.05,
            max_value=0.90,
            value=0.20,
            step=0.05,
        )
    with col2:
        top_k = st.number_input(
            "Possible matches",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
        )

    if st.button("🐦 Identify Bird", type="primary", use_container_width=True):
        if not audio:
            st.session_state.error = "Please record or upload a bird sound first."
            st.session_state.result = None
        else:
            st.session_state.error = None
            suffix = Path(audio.name).suffix.lower() or ".wav"

            temp_dir = Path("data") / "temp"
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_path = temp_dir / f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}{suffix}"

            try:
                temp_path.write_bytes(audio.getvalue())

                with st.spinner("Listening with local BirdNET…"):
                    predictions = identify_bird(
                        str(temp_path),
                        min_conf=float(min_conf),
                        top_k=int(top_k),
                    )

                st.session_state.result = predictions

                if predictions:
                    top = predictions[0]
                    add_observation({
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "bird": top["common_name"],
                        "scientific_name": top["scientific_name"],
                        "confidence": top["confidence"],
                        "filename": audio.name,
                    })
            except Exception as exc:
                st.session_state.error = str(exc)
                st.session_state.result = None
            finally:
                try:
                    temp_path.unlink()
                except OSError:
                    pass

    if st.session_state.error:
        st.error(st.session_state.error)

with right:
    st.subheader("🔎 Identification")

    predictions = st.session_state.result

    if predictions is None:
        st.info("Your result will appear here after an audio recording is analyzed.")
        st.markdown("""
        **Field loop**

        1. Go outside 🌳  
        2. Listen for a bird 🎧  
        3. Record 10–30 seconds 🎙️  
        4. Identify locally 🧠  
        5. Put the phone down and explore 🥾
        """)
    elif not predictions:
        st.warning("No confident bird match was found. Try a clearer recording.")
    else:
        top = predictions[0]

        st.markdown(
            f"""
            <div class="result">
                <div class="hero-tag">TOP MATCH</div>
                <div class="big-bird">🐦 {top['common_name']}</div>
                <i>{top['scientific_name']}</i>
                <div class="conf">{round(top['confidence'] * 100)}% confidence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Other possible matches")

        for bird in predictions[1:]:
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**{bird['common_name']}**")
                st.caption(bird["scientific_name"])
            with c2:
                st.metric("Match", f"{round(bird['confidence'] * 100)}%")

        st.markdown(
            '<div class="local">🔒 Identified locally with BirdNET. '
            'No closed AI API was used for inference.</div>',
            unsafe_allow_html=True,
        )

st.divider()

st.subheader("📓 Recent Field Notes")
history = load_history()

if not history:
    st.caption("No observations yet. Your first bird is waiting outside.")
else:
    for item in history[:8]:
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            st.write(f"**🐦 {item['bird']}**")
            st.caption(item.get("scientific_name", ""))
        with c2:
            st.caption(item.get("filename", ""))
        with c3:
            st.write(f"{round(float(item['confidence']) * 100)}%")

st.divider()
st.caption(
    "BirdSnap Offline · Open-source AI · Local inference · Built for Hacktoberfest 2026 Touch Grass"
)
