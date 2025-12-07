# Evrak Takip

Basit bir FastAPI + React (CDN) uygulamasıyla PDF evraklarını indeksleyip arama yapabileceğiniz bir örnek.

## Bilgisayarınızda çalıştırma adımları

### Ön koşullar
- Python 3.10+ kurulu olmalı (Windows, macOS veya Linux).
- Tarayıcıda statik dosya servis edebileceğiniz basit bir HTTP sunucusu (Python ile gelen `http.server` yeterli).

### Kaynak kodu hazırlığı
1. Depoyu indirin veya proje klasörüne geçin.
2. PDF dosyalarınızı `backend/documents` klasörüne kopyalayın. Sunucu açıldığında bu klasördeki tüm PDF'ler otomatik indekslenir.
3. Yeniden indekslemek için `backend/app` içindeki `documents.db` dosyasını silip sunucuyu yeniden başlatmanız yeterli.

### Backend (API) çalıştırma
```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows PowerShell için: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Sunucu açıldıktan sonra `http://localhost:8000/docs` adresinden API dokümantasyonuna ulaşabilir ve sorgularınızı test edebilirsiniz.

### Frontend çalıştırma
`frontend/index.html` statik bir dosya olduğundan herhangi bir web sunucusuyla servis edilebilir. Python ile örnek:

```bash
cd frontend
python -m http.server 4173
```

Tarayıcınızı `http://localhost:4173` adresine açın. API `http://localhost:8000` portunda çalışıyorsa otomatik bağlanır. Farklı bir
port kullanıyorsanız tarayıcı konsolunda aşağıdakini çalıştırarak güncelleyebilirsiniz:

```js
window.API_BASE = 'http://localhost:PORT';
```

## Özellikler
- PDF içindeki `Konu:` satırını konu olarak okur.
- `Sayı : ...-<numara>` kalıbındaki son numarayı evrak numarası olarak işler.
- Tarih bilgisi varsa `YYYY.MM.DD` formatını dosya adına ekler.
- Arama kutusu boş bırakıldığında tüm evraklar listelenir, sayfa başına 100 kayıt gösterilir.
