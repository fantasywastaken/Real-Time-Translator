# Real-Time Voice Translator

<img src="https://i.imgur.com/FEinl3p.png" width="1000px">

Gerçek zamanlı ses tanıma ve Google Translate API kullanarak çok dilli sesli çeviri yapabilen, sürekli dinleme modlu Python uygulaması.

---

### ⚙️ Nasıl Çalışır

- `speech_recognition` kütüphanesi ile mikrofondan ses alır ve Google Speech-to-Text API'sini kullanarak metne çevirir.
- `googletrans` kütüphanesi ile Google Translate API'sine bağlanarak çeviri yapar.
- `pyttsx3` text-to-speech motoru ile çevrilen metni seslendirir.
- `langdetect` ile kaynak dilin otomatik tespitini yapar.
- 12 farklı dili destekler (Türkçe, İngilizce, Almanca, Fransızca, vb.).
- Tek seferlik ve sürekli çeviri olmak üzere iki mod sunar.
- Sesli komutlarla kontrol edilebilir ve hedef dil değiştirilebilir.

---

## 📁 Kurulum

### 1. Gereksinimler

Gerekli kütüphaneleri pip ile yükleyin:
```python
pip install speechrecognition pyttsx3 pyaudio googletrans==4.0.0-rc1 langdetect
```

### 2. Sistem Gereksinimleri

- **Mikrofon**: Ses girişi için çalışan mikrofon
- **İnternet Bağlantısı**: Google API'leri için aktif internet
- **Ses Çıkışı**: Text-to-speech için hoparlör/kulaklık

---

### 🚀 Kullanım

Python scriptini çalıştırın:
```bash
python translator.py
```

#### 📢 Sesli Komutlar

- **"çeviri başlat"** → Tek seferlik çeviri yapır
- **"sürekli çeviri"** → Sürekli dinleme modunu başlatır
- **"dur"** → Aktif çeviriyi durdurur
- **"dil değiştir"** → Hedef dili değiştirir
- **"dil listesi"** → Desteklenen dilleri gösterir
- **"çıkış"** → Programı kapatır

---

### 🌍 Desteklenen Diller

- 🇹🇷 Türkçe (tr)
- 🇺🇸 İngilizce (en)
- 🇩🇪 Almanca (de)
- 🇫🇷 Fransızca (fr)
- 🇪🇸 İspanyolca (es)
- 🇮🇹 İtalyanca (it)
- 🇵🇹 Portekizce (pt)
- 🇷🇺 Rusça (ru)
- 🇯🇵 Japonca (ja)
- 🇰🇷 Korece (ko)
- 🇨🇳 Çince (zh)
- 🇸🇦 Arapça (ar)

---

### 🛡️ Notlar

- Program başlangıçta mikrofon testi yapar ve çalışabilirliği kontrol eder.
- Türkçe ve İngilizce TTS sesleri otomatik olarak seçilir.
- Ambient gürültü seviyesine göre mikrofon hassasiyeti ayarlanır.
- Çeviri sonuçları hem ekranda gösterilir hem de seslendirilir.

---

### ⚠️ Uyarı

Bu proje eğitim ve araştırma amaçları için geliştirilmiştir. Google API kullanım şartlarına uygun olarak kullanılmalıdır. Geliştirici, aracın kötüye kullanılmasından sorumlu değildir.
