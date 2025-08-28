# import os
# import kagglehub
# import json
# from typing import Dict
# from pathlib import Path

# class SignLanguage:
#     def __init__(self):
#         self.dataset_path = self._get_dataset()
#         self.signs_path = Path(self.dataset_path) / "ISL_Dataset"
#         self.sign_dict = self._load_sign_dictionary()

#     def _get_dataset(self) -> str:
#         """Download and get path to the ISL dataset"""
#         path = kagglehub.dataset_download("prathumarikeri/indian-sign-language-isl")
#         return path

#     def _load_sign_dictionary(self) -> Dict[str, str]:
#         """Create mapping of characters to their sign image paths"""
#         sign_dict = {}
#         if self.signs_path.exists():
#             for item in self.signs_path.iterdir():
#                 if item.is_dir():
#                     # Each folder name represents a character/number
#                     char = item.name.lower()
#                     # Store the path to the first image for each character
#                     images = list(item.glob('*.jpg'))
#                     if images:
#                         sign_dict[char] = str(images[0])
#         return sign_dict

#     def text_to_sign(self, text: str) -> dict:
#         """Convert text to sign language image references"""
#         try:
#             text = text.lower()
#             words = text.split()
            
#             sign_refs = []
#             for word in words:
#                 word_signs = []
#                 for char in word:
#                     if char in self.sign_dict:
#                         word_signs.append({
#                             'character': char,
#                             'image_path': self.sign_dict[char]
#                         })
#                     else:
#                         word_signs.append({
#                             'character': char,
#                             'image_path': None,
#                             'error': 'No sign available'
#                         })
#                 sign_refs.append(word_signs)

#             return {
#                 "status": "success",
#                 "original_text": text,
#                 "sign_references": sign_refs
#             }
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": str(e)
#             }

# def text_to_sign(text: str) -> dict:
#     """Helper function to convert text to sign language"""
#     converter = SignLanguage()
#     return converter.text_to_sign(text)
import os

from typing import Dict
from pathlib import Path

class SignLanguage:
    def __init__(self):
        # Update path to local assets folder
        self.signs_path = Path("assets/Signs/Indian")
        self.sign_dict = self._load_sign_dictionary()

    def _load_sign_dictionary(self) -> Dict[str, str]:
        """Create mapping of characters to their sign image paths"""
        sign_dict = {}
        if self.signs_path.exists():
            for item in self.signs_path.iterdir():
                if item.is_file() and item.suffix.lower() in ['.jpg', '.png']:
                    # Get character from filename (assuming filename format is 'char.jpg')
                    char = item.stem.lower()
                    sign_dict[char] = str(item)
        return sign_dict

    def text_to_sign(self, text: str) -> dict:
        """Convert text to sign language image references"""
        try:
            text = text.lower()
            words = text.split()
            
            sign_refs = []
            for word in words:
                word_signs = []
                for char in word:
                    if char in self.sign_dict:
                        word_signs.append({
                            'character': char,
                            'image_path': self.sign_dict[char]
                        })
                    else:
                        word_signs.append({
                            'character': char,
                            'image_path': None,
                            'error': 'No sign available'
                        })
                sign_refs.append(word_signs)

            return {
                "status": "success",
                "original_text": text,
                "sign_references": sign_refs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

def text_to_sign(text: str) -> dict:
    """Helper function to convert text to sign language"""
    converter = SignLanguage()
    return converter.text_to_sign(text)