from googletrans import Translator
import speech_recognition as sr
from datetime import datetime
import langdetect
import threading
import pyttsx3
import asyncio
import json
import time

class RealTimeTranslator:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()
        self.target_language = 'en'
        self.source_language = 'auto'
        self.is_listening = False
        self.continuous_mode = False
        self.languages = {
            'tr': 'Türkçe',
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Français',
            'es': 'Español',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ja': '日本語',
            'ko': '한국어',
            'zh': '中文',
            'ar': 'العربية'
        }
        print("🌍 Real-Time Voice Translator hazır!")
        print("\nKomutlar:")
        print("- 'çeviri başlat' -> Tek seferlik çeviri")
        print("- 'sürekli çeviri' -> Sürekli dinleme modu")
        print("- 'dur' -> Çeviriyi durdur")
        print("- 'dil değiştir' -> Hedef dili değiştir")
        print("- 'dil listesi' -> Desteklenen dilleri göster")
        print("- 'çıkış' -> Programı kapat")
        print(f"\n🎯 Şu anki hedef dil: {self.languages.get(self.target_language, self.target_language)}")

    def setup_tts(self):
        voices = self.tts_engine.getProperty('voices')
        turkish_voice = None
        for voice in voices:
            if 'tr' in voice.id.lower() or 'turkish' in voice.name.lower():
                turkish_voice = voice.id
                break
        if turkish_voice:
            self.tts_engine.setProperty('voice', turkish_voice)
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.9)

    def speak(self, text, language='tr'):
        print(f"🤖 Bot: {text}")
        voices = self.tts_engine.getProperty('voices')
        target_voice = None
        if language == 'en':
            for voice in voices:
                if 'en' in voice.id.lower() or 'english' in voice.name.lower():
                    target_voice = voice.id
                    break
        elif language == 'tr':
            for voice in voices:
                if 'tr' in voice.id.lower() or 'turkish' in voice.name.lower():
                    target_voice = voice.id
                    break
        if target_voice:
            self.tts_engine.setProperty('voice', target_voice)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen_for_speech(self, timeout=5):
        try:
            with self.microphone as source:
                print("🎤 Dinliyorum... (Konuşun)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                print("🔄 Ses işleniyor...")
                try:
                    text = self.recognizer.recognize_google(audio, language='tr-TR')
                    detected_lang = 'tr'
                except:
                    try:
                        text = self.recognizer.recognize_google(audio, language='en-US')
                        detected_lang = 'en'
                    except:
                        text = self.recognizer.recognize_google(audio)
                        try:
                            detected_lang = langdetect.detect(text)
                        except:
                            detected_lang = 'auto'
                print(f"👤 Algılanan metin ({detected_lang}): {text}")
                return text, detected_lang
        except sr.WaitTimeoutError:
            return "timeout", None
        except sr.UnknownValueError:
            return "anlaşılmadı", None
        except sr.RequestError as e:
            print(f"❌ STT hatası: {e}")
            return "hata", None

    def translate_text(self, text, source_lang='auto', target_lang='en'):
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.translator.translate(text, src=source_lang, dest=target_lang)
            )
            detected_lang = result.src
            translated_text = result.text
            print(f"🌍 Çeviri:")
            print(f"   Kaynak ({self.languages.get(detected_lang, detected_lang)}): {text}")
            print(f"   Hedef ({self.languages.get(target_lang, target_lang)}): {translated_text}")
            return translated_text, detected_lang
        except Exception as e:
            print(f"❌ Çeviri hatası: {e}")
            return None, None

    def single_translation(self):
        self.speak("Çevirmek istediğiniz metni söyleyin.")
        text, detected_lang = self.listen_for_speech(timeout=10)
        if text in ["timeout", "anlaşılmadı", "hata"]:
            self.speak("Ses alınamadı. Tekrar deneyin.")
            return
        translated_text, source_lang = self.translate_text(text, detected_lang, self.target_language)
        if translated_text:
            self.speak(translated_text, self.target_language)
        else:
            self.speak("Çeviri yapılamadı.")

    def continuous_translation(self):
        self.continuous_mode = True
        self.speak("Sürekli çeviri modu başladı. Konuşmaya başlayabilirsiniz. Durdurmak için 'dur' deyin.")
        while self.continuous_mode:
            try:
                text, detected_lang = self.listen_for_speech(timeout=3)
                if text == "timeout":
                    continue
                elif text in ["anlaşılmadı", "hata"]:
                    continue
                if any(word in text.lower() for word in ["dur", "stop", "bitir", "çık"]):
                    self.continuous_mode = False
                    self.speak("Sürekli çeviri modu durdu.")
                    break
                if len(text.strip()) < 3:
                    continue
                translated_text, source_lang = self.translate_text(text, detected_lang, self.target_language)
                if translated_text:
                    self.speak(translated_text, self.target_language)
                time.sleep(0.5)
            except KeyboardInterrupt:
                self.continuous_mode = False
                self.speak("Sürekli çeviri modu durdu.")
                break

    def change_target_language(self):
        self.speak("Hangi dile çevirmek istiyorsunuz? Dil kodunu söyleyin.")
        self.show_languages()
        response, _ = self.listen_for_speech(timeout=10)
        if response in ["timeout", "anlaşılmadı", "hata"]:
            self.speak("Dil değiştirilemedi.")
            return
        response = response.lower().strip()
        if response in self.languages:
            self.target_language = response
            lang_name = self.languages[response]
            self.speak(f"Hedef dil {lang_name} olarak değiştirildi.")
            return
        for code, name in self.languages.items():
            if response in name.lower():
                self.target_language = code
                self.speak(f"Hedef dil {name} olarak değiştirildi.")
                return
        if "ingilizce" in response or "english" in response:
            self.target_language = 'en'
            self.speak("Hedef dil İngilizce olarak değiştirildi.")
        elif "türkçe" in response or "turkish" in response:
            self.target_language = 'tr'
            self.speak("Hedef dil Türkçe olarak değiştirildi.")
        elif "almanca" in response or "german" in response:
            self.target_language = 'de'
            self.speak("Hedef dil Almanca olarak değiştirildi.")
        elif "fransızca" in response or "french" in response:
            self.target_language = 'fr'
            self.speak("Hedef dil Fransızca olarak değiştirildi.")
        elif "ispanyolca" in response or "spanish" in response:
            self.target_language = 'es'
            self.speak("Hedef dil İspanyolca olarak değiştirildi.")
        else:
            self.speak("Dil tanınmadı. Lütfen dil listesinden seçin.")

    def show_languages(self):
        print("\n🌍 Desteklenen Diller:")
        for code, name in self.languages.items():
            print(f"   {code} -> {name}")
        print()

    def listen_for_commands(self):
        while True:
            try:
                print("\n🎤 Komut bekliyorum...")
                command, _ = self.listen_for_speech(timeout=30)
                if command == "timeout":
                    continue
                elif command in ["anlaşılmadı", "hata"]:
                    continue
                command = command.lower()
                if "çeviri başlat" in command or "translate" in command:
                    self.single_translation()
                elif "sürekli çeviri" in command or "continuous" in command:
                    self.continuous_translation()
                elif "dur" in command or "stop" in command:
                    if self.continuous_mode:
                        self.continuous_mode = False
                        self.speak("Çeviri durduruldu.")
                    else:
                        self.speak("Şu anda aktif bir çeviri yok.")
                elif "dil değiştir" in command or "change language" in command:
                    self.change_target_language()
                elif "dil listesi" in command or "language list" in command:
                    self.speak("Desteklenen diller ekranda gösteriliyor.")
                    self.show_languages()
                elif "çıkış" in command or "kapat" in command or "exit" in command:
                    self.speak("Görüşmek üzere!")
                    break
                else:
                    self.speak("Anlamadım. Komutları tekrar söyleyeyim mi?")
                    print("\nGeçerli komutlar:")
                    print("- 'çeviri başlat'")
                    print("- 'sürekli çeviri'")
                    print("- 'dur'")
                    print("- 'dil değiştir'")
                    print("- 'dil listesi'")
                    print("- 'çıkış'")
            except KeyboardInterrupt:
                print("\n👋 Çıkılıyor...")
                break

def main():
    print("🌍 Real-Time Voice Translator başlatılıyor...")
    print("⚠️  Mikrofon izni ve internet bağlantısı gerekli!")
    try:
        translator = RealTimeTranslator()
        print("\n🧪 Mikrofon testi... 'Test' deyin:")
        test_audio, _ = translator.listen_for_speech(timeout=5)
        if test_audio in ["timeout", "anlaşılmadı", "hata"]:
            print("❌ Mikrofon sorunu! Lütfen mikrofon ayarlarını kontrol edin.")
            return
        else:
            translator.speak("Mikrofon çalışıyor! Komutlarınızı bekliyorum.")
        print("\n🎤 Translator komutları dinliyor...")
        translator.listen_for_commands()
    except Exception as e:
        print(f"❌ Program hatası: {e}")
        print("\nGerekli kütüphaneler yüklü mü?")
        print("pip install speechrecognition pyttsx3 pyaudio googletrans==4.0.0-rc1 langdetect")

if __name__ == "__main__":
    main()
