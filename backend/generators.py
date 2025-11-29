import os
from langchain_openai import OpenAIEmbeddings           # ✅ Replaced Azure embeddings
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


class Generators:

    # ------------------------------------------------------------
    # 🧠 SUMMARIZATION (OpenAI-compatible)
    # ------------------------------------------------------------
    def summarize_code(self, llm, code_text):
        """
        Summarize large codebases using LangChain’s map-reduce summarization.
        Works with ChatOpenAI or Gemini models.
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=200,
            separators=["\nFile:", "\n\n", "\n", " ", ""]
        )

        chunks = text_splitter.split_text(code_text)
        documents = [Document(page_content=chunk) for chunk in chunks]

        print(f"Split code into {len(documents)} chunks for processing")

        chain = load_summarize_chain(llm, chain_type="map_reduce")
        return chain.invoke({"input_documents": documents})

    # ------------------------------------------------------------
    # 🧠 README GENERATION WITH VECTORSTORE (OpenAI version)
    # ------------------------------------------------------------
    def generate_readme_with_examples_vectorstore(self, llm, embeddings, summary: str) -> str:
        """
        Generate a README by retrieving the best example READMEs using vector search.
        """

        if not isinstance(summary, str):
            print(f"Warning: summary is {type(summary)}, converting to string.")
            summary = str(summary)

        # Load example markdown files
        example_docs = []
        for root, _, files in os.walk("examples"):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            example_docs.append(Document(
                                page_content=f.read(),
                                metadata={"source": path}
                            ))
                    except Exception as e:
                        print(f"Error loading {file}: {e}")

        if not example_docs:
            print("No example markdown found. Falling back to standard README.")
            return self.generate_readme(llm, summary)

        # Create embedding-based vectorstore
        vectorstore = FAISS.from_documents(example_docs, embeddings)

        # Condense extremely long summaries
        if len(summary) > 800:
            summary_for_search = self._condense_summary(llm, summary)
        else:
            summary_for_search = summary

        # Retrieve top examples
        relevant_examples = vectorstore.similarity_search(summary_for_search, k=2)

        processed_examples = []
        for doc in relevant_examples:
            content = doc.page_content

            # Shorten if needed
            if len(content) > 1000:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=800, chunk_overlap=100,
                    separators=["\n## ", "\n### ", "\n\n", "\n", ""]
                )
                content = splitter.split_text(content)[0]

            processed_examples.append(
                f"### Example from {doc.metadata['source']}\n\n{content}"
            )

        relevant_content = "\n\n".join(processed_examples)

        # FINAL README PROMPT
        prompt = f"""
You are a professional technical writer. Your task is to generate a polished README.md.

REFERENCE README STYLES:
{relevant_content}

CODEBASE SUMMARY:
{summary_for_search}

INSTRUCTIONS:
- Follow modern open source README standards
- Include only relevant technical details
- Use clean formatting and concise sections
- Avoid Azure-specific instructions unless needed
- Produce a complete README.md document

Now generate the README.md:
"""

        return llm.invoke(prompt)

    # ------------------------------------------------------------
    # 🧠 Standard README Generation (OpenAI)
    # ------------------------------------------------------------
    def generate_readme(self, llm, summary: str) -> str:

        if not isinstance(summary, str):
            summary = str(summary)

        # If summary is huge, condense it first
        if len(summary) > 2000:
            print("Summary is long → condensing...")
            summary = self._condense_summary(llm, summary)

        prompt = f"""
You are a senior technical writer creating a README.md for a software project.

USING THIS SUMMARY:
{summary}

Generate a clean, modern README.md including:

# Project Title
- Clear and descriptive

# Description
- What the project does
- Why it exists

# Features

# Architecture / How It Works (if applicable)

# Installation

# Usage

# Configuration
- Environment variables

# API (if applicable)

# Examples

# Development (optional)

# Deployment

# Security

# Troubleshooting

# License

Produce the README.md now:
"""
        try:
            return llm.invoke(prompt)

        except Exception as e:
            if "maximum context length" in str(e):
                print("Token limit hit → aggressive summarization applied.")
                ultra = self._ultra_condense(llm, summary)
                return llm.invoke(
                    f"Create a minimal README.md using this summary:\n\n{ultra}"
                )
            else:
                raise

    # ------------------------------------------------------------
    # INTERNAL HELPERS (condensing)
    # ------------------------------------------------------------
    def _condense_summary(self, llm, text):
        """Condense long summaries using map-reduce."""
        docs = [Document(page_content=text)]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )
        split_docs = splitter.split_documents(docs)

        map_prompt = PromptTemplate(
            template="Extract key points from:\n\n{text}\n\nKEY POINTS:",
            input_variables=["text"]
        )
        combine_prompt = PromptTemplate(
            template="Combine these key points into a concise technical summary:\n\n{text}\n\nSUMMARY:",
            input_variables=["text"]
        )

        chain = load_summarize_chain(
            llm, chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=combine_prompt
        )

        result = chain.invoke({"input_documents": split_docs})
        return result.get("output_text", str(result))

    def _ultra_condense(self, llm, text):
        """Extreme summarization when token limits fail."""
        chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                template="Summarize this text in under 400 words:\n\n{text}\n\nSUMMARY:",
                input_variables=["text"]
            )
        )
        out = chain.invoke({"text": text[:3000]})
        return out.get("text", str(out))
