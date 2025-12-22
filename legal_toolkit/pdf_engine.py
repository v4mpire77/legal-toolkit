"""
Module: PDF Engine
Description: High-performance PDF manipulation using PyMuPDF (fitz).
             Handles merging, Bates stamping, and TOC generation.
"""

import os
import fitz  # PyMuPDF
from typing import List, Dict

class PDFEngine:
    def __init__(self):
        pass

    def merge_pdfs(self, input_files: List[str], output_path: str, bates_prefix: str = None):
        """
        Merges multiple PDFs into a single document and optionally applies Bates stamping.
        """
        result_doc = fitz.open()
        toc = []
        current_page = 0

        for file_path in input_files:
            if not os.path.exists(file_path) or not file_path.lower().endswith('.pdf'):
                continue
            
            src_doc = fitz.open(file_path)
            page_count = len(src_doc)
            
            # Add to TOC
            file_name = os.path.basename(file_path)
            toc.append([1, file_name, current_page + 1])
            
            # Insert pages
            result_doc.insert_pdf(src_doc)
            current_page += page_count
            src_doc.close()

        # Apply Bates Stamping if requested
        if bates_prefix:
            self._apply_bates_stamping(result_doc, bates_prefix)

        # Set TOC
        result_doc.set_toc(toc)
        result_doc.save(output_path)
        result_doc.close()
        return output_path

    def _apply_bates_stamping(self, doc: fitz.Document, prefix: str):
        """
        Applies sequential Bates numbering to the footer of every page.
        Format: [PREFIX]-[000001]
        """
        for i, page in enumerate(doc):
            # Page dimensions
            rect = page.rect
            # Calculate position: Bottom Right with margin
            # Rect(x0, y0, x1, y1)
            # We want to place it near (x1-100, y1-20)
            p = fitz.Point(rect.width - 120, rect.height - 20)
            
            bates_text = f"{prefix}-{i+1:06d}"
            
            page.insert_text(
                p,
                bates_text,
                fontsize=10,
                fontname="helv",  # Standard Helvetica
                color=(0, 0, 0)   # Black
            )

    def generate_smart_bundle(self, source_dir: str, output_name: str, bates_prefix: str = "BUNDLE"):
        """
        Automatically finds all PDFs in a directory and creates a stamped, indexed bundle.
        """
        files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.lower().endswith('.pdf')]
        files.sort()
        
        # Security: Prevent Path Traversal
        output_path = os.path.join(source_dir, output_name)
        if not os.path.abspath(output_path).startswith(os.path.abspath(source_dir)):
             raise ValueError("Security Violation: Output filename attempts to escape the directory.")
             
        return self.merge_pdfs(files, output_path, bates_prefix)
