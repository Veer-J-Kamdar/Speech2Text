import os
from typing import Dict
from src.braille import text_to_braille
import PyPDF2

class FileHandler:
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt']

    def read_pdf(self, file_content: bytes) -> str:
        text = ""
        try:
            reader = PyPDF2.PdfReader(file_content)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def read_txt(self, file_content: bytes) -> str:
        try:
            return file_content.decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")

    def process_file(self, file_content: bytes, filename: str) -> Dict:
        """
        Process file content and convert to braille
        Returns: dictionary containing original and braille text
        """
        ext = filename.rsplit('.', 1)[-1].lower()
        if f'.{ext}' not in self.supported_formats:
            raise ValueError(f"Unsupported file type. Supported formats: {', '.join(self.supported_formats)}")

        try:
            if ext == 'pdf':
                content = self.read_pdf(file_content)
            else:  # txt
                content = self.read_txt(file_content)
            
            braille_text = text_to_braille(content)
            
            return {
                "file_type": ext,
                "original_text": content,
                "braille_text": braille_text
            }
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")