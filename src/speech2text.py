import os
import json
import logging
import time
from functools import wraps
from typing import Tuple, Dict, Optional

from moviepy.editor import AudioFileClip
import speech_recognition as sr
from pydub import AudioSegment
from requests.exceptions import RequestException

try:
    from src.config import ENGINE, LANGUAGE, PATH_MP3, PATH_JSON
except ImportError:
    from config import ENGINE, LANGUAGE, PATH_MP3, PATH_JSON

MULTITASK = False
if MULTITASK:
    from concurrent.futures import ThreadPoolExecutor

class Speech2Text:
    def __init__(self, path_mp3: str = PATH_MP3, path_json: str = PATH_JSON):
        self.recognizer = sr.Recognizer()
        self.path_mp3 = path_mp3
        self.path_json = path_json
        self.engine = ENGINE
        self.language = LANGUAGE
        self.name = ""

        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            filename='speech2text.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )

    @staticmethod
    def ensure_directory(directory: str):
        os.makedirs(directory, exist_ok=True)
        logging.info(f"Created directory: {directory}")

    def convert_to_wav(self, input_file: str, output_file: str):
        try:
            ext_file = os.path.splitext(input_file)[1].lower()
            if ext_file == ".mp3":
                audio = AudioSegment.from_mp3(input_file)
                audio.export(output_file, format="wav")
            else:
                audio = AudioFileClip(input_file)
                audio.write_audiofile(output_file, codec='pcm_s16le')
                audio.close()
            logging.info(f"Converted file: [{input_file}] to WAV [{output_file}]")
        except Exception as e:
            logging.error(f"Error converting file {input_file}: {str(e)}")
            raise

    def retry_on_exception(max_retries: int = 3, delay: int = 1):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except (sr.RequestError, RequestException) as e:
                        if attempt == max_retries - 1:
                            raise
                        logging.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                        time.sleep(delay)
            return wrapper
        return decorator

    @retry_on_exception()
    def speech_to_text(self, file: str) -> Tuple[Dict, Optional[str]]:
        if self.engine != "speech_recognition":
            return {"Error": "Unsupported engine"}, None

        wav_file = f"{self.path_mp3}/{self.name}.wav"
        if not file.lower().endswith('.wav'):
            self.convert_to_wav(file, wav_file)
        else:
            wav_file = file

        with sr.AudioFile(wav_file) as source:
            if MULTITASK:
                self.recognizer.adjust_for_ambient_noise(source)
                self.recognizer.dynamic_energy_threshold = True
            audio = self.recognizer.record(source)
        
        try:
            transcript = self.recognizer.recognize_google(audio, language=self.language)
            return {"audio": file, "text": transcript}, wav_file
        except sr.UnknownValueError:
            logging.warning(f"Speech Recognition could not understand audio: {file}")
            return {"Error": "Audio not understood"}, wav_file
        except sr.RequestError as e:
            logging.error(f"Could not request results from Speech Recognition service; {e}")
            return {"Error": f"Request failed: {str(e)}"}, wav_file
        except Exception as e:
            logging.error(f"Unexpected error processing file {file}: {str(e)}")
            return {"Error": f"Unexpected error: {str(e)}"}, wav_file

    def save_json(self, data: Dict, file_name: str) -> str:
        full_path = f"{self.path_json}/{file_name}.json"
        try:
            with open(full_path, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return full_path
        except Exception as e:
            logging.error(f"Error saving JSON for {file_name}: {str(e)}")
            raise

    def start(self, file_name: str) -> Tuple[Dict, Optional[str], Optional[str]]:
        logging.info("=" * 80)
        logging.info("Single file processing")
        self.ensure_directory(self.path_json)
        self.ensure_directory(self.path_mp3)
        self.name = os.path.splitext(os.path.basename(file_name))[0]

        try:
            result, audio_file = self.speech_to_text(file_name)
            # json_file = self.save_json(result, self.name)
            logging.info(f"Successfully processed file: {file_name}")
            # return result, json_file, audio_file
            return result, None, audio_file
        except Exception as e:
            logging.error(f"Error processing file {file_name}: {str(e)}")
            return {"Error": f"Processing failed: {str(e)}"}, None, None

    if MULTITASK:
        def process_multiple(self, file_names: List[str]) -> List[Tuple[Dict, Optional[str], Optional[str]]]:
            logging.info("=" * 80)
            logging.info("Multiple file processing")
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(self.start, file_names))
            return results

# Uncomment for testing
# if __name__ == "__main__":
#     stt = Speech2Text()
#     # Single file processing
#     print(stt.start("../test/Thank_you.mp3"))

#     # Multiple file processing
#     # files = ["../temp/Thank_you.mp3", "../temp/Thank_you.wav", "../temp/video.mp4"]
#     # results = stt.process_multiple(files)
#     # for result in results:
#     #     print(result)