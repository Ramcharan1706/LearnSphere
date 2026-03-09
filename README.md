# ML Learning Assistant 🧠

A comprehensive full-stack web application for learning machine learning concepts through AI-powered explanations, code generation, audio lessons, and visual diagrams.

![ML Learning Assistant](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

### Four Learning Modes

1. **Text Explanation Mode** 📚
   - AI-generated detailed explanations of ML topics
   - Structured content with real-world applications
   - Copy and share functionality

2. **Code Generation Mode** 💻
   - Generate Python implementations of ML algorithms
   - Production-ready code with detailed comments
   - Downloadable .py files
   - Syntax validation
   - Code statistics

3. **Audio Learning Mode** 🎧
   - Convert explanations to audio (MP3)
   - Downloadable audio files
   - Support for slow speech mode
   - Perfect for learning on the go

4. **Visual Diagram Mode** 📊
   - Interactive Mermaid.js diagrams
   - AI-generated diagram descriptions
   - Flowcharts and architecture visualizations

## 🛠 Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0
- Google Gemini AI API
- gTTS (Google Text-to-Speech)

**Frontend:**
- HTML5
- CSS3 (Custom styling)
- JavaScript (Vanilla)
- Mermaid.js for diagrams

**Libraries:**
- Flask-CORS
- python-dotenv
- requests
- Pillow

## 📁 Project Structure

```
ML-Learning-Assistant/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── genai_utils.py             # Gemini AI integration
│   ├── audio_utils.py             # Text-to-speech functionality
│   ├── image_utils.py             # Diagram generation
│   └── code_executor.py           # Code file management
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Main stylesheet
│   ├── js/
│   │   ├── main.js                # Common functions
│   │   ├── text_explanation.js   # Text mode JS
│   │   ├── code_generation.js    # Code mode JS
│   │   ├── audio_learning.js     # Audio mode JS
│   │   └── image_visualization.js # Image mode JS
│   └── audio/                     # Generated audio files
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Landing page
│   ├── text_explanation.html     # Text mode
│   ├── code_generation.html      # Code mode
│   ├── audio_learning.html       # Audio mode
│   └── image_visualization.html  # Image mode
│
└── generated_code/                 # Generated Python files
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
  - Download from: https://www.python.org/downloads/
  - Verify: `python --version`

- **pip** (Python package manager)
  - Usually comes with Python
  - Verify: `pip --version`

- **Git** (optional, for cloning)
  - Download from: https://git-scm.com/

- **Google Gemini API Key**
  - Get your free API key from: https://makersuite.google.com/app/apikey

## 🚀 Local Setup

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd ML-Learning-Assistant

# Or download and extract the ZIP file
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask and Flask-CORS
- google-generativeai (Gemini AI)
- gTTS (Google Text-to-Speech)
- python-dotenv
- requests
- Pillow
- gunicorn (for production)

### Step 4: Configure Environment Variables

1. Copy the example environment file:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Edit the `.env` file and add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
HOST=0.0.0.0
PORT=5000
```

**Important:** Never commit your `.env` file with real API keys to version control!

## ⚙️ Configuration

### Getting Google Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in your `.env` file

### Environment Variables Explained

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Required |
| `FLASK_ENV` | Flask environment mode | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Flask secret key for sessions | Random string |
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port number | `5000` |

## 🏃 Running the Application

### Development Mode

```bash
python app.py
```

The application will start at: **http://localhost:5000**

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║        ML Learning Assistant - Server Starting            ║
╚═══════════════════════════════════════════════════════════╝
    
🚀 Server running at: http://0.0.0.0:5000
📚 Learning Modes Available:
   - Text Explanation
   - Code Generation
   - Audio Learning
   - Visual Diagrams
    
⚙️  Debug Mode: True
🔑 API Key Configured: Yes
    
Press CTRL+C to stop the server
```

### Production Mode

For production deployment:

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## 📖 Usage Guide

### 1. Text Explanation Mode

**Purpose:** Get comprehensive explanations of ML concepts

**How to use:**
1. Navigate to "Text Explanation" from the main menu
2. Enter a topic (e.g., "Neural Networks", "Backpropagation")
3. Click "Generate Explanation"
4. Read the AI-generated explanation
5. Use "Copy" to copy text or "Audio" to convert to speech

**Example prompts:**
- "Explain backpropagation in neural networks"
- "What is gradient descent optimization?"
- "How do convolutional neural networks work?"
- "Difference between supervised and unsupervised learning"

### 2. Code Generation Mode

**Purpose:** Generate Python implementations of ML algorithms

**How to use:**
1. Navigate to "Code Generation"
2. Enter an algorithm name (e.g., "K-Means Clustering")
3. Choose whether to include detailed comments
4. Click "Generate Code"
5. Download the .py file or copy the code

**Example prompts:**
- "Backpropagation algorithm from scratch"
- "K-Means clustering implementation"
- "Simple neural network with NumPy"
- "Decision tree classifier"
- "Linear regression with gradient descent"

**Features:**
- Syntax validation
- Code statistics (lines, functions, classes)
- Downloadable Python files
- Ready for Google Colab

### 3. Audio Learning Mode

**Purpose:** Convert text to audio for mobile learning

**How to use:**
1. Navigate to "Audio Learning"
2. Enter a topic or paste text
3. Optionally click "Generate Explanation First" for AI content
4. Choose slow speech for complex topics
5. Click "Generate Audio"
6. Listen or download the MP3 file

**Tips:**
- Use slow speech for better comprehension
- Maximum 5000 characters per audio
- Downloads are in MP3 format
- Perfect for commuting or exercising

### 4. Visual Diagram Mode

**Purpose:** Visualize ML concepts with interactive diagrams

**How to use:**
1. Navigate to "Visual Diagrams"
2. Enter a concept to visualize
3. Choose diagram type (Mermaid, Description, or Both)
4. Click "Generate Diagram"
5. View the interactive diagram

**Supported diagrams:**
- Neural network architectures
- Backpropagation flow
- Gradient descent process
- Decision trees
- General flowcharts

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Generate Explanation
```http
POST /api/generate-explanation
Content-Type: application/json

{
  "topic": "neural networks"
}
```

**Response:**
```json
{
  "success": true,
  "explanation": "Neural networks are...",
  "topic": "neural networks"
}
```

#### 2. Generate Code
```http
POST /api/generate-code
Content-Type: application/json

{
  "topic": "backpropagation",
  "include_comments": true
}
```

#### 3. Generate Audio
```http
POST /api/generate-audio
Content-Type: application/json

{
  "text": "Neural networks are computational models...",
  "language": "en",
  "slow": false
}
```

#### 4. Generate Diagram
```http
POST /api/generate-diagram
Content-Type: application/json

{
  "topic": "convolutional neural network"
}
```

#### 5. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "ML Learning Assistant",
  "version": "1.0.0"
}
```

## 🌐 Deployment

### Deploy to Render

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**
   - Connect your GitHub repository
   - Or upload your project files

3. **Configure the service:**
   ```
   Name: ml-learning-assistant
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
   ```

4. **Add environment variables:**
   - Go to "Environment" tab
   - Add your `GEMINI_API_KEY`
   - Add `FLASK_ENV=production`
   - Add `SECRET_KEY=<random-string>`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access your app at the provided URL

### Deploy to Railway

1. **Create a Railway account** at https://railway.app

2. **Create a new project**
   - Connect GitHub or upload files

3. **Add environment variables:**
   ```
   GEMINI_API_KEY=your_key_here
   FLASK_ENV=production
   SECRET_KEY=your_secret_key
   PORT=5000
   ```

4. **Deploy**
   - Railway automatically detects Python and Flask
   - Sets up the deployment pipeline
   - Provides a public URL

### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Follow instructions at https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile**
   ```
   web: gunicorn app:app
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create ml-learning-assistant
   git push heroku main
   heroku config:set GEMINI_API_KEY=your_key_here
   heroku open
   ```

## 🐛 Troubleshooting

### Common Issues

**1. API Key Error**
```
Error: Gemini API key not configured
```
**Solution:** Check your `.env` file and ensure `GEMINI_API_KEY` is set correctly.

**2. Module Not Found**
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

**3. Port Already in Use**
```
OSError: [Errno 48] Address already in use
```
**Solution:** Change the port in `.env` or kill the process using the port:
```bash
# Find process on port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

**4. Audio Generation Fails**
```
Error generating audio: 403 Forbidden
```
**Solution:** Check internet connection. gTTS requires internet access to Google's TTS service.

**5. Gemini API Rate Limit**
```
Error: 429 Too Many Requests
```
**Solution:** Wait a few minutes. Gemini API has rate limits. Consider upgrading your API plan for higher limits.

### Debug Mode

Enable detailed error messages:
```python
# In .env file
FLASK_DEBUG=True
FLASK_ENV=development
```

### Logs

Check console output for detailed error messages and stack traces.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language model capabilities
- **gTTS** for text-to-speech conversion
- **Mermaid.js** for beautiful diagram rendering
- **Flask** community for excellent web framework

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## 🎯 Future Enhancements

- [ ] User authentication and saved history
- [ ] Support for multiple languages
- [ ] Advanced diagram types (PlotNeuralNet integration)
- [ ] Code execution sandbox
- [ ] Quiz mode for testing knowledge
- [ ] Mobile app version
- [ ] Offline mode with cached explanations

---

**Built with ❤️ for ML learners worldwide**

Happy Learning! 🚀
