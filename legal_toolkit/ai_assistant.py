"""
Module: AI Assistant
Description: Hybrid interface for Local LLM (Ollama) and Cloud LLM (Google Gemini).
"""

import fitz  # PyMuPDF
import tempfile
import os
import streamlit as st
from typing import Optional
from .tables import extract_tables

class AIAssistant:
    def __init__(self, model_name: str = "llama3", provider: str = "ollama"):
        """
        Initializes the AI Assistant.
        
        Args:
            model_name: The model ID (e.g., 'llama3' for Ollama or 'gemini-1.5-flash' for Google).
            provider: 'ollama' or 'gemini'.
        """
        self.model_name = model_name
        self.provider = provider
        self.gemini_api_key = os.environ.get("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

    def is_available(self) -> bool:
        """Checks if the selected provider is available."""
        if self.provider == "gemini":
            return self.gemini_api_key is not None
        
        # Default to Ollama check
        try:
            import ollama
            ollama.list()
            return True
        except (ImportError, Exception):
            return False

    def extract_text_from_pdf(self, pdf_bytes) -> str:
        """Extracts text from a PDF file stream."""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def extract_tables_from_pdf(self, pdf_bytes) -> str:
        """Extracts tables from a PDF file stream and returns them as CSV strings."""
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb') as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_path = tmp_file.name
            
            tables = extract_tables(tmp_path)
            if not tables:
                return ""
            
            table_text = "\n\n=== STRUCTURED TABLES ===\n\n"
            for i, df in enumerate(tables, 1):
                table_text += f"--- Table {i} ---\n"
                table_text += df.to_csv(index=False)
                table_text += "\n"
            return table_text
        except Exception:
            return ""
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    def summarize_document(self, pdf_bytes, prompt_type: str = "summary") -> str:
        """Sends document text to the selected LLM (Ollama or Gemini)."""
        if not self.is_available():
            if self.provider == "gemini":
                return "Error: Gemini API Key not found. Please set GOOGLE_API_KEY in secrets or environment variables."
            return "Error: Ollama is not running. Please launch Ollama to use local AI features."

        text = self.extract_text_from_pdf(pdf_bytes)
        table_text = self.extract_tables_from_pdf(pdf_bytes)
        
        full_text = text
        if table_text:
            full_text += "\n\n" + table_text
        
        # Context limits: Gemini Flash handles 1M+ tokens, so we only truncate for Ollama
        if self.provider == "ollama" and len(full_text) > 30000:
            full_text = full_text[:30000] + "\n[...Truncated...]"

        prompts = {
            "summary": (
                "You are a senior UK legal assistant. Summarize the following legal document. "
                "Identify the Parties, the Core Claim/Dispute, and the Relief Sought. "
                "STRICT GROUNDING: Use ONLY the provided text. If specific information is not stated, write 'Not Specified'. "
                "Keep it professional and concise.\n\n"
            ),
            "dates": (
                "You are a UK legal assistant. Extract all critical procedural dates from the text below. "
                "STRICT GROUNDING: Use ONLY the provided text. List them in a table format: Date | Event | Significance.\n\n"
            )
        }
        system_prompt = prompts.get(prompt_type, prompts["summary"])

        if self.provider == "gemini":
            return self._query_gemini(system_prompt, full_text)
        else:
            return self._query_ollama(system_prompt, full_text)

    def _query_ollama(self, system_prompt, user_content):
        import ollama
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Document Text:\n{user_content}"},
            ])
            return response['message']['content']
        except Exception as e:
            return f"Ollama Error: {str(e)}"

    def _query_gemini(self, system_prompt, user_content):
        import google.generativeai as genai
        try:
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
            response = model.generate_content(f"Document Text:\n{user_content}")
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"