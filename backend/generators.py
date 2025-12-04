import os
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


class Generators:

    # ------------------------------------------------------------
    # 🧠 CODE SUMMARIZATION (Gemini-safe output)
    # ------------------------------------------------------------
    def summarize_code(self, llm, code_text):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=200,
            separators=["\nFile:", "\n\n", "\n", " ", ""]
        )

        chunks = text_splitter.split_text(code_text)
        documents = [Document(page_content=chunk) for chunk in chunks]

        print(f"Split code into {len(documents)} chunks for processing")

        chain = load_summarize_chain(llm, chain_type="map_reduce")
        result = chain.invoke({"input_documents": documents})

        return self._to_text(result)

    # ------------------------------------------------------------
    # 🧠 README GENERATION WITH VECTORSTORE (Gemini ready)
    # ------------------------------------------------------------
    def generate_readme_with_examples_vectorstore(self, llm, embeddings, summary: str) -> str:

        if not isinstance(summary, str):
            print(f"Warning: summary was {type(summary)} — converting.")
            summary = str(summary)

        example_docs = []
        for root, _, files in os.walk("examples"):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            example_docs.append(
                                Document(page_content=f.read(), metadata={"source": path})
                            )
                    except Exception as e:
                        print(f"Error reading {file}: {e}")

        if not example_docs:
            print("No example README files found → using standard generation")
            return self.generate_readme(llm, summary)

        vectorstore = FAISS.from_documents(example_docs, embeddings)

        summary_for_search = summary if len(summary) < 800 else self._condense_summary(llm, summary)
        relevant_examples = vectorstore.similarity_search(summary_for_search, k=2)

        processed = []
        for doc in relevant_examples:
            text = doc.page_content[:1000]
            processed.append(f"### Example Source → {doc.metadata['source']}\n\n{text}")

        relevant_text = "\n\n".join(processed)

        prompt = f"""
You are a highly-skilled technical writer.
Generate a clean README.md inspired by these examples:

{relevant_text}

Using summary:
{summary_for_search}

Write full markdown output now.
"""

        result = llm.invoke(prompt)
        return self._to_text(result)

    # ------------------------------------------------------------
    # 🧠 STANDARD README GENERATION
    # ------------------------------------------------------------
    def generate_readme(self, llm, summary: str) -> str:

        if not isinstance(summary, str):
            summary = str(summary)

        if len(summary) > 2000:
            print("Summary large → condensing")
            summary = self._condense_summary(llm, summary)

        prompt = f"""
You are a professional documentation writer.

SUMMARY:
{summary}

Produce a complete README.md including:
- Title
- Description
- Features
- Setup/installation
- Usage
- API details (if any)
- Configuration
- Examples
- Development & Contribution
- License
"""

        try:
            result = llm.invoke(prompt)
            return self._to_text(result)

        except Exception as e:
            if "context" in str(e).lower():
                ultra = self._ultra_condense(llm, summary)
                result = llm.invoke(f"Generate minimal README.md using:\n\n{ultra}")
                return self._to_text(result)
            raise

    # ------------------------------------------------------------
    # 🔥 INTERNAL HELPERS — Converts AIMessage → String
    # ------------------------------------------------------------
    def _to_text(self, response):
        """Normalize Gemini output to string always."""
        if hasattr(response, "content"):      # AIMessage
            return response.content.strip()
        if isinstance(response, dict):
            return response.get("output_text", str(response)).strip()
        return str(response).strip()

    def _condense_summary(self, llm, text):
        docs = [Document(page_content=text)]

        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)

        map_prompt = PromptTemplate(
            template="Extract key points:\n\n{text}\n\nPOINTS:",
            input_variables=["text"]
        )
        combine_prompt = PromptTemplate(
            template="Combine points into a short technical summary:\n\n{text}\n\nSUMMARY:",
            input_variables=["text"]
        )

        chain = load_summarize_chain(llm, chain_type="map_reduce",
                                     map_prompt=map_prompt,
                                     combine_prompt=combine_prompt)

        res = chain.invoke({"input_documents": split_docs})
        return self._to_text(res)

    def _ultra_condense(self, llm, text):
        chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                template="Summarize under 400 words:\n\n{text}",
                input_variables=["text"]
            )
        )
        res = chain.invoke({"text": text[:3000]})
        return self._to_text(res)
