# Admin Panel - Manuel Paket Yönetimi Rehberi

## Özellik Özeti

Admin panelinde kayıtlı kullanıcılara manuel olarak paket (Free/Pro/Enterprise) atayabilme özelliği eklendi.

## Özellikler

### 1. Kullanıcı Listesi
- Tüm kayıtlı kullanıcılar Admin panelinde görüntülenir
- Her kullanıcının email, isim, rol, mevcut paketi ve katılım tarihi görünür

### 2. Paket Atama
- Admin, herhangi bir kullanıcıya Free/Pro/Enterprise paketi atayabilir
- Dropdown menüden paket seçimi yapılır
- Paket değişikliği anında Firebase'e kaydedilir
- Başarılı işlem sonrası bildirim gösterilir

### 3. Rol Yönetimi
- Admin, kullanıcıların rollerini (User/Admin) değiştirebilir
- Rol değişiklikleri de anında kaydedilir

## Teknik Detaylar

### Frontend (Admin.tsx)
```typescript
// Paket güncelleme fonksiyonu
const handleSubscriptionChange = async (userId: string, tier: 'free' | 'pro' | 'enterprise') => {
  const subscription: UserSubscription = {
    tier,
    startDate: new Date().toISOString(),
    status: 'active',
    endDate: tier === 'free' ? undefined : new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
  };
  
  await setUserSubscription(userId, subscription);
}
```

### Backend API (backend/api/admin.py)

#### Endpoint: POST /api/admin/update-plan
```json
{
  "user_id": "firebase-user-id",
  "plan": "pro"  // "free", "pro", veya "enterprise"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully updated user to pro plan"
}
```

#### Endpoint: POST /api/admin/update-role
```json
{
  "user_id": "firebase-user-id",
  "role": "admin"  // "admin" veya "user"
}
```

### Firebase Veritaşı Yapısı

#### User Subscriptions
```
/user_subscriptions/{userId}/
  ├── tier: "free" | "pro" | "enterprise"
  ├── startDate: "2024-01-15T10:00:00.000Z"
  ├── endDate: "2024-02-15T10:00:00.000Z" (opsiyonel)
  └── status: "active" | "expired" | "cancelled"
```

#### User Roles
```
/user_roles/{userId}/
  ├── role: "admin" | "user"
  └── updatedAt: "2024-01-15T10:00:00.000Z"
```

## Paket Limitleri

### Free Plan
- 1 açık pozisyon
- Temel özellikler
- Ücretsiz

### Pro Plan
- 10 açık pozisyon
- Otomatik trading
- EMA sinyalleri
- TP/SL hesaplayıcı
- Aylık ücretli

### Enterprise Plan
- 50 açık pozisyon
- Tüm Pro özellikleri
- Özel stratejiler
- API erişimi
- Öncelikli destek
- Aylık ücretli

## Admin Erişimi

Admin paneline yalnızca `role: "admin"` olan kullanıcılar erişebilir.

### Admin Kontrolü
1. Frontend: `useAdmin()` hook ile kontrol
2. Backend: `verify_admin()` middleware ile doğrulama

## Kullanım Adımları

1. Admin olarak giriş yapın
2. Dashboard'dan "Admin" butonuna tıklayın
3. Kullanıcı listesinde değiştirmek istediğiniz kullanıcıyı bulun
4. "Subscription" sütunundaki dropdown'dan yeni paketi seçin
5. Değişiklik otomatik olarak kaydedilir
6. Kullanıcının yeni paket limitleri anında aktif olur

## Güvenlik

- Tüm admin endpoint'leri Firebase token ile korunur
- Admin rolü kontrolü hem frontend hem backend'de yapılır
- Paket değişiklikleri audit log'a kaydedilir (opsiyonel - eklenebilir)

## LemonSqueezy Entegrasyonu

Manuel paket ataması, LemonSqueezy ödemelerinden bağımsız çalışır:
- LemonSqueezy webhook'ları otomatik paket güncellemesi yapar
- Admin manuel olarak paket değişikliği yapabilir (demo, test, özel durumlar için)
- Her iki yöntem de Firebase'e aynı formatta kaydedilir

## Test Senaryoları

1. **Manuel Paket Yükseltme:**
   - Free kullanıcıyı Pro'ya yükselt
   - Kullanıcı 10 pozisyon açabilmeli

2. **Manuel Paket Düşürme:**
   - Pro kullanıcıyı Free'ye düşür
   - Kullanıcı yalnızca 1 pozisyon açabilmeli

3. **Admin Rol Atama:**
   - Normal kullanıcıya admin rolü ver
   - Kullanıcı Admin paneline erişebilmeli

## Geliştirme Notları

### Firebase Admin SDK Kurulumu
Backend için Firebase Admin SDK gereklidir:

```bash
pip install firebase-admin
```

### Ortam Değişkenleri
```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
```

## Sonraki Adımlar

- [ ] LemonSqueezy onayı alındıktan sonra gerçek webhook entegrasyonu
- [ ] Paket değişiklik geçmişi (audit log)
- [ ] Toplu paket güncelleme özelliği
- [ ] Paket süre uzatma/kısaltma
- [ ] Email bildirimleri (paket değişikliği için)
