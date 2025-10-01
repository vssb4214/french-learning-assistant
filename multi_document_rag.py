#!/usr/bin/env python3
"""
Multi-Document RAG System for French Cultural Knowledge
Handles multiple documents including PDFs and text files for cultural context.
"""

import PyPDF2
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import json
from typing import List, Tuple, Dict
from pathlib import Path

class MultiDocumentRAG:
    def __init__(self, embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.documents = {}  # {doc_id: {title, chunks, embeddings}}
        self.cache_file = "multi_document_embeddings.pkl"
        self.metadata_file = "document_metadata.json"
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from text file"""
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    
    def chunk_text(self, text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def process_document(self, file_path: str, doc_id: str = None) -> Dict:
        """Process a single document and return document info"""
        if doc_id is None:
            doc_id = os.path.basename(file_path)
        
        print(f"Processing: {file_path}")
        
        # Extract text based on file type
        if file_path.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.txt'):
            text = self.extract_text_from_txt(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return None
        
        if not text.strip():
            print(f"No text extracted from: {file_path}")
            return None
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        # Generate embeddings
        embeddings = self.model.encode(chunks)
        
        # Store document info
        doc_info = {
            'title': os.path.basename(file_path),
            'path': file_path,
            'chunks': chunks,
            'embeddings': embeddings,
            'chunk_count': len(chunks)
        }
        
        self.documents[doc_id] = doc_info
        return doc_info
    
    def process_documents_folder(self, folder_path: str):
        """Process all documents in a folder"""
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return
        
        # Try to load existing cache
        if self.load_cache():
            print("Loaded existing embeddings from cache")
            return
        
        # Process all files in folder
        for file_path in Path(folder_path).rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt']:
                try:
                    self.process_document(str(file_path))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        # Save cache
        self.save_cache()
        self.save_metadata()
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant chunks across all documents"""
        if not self.documents:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        all_results = []
        
        # Search across all documents
        for doc_id, doc_info in self.documents.items():
            if 'embeddings' not in doc_info:
                continue
            
            # Calculate similarities
            similarities = cosine_similarity(query_embedding, doc_info['embeddings'])[0]
            
            # Get top results for this document
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            for idx in top_indices:
                if similarities[idx] > 0.3:  # Minimum similarity threshold
                    all_results.append({
                        'text': doc_info['chunks'][idx],
                        'source': doc_info['title'],
                        'similarity': float(similarities[idx]),
                        'doc_id': doc_id
                    })
        
        # Sort by similarity and return top results
        all_results.sort(key=lambda x: x['similarity'], reverse=True)
        return all_results[:top_k]
    
    def get_document_stats(self) -> List[Dict]:
        """Get statistics about loaded documents"""
        stats = []
        for doc_id, doc_info in self.documents.items():
            stats.append({
                'title': doc_info['title'],
                'chunks': doc_info['chunk_count'],
                'path': doc_info['path']
            })
        return stats
    
    def save_cache(self):
        """Save embeddings to cache file"""
        try:
            cache_data = {}
            for doc_id, doc_info in self.documents.items():
                cache_data[doc_id] = {
                    'title': doc_info['title'],
                    'path': doc_info['path'],
                    'chunks': doc_info['chunks'],
                    'embeddings': doc_info['embeddings'],
                    'chunk_count': doc_info['chunk_count']
                }
            
            with open(self.cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            print(f"Cache saved to {self.cache_file}")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def load_cache(self) -> bool:
        """Load embeddings from cache file"""
        try:
            if not os.path.exists(self.cache_file):
                return False
            
            with open(self.cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            self.documents = cache_data
            print(f"Cache loaded from {self.cache_file}")
            return True
        except Exception as e:
            print(f"Error loading cache: {e}")
            return False
    
    def save_metadata(self):
        """Save document metadata to JSON file"""
        try:
            metadata = []
            for doc_id, doc_info in self.documents.items():
                metadata.append({
                    'doc_id': doc_id,
                    'title': doc_info['title'],
                    'path': doc_info['path'],
                    'chunk_count': doc_info['chunk_count']
                })
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"Metadata saved to {self.metadata_file}")
        except Exception as e:
            print(f"Error saving metadata: {e}")

if __name__ == "__main__":
    # Test the RAG system
    rag = MultiDocumentRAG()
    
    # Process documents if folder exists
    if os.path.exists("Info for French"):
        rag.process_documents_folder("Info for French")
        
        # Test search
        test_query = "Le Petit Prince"
        results = rag.search(test_query, top_k=2)
        
        print(f"\nSearch results for '{test_query}':")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['text'][:100]}...")
            print(f"   Source: {result['source']}")
            print(f"   Similarity: {result['similarity']:.3f}")
            print()
    else:
        print("Documents folder not found. Run setup_documents.py first.")