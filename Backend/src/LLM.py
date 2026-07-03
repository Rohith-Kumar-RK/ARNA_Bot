from dotenv import load_dotenv
from Backend.src.Rag import FaissVectorStore, load_all_documents
import os
import google.generativeai as genai
import time
from google.api_core.exceptions import InternalServerError
# Set up Gemini AI
# BASE_DIR = os.path.dirname(
#     os.path.abspath(__file__)
# )

class RAGSearch:
    def __init__(
        self,
        persist_dir: str = "Backend/src/Dataset/Rag/faiss_store",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "gemma2-9b-it",
    ):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        load_dotenv()
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        print("[faiss_path]",faiss_path)
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            # from data_loader import load_all_documents
            docs = load_all_documents("Backend/src/Dataset/Rag/data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        genai.configure(api_key=os.getenv("API_TOKEN"))
        self.llm = genai.GenerativeModel("models/gemini-2.5-flash")
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = list(
            set(r["metadata"].get("text", "").strip() for r in results if r["metadata"])
        )

        context = "\n".join(texts).strip()
        print("[context]:", context)
        if not context:
            return "I don't know it's not my cup of tea."

        prompt = f"""
        Context:
        {context}

        Question:
        {query}

        Answer briefly using only the context.
        If answer is unavailable, say:
       I don't know it's not my cup of tea."""

        response = None
        for attempt in range(3):
            try:
                response = self.llm.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 256,   # 50 was too low — it was truncating mid-word
                        "temperature": 0.1
                    }
                )
                break
            except InternalServerError as e:
                print(f"Gemini API Error: {e}")
                time.sleep(5)

        if response is None:
            return "LLM service unavailable"

        # ── THE FIX: extract plain text instead of returning the raw
        # GenerateContentResponse object, which FastAPI/pydantic cannot
        # JSON-serialize (that's what caused the 500 error).
        try:
            text = response.text.strip()
        except Exception as e:
            print(f"[WARN] Could not extract text from Gemini response: {e}")
            text = ""

        if not text:
            return "I don't know it's not my cup of tea."

        return text


def gemini_response(text):
    rag_search = RAGSearch()
    summary = rag_search.search_and_summarize(text, top_k=3)
    print(summary)
    return summary if summary else "❌ No response from Gemini AI."

# def gemini_response(text):
#     rag_search = RAGSearch()
#     # query = "What is attention mechanism?"
#     summary = rag_search.search_and_summarize(text, top_k=3)
#     print(summary)
#     # print("the text of the summar :",summary.text.strip())
#     print("result")
#     return summary if summary else "❌ No response from Gemini AI."
