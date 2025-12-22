"""
Module: AI Assistant
Description: Interface for Local LLM (Ollama) to perform privacy-first document analysis.
"""

import ollama
import fitz  # PyMuPDF
from typing import Optional

class AIAssistant:
    def __init__(self, model_name: str = "llama3"):
        self.model = model_name

    def is_available(self) -> bool:
        """Checks if Ollama is running and accessible."""
        try:
            ollama.list()
            return True
        except Exception:
            return False

    def extract_text_from_pdf(self, pdf_bytes) -> str:
        """Extracts text from a PDF file stream."""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def summarize_document(self, pdf_bytes, prompt_type: str = "summary") -> str:
        """
        Sends document text to the local LLM for analysis.
        
        Args:
            pdf_bytes: The uploaded file stream.
            prompt_type: 'summary' or 'dates'.
        """
        if not self.is_available():
            return "Error: Ollama is not running. Please launch Ollama to use AI features."

        text = self.extract_text_from_pdf(pdf_bytes)
        
        # Truncate text if too long (basic handling for context window)
        # 1 token ~= 4 chars. 8k context ~= 32k chars.
        if len(text) > 30000:
            text = text[:30000] + "\n[...Truncated due to context limit...]"

        prompts = {
            "summary": (
                "You are a senior UK legal assistant. Summarize the following legal document. "
                "Identify the Parties, the Core Claim/Dispute, and the Relief Sought. "
                "STRICT GROUNDING: Use ONLY the provided text. If specific information (like the relief sought) "
                "is not explicitly stated in the text, write 'Not Specified'. Do not hallucinate or assume facts. "
                "Keep it professional and concise.\n\n"
            ),
            "dates": (
                "You are a UK legal assistant. Extract all critical procedural dates from the text below. "
                "STRICT GROUNDING: Use ONLY the provided text. If a date or its significance is not explicitly "
                "mentioned, do not invent it. List them in a table format: Date | Event | Legal Significance. "
                "If no year is specified, infer from context only if certain, otherwise mark as 'Unknown'.\n\n"
            )
        }

        system_prompt = prompts.get(prompt_type, prompts["summary"])
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Document Text:\n{text}"},
            ])
            return response['message']['content']
        except Exception as e:
            return f"AI Error: {str(e)}"

