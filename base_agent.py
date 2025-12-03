from abc import ABC, abstractmethod
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from typing import Dict, List, Any
import os

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_name: str, model_name: str = "llama3.2"):
        self.agent_name = agent_name
        self.model_name = model_name
        
        # Initialize LLM
        try:
            self.llm = Ollama(model=model_name, temperature=0.3)
            print(f"✓ {agent_name}: LLM initialized with {model_name}")
        except Exception as e:
            print(f"✗ {agent_name}: Failed to initialize LLM - {e}")
            print("  Make sure Ollama is running: ollama serve")
            raise
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Setup vector store directory
        self.persist_directory = f"./chroma_db/{agent_name.lower().replace(' ', '_')}"
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize vector store
        self.vectorstore = None
        self._init_vectorstore()
    
    def _init_vectorstore(self):
        """Initialize or load existing vector store"""
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print(f"✓ {self.agent_name}: Vector store initialized")
        except Exception as e:
            print(f"✗ {self.agent_name}: Failed to initialize vector store - {e}")
            raise
    
    def add_documents(self, texts: List[str], metadatas: List[Dict] = None):
        """Add documents to vector store"""
        if not texts:
            print(f"⚠ {self.agent_name}: No documents to add")
            return
        
        try:
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            print(f"✓ {self.agent_name}: Added {len(texts)} documents")
        except Exception as e:
            print(f"✗ {self.agent_name}: Failed to add documents - {e}")
    
    def retrieve_context(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant documents"""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        except Exception as e:
            print(f"✗ {self.agent_name}: Failed to retrieve context - {e}")
            return []
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using LLM"""
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            print(f"✗ {self.agent_name}: Failed to generate response - {e}")
            return f"Error: {str(e)}"
    
    @abstractmethod
    def analyze(self, query: str, **kwargs) -> Dict[str, Any]:
        """Main analysis method - must be implemented by subclasses"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "agent_name": self.agent_name,
                "documents_count": count,
                "model": self.model_name
            }
        except:
            return {
                "agent_name": self.agent_name,
                "documents_count": 0,
                "model": self.model_name
            }