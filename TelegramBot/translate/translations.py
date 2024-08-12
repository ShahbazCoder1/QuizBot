'''
Title: Text transalation using gettext library
Code Written by: 𝗠𝗱 𝗦𝗵𝗮𝗵𝗯𝗮𝘇 𝗛𝗮𝘀𝗵𝗺𝗶 𝗔𝗻𝘀𝗮𝗿𝗶
programing languages: Python
Description: This code implements a translation manager for a Python application, specifically designed to handle translations based on chat IDs. 
It utilizes the gettext library to load translations from locale files and provides functions to set and retrieve translations for different languages.
Code Version: V1.0
Copyright ©: Open-source
'''

import gettext
import os

class Translations:
    def __init__(self):
        self.translations = {}
        self.chat_languages = {}
        
        localedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'locale'))
        for lang in ['en', 'es', 'hi']:
            try:
                self.translations[lang] = gettext.translation('messages', localedir, languages=[lang], fallback=True)
            except Exception as e:
                print(f"Error loading translation for {lang}: {e}")
                self.translations[lang] = gettext.NullTranslations()
    
    def set_language(self, chat_id, language):
        self.chat_languages[chat_id] = language
    
    def gettext(self, chat_id, message):
        language = self.chat_languages.get(chat_id, 'en')  # Default to English if not set
        return self.translations[language].gettext(message)


translations = Translations()

def _(chat_id:int, message):
    return translations.gettext(chat_id, message)