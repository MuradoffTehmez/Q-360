# HTML Səhifələri və UI İstifadə Təlimatları

## 📌 Yaradılmış HTML Səhifələr

### 🏅 Kompetensiya Modulu

1. **Kompetensiya Siyahısı** - `/competencies/`
   - Bütün kompetensiyaların siyahısı
   - Axtarış və filter funksiyası
   - Admin üçün yeni kompetensiya əlavə etmə
   - Real-time statistika kartları
   - **Fayl:** `templates/competencies/competency_list.html`

2. **Kompetensiya Detayları** - `/competencies/<id>/`
   - Kompetensiya haqqında ətraflı məlumat
   - Pozisiyaların və istifadəçilərin siyahısı
   - Statistika və vizual qrafiklər
   - Admin üçün edit və delete funksiyaları
   - **Fayl:** `templates/competencies/competency_detail.html`

3. **Mənim Bacarıqlarım** - `/competencies/my-skills/`
   - İstifadəçinin öz bacarıqlarının siyahısı
   - Yeni bacarıq əlavə etmə modal
   - Təsdiq statusu göstəricisi
   - Bacarıq səviyyələri diaqramı
   - **Fayl:** `templates/competencies/my_skills.html`

### 📚 Təlim Modulu

4. **Mənim Təlimlərim** - `/training/`
   - Tab-based interfeys (Pending, In Progress, Completed)
   - Proqres göstəriciləri
   - Son tarix xatırlatmaları
   - **Fayl:** `templates/training/my_trainings.html`

5. **Təlim Kataloqu** - `/training/catalog/`
   - Bütün təlimlərin kataloqu
   - Filter (növ, çətinlik)
   - Təlim kartları (müddət, qiymət)
   - Detal məlumat linkləri
   - **Fayl:** `templates/training/catalog.html`

6. **Təlim Detayları** - `/training/<id>/`
   - Təlim haqqında ətraflı məlumat
   - Proqres yeniləmə funksiyası
   - Qeydlər (notes) əlavə etmə
   - Təlim resursunun detalları
   - Tələb olunan kompetensiyalar
   - **Fayl:** `templates/training/training_detail.html`

### 🛡️ Təhlükəsizlik Modulu

7. **Təhlükəsizlik Dashboard** - `/audit/security/` (Yalnız Admin)
   - Son 7 günün uğursuz giriş statistikası
   - Chart.js ilə vizual qrafiklər
   - Top 3 uğursuz IP ünvanları
   - Top 3 uğursuz istifadəçilər
   - Son uğursuz giriş cəhdləri cədvəli
   - **Fayl:** `templates/audit/security_dashboard.html`

---

## 🔗 URL Strukturu

### Template URL-lər (İnsan üçün)
```
/competencies/                  → Kompetensiya siyahısı
/competencies/<id>/             → Kompetensiya detayları
/competencies/my-skills/        → Mənim bacarıqlarım
/competencies/manage/           → Kompetensiya idarəetməsi (Admin)

/training/                      → Mənim təlimlərim
/training/<id>/                 → Təlim detayları
/training/catalog/              → Təlim kataloqu
/training/manage/               → Təlim idarəetməsi (Admin)

/audit/security/                → Təhlükəsizlik dashboard (Admin)
```

### API URL-lər (JavaScript üçün)
```
/api/competencies/competencies/         → GET/POST kompetensiyalar
/api/competencies/user-skills/my_skills/ → GET mənim bacarıqlarım

/api/training/resources/                → GET təlim resursları
/api/training/user-trainings/my_pending/ → GET pending təlimlər

/api/audit/security-stats/              → GET təhlükəsizlik statistikaları
```

---

## 🎨 UI Xüsusiyyətləri

### Bootstrap 5 Komponentləri
- ✅ Responsive card layout
- ✅ Modal dialogs
- ✅ Tab navigation
- ✅ Progress bars
- ✅ Badges və statuslar
- ✅ Table formatlaşdırması
- ✅ Form validasiyası

### Font Awesome İkonlar
- 🏅 `fa-lightbulb` - Kompetensiyalar
- ⭐ `fa-star` - Bacarıqlar
- 🎓 `fa-graduation-cap` - Təlimlər
- 📚 `fa-book` - Katal oq
- 🛡️ `fa-shield-alt` - Təhlükəsizlik

### Chart.js Qrafiklər
- Line chart - Uğursuz giriş statistikaları (Security dashboard)
- Gələcək: Pie chart - Bacarıq paylanması

---

## 🔧 Quraşdırma və Test

### 1. Migration-ları tətbiq et
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Serveri işə sal
```bash
python manage.py runserver
```

### 3. Login ol
```
http://localhost:8000/accounts/login/
```

### 4. Səhifələrə get
```
http://localhost:8000/competencies/
http://localhost:8000/training/
http://localhost:8000/audit/security/  (Admin only)
```

---

## 📱 Responsive Design

Bütün səhifələr mobil, tablet və desktop üçün optimize edilib:

- **Mobile** (< 768px): Sidebar collapse, card stack
- **Tablet** (768px - 992px): 2 column layout
- **Desktop** (> 992px): 3-4 column layout

---

## 🔐 İcazələr

| Səhifə | Employee | Manager | Admin |
|--------|----------|---------|-------|
| Kompetensiya siyahısı | ✓ (Oxu) | ✓ (Oxu) | ✓ (CRUD) |
| Mənim bacarıqlarım | ✓ | ✓ | ✓ |
| Təlim kataloqu | ✓ | ✓ | ✓ |
| Mənim təlimlərim | ✓ | ✓ | ✓ |
| Kompetensiya idarəetməsi | ✗ | ✗ | ✓ |
| Təlim idarəetməsi | ✗ | ✓ | ✓ |
| Təhlükəsizlik dashboard | ✗ | ✗ | ✓ |

---

## 💡 JavaScript Funksiyaları

### Kompetensiya Siyahısı
```javascript
loadCompetencies(page)      // Kompetensiyaları yüklə
loadStatistics()            // Statistikaları yüklə
renderCompetencies(data)    // Cədvəli render et
renderPagination(data)      // Paginasiya göstər
```

### Mənim Bacarıqlarım
```javascript
loadMySkills()             // İstifadəçi bacarıqlarını yüklə
```

### Təlim Kataloqu
```javascript
loadCatalog()              // Təlim kataloqunu yüklə (filter ilə)
```

### Təhlükəsizlik Dashboard
```javascript
// Avtomatik yüklənir
// Chart.js ilə vizual qrafik yaradır
```

---

## 🎯 Nümunə İstifadə Ssenariləri

### Ssenarı 1: İstifadəçi yeni bacarıq əlavə edir
1. `/competencies/my-skills/` səhifəsinə get
2. "Add Skill" düyməsini klikə
3. Modal açılır
4. Kompetensiya, səviyyə və bal seç
5. "Add" düyməsini klikə
6. AJAX request göndərilir
7. Səhifə avtomatik yenilənir

### Ssenarı 2: Admin təhlükəsizlik dashboardunu yoxlayır
1. `/audit/security/` səhifəsinə get
2. Son 7 günün statistikasını görür
3. Qrafik və cədvəlləri təhlil edir
4. Şübhəli IP-ləri müəyyənləşdirir

### Ssenarı 3: İstifadəçi təlim axtarır
1. `/training/catalog/` səhifəsinə get
2. Filter seçir (növ: Course, çətinlik: Beginner)
3. "Apply" düyməsini klikə
4. Filtered nəticələr göstərilir
5. Təlim kartına klikə
6. Detal səhifəyə yönləndirilir

---

## 🐛 Troubleshooting

### Problem: Səhifə 404 xətası verir
**Həll:** URL-nin düzgün konfiqurasiya olunduğunu yoxlayın
```python
# config/urls.py-də yoxlayın
path('competencies/', include('apps.competencies.urls', namespace='competencies')),
```

### Problem: API cavab vermir
**Həll:**
1. Token-in mövcudluğunu yoxlayın
2. Browser console-da JavaScript xətaları yoxlayın
3. Network tab-da API request statusunu yoxlayın

### Problem: Chart.js qrafik göstərilmir
**Həll:**
```html
<!-- Chart.js CDN yükləndiyini yoxlayın -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

### Problem: Modal açılmır
**Həll:**
```html
<!-- Bootstrap JS yükləndiyini yoxlayın -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

---

## 📊 Performans Optimallaşdırması

1. **Lazy Loading:** Böyük səhifələrdə təsvirləri lazy load edin
2. **Pagination:** API nəticələrində paginasiya istifadə edin
3. **Caching:** StaticFiles-ı cache edin
4. **Minification:** Production-da JS/CSS minify edin

---

## 🔄 Gələcək Təkmilləşdirmələr

- [ ] Real-time bildirişlər (WebSocket)
- [ ] Offline dəstəyi (Service Worker)
- [ ] Export funksiyası (PDF, Excel)
- [ ] Advanced filter və axtarış
- [ ] Bulk əməliyyatlar
- [ ] Dark mode dəstəyi

---

**Qeyd:** Bütün səhifələr Django template engine və Bootstrap 5 ilə yaradılıb. JavaScript funksiyaları jQuery istifadə edir və REST API ilə əlaqələnir.
