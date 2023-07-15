from core import TextToSpeechModule, Request, cfg, log, DEBUG_LEVEL_OFF, DEBUG_LEVEL_MIN, DEBUG_LEVEL_MID, DEBUG_LEVEL_MAX
from distutils.command import clean
import pyttsx3
import re

voice = cfg('voice')

class TextToSpeech_System(TextToSpeechModule):
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        installed_voices = self.engine.getProperty('voices')
        log(DEBUG_LEVEL_MAX, f'  [pyttsx] available voices:')
        for installed_voice in installed_voices:
            log(DEBUG_LEVEL_MAX, f'    [pyttsx] {installed_voice}')
        if not voice is None:
            for installed_voice in installed_voices:
                if voice in installed_voice.name:
                    log(DEBUG_LEVEL_MAX, f'  [pyttsx] voice set to {installed_voice.name}')
                    self.engine.setProperty('voice', installed_voice.id)

    def remove_links(self, text):
        """
        Removes all links from a text, we don't want them to be spoken out
        """

        # matches most common URL formats
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

        # replace any matched patterns with an empty string
        no_links = re.sub(pattern, '', text)
        return no_links    

    def perform_text_to_speech(self, 
            request: Request) -> None: 
        
        spoken_text = self.remove_links(request.output)

        log(DEBUG_LEVEL_MAX, f'  [pyttsx] synthesizing speech for text [{spoken_text}]')
        self.engine.say(spoken_text)
        self.engine.runAndWait()