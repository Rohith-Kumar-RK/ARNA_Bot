from dotenv import load_dotenv
from Rag import FaissVectorStore ,load_all_documents
import os
import google.generativeai as genai

# Set up Gemini AI

genai.configure(api_key="API_TOKEN")

load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = "../Rag/faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "gemma2-9b-it"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            # from data_loader import load_all_documents
            docs = load_all_documents("../Rag/data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        
        self.llm = genai.GenerativeModel("models/gemma-3n-e2b-it")
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\nContext:\n{context}\n\nSummary:"""
        print(f"[INFO] Prompt for LLM:\n{prompt}")
        response = self.llm.generate_content(prompt)
        return response

def gemini_response(text):
    rag_search = RAGSearch()
    # query = "What is attention mechanism?"
    summary = rag_search.search_and_summarize(text, top_k=3)

    # model_id = 'tunedModels/farmerqa-m3phv20xubea'

    # model = genai.GenerativeModel(model_id)

    # response = model.generate_content(text)
    return summary.text if summary else "❌ No response from Gemini AI."