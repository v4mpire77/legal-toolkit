"""
Module: AI Assistant
Description: Interface for Local LLM (Ollama) to perform privacy-first document analysis.
"""

import ollama
import fitz  # PyMuPDF
import tempfile
import os
from typing import Optional
from .tables import extract_tables

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

    def extract_tables_from_pdf(self, pdf_bytes) -> str:
        """
        Extracts tables from a PDF file stream and returns them as CSV-formatted strings.
        
        Returns:
            A string containing all extracted tables in CSV format, separated by newlines.
            Returns empty string if no tables are found.
        """
        # Save bytes to temporary file since pdfplumber requires a file path
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name
        
        try:
            tables = extract_tables(tmp_path)
            
            if not tables:
                return ""
            
            # Convert tables to CSV format
            table_text = "\n\n=== STRUCTURED TABLES ===\n\n"
            for i, df in enumerate(tables, 1):
                table_text += f"--- Table {i} ---\n"
                table_text += df.to_csv(index=False)
                table_text += "\n"
            
            return table_text
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

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
        
        # Extract tables and add to context
        table_text = self.extract_tables_from_pdf(pdf_bytes)
        
        # Combine text and tables
        full_text = text
        if table_text:
            full_text += "\n\n" + table_text
        
        # Truncate text if too long (basic handling for context window)
        # 1 token ~= 4 chars. 8k context ~= 32k chars.
        if len(full_text) > 30000:
            full_text = full_text[:30000] + "\n[...Truncated due to context limit...]"

        prompts = {
            "summary": (
                "You are a senior UK legal assistant. Summarize the following legal document. "
                "Identify the Parties, the Core Claim/Dispute, and the Relief Sought. "
                "If structured tables are present, incorporate key financial or procedural information from them. "
                "Keep it professional and concise.\n\n"
            ),
            "dates": (
                "You are a UK legal assistant. Extract all critical procedural dates from the text below. "
                "List them in a table format: Date | Event | Legal Significance. "
                "If no year is specified, infer from context if possible or mark as 'Unknown'.\n\n"
            )
        }

        system_prompt = prompts.get(prompt_type, prompts["summary"])
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Document Text:\n{full_text}"},
            ])
            return response['message']['content']
        except Exception as e:
            return f"AI Error: {str(e)}"

