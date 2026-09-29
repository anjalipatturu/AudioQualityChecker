# 🎧 Audio Quality Checker

A lightweight **audio quality analysis tool** built with Python and Streamlit to evaluate whether an audio recording is suitable for downstream speech-processing applications.

The application analyzes important audio characteristics such as **silence, clipping, RMS energy, Zero-Crossing Rate (ZCR), and approximate Signal-to-Noise Ratio (SNR)**. It also provides visualizations using the **waveform and STFT spectrogram**.

---

## 🚀 Features

* 🎵 Upload WAV, MP3, and OGG audio files
* 📊 Analyze basic audio information
* 🔊 Calculate RMS energy
* 🤫 Detect percentage of silence
* ⚠️ Detect audio clipping
* 📈 Calculate Zero-Crossing Rate (ZCR)
* 📡 Estimate Signal-to-Noise Ratio (SNR)
* 〰️ Visualize audio waveform
* 🌈 Generate STFT spectrogram
* 🧠 Provide a simple rule-based quality assessment
* 🖥️ Interactive Streamlit interface

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** — Interactive web interface
* **Librosa** — Audio processing and feature extraction
* **NumPy** — Numerical computations
* **Matplotlib** — Audio visualization
* **SoundFile** — Audio file handling

---

## 🏗️ Project Structure

```text
AudioQualityChecker/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .venv/
```

> `.venv/` is used only for local development and is excluded from GitHub using `.gitignore`.

---

## ⚙️ How It Works

The application follows a simple audio-processing pipeline:

```text
              Audio File
                  │
                  ▼
          Audio Loading
          (16 kHz Mono)
                  │
                  ▼
        ┌───────────────────┐
        │ Audio Preprocessing│
        └───────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Feature Extraction │
        └───────────────────┘
          │    │    │    │
          ▼    ▼    ▼    ▼
        RMS  Silence ZCR  SNR
          │    │    │    │
          └────┴────┴────┘
                  │
                  ▼
        Clipping Detection
                  │
                  ▼
       Waveform Visualization
                  │
                  ▼
          STFT Spectrogram
                  │
                  ▼
        Quality Assessment
```

---

## 📊 Audio Metrics

### 1. Sample Rate

The uploaded audio is loaded at:

```text
16,000 Hz
```

A 16 kHz sampling rate is commonly used in speech-processing applications.

According to the Nyquist principle, this allows frequencies up to approximately:

```text
8,000 Hz
```

to be represented.

---

### 2. RMS Energy

RMS (Root Mean Square) is used to estimate the overall energy level of the audio signal.

The calculation used is:

```text
RMS = √(mean(audio²))
```

Higher RMS generally indicates a stronger audio signal, while very low RMS can indicate a quiet or mostly silent recording.

---

### 3. Silence Detection

The application calculates the RMS energy of short audio frames.

A threshold is used:

```python
threshold = 0.01
```

Frames below this threshold are considered silent.

The application then calculates:

```text
Silence Percentage
```

This helps identify recordings containing large periods of silence.

---

### 4. Clipping Detection

Clipping can occur when an audio signal reaches the maximum representable amplitude.

The application checks:

```python
np.abs(audio) >= 0.99
```

A high clipping percentage can indicate possible distortion caused by excessive recording levels.

---

### 5. Zero-Crossing Rate

Zero-Crossing Rate (ZCR) measures how frequently the audio waveform changes sign.

It can provide basic information about the characteristics of an audio signal and is commonly used in audio and speech analysis.

---

### 6. Signal-to-Noise Ratio

The application calculates an **approximate SNR** in decibels.

The general formula is:

```text
SNR = 10 × log10(Psignal / Pnoise)
```

A higher SNR generally indicates a stronger signal relative to the estimated noise level.

> The SNR implementation in this project is a simplified estimate intended for demonstration and learning purposes, not a production-grade noise measurement.

---

## 🌈 STFT Spectrogram

The project uses the **Short-Time Fourier Transform (STFT)** to analyze how frequency content changes over time.

The processing pipeline is:

```text
Audio Signal
     ↓
STFT
     ↓
Magnitude
     ↓
Convert to Decibels
     ↓
Spectrogram
```

The spectrogram represents:

* **X-axis:** Time
* **Y-axis:** Frequency
* **Intensity:** Signal strength in dB

This is particularly useful for speech because speech is a **non-stationary signal**, meaning its frequency content changes over time.

---

## 🖥️ Application Interface

The application provides:

```text
🎧 Audio Quality Checker

        ↓

Upload Audio

        ↓

Audio Information
├── Sample Rate
├── Duration
└── RMS Energy

        ↓

Quality Metrics
├── Silence
├── Clipping
├── ZCR
└── SNR

        ↓

Waveform

        ↓

STFT Spectrogram

        ↓

Quality Assessment
```

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/anjalipatturu/AudioQualityChecker.git
```

Move into the project directory:

```bash
cd AudioQualityChecker
```

---

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

### 4. Run the application

```powershell
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 🧪 Testing

You can test the application with different types of audio:

| Audio Type          | Expected Result                                     |
| ------------------- | --------------------------------------------------- |
| Clean audio         | Lower silence and clipping                          |
| Noisy audio         | Lower estimated SNR                                 |
| Mostly silent audio | Higher silence percentage                           |
| Clipped audio       | Higher clipping percentage                          |
| Speech recording    | Visible speech patterns in waveform and spectrogram |

---

## 🎯 Quality Assessment

The current version uses simple rule-based conditions.

The audio is considered **GOOD** when:

```text
Silence < 30%
Clipping < 1%
SNR > 10 dB
```

Otherwise, the application displays:

```text
NEEDS IMPROVEMENT
```

These thresholds are simplified rules for this project and should not be treated as universal professional audio-quality standards.

---

## 🔗 Relation to Speech Processing

This project can be considered a preprocessing or quality-assessment component in a larger speech-processing pipeline:

```text
        Audio Input
             │
             ▼
   Audio Quality Checker
             │
             ▼
     Quality Assessment
             │
             ▼
   Audio Preprocessing
             │
             ▼
    Speech Processing
             │
             ▼
     AI / ML Model
```

The project was also useful for understanding audio preprocessing concepts used in my **Voxora** noise-suppression project.

---

## 🔮 Future Improvements

Possible improvements include:

* 🎙️ Add real Voice Activity Detection (VAD)
* 🔊 Improve noise estimation
* 🤖 Train an ML model for audio-quality classification
* 📱 Add microphone recording directly in the application
* 🎚️ Add automatic noise-level analysis
* 📈 Add MFCC and Mel-spectrogram features
* 🧠 Use a trained model instead of fixed quality thresholds
* ☁️ Deploy the application using Docker
* 🚀 Deploy the application to a cloud platform
* 🔄 Integrate the quality checker with a speech-processing pipeline

---

## 📚 Concepts Learned

Through this project, I explored:

* Digital Signal Processing
* Audio preprocessing
* Sampling rate
* Nyquist principle
* RMS energy
* Silence detection
* Clipping detection
* Zero-Crossing Rate
* Signal-to-Noise Ratio
* STFT
* Spectrograms
* Time-frequency analysis
* Python audio processing
* Streamlit application development

