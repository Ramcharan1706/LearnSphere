"""
Audio Generation Module using Google Text-to-Speech (gTTS)
Converts text explanations into downloadable audio files
"""

import os
from gtts import gTTS
import hashlib
from datetime import datetime


def generate_audio(text: str, language: str = 'en', slow: bool = False) -> dict:
    """
    Convert text to speech and save as MP3 file
    
    Args:
        text (str): The text content to convert to speech
        language (str): Language code (default: 'en' for English)
        slow (bool): Whether to speak slowly for better clarity
        
    Returns:
        dict: Contains 'success' status, 'audio_url', 'filename', and optional 'error'
    """
    try:
        if not text or len(text.strip()) == 0:
            return {
                'success': False,
                'error': 'No text provided for audio generation'
            }
        
        # Limit text length to prevent very large audio files
        max_length = 5000
        if len(text) > max_length:
            text = text[:max_length] + "... (content truncated for audio generation)"
        
        # Create unique filename based on text hash and timestamp
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'ml_audio_{timestamp}_{text_hash}.mp3'
        
        # Define output path
        audio_dir = os.path.join('static', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        filepath = os.path.join(audio_dir, filename)
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(filepath)
        
        # Return URL path for frontend access
        audio_url = f'/static/audio/{filename}'
        
        return {
            'success': True,
            'audio_url': audio_url,
            'filename': filename,
            'message': 'Audio generated successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating audio: {str(e)}'
        }


def delete_old_audio_files(max_age_hours: int = 24):
    """
    Clean up old audio files to save disk space
    
    Args:
        max_age_hours (int): Delete files older than this many hours (default: 24)
    """
    try:
        audio_dir = os.path.join('static', 'audio')
        if not os.path.exists(audio_dir):
            return
        
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(audio_dir):
            if filename.endswith('.mp3'):
                filepath = os.path.join(audio_dir, filename)
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    print(f"Deleted old audio file: {filename}")
                    
    except Exception as e:
        print(f"Error cleaning up audio files: {str(e)}")


def get_audio_info(filename: str) -> dict:
    """
    Get information about an audio file
    
    Args:
        filename (str): Name of the audio file
        
    Returns:
        dict: File information including size and creation time
    """
    try:
        filepath = os.path.join('static', 'audio', filename)
        
        if not os.path.exists(filepath):
            return {
                'success': False,
                'error': 'Audio file not found'
            }
        
        file_stats = os.stat(filepath)
        file_size_kb = file_stats.st_size / 1024
        creation_time = datetime.fromtimestamp(file_stats.st_ctime)
        
        return {
            'success': True,
            'filename': filename,
            'size_kb': round(file_size_kb, 2),
            'created_at': creation_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error getting audio info: {str(e)}'
        }
