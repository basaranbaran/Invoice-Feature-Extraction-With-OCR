# Invoice OCR Web Application

Bahçeşehir Üniversitesi Bilgisayar Mühendisliği Bölümü bitirme projesi olarak geliştirilmiştir. Bu proje, fatura ve fiş görsellerinden OCR ve yapay zeka teknolojileri kullanarak otomatik veri çıkarımı yapmayı amaçlamaktadır.

## Proje Hakkında

Günümüzde işletmeler ve bireyler, fatura ve fiş verilerini manuel olarak sisteme girme zorluğu yaşamaktadır. Bu proje, Tesseract OCR ile görsel işleme ve Ollama LLM ile akıllı veri çıkarımı yaparak bu süreci otomatikleştirmektedir.

Sistem, kullanıcıların yükledikleri fatura görsellerini (JPG, PNG) veya PDF dosyalarını analiz eder ve fatura numarası, tarih, toplam tutar, ürün listesi gibi önemli bilgileri yapılandırılmış JSON formatında sunar. Bu sayede manuel veri girişi hatası ortadan kalkar ve işlem süresi önemli ölçüde azalır.

## Özellikler

- Kullanıcı kayıt ve giriş sistemi (JWT tabanlı güvenlik)
- Çoklu format desteği (JPG, PNG, PDF)
- Tesseract OCR ile metin çıkarma
- Ollama LLaMA 3.1 ve gemma2:9b ile akıllı veri analizi
- Fatura bilgilerinin yapılandırılmış görüntülenmesi
- PostgreSQL ile veri saklama
- Modern ve responsive kullanıcı arayüzü

## Teknolojiler

**Frontend**
- React 19 + Vite
- React Router
- Bootstrap 5
- Axios

**Backend**
- Node.js + Express
- Prisma ORM
- PostgreSQL
- JWT Authentication
- Multer (dosya yükleme)

**Python Servisi**
- FastAPI
- Tesseract OCR
- OpenCV (görüntü ön işleme)
- LangChain + Ollama
- pdf2image

## Gereksinimler

Projeyi çalıştırmadan önce aşağıdaki yazılımların sisteminizde kurulu olması gerekmektedir:

### Gerekli Yazılımlar

1. **Node.js** (v18 veya üzeri)
   - [nodejs.org](https://nodejs.org/) adresinden indirin

2. **Python** (3.9 veya üzeri)
   - [python.org](https://www.python.org/) adresinden indirin

3. **PostgreSQL** (v12 veya üzeri)
   - [postgresql.org](https://www.postgresql.org/download/) adresinden indirin
   - Kurulum sonrası PostgreSQL servisinin çalıştığından emin olun

4. **Tesseract OCR**
   - **Windows:** 
     ```powershell
     winget install -e --id UB-Mannheim.TesseractOCR
     ```
   - **macOS:** 
     ```bash
     brew install tesseract
     ```
   - **Linux:** 
     ```bash
     sudo apt-get install tesseract-ocr
     ```

5. **Ollama** ve **LLaMA 3.1 Modeli**
   - [ollama.ai](https://ollama.ai/) adresinden Ollama'yı indirin ve kurun
   - Model kurulumu:
     ```bash
     ollama pull llama3.1
     ```

## Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/kullanici-adiniz/invoice-ocr-web.git
cd invoice-ocr-web
```

### 2. PostgreSQL Veritabanı Hazırlığı

PostgreSQL'in çalıştığından emin olun ve bir veritabanı oluşturun:

```sql
CREATE DATABASE invoice_db;
```

Veya pgAdmin arayüzünden `invoice_db` adında yeni bir veritabanı oluşturun.

### 3. Backend Kurulumu

```bash
cd backend
npm install

# .env dosyasını oluşturun
cp env.example .env

# .env dosyasını düzenleyin:
# DATABASE_URL="postgresql://KULLANICI_ADI:SIFRE@localhost:5432/invoice_db"
# JWT_SECRET="gizli_anahtar_buraya"
# PORT=3000

# Veritabanı tablolarını oluşturun
npx prisma migrate dev
npx prisma generate

# Sunucuyu başlatın
npm start
```

Backend `http://localhost:3000` adresinde çalışacaktır.

### 4. Python Servisi Kurulumu

```bash
cd ../python_service

# Virtual environment oluşturun
python -m venv venv

# Virtual environment'ı aktive edin
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Servisi başlatın
uvicorn app:app --reload --port 8000
```

Python servisi `http://localhost:8000` adresinde çalışacaktır.

### 5. Frontend Kurulumu

```bash
cd ../frontend
npm install

# .env dosyasını oluşturun (opsiyonel)
cp env.example .env
# Varsayılan API URL zaten localhost:3000 olarak ayarlıdır

# Geliştirme sunucusunu başlatın
npm run dev
```

Frontend `http://localhost:5173` adresinde çalışacaktır.

## Kullanım

1. Tarayıcınızda `http://localhost:5173` adresine gidin
2. "Kayıt Ol" butonuyla yeni bir hesap oluşturun
3. Giriş yapın
4. "Yeni Fatura Yükle" butonuna tıklayın
5. Bir fatura görseli seçin (test için `invoice_sample.png` dosyasını kullanabilirsiniz)
6. AI modelini seçin (LLaMA 3.1 önerilir - 12GB GPU için uygun)
7. "Yükle ve İşle" butonuna tıklayın
8. "Yüklenen Faturalar" sayfasından sonuçları görüntüleyin

## Proje Yapısı

```
├── backend/              # Node.js API sunucusu
│   ├── controllers/     # İş mantığı
│   ├── routes/          # API endpoint'leri
│   ├── prisma/          # Veritabanı şeması
│   └── env.example      # Ortam değişkenleri şablonu
├── frontend/            # React kullanıcı arayüzü
│   ├── src/
│   │   ├── components/  # Bileşenler
│   │   └── pages/       # Sayfa bileşenleri
│   └── env.example      # Ortam değişkenleri şablonu
├── python_service/      # OCR ve AI servisi
│   ├── app.py          # FastAPI uygulaması
│   ├── ocr.py          # OCR işleme mantığı
│   └── requirements.txt # Python bağımlılıkları
├── invoice_sample.png   # Test için örnek fatura
└── README.md           # Bu dosya
```

## Sorun Giderme

**Veritabanı bağlantı hatası alıyorsanız:**
- PostgreSQL servisinin çalıştığından emin olun
- `.env` dosyasındaki `DATABASE_URL` bilgilerini kontrol edin
- Veritabanı kullanıcı adı ve şifresinin doğru olduğundan emin olun

**Python servisi başlamıyorsa:**
- Tesseract OCR'ın doğru yüklendiğinden emin olun (`tesseract --version`)
- Virtual environment'ın aktif olduğundan emin olun
- Tüm Python bağımlılıklarının yüklendiğini kontrol edin

**Ollama modeli bulunamıyorsa:**
- `ollama list` komutuyla yüklü modelleri kontrol edin
- `ollama pull llama3.1` ile modeli indirin

## Katkıda Bulunanlar

Bu proje Bahçeşehir Üniversitesi Bilgisayar Mühendisliği öğrencileri tarafından geliştirilmiştir.

---

**Bahçeşehir Üniversitesi - Bilgisayar Mühendisliği Bölümü**  
Bitirme Projesi 2024-2025
