"""
Google Gemini API Integration Module
Handles AI-powered text generation for ML explanations and code generation.

Features:
  - Automatic retry with exponential back-off on 429 (quota) errors
  - Automatic model fallback chain when a model is unavailable
"""

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ─── Model fallback chain (tried in order) ───────────────────────────────────
MODEL_CHAIN = [
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

MAX_RETRIES = 3          # retries per model
INITIAL_BACKOFF = 2      # seconds – doubles each retry


def _call_with_retry(prompt: str) -> str:
    """
    Try each model in MODEL_CHAIN. For every model:
      - Attempt up to MAX_RETRIES times with exponential back-off.
      - On 429 / quota errors, wait and retry.
      - On 404 (model not found), skip to next model immediately.

    Returns the generated text on success, or raises the last exception.
    """
    last_error = None

    for model_name in MODEL_CHAIN:
        backoff = INITIAL_BACKOFF
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text          # success
            except Exception as e:
                last_error = e
                err_str = str(e)

                # Model doesn't exist → skip to next model
                if "404" in err_str and "not found" in err_str.lower():
                    break

                # Quota / rate-limit → wait & retry same model
                if "429" in err_str or "quota" in err_str.lower():
                    if attempt < MAX_RETRIES:
                        time.sleep(backoff)
                        backoff *= 2
                        continue
                    else:
                        break   # exhausted retries → try next model

                # Any other error → bubble up immediately
                raise

    # All models exhausted
    raise last_error  # type: ignore[misc]


# ─── Public API ───────────────────────────────────────────────────────────────

def generate_explanation(topic: str) -> dict:
    """Generate a detailed explanation of an ML topic using Gemini AI."""
    try:
        if not GEMINI_API_KEY:
            return {
                'success': False,
                'error': 'Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.'
            }

        prompt = f"""
You are an expert machine learning educator. Provide a clear, comprehensive explanation of the following topic:

Topic: {topic}

Structure your explanation as follows:
1. **Introduction** – Brief overview of the concept
2. **Core Concepts** – Detailed explanation of key principles
3. **How It Works** – Step-by-step breakdown
4. **Real-World Applications** – Practical use cases
5. **Key Takeaways** – Summary of important points

Use clear language suitable for students learning machine learning.
"""

        text = _call_with_retry(prompt)
        return {
            'success': True,
            'explanation': text,
            'topic': topic,
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating explanation: {str(e)}'
        }


def generate_code_example(topic: str, include_comments: bool = True) -> dict:
    """Generate Python code implementation for an ML algorithm or concept."""
    try:
        if not GEMINI_API_KEY:
            return {
                'success': False,
                'error': 'Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.'
            }

        comments_instruction = "with detailed comments" if include_comments else "with minimal comments"

        prompt = f"""
You are an expert Python programmer specialising in machine learning.

Generate a complete, runnable Python implementation of: {topic}

Requirements:
- Write clean, well-structured Python code {comments_instruction}
- Include necessary imports (NumPy, scikit-learn, TensorFlow, or PyTorch as appropriate)
- Add example usage at the end showing how to run the code
- Make it educational and easy to understand for students
- Ensure the code follows best practices

Format:
1. Code implementation
2. Brief explanation of what the code does
"""

        text = _call_with_retry(prompt)
        return {
            'success': True,
            'code': text,
            'topic': topic,
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating code: {str(e)}'
        }


def generate_visual_description(topic: str) -> dict:
    """Generate a detailed description for creating visual diagrams of ML concepts."""
    try:
        if not GEMINI_API_KEY:
            return {
                'success': False,
                'error': 'Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.'
            }

        prompt = f"""
Describe how to create a visual diagram for the following machine learning concept: {topic}

Include:
- Key components to visualise
- Flow of data or information
- Important labels and annotations
- Colour suggestions for different elements
- Layout recommendations

Make the description detailed enough that it could be used to create an educational diagram.
"""

        text = _call_with_retry(prompt)
        return {
            'success': True,
            'description': text,
            'topic': topic,
        }

    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating visual description: {str(e)}'
        }
