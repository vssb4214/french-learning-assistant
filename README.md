# French Voice Assistant with Cultural Knowledge

A voice-activated French conversation assistant enhanced with knowledge from French literature and cinema. The assistant responds as "Lucas," a 21-year-old French student, using simple vocabulary and providing cultural context from French films and books.

## Features

- **Voice Activity Detection**: Automatically detects when you start and stop speaking
- **French Speech Recognition**: Uses Whisper to transcribe French speech accurately
- **Cultural Knowledge Integration**: References relevant content from French literature and cinema
- **Multi-Document Support**: Works with PDFs, text files, and markdown documents
- **Natural Conversation**: Maintains context throughout the conversation
- **Source Attribution**: Shows which cultural work is being referenced
- **Simple Vocabulary**: Uses elementary-level French suitable for learners

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key
```bash
export OPENAI_API_KEY="your-actual-api-key-here"
```

Or edit `config.py` and replace `YOUR_API_KEY_HERE` with your actual API key.

### 3. Setup Cultural Documents
```bash
python setup_documents.py
```

This creates a `Info for French` folder with guidelines for adding cultural content.

### 4. Add Your Cultural Content

**✅ LEGAL SOURCES to use:**
- IMDb plot summaries
- Wikipedia film articles
- Your own viewing notes
- Educational website analyses
- Book summaries and reviews

**❌ AVOID:**
- Full movie transcripts (copyrighted)
- Complete book texts (unless public domain)
- Any copyrighted material

### 5. Process Documents
After adding files, run the setup script again:
```bash
python setup_documents.py
```

### 6. Start the Assistant
```bash
python french_vad_assistant.py
```

## Usage

1. **Start the assistant** and wait for "Listening..." prompt
2. **Speak in French** - the system will detect your voice automatically
3. **Wait for processing** - you'll see "Processing speech..." when done
4. **Get response** - Lucas will respond with simple French and cultural context

## Example Conversation

```
You: Parle-moi du Petit Prince
Lucas: Le Petit Prince est un livre d'Antoine de Saint-Exupéry. 
Il raconte l'histoire d'un petit garçon qui voyage de planète en planète. 
Il rencontre des personnages bizarres sur chaque planète.

Cultural Context:
Source: LE PETIT PRINCE.pdf
Le petit prince arrive sur une planète où il y a un roi. 
Le roi pense qu'il commande tout, mais il n'y a personne d'autre sur sa planète.
```

## Configuration

Edit `config.py` to customize:

- **Audio settings**: Sample rate, frame duration, silence detection
- **Whisper model**: Choose between tiny, base, small, medium, large
- **RAG settings**: Chunk size, overlap, context length
- **Assistant personality**: System prompt and response style

## File Structure

```
├── french_vad_assistant.py    # Main voice assistant
├── multi_document_rag.py      # Document processing and search
├── petit_prince_rag.py        # Single document RAG (legacy)
├── setup_documents.py         # Document setup script
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── Info for French/           # Your cultural documents
├── example_documents/         # Example content
└── README.md                  # This file
```

## Technical Details

### Voice Activity Detection
- Uses WebRTC VAD for real-time speech detection
- Configurable sensitivity and silence thresholds
- Automatic recording start/stop

### Speech Recognition
- OpenAI Whisper for French speech transcription
- Configurable model size (tiny to large)
- Optimized for French language

### Document Processing
- Multi-document RAG system with sentence transformers
- Supports PDF and text files
- Semantic search with cosine similarity
- Caching for faster startup

### AI Integration
- OpenAI GPT-3.5-turbo for responses
- Cultural context injection
- Simple vocabulary enforcement
- Conversation memory

## Requirements

- Python 3.8+
- Microphone access
- OpenAI API key
- Internet connection (for AI responses)

## Dependencies

- `webrtcvad`: Voice activity detection
- `openai`: AI responses
- `pyaudio`: Audio recording
- `openai-whisper`: Speech recognition
- `PyPDF2`: PDF text extraction
- `sentence-transformers`: Document embeddings
- `scikit-learn`: Similarity calculations

## Troubleshooting

### Audio Issues
- Ensure microphone permissions are granted
- Check audio device settings
- Try adjusting VAD sensitivity in config

### API Issues
- Verify OpenAI API key is correct
- Check internet connection
- Monitor API usage limits

### Document Issues
- Ensure documents are in supported formats
- Check file encoding (UTF-8 recommended)
- Verify document processing completed successfully

## Legal Notice

This project is for educational purposes. Users are responsible for ensuring all cultural content they add is legally obtained and properly attributed. The system is designed to work with:

- Public domain texts
- Plot summaries and analyses
- Personal notes and reviews
- Educational content

Do not use copyrighted material without proper authorization.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please respect copyright laws when adding cultural content.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration options
3. Ensure all dependencies are installed
4. Verify your OpenAI API key is working