import os
import PyPDF2
import requests
import json
from typing import List, Dict, Generator, Tuple

class RAGBackend:
    def __init__(self, document_set="employee"):
        self.document_set = document_set
        self.documents = self._load_documents()
        self.conversation_history = []
    
    def switch_document_set(self, document_set: str):
        """Switch to a different document set and reload documents."""
        if document_set != self.document_set:
            self.document_set = document_set
            self.documents = self._load_documents()
            self.conversation_history = []  # Clear history when switching
    
    def _load_documents(self) -> List[Dict]:
        docs = []
        if self.document_set == "employee":
            docs_dir = "documents"
        elif self.document_set == "police":
            docs_dir = "police_documents"
        elif self.document_set == "insurance":
            docs_dir = "insurance_documents"
        elif self.document_set == "nutanix":
            docs_dir = "nutanix_documents"
        else:
            docs_dir = "law_documents"
        
        if not os.path.exists(docs_dir):
            return docs
            
        for filename in os.listdir(docs_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(docs_dir, filename)
                try:
                    with open(filepath, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        
                        docs.append({
                            'filename': filename,
                            'content': text.strip(),
                            'title': filename.replace('.pdf', '').replace('_', ' ').title()
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        return docs
    
    def _search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc['content'].lower()
            title_lower = doc['title'].lower()
            
            # Simple scoring based on keyword matches
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if len(word) > 2:  # Skip very short words
                    score += content_lower.count(word) * 1
                    score += title_lower.count(word) * 3  # Title matches weighted higher
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:top_k]]
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count using word count approximation."""
        return int(len(text.split()) * 1.3)
    
    def generate_response_stream(self, query: str, endpoint_url: str, model_name: str, api_key: str) -> Tuple[Generator[str, None, None], int, int]:
        """Generate streaming response with accurate token tracking."""
        # Search relevant documents
        relevant_docs = self._search_documents(query)
        
        # Build context from documents
        context = ""
        if relevant_docs:
            context = "Relevant documents:\n\n"
            for doc in relevant_docs:
                context += f"Document: {doc['title']}\n{doc['content'][:1000]}...\n\n"
        
        # Build conversation context from history
        conversation_context = ""
        if self.conversation_history:
            conversation_context = "Previous conversation:\n"
            for msg in self.conversation_history[-6:]:  # Last 6 messages for better context
                conversation_context += f"{msg['role']}: {msg['content']}\n"
            conversation_context += "\n"
        
        # Create system prompt with RAG instructions
        if self.document_set == "nutanix":
            system_prompt = """You are a Nutanix technical documentation assistant. Use the provided Nutanix documentation and conversation history to answer questions about Nutanix products, configurations, and best practices. Provide detailed technical guidance based on the documentation. If the information isn't in the documents, say so clearly."""
        elif self.document_set == "police":
            system_prompt = """You are a police procedures assistant. Use the provided police documentation and conversation history to answer questions about law enforcement procedures and protocols. If the information isn't in the documents, say so clearly."""
        elif self.document_set == "insurance":
            system_prompt = """You are an insurance agency assistant. Use the provided insurance documentation and conversation history to answer questions about insurance policies and procedures. If the information isn't in the documents, say so clearly."""
        elif self.document_set == "law":
            system_prompt = """You are a North Carolina driving law assistant. Use the provided legal documentation and conversation history to answer questions about NC traffic laws and regulations. If the information isn't in the documents, say so clearly."""
        else:
            system_prompt = """You are a helpful employee knowledge assistant. Use the provided documents and conversation history to answer questions about company processes and policies. Maintain context from previous messages in the conversation. If the information isn't in the documents, say so clearly."""
        
        user_prompt = f"{conversation_context}{context}Current question: {query}"
        
        # API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Make non-streaming call first to get complete response and accurate tokens
        data = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.35,
            "max_tokens": 5000,
            "stream": False
        }
        
        try:
            response = requests.post(endpoint_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Extract response and token counts
            full_response = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            input_tokens = usage.get('prompt_tokens', 0)
            output_tokens = usage.get('completion_tokens', 0)
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            # Keep only last 12 messages (6 exchanges)
            if len(self.conversation_history) > 12:
                self.conversation_history = self.conversation_history[-12:]
            
            # Create streaming generator that yields character by character
            def stream_generator():
                for char in full_response:
                    yield char
            
            return stream_generator(), input_tokens, output_tokens
            
        except requests.exceptions.RequestException as req_error:
            def error_generator():
                yield f"API request failed: {str(req_error)}"
            return error_generator(), 0, 0
        except Exception as gen_error:
            def error_generator():
                yield f"Error generating response: {str(gen_error)}"
            return error_generator(), 0, 0
    
    def generate_response(self, query: str, endpoint_url: str, model_name: str, api_key: str) -> str:
        """Non-streaming response for backward compatibility."""
        stream_gen, input_tokens, output_tokens = self.generate_response_stream(query, endpoint_url, model_name, api_key)
        return ''.join(list(stream_gen))