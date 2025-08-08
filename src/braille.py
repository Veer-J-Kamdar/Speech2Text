from typing import Optional, Dict

class BrailleConverter:
    BRAILLE_DICT = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
        'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
        'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
        's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
        'y': '⠽', 'z': '⠵', ' ': '⠀', '.': '⠲', ',': '⠂', '!': '⠖',
        '?': '⠦', "'": '⠄', '"': '⠐⠂', '-': '⠤', '@': '⠈⠁',
        '1': '⠂', '2': '⠆', '3': '⠒', '4': '⠲', '5': '⠢',
        '6': '⠖', '7': '⠶', '8': '⠦', '9': '⠔', '0': '⠴'
    }

    def __init__(self):
        self.language = "en"

    def convert(self, text: str) -> Dict[str, str]:
        # """Convert text to Braille."""
        if not text:
            return {"error": "No text provided"}

        braille_text = ""
        text = text.lower()
        
        for char in text:
            if char in self.BRAILLE_DICT:
                braille_text += self.BRAILLE_DICT[char]
            else:
                braille_text += char

        return {
            "original_text": text,
            "braille_text": braille_text,
            "language": self.language
        }

def text_to_braille(text: str) -> Dict[str, str]:
    # """Helper function to convert text to Braille."""
    converter = BrailleConverter()
    return converter.convert(text)