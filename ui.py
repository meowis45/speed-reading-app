import streamlit as st
import numpy as np
import cv2
import os
import time
from concurrent.futures import ProcessPoolExecutor
from app import create_word_frame



def concat_videos(video_files, output_file):
    """Stitches mp4 files together using ffmpeg (fast stream copy)"""
    import subprocess

    # Create a temporary list file for ffmpeg
    with open("mylist.txt", "w") as f:
        for vid in video_files:
            f.write(f"file '{vid}'\n")

    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "mylist.txt",
        "-c", "copy", "-y",
        output_file
    ], check=True)

    # Cleanup
    os.remove("mylist.txt")
    for vid in video_files:
        if os.path.exists(vid):
            os.remove(vid)


def render_chunk(chunk_data):
    """
    Independent worker function.
    args: (chunk_id, words, start_wpm, end_wpm, total_words, global_start_index)
    """
    chunk_id, words, s_wpm, e_wpm, total_count, global_offset = chunk_data

    filename = f"temp_chunk_{chunk_id}.mp4"
    fps = 30
    height, width = 1920, 1080

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    for i, word in enumerate(words):
        global_index = global_offset + i

        current_wpm = s_wpm + (e_wpm - s_wpm) * (global_index / total_count)

        base_duration = 60 / current_wpm
        weight = 1.0 + (len(word) - 5) * 0.05
        duration = max(0.08, base_duration * weight)

        pil_image = create_word_frame(word, current_wpm)
        frame_bgr = cv2.cvtColor(pil_image, cv2.COLOR_RGB2BGR)

        frames_to_write = int(duration * fps)

        for _ in range(frames_to_write):
            out.write(frame_bgr)

    out.release()
    return filename


st.set_page_config(page_title="Fixed-Focus Reader")
st.title("Fixed-Focus RSVP Generator (High Performance)")

text_input = st.text_area("Paste Content", "The secret to speed reading is keeping your eyes perfectly still...",
                          height=150)

col1, col2 = st.columns(2)
with col1:
    s_wpm = st.slider("Start Speed", 200, 800, 400)
with col2:
    e_wpm = st.slider("Target Speed", 400, 1200, 800)

output_filename = "fixed_focus_reading.mp4"

if st.button("🚀 Generate Video (Multi-Threaded)", use_container_width=True):
    if not text_input.strip():
        st.warning("Please enter text.")
    else:
        st_time = time.time()
        words = text_input.split()
        total_words = len(words)

        num_cores = os.cpu_count() or 4
        if total_words < 50: num_cores = 1

        chunk_size = int(np.ceil(total_words / num_cores))
        chunks_payload = []

        for i in range(num_cores):
            start = i * chunk_size
            end = start + chunk_size
            word_batch = words[start:end]

            if not word_batch: continue

            payload = (i, word_batch, s_wpm, e_wpm, total_words, start)
            chunks_payload.append(payload)

        progress_bar = st.progress(0)
        status_text = st.empty()

        temp_files = []
        status_text.text(f"Rendering on {num_cores} cores...")

        try:
            with ProcessPoolExecutor(max_workers=num_cores) as executor:
                results = executor.map(render_chunk, chunks_payload)

                for i, vid_file in enumerate(results):
                    temp_files.append(vid_file)
                    progress_bar.progress((i + 1) / len(chunks_payload))

            status_text.text("Stitching chunks together...")
            temp_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

            concat_videos(temp_files, output_filename)

            end_time = time.time()
            st.success(f"Video generated in {end_time - st_time:.2f} seconds!")

            st.video(output_filename)

            with open(output_filename, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name="fixed_speed_reading.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
            for f in temp_files:
                if os.path.exists(f): os.remove(f)