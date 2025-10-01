# Quick Start Guide

## 🚀 Get Your French Assistant Running with Cultural Knowledge

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Your OpenAI API Key
```bash
export OPENAI_API_KEY="your-actual-api-key-here"
```

### Step 3: Create Document Structure
```bash
python setup_documents.py
```
This creates a `documents` folder with guidelines.

### Step 4: Add Your Cultural Content

**✅ LEGAL SOURCES to use:**
- IMDb plot summaries
- Wikipedia film articles
- Your own viewing notes
- Educational website analyses
- Book summaries and reviews

**❌ AVOID:**
- Full movie transcripts (copyrighted)
- Pirated content
- Unauthorized reproductions

**Example files to add to `documents/` folder:**
```
documents/
├── le_petit_prince.pdf                    # Your book PDF
├── coco_avant_chanel_summary.txt          # Plot summary
├── la_mome_analysis.txt                   # Film analysis
├── cyrano_notes.txt                       # Your notes
├── femmes_6eme_etage_review.txt           # Review/summary
└── joyeux_noel_summary.txt                # Plot summary
```

### Step 5: Process Your Documents
```bash
python setup_documents.py
```
Run again after adding files. This will:
- Extract and chunk all text
- Create searchable embeddings
- Test the system

### Step 6: Start Your Assistant
```bash
python french_vad_assistant.py
```

## 💡 Tips for Best Results

1. **File Naming**: Include keywords like `coco_avant_chanel`, `la_mome`, `cyrano` in filenames
2. **Content Quality**: Detailed summaries work better than brief descriptions
3. **French Content**: Use French-language summaries when possible
4. **Multiple Sources**: Add multiple perspectives on the same work

## 🧪 Test Your Setup

Try speaking these phrases to test cultural references:
- "Parle-moi de Coco Chanel"
- "Qu'est-ce que tu penses de l'amour?"
- "Raconte-moi l'histoire de Cyrano"

## 📁 Example Content

Check `example_documents/coco_avant_chanel_summary.txt` for a sample of the type of content that works well.

## 🔧 Troubleshooting

- **No cultural references**: Check if documents folder exists and contains files
- **API errors**: Verify your OpenAI API key is set correctly
- **Audio issues**: Check microphone permissions and PyAudio installation
- **Empty responses**: Ensure documents contain substantial French text

## 📜 Copyright Reminder

Always use legally obtained content:
- ✅ Plot summaries, analyses, reviews
- ✅ Your own notes and observations  
- ✅ Educational materials
- ❌ Full transcripts or copyrighted texts 