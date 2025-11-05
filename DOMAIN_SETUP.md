# Domain Setup Guide: aitraderglobal.com

## ✅ Tamamlanan İşlemler

### 1. Google Search Console Verification
- ✅ Verification meta tag eklendi: `google-site-verification=BOpjD70xkPUH-fq0DEWNTJulA-GCQcCXsAd1ZskxPvg`
- ✅ index.html dosyasına eklendi

### 2. SEO Optimizasyonu
- ✅ Open Graph meta tags güncellendi (domain ile)
- ✅ Twitter Card meta tags eklendi
- ✅ Canonical URL eklendi
- ✅ robots.txt dosyası oluşturuldu

---

## 📋 Yapılması Gereken İşlemler

### 1. Domain'i Lovable'a Bağlama

**Adım 1: Lovable Settings**
1. Lovable projenize gidin
2. Üst menüden **Settings** → **Domains**'e tıklayın
3. **Connect Domain** butonuna basın
4. Domain adını girin: `aitraderglobal.com`

**Adım 2: DNS Kayıtları (Domain Sağlayıcınızda)**

Domain sağlayıcınızın (GoDaddy, Namecheap, vb.) DNS yönetim paneline gidin ve şu kayıtları ekleyin:

#### A Records (Root Domain için)
```
Type: A
Name: @ (veya boş bırakın)
Value: 185.158.133.1
TTL: 3600 (veya otomatik)
```

#### A Record (WWW için)
```
Type: A
Name: www
Value: 185.158.133.1
TTL: 3600 (veya otomatik)
```

#### TXT Record (Lovable Verification)
Lovable size bir TXT kaydı verecek, şu formatta olacak:
```
Type: TXT
Name: _lovable
Value: lovable_verify=XXXXX (Lovable'dan alacağınız değer)
TTL: 3600 (veya otomatik)
```

**Adım 3: Bekleme**
- DNS propagation 10 dakika ile 72 saat arasında sürebilir
- Lovable otomatik olarak SSL sertifikası oluşturacak
- Domain durumu "Active" olana kadar bekleyin

### 2. Backend URL Güncelleme

Backend'inizi deploy ettikten sonra, frontend'in backend URL'sini güncellemeniz gerekiyor:

**Render.com'da (Frontend):**
1. Frontend service'inize gidin
2. Environment → Environment Variables
3. `VITE_API_URL` değişkenini güncelleyin:
   ```
   VITE_API_URL=https://ema-navigator-backend.onrender.com
   ```
   (veya kendi backend URL'iniz)

### 3. Backend CORS Güncelleme

Backend'de CORS ayarlarını yeni domain için güncellemeniz gerekiyor:

**backend/main.py dosyasında:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://aitraderglobal.com",
        "https://www.aitraderglobal.com",
        "https://aitraderglobal.lovable.app"  # staging için
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. LemonSqueezy Webhook URL Güncelleme

LemonSqueezy'de webhook URL'sini güncelleyin:
```
https://aitraderglobal.com/api/payments/lemonsqueezy/webhook
```

veya backend'iniz ayrıysa:
```
https://your-backend-url.onrender.com/api/payments/lemonsqueezy/webhook
```

### 5. Firebase Authorized Domains

Firebase Console'da:
1. Authentication → Settings → Authorized Domains
2. Şu domainleri ekleyin:
   - `aitraderglobal.com`
   - `www.aitraderglobal.com`

---

## 🧪 Test Etme

Domain bağlandıktan sonra test edin:

### 1. DNS Kontrolü
```bash
# A record kontrolü
nslookup aitraderglobal.com

# TXT record kontrolü
nslookup -type=TXT _lovable.aitraderglobal.com
```

veya online araçlar:
- https://dnschecker.org
- https://mxtoolbox.com/SuperTool.aspx

### 2. SSL Kontrolü
```
https://www.ssllabs.com/ssltest/analyze.html?d=aitraderglobal.com
```

### 3. Site Erişimi
- https://aitraderglobal.com
- https://www.aitraderglobal.com
- Her iki URL de çalışmalı ve SSL sertifikası geçerli olmalı

### 4. Google Search Console
1. https://search.google.com/search-console
2. Property ekle: `aitraderglobal.com`
3. Verification otomatik olarak geçmeli (meta tag zaten eklendi)
4. Sitemap gönderin: `https://aitraderglobal.com/sitemap.xml` (oluşturduğunuzda)

---

## 🔧 Sorun Giderme

### DNS Propagation Yavaş
- 72 saate kadar sürebilir
- https://dnschecker.org ile durumu kontrol edin
- Telefonunuzun mobil internetinden deneyin (farklı DNS)

### SSL Sertifikası Oluşturulmuyor
- DNS kayıtlarının doğru olduğundan emin olun
- CAA record'larınız varsa, Let's Encrypt'e izin verdiğinden emin olun
- Lovable support ile iletişime geçin

### "Domain Already Connected" Hatası
- Domain başka bir Lovable projesinde kullanılıyor olabilir
- O projeden kaldırıp yeniden bağlayın
- Veya ownership verification ile override edin

---

## 📊 Sonraki Adımlar

1. ✅ Domain bağlandıktan sonra Google Search Console'da verify edin
2. ✅ Google Analytics ekleyin (isteğe bağlı)
3. ✅ Sitemap oluşturun ve Google'a gönderin
4. ✅ Backend CORS'u güncelleyin
5. ✅ LemonSqueezy webhook URL'sini güncelleyin
6. ✅ Social media paylaşım kartlarını test edin: https://cards-dev.twitter.com/validator

---

## 📞 Destek

- Lovable Docs: https://docs.lovable.dev/features/custom-domain
- Lovable Discord: https://discord.gg/lovable
- DNS Checker: https://dnschecker.org
