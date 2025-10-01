# petit_prince_rag.py
import PyPDF2
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from typing import List, Tuple

class PetitPrinceRAG:
    def __init__(self, embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.chunks = []
        self.embeddings = None
        self.cache_file = "petit_prince_embeddings.pkl"
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 20:  # Only keep meaningful chunks
                chunks.append(chunk.strip())
        
        return chunks
    
    def create_embeddings(self, chunks: List[str]) -> np.ndarray:
        """Create embeddings for text chunks"""
        print("Creating embeddings... (this may take a moment)")
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        return embeddings
    
    def setup_knowledge_base(self, pdf_path: str, force_refresh: bool = False):
        """Setup the knowledge base from PDF"""
        if os.path.exists(self.cache_file) and not force_refresh:
            print("Loading cached embeddings...")
            with open(self.cache_file, 'rb') as f:
                data = pickle.load(f)
                self.chunks = data['chunks']
                self.embeddings = data['embeddings']
            print(f"Loaded {len(self.chunks)} chunks from cache.")
            return
        
        print("Extracting text from PDF...")
        text = self.extract_text_from_pdf(pdf_path)
        
        print("Chunking text...")
        self.chunks = self.chunk_text(text)
        
        print(f"Created {len(self.chunks)} chunks.")
        
        self.embeddings = self.create_embeddings(self.chunks)
        
        # Cache the results
        print("Caching embeddings...")
        with open(self.cache_file, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'embeddings': self.embeddings
            }, f)
        
        print("Knowledge base setup complete!")
    
    def search_relevant_passages(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Find most relevant passages for a query"""
        if self.embeddings is None:
            return []
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top-k most similar chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Only include reasonably similar passages
                results.append((self.chunks[idx], similarities[idx]))
        
        return results
    
    def get_context_for_query(self, query: str, max_context_length: int = 500) -> str:
        """Get relevant context from Le Petit Prince for a query"""
        relevant_passages = self.search_relevant_passages(query, top_k=2)
        
        if not relevant_passages:
            return ""
        
        context_parts = []
        current_length = 0
        
        for passage, score in relevant_passages:
            if current_length + len(passage) <= max_context_length:
                context_parts.append(passage)
                current_length += len(passage)
            else:
                # Truncate last passage if needed
                remaining_space = max_context_length - current_length
                if remaining_space > 50:
                    context_parts.append(passage[:remaining_space] + "...")
                break
        
        if context_parts:
            return "Référence du Petit Prince: " + " ".join(context_parts)
        
        return "" 