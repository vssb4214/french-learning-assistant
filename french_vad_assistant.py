#!/usr/bin/env python3
"""
French Voice Assistant with Cultural Knowledge
A voice-activated French conversation assistant enhanced with knowledge from French literature and cinema.
"""

import webrtcvad
import collections
import sys
import signal
import whisper
from openai import OpenAI
import pyaudio
import wave
import os
import time
import numpy as np
from scipy import signal as scipy_signal
import textwrap
from multi_document_rag import MultiDocumentRAG
import config
import importlib

# Force reload config to pick up changes
importlib.reload(config)

# Suppress warnings for cleaner output
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Configuration
client = OpenAI(api_key=config.OPENAI_API_KEY)
FRAME_DURATION = config.FRAME_DURATION
SAMPLE_RATE = config.SAMPLE_RATE
CHANNELS = config.CHANNELS
RECORD_SECONDS = config.RECORD_SECONDS
MAX_SILENCE_MS = config.MAX_SILENCE_MS
MODEL_SIZE = config.MODEL_SIZE

# Prepare VAD - optimized for faster response
vad = webrtcvad.Vad(2)  # 0-3 (aggressiveness) - moderately aggressive for quick detection

# Whisper model
model = whisper.load_model(MODEL_SIZE, device="cpu", download_root=None, in_memory=False)

# Initialize Multi-Document RAG system
rag_system = None
try:
    if os.path.exists(config.DOCUMENTS_FOLDER):
        print("Loading cultural knowledge...")
        rag_system = MultiDocumentRAG()
        rag_system.process_documents_folder(config.DOCUMENTS_FOLDER)
        stats = rag_system.get_document_stats()
        print(f"Ready! {len(stats)} cultural works loaded.")
    else:
        print(f"Cultural documents folder '{config.DOCUMENTS_FOLDER}' not found.")
        print("Run 'python setup_documents.py' to create the folder structure.")
except Exception as e:
    print(f"Error loading cultural knowledge: {e}")
    print("Continuing without cultural context...")

class AudioBuffer:
    def __init__(self, sample_rate, frame_duration_ms):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.buffer = collections.deque(maxlen=30)  # Keep last 30 frames
        self.speech_buffer = []
        self.is_recording = False
        self.silence_frames = 0
        self.max_silence_frames = MAX_SILENCE_MS // frame_duration_ms

    def add_frame(self, frame):
        self.buffer.append(frame)
        
        # Check for speech activity
        is_speech = vad.is_speech(frame, self.sample_rate)
        
        if is_speech:
            self.silence_frames = 0
            if not self.is_recording:
                self.is_recording = True
                self.speech_buffer = list(self.buffer)  # Start with recent context
            else:
                self.speech_buffer.append(frame)
        else:
            if self.is_recording:
                self.silence_frames += 1
                self.speech_buffer.append(frame)
                
                if self.silence_frames >= self.max_silence_frames:
                    self.is_recording = False
                    return True  # Speech ended
        
        return False

    def get_audio_data(self):
        if not self.speech_buffer:
            return None
        
        # Convert to numpy array
        audio_data = b''.join(self.speech_buffer)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Normalize and convert to float
        audio_float = audio_array.astype(np.float32) / 32768.0
        
        return audio_float

def record_audio():
    """Record audio using PyAudio with VAD"""
    audio = pyaudio.PyAudio()
    
    try:
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=FRAME_DURATION * SAMPLE_RATE // 1000
        )
        
        buffer = AudioBuffer(SAMPLE_RATE, FRAME_DURATION)
        
        print("Listening... (speak now)")
        
        while True:
            frame = stream.read(FRAME_DURATION * SAMPLE_RATE // 1000, exception_on_overflow=False)
            
            if buffer.add_frame(frame):
                print("Processing speech...")
                break
        
        stream.stop_stream()
        stream.close()
        
        return buffer.get_audio_data()
        
    finally:
        audio.terminate()

def transcribe_audio(audio_data):
    """Transcribe audio using Whisper"""
    if audio_data is None:
        return None
    
    try:
        result = model.transcribe(audio_data, language="fr")
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def get_cultural_context(user_input):
    """Get relevant cultural context from RAG system"""
    if not rag_system:
        return ""
    
    try:
        relevant_chunks = rag_system.search(user_input, top_k=2)
        if relevant_chunks:
            context = "\n".join([f"Source: {chunk['source']}\n{chunk['text']}" for chunk in relevant_chunks])
            return f"\n\nCultural Context:\n{context}"
    except Exception as e:
        print(f"Error getting cultural context: {e}")
    
    return ""

def get_ai_response(user_input, cultural_context=""):
    """Get AI response from OpenAI"""
    try:
        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": user_input + cultural_context}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI response error: {e}")
        return "Désolé, je ne peux pas répondre maintenant."

def print_response(text, width=70):
    """Print response with word wrapping"""
    wrapped = textwrap.fill(text, width=width)
    print(f"\nLucas: {wrapped}\n")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nAu revoir!")
    sys.exit(0)

def main():
    """Main conversation loop"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("French Voice Assistant with Cultural Knowledge")
    print("=" * 60)
    print("Press Ctrl+C to exit")
    print("Speak in French and I'll respond as Lucas!")
    print("=" * 60)
    
    if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Please set your OpenAI API key in config.py or as environment variable")
        return
    
    while True:
        try:
            # Record audio
            audio_data = record_audio()
            if audio_data is None:
                continue
            
            # Transcribe
            user_input = transcribe_audio(audio_data)
            if not user_input:
                print("Could not understand. Please try again.")
                continue
            
            print(f"You: {user_input}")
            
            # Get cultural context
            cultural_context = get_cultural_context(user_input)
            
            # Get AI response
            response = get_ai_response(user_input, cultural_context)
            
            # Print response
            print_response(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print("Au revoir!")

if __name__ == "__main__":
    main()