# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os
# import time

# load_dotenv()

# class GitReadmeBrain:
#     """
#     Core LLM brain for GitReadme.
#     Uses OpenAI (non-Azure) + optional Google Gemini.
#     """

#     def __init__(self):
#         # OpenAI keys
#         self.openai_api_key = os.getenv("OPENAI_API_KEY")

#         # Models (configurable through .env)
#         self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
#         self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

#         # Gemini (optional)
#         self.gemini_api_key = os.getenv("GEMINI_API_KEY")

#         # Rate limiting buckets (for Gemini)
#         self._gemini_flash_calls = []
#         self._gemini_pro_calls = []

#     # ---------------------------
#     # 🧠 OpenAI Chat Model
#     # ---------------------------
#     def getLLM(self, max_tokens: int = 1000, temperature: float = 0.3):
#         """
#         Returns an OpenAI Chat model for README generation.
#         """
#         return ChatOpenAI(
#             api_key=self.openai_api_key,
#             model=self.openai_model,
#             max_tokens=max_tokens,
#             temperature=temperature
#         )

#     # ---------------------------
#     # 🧠 Google Gemini Model (Optional)
#     # ---------------------------
#     def get_gemini_llm(self, model_name="gemini-1.5-flash", max_tokens: int = 1000, temperature: float = 0.3):
#         """
#         Returns a LangChain LLM for Gemini.
#         """
#         return ChatGoogleGenerativeAI(
#             model=model_name,
#             google_api_key=self.gemini_api_key,
#             temperature=temperature,
#             max_output_tokens=max_tokens,
#             convert_system_message_to_human=True
#         )

#     # ---------------------------
#     # 🔠 OpenAI Embeddings
#     # ---------------------------
#     def getEmbeddingModel(self):
#         """
#         Returns OpenAI embeddings using the new text-embedding-3 models.
#         """
#         return OpenAIEmbeddings(
#             api_key=self.openai_api_key,
#             model=self.embedding_model
#         )
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os

load_dotenv()

class GitReadmeBrain:
    """
    🚀 Gemini-Powered Brain
    Replaces OpenAI completely.
    """

    def __init__(self):

        # === GEMINI KEYS ===
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_api_key:
            raise Exception("❌ GEMINI_API_KEY missing in .env")

        # === MODEL NAMES ===
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")  # free+fast
        self.embedding_model = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")

    # ───────────────────────────────────────────────────────────────
    #  Gemini LLM (main text generator)
    # ───────────────────────────────────────────────────────────────
    def getLLM(self, max_tokens=2000, temperature=0.4):
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.gemini_api_key,
            temperature=temperature,
            max_output_tokens=max_tokens
        )

    # ───────────────────────────────────────────────────────────────
    # Gemini Embedding Model (vector search)
    # ───────────────────────────────────────────────────────────────
    def getEmbeddingModel(self):
        return GoogleGenerativeAIEmbeddings(
            model=self.embedding_model,
            google_api_key=self.gemini_api_key
        )
