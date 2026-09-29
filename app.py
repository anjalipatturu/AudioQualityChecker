import streamlit as st
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Audio Quality Checker",
    page_icon="🎧",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🎧 Audio Quality Checker")

st.write(
    "Analyze whether an audio recording is suitable "
    "for speech processing."
)


# --------------------------------------------------
# Upload Audio
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=["wav", "mp3", "ogg"]
)


# --------------------------------------------------
# Process Audio
# --------------------------------------------------

if uploaded_file:

    try:

        # Load audio at 16 kHz
        audio, sr = librosa.load(
            uploaded_file,
            sr=16000,
            mono=True
        )

        # Check whether audio contains data
        if len(audio) == 0:
            st.error("The uploaded audio file is empty.")
            st.stop()

        # --------------------------------------------------
        # Basic Information
        # --------------------------------------------------

        duration = len(audio) / sr

        # --------------------------------------------------
        # RMS Energy
        # --------------------------------------------------

        rms = np.sqrt(
            np.mean(audio ** 2)
        )

        # --------------------------------------------------
        # Silence Detection
        # --------------------------------------------------

        rms_frames = librosa.feature.rms(
            y=audio
        )[0]

        threshold = 0.01

        silence_percentage = (
            np.mean(rms_frames < threshold) * 100
        )

        # --------------------------------------------------
        # Clipping Detection
        # --------------------------------------------------

        clipped = np.abs(audio) >= 0.99

        clipping_percentage = (
            np.mean(clipped) * 100
        )

        # --------------------------------------------------
        # Zero Crossing Rate
        # --------------------------------------------------

        zcr = librosa.feature.zero_crossing_rate(
            audio
        )[0]

        average_zcr = np.mean(zcr)

        # --------------------------------------------------
        # Approximate SNR
        # --------------------------------------------------

        power = audio ** 2

        noise_power = np.percentile(
            power,
            20
        )

        signal_power = np.mean(power)

        if noise_power > 0:

            snr = 10 * np.log10(
                signal_power / noise_power
            )

        else:

            snr = 0

        # ==================================================
        # AUDIO INFORMATION
        # ==================================================

        st.subheader("🎵 Audio Information")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Sample Rate",
            f"{sr} Hz"
        )

        col2.metric(
            "Duration",
            f"{duration:.2f} sec"
        )

        col3.metric(
            "RMS Energy",
            f"{rms:.4f}"
        )

        # ==================================================
        # QUALITY METRICS
        # ==================================================

        st.subheader("📊 Quality Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Silence",
            f"{silence_percentage:.2f}%"
        )

        col2.metric(
            "Clipping",
            f"{clipping_percentage:.2f}%"
        )

        col3.metric(
            "ZCR",
            f"{average_zcr:.4f}"
        )

        col4.metric(
            "SNR",
            f"{snr:.2f} dB"
        )

        # ==================================================
        # WAVEFORM
        # ==================================================

        st.subheader("〰️ Waveform")

        fig_waveform, ax_waveform = plt.subplots(
            figsize=(10, 4)
        )

        librosa.display.waveshow(
            audio,
            sr=sr,
            ax=ax_waveform
        )

        ax_waveform.set_title(
            "Audio Waveform"
        )

        ax_waveform.set_xlabel(
            "Time (seconds)"
        )

        ax_waveform.set_ylabel(
            "Amplitude"
        )

        fig_waveform.tight_layout()

        st.pyplot(
            fig_waveform,
            use_container_width=True
        )

        plt.close(fig_waveform)

        # ==================================================
        # SPECTROGRAM
        # ==================================================

        st.subheader("🌈 Spectrogram")

        # Calculate STFT
        stft = librosa.stft(
            audio,
            n_fft=1024,
            hop_length=256
        )

        # Convert complex values to magnitude
        magnitude = np.abs(stft)

        # Convert magnitude to decibels
        db = librosa.amplitude_to_db(
            magnitude,
            ref=np.max
        )

        # Create spectrogram figure
        fig_spec, ax_spec = plt.subplots(
            figsize=(10, 5)
        )

        # Display spectrogram
        img = librosa.display.specshow(
            db,
            sr=sr,
            hop_length=256,
            x_axis="time",
            y_axis="hz",
            ax=ax_spec
        )

        ax_spec.set_title(
            "STFT Spectrogram"
        )

        ax_spec.set_xlabel(
            "Time (seconds)"
        )

        ax_spec.set_ylabel(
            "Frequency (Hz)"
        )

        # Add color bar
        fig_spec.colorbar(
            img,
            ax=ax_spec,
            format="%+2.0f dB"
        )

        fig_spec.tight_layout()

        # Display spectrogram
        st.pyplot(
            fig_spec,
            use_container_width=True
        )

        # Close figure
        plt.close(fig_spec)

        # ==================================================
        # TECHNICAL INFORMATION
        # ==================================================

        with st.expander("🔍 Technical Information"):

            st.write(
                "Audio samples:",
                len(audio)
            )

            st.write(
                "Sample rate:",
                sr
            )

            st.write(
                "STFT shape:",
                stft.shape
            )

            st.write(
                "Spectrogram shape:",
                db.shape
            )

        # ==================================================
        # QUALITY DECISION
        # ==================================================

        st.subheader("🧠 Quality Assessment")

        if (
            silence_percentage < 30
            and clipping_percentage < 1
            and snr > 10
        ):

            st.success(
                "Audio Quality: GOOD ✅"
            )

        else:

            st.warning(
                "Audio Quality: NEEDS IMPROVEMENT ⚠️"
            )

    except Exception as e:

        st.error(
            "Something went wrong while processing the audio."
        )

        st.exception(e)