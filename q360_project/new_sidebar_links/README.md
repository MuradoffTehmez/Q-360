# Yeni Səhifələr üçün Sidebar Linkləri

Bu qovluqda sistemə əlavə edilmiş yeni funksiyalar üçün sidebar linklərinin HTML şablonları mövcuddur.

## Əlavə Ediləcək Linklər:

### 1. Dashboard Modulu
**Fayl:** `dashboard_sentiment_analysis.html`
**Yer:** Dashboard bölməsinin içinə (Proqnozlaşdırmadan sonra)

Bu link əhval-ruhiyyə analizi dashboardunu göstərir.

### 2. Notifications Modulu
**Fayl:** `notifications_delivery_logs.html`
**Yer:** Bildirişlər bölməsinin içinə (Email şablonlarından sonra, test bildirişlərindən əvvəl)

Bu link bildiriş göndəriş loglarını göstərir.

### 3. Audit Modulu
**Fayl:** `audit_log_search.html`
**Yer:** Audit bölməsinin içinə (Təhlükəsizlik panelindən sonra)

Bu link audit log axtarışı səhifəsinə keçidi təmin edir.

### 4. Dashboard Modulu
**Fayl:** `dashboard_ai_management.html`
**Yer:** Dashboard bölməsinin içinə (Proqnozlaşdırmadan sonra)

Bu link AI model idarəetmə panelini göstərir.

## Əlavə Etme Qaydası:

1. Mövcud `templates/base/sidebar.html` faylını açın
2. Uyğun bölməni tapın
3. Hər bir fayldakı HTML kodunu uyğun yerə əlavə edin
4. Yenidən yükləyin

## Qeyd:

Bütün linklər artıq backend tərəfində uyğundur və müvafiq URL-lər qurulubdur.