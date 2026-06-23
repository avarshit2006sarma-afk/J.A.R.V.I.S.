# J.A.R.V.I.S

AI-powered virtual desktop assistant inspired by Tony Stark's J.A.R.V.I.S, built using Python. The assistant combines voice interaction, face recognition, automation, system controls, and AI capabilities to create a smart personal assistant experience.

---

## Features

### Voice Interaction
- Speech Recognition
- Text-to-Speech Responses
- Wake Word Activation

### AI Capabilities
- Gemini AI Integration
- Conversational Responses
- Intelligent Query Handling

### Face Recognition
- User Authentication
- Secure Access Verification

### System Controls
- Open Applications
- Adjust Volume
- Control Brightness
- Perform Basic Automation Tasks

### Utilities
- Weather Information
- Current Time & Date
- Web Search Assistance

### User Interface
- Custom GUI
- Animated Visual Feedback
- Interactive Assistant Dashboard

---

## Tech Stack

- Python 3.11
- OpenCV
- Face Recognition
- SpeechRecognition
- Pyttsx3
- CustomTkinter
- Pillow
- Google Gemini API
- Requests
- Python-dotenv

---

## Project Structure

```text
J.A.R.V.I.S/
│
├── assets/
├── screenshots/
├── src/
├── known_face_fixed.jpg
├── requirements.txt
├── README.md
└── .env
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/avarshit2006sarma-afk/J.A.R.V.I.S.git
cd J.A.R.V.I.S
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=your_api_key_here
```

### Run J.A.R.V.I.S

```bash
python main.py
```

---

## Future Improvements

- Multi-user Face Recognition
- Cross-platform Support
- Smart Home Integration
- Custom Command Builder
- Improved AI Memory
- Mobile Companion App

---

## Author

**A. Varshit Sarma**

B.Tech Electronics and Communication Engineering (Embedded Systems)

VIT-AP University

---

## License

This project is licensed under the MIT License.
