
# =========================================================
# ULTIMATE VIDEO PROCESSOR 2026
# FULL WORKING SINGLE FILE
# SAVE AS: video.py
# =========================================================

# =========================================================
# INSTALL
# =========================================================

# pip install streamlit

# =========================================================
# RUN
# =========================================================

# python -m streamlit run video.py

# =========================================================
# IMPORTS
# =========================================================

import asyncio
import platform

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

import streamlit as st
import tempfile
import os
import subprocess
import math

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Ultimate Video Processor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎬 Video Tools")

tool = st.sidebar.radio(
    "Select Tool",
    [
        "🎞 Multiple Shorts",
        "✂ Video Cutter",
        "📱 Resize Video",
        "⚡ Compress Video",
        "🚀 Speed Control",
        "🔄 Reverse Video",
        "🔇 Mute Audio",
        "🎵 Extract MP3",
        "📸 Thumbnail Creator"
    ]
)

# =========================================================
# TITLE
# =========================================================

st.title("🎬 Ultimate Offline Video Processor")

st.write("Offline • FFmpeg • Fast Processing")

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_video = st.file_uploader(
    "📤 Upload Video",
    type=["mp4", "mov", "avi", "mkv"]
)

# =========================================================
# MAIN
# =========================================================

if uploaded_video:

    temp_dir = tempfile.mkdtemp()

    input_path = os.path.join(
        temp_dir,
        uploaded_video.name
    )

    with open(input_path, "wb") as f:
        f.write(uploaded_video.read())

    st.subheader("🎥 Input Preview")

    st.video(input_path)

    # =====================================================
    # VIDEO DURATION
    # =====================================================

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        input_path
    ]

    duration = int(
        float(
            subprocess.check_output(cmd).decode().strip()
        )
    )

    # =====================================================
    # MULTIPLE SHORTS
    # =====================================================

    if tool == "🎞 Multiple Shorts":

        st.subheader("🎞 Multiple Shorts")

        split_mode = st.selectbox(
            "Split Duration",
            [
                15,
                30,
                60
            ]
        )

        start_time = st.slider(
            "Start Time",
            0,
            duration,
            0
        )

        end_time = st.slider(
            "End Time",
            1,
            duration,
            duration
        )

        resize_mode = st.selectbox(
            "Resize Format",
            [
                "Original",
                "9:16 Reels",
                "16:9 YouTube",
                "1:1 Instagram"
            ]
        )

        quality = st.selectbox(
            "Quality",
            [
                "Non-HD",
                "HD"
            ]
        )

        if st.button("🚀 Create Shorts"):

            crf = "32"

            if quality == "HD":
                crf = "23"

            output_folder = os.path.join(
                temp_dir,
                "shorts"
            )

            os.makedirs(
                output_folder,
                exist_ok=True
            )

            total_duration = end_time - start_time

            total_parts = math.ceil(
                total_duration / split_mode
            )

            progress = st.progress(0)

            for i in range(total_parts):

                current_start = (
                    start_time +
                    (i * split_mode)
                )

                output_path = os.path.join(
                    output_folder,
                    f"short_{i+1}.mp4"
                )

                command = [
                    "ffmpeg",
                    "-y",

                    "-ss",
                    str(current_start),

                    "-i",
                    input_path,

                    "-t",
                    str(split_mode)
                ]

                # =========================================
                # RESIZE FILTERS
                # =========================================

                if resize_mode == "9:16 Reels":

                    vf = (
                        "scale=1080:1920:"
                        "force_original_aspect_ratio=decrease,"
                        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
                    )

                    command += [
                        "-vf",
                        vf
                    ]

                elif resize_mode == "16:9 YouTube":

                    vf = (
                        "scale=1280:720:"
                        "force_original_aspect_ratio=decrease,"
                        "pad=1280:720:(ow-iw)/2:(oh-ih)/2"
                    )

                    command += [
                        "-vf",
                        vf
                    ]

                elif resize_mode == "1:1 Instagram":

                    vf = (
                        "scale=1080:1080:"
                        "force_original_aspect_ratio=decrease,"
                        "pad=1080:1080:(ow-iw)/2:(oh-ih)/2"
                    )

                    command += [
                        "-vf",
                        vf
                    ]

                command += [

                    "-c:v",
                    "libx264",

                    "-preset",
                    "ultrafast",

                    "-crf",
                    crf,

                    "-c:a",
                    "aac",

                    "-threads",
                    "4",

                    output_path
                ]

                subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                progress.progress(
                    (i + 1) / total_parts
                )

            st.success("✅ Shorts Created")

            files = sorted(
                os.listdir(output_folder)
            )

            for file in files:

                file_path = os.path.join(
                    output_folder,
                    file
                )

                st.video(file_path)

                with open(file_path, "rb") as f:

                    st.download_button(
                        f"⬇ Download {file}",
                        f,
                        file_name=file
                    )

    # =====================================================
    # VIDEO CUTTER
    # =====================================================

    elif tool == "✂ Video Cutter":

        st.subheader("✂ Video Cutter")

        start_time = st.slider(
            "Start Time",
            0,
            duration,
            0
        )

        end_time = st.slider(
            "End Time",
            1,
            duration,
            duration
        )

        if st.button("🚀 Cut Video"):

            output_path = os.path.join(
                temp_dir,
                "cut_video.mp4"
            )

            command = [
                "ffmpeg",
                "-y",

                "-ss",
                str(start_time),

                "-to",
                str(end_time),

                "-i",
                input_path,

                "-c:v",
                "libx264",

                "-preset",
                "ultrafast",

                "-c:a",
                "aac",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Video Cut Complete")

            st.video(output_path)

            with open(output_path, "rb") as f:

                st.download_button(
                    "⬇ Download Video",
                    f,
                    file_name="cut_video.mp4"
                )

    # =====================================================
    # RESIZE VIDEO
    # =====================================================

    elif tool == "📱 Resize Video":

        st.subheader("📱 Resize Video")

        resize_mode = st.selectbox(
            "Resize Format",
            [
                "9:16 Reels",
                "16:9 YouTube",
                "1:1 Instagram"
            ]
        )

        quality = st.selectbox(
            "Quality",
            [
                "Non-HD",
                "HD"
            ]
        )

        if st.button("🚀 Resize Video"):

            output_path = os.path.join(
                temp_dir,
                "resize.mp4"
            )

            crf = "32"

            if quality == "HD":
                crf = "23"

            vf = ""

            if resize_mode == "9:16 Reels":

                vf = (
                    "scale=1080:1920:"
                    "force_original_aspect_ratio=decrease,"
                    "pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
                )

            elif resize_mode == "16:9 YouTube":

                vf = (
                    "scale=1280:720:"
                    "force_original_aspect_ratio=decrease,"
                    "pad=1280:720:(ow-iw)/2:(oh-ih)/2"
                )

            elif resize_mode == "1:1 Instagram":

                vf = (
                    "scale=1080:1080:"
                    "force_original_aspect_ratio=decrease,"
                    "pad=1080:1080:(ow-iw)/2:(oh-ih)/2"
                )

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-vf",
                vf,

                "-c:v",
                "libx264",

                "-preset",
                "ultrafast",

                "-crf",
                crf,

                "-c:a",
                "aac",

                "-threads",
                "4",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Resize Complete")

            st.video(output_path)

            with open(output_path, "rb") as f:

                st.download_button(
                    "⬇ Download Video",
                    f,
                    file_name="resized_video.mp4"
                )

    # =====================================================
    # COMPRESS VIDEO
    # =====================================================

    elif tool == "⚡ Compress Video":

        quality = st.selectbox(
            "Compression",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

        if st.button("🚀 Compress Video"):

            output_path = os.path.join(
                temp_dir,
                "compressed.mp4"
            )

            crf = "32"

            if quality == "Medium":
                crf = "28"

            elif quality == "High":
                crf = "23"

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-vcodec",
                "libx264",

                "-preset",
                "ultrafast",

                "-crf",
                crf,

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Compression Complete")

            st.video(output_path)

    # =====================================================
    # SPEED CONTROL
    # =====================================================

    elif tool == "🚀 Speed Control":

        speed = st.selectbox(
            "Select Speed",
            [
                "0.5x Slow",
                "Normal",
                "2x Fast"
            ]
        )

        if st.button("🚀 Apply Speed"):

            output_path = os.path.join(
                temp_dir,
                "speed.mp4"
            )

            pts = "1.0*PTS"

            if speed == "0.5x Slow":
                pts = "2.0*PTS"

            elif speed == "2x Fast":
                pts = "0.5*PTS"

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-filter:v",
                f"setpts={pts}",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Speed Applied")

            st.video(output_path)

    # =====================================================
    # REVERSE VIDEO
    # =====================================================

    elif tool == "🔄 Reverse Video":

        if st.button("🚀 Reverse Video"):

            output_path = os.path.join(
                temp_dir,
                "reverse.mp4"
            )

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-vf",
                "reverse",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Reverse Complete")

            st.video(output_path)

    # =====================================================
    # MUTE AUDIO
    # =====================================================

    elif tool == "🔇 Mute Audio":

        if st.button("🚀 Mute Audio"):

            output_path = os.path.join(
                temp_dir,
                "mute.mp4"
            )

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-an",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Audio Muted")

            st.video(output_path)

    # =====================================================
    # EXTRACT MP3
    # =====================================================

    elif tool == "🎵 Extract MP3":

        if st.button("🚀 Extract MP3"):

            output_path = os.path.join(
                temp_dir,
                "audio.mp3"
            )

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-q:a",
                "0",

                "-map",
                "a",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ MP3 Extracted")

            with open(output_path, "rb") as f:

                st.download_button(
                    "⬇ Download MP3",
                    f,
                    file_name="audio.mp3"
                )

    # =====================================================
    # THUMBNAIL
    # =====================================================

    elif tool == "📸 Thumbnail Creator":

        if st.button("🚀 Create Thumbnail"):

            output_path = os.path.join(
                temp_dir,
                "thumbnail.jpg"
            )

            command = [
                "ffmpeg",
                "-y",

                "-i",
                input_path,

                "-ss",
                "00:00:01",

                "-vframes",
                "1",

                output_path
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            st.success("✅ Thumbnail Created")

            st.image(output_path)

# =========================================================
# FOOTER
# =========================================================

st.sidebar.markdown("---")
st.sidebar.write("🚀 Offline Video Processing Tool")