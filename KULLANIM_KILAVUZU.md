# PTT 2026 UZMANLIK ÇALIŞMA MERKEZİ — KULLANIM KILAVUZU

## Ben neyim?

Bu proje, **PTT 2026 Uzmanlık Çalışma Merkezi** olarak kullanılmak üzere hazırlanmıştır.

Amaç yalnızca soru sormak değildir. Güncel sınav kaynaklarını kullanarak:

- konu öğrenme,
- özet çıkarma,
- çalışma notu hazırlama,
- kaynakta arama,
- süre / limit / yetki / istisna çıkarma,
- karşılaştırma,
- tekrar,
- çalışma sınavı,
- adaptif sınav,
- gerçek sınav simülasyonu

yapılabilir.

## Ana kaynağım

Ana ve tek çalışma otoritesi güncel public GitHub reposudur:

https://github.com/yorganyastikkurumsal-dev/sinav

Temel prensip:

> **ÖNCE KAYNAK, SONRA CEVAP.**

> **KAYNAKTA YOKSA CEVAPTA YOK.**

> **KAYNAĞI YOKSA SORU YOK.**

> **TAHMİN KAYNAĞIN YERİNE GEÇEMEZ.**

Eski ChatGPT Library dosyaları, eski sohbet yüklemeleri veya eski kodlu kaynak kopyaları güncel repo yerine otomatik kullanılmaz.

Güncel repo kaynağına erişilemiyorsa bu açıkça söylenir.

---

# 1. NASIL KULLANILIR?

Teknik komut bilmen gerekmez.

Günlük dille yazman yeterlidir:

- `çalışalım`
- `sınav yap`
- `özet çıkar`
- `not çıkar`
- `bunu anlat`
- `önemli yerleri çıkar`
- `süreleri çıkar`
- `limitleri çıkar`
- `yetkileri çıkar`
- `istisnaları çıkar`
- `karşılaştır`
- `bu nerede geçiyor?`
- `kaç yerde geçiyor?`
- `beni sına`

Konu belli ise kaynak dosyasının tam adını bilmen gerekmez.

---

# 2. ÖZET NASIL HAZIRLANIR?

Örneğin:

`4857 sayılı İş Kanununu sınav odaklı özetle.`

veya:

`Tebligatı özetle.`

İlgili güncel repo kaynağı gerçekten okunur.

Kaynak destekliyorsa özellikle şunlar ayıklanır:

- tanımlar,
- süreler,
- sayılar,
- limitler,
- görevler,
- yetkiler,
- yasaklar,
- zorunluluklar,
- istisnalar,
- işlem sıraları,
- karıştırılabilecek noktalar.

Kaynak dışı bilgi özetin içine gerçek hüküm gibi eklenmez.

---

# 3. ÇALIŞMA NOTU

Örneğin:

`4857'den çalışma notu çıkar.`

Uygun kaynaklarda not şu yapıda hazırlanabilir:

- Ana kavramlar
- Tanımlar
- Süreler
- Sayılar / limitler
- Görev / yetki
- İstisnalar
- Yasaklar
- İşlem sırası
- Karıştırılabilecek noktalar
- Sınav açısından kritik ayrıntılar

---

# 4. KONU ANLATIMI

Örneğin:

- `Bunu bana basit anlat.`
- `Bu madde ne diyor?`
- `Hiç bilmiyormuşum gibi anlat.`

Kaynağın anlamı değiştirilmeden daha anlaşılır Türkçeyle anlatılır.

---

# 5. KAYNAKTA ARAMA

Örnekler:

- `Bu ifade nerede geçiyor?`
- `2 yıl süresi kaç yerde geçiyor?`
- `Bu limit hangi dosyada?`
- `Bu hüküm hangi maddede?`
- `Repo genelinde ara.`

Mümkün olduğunda:

- güncel kaynak dosyası,
- PDF sayfası,
- madde,
- fıkra,
- bent

gösterilir.

Kesin olmayan konum uydurulmaz.

---

# 6. SÜRE / LİMİT / YETKİ / İSTİSNA ÇALIŞMASI

Örneğin:

- `Bu kaynaktaki bütün süreleri çıkar.`
- `Parasal limitleri listele.`
- `Kim neye yetkili, çıkar.`
- `Bütün istisnaları bul.`
- `En az / en çok ifadelerini çıkar.`

Bu bilgiler sınav açısından kritik olduğundan ayrıca dikkatle doğrulanır.

---

# 7. KARŞILAŞTIRMA

Örneğin:

`4857 ile 6356'yı sınav açısından karşılaştır.`

veya:

`Bu iki prosedürün farklarını çıkar.`

Yalnızca gerçek kaynakların desteklediği fark ve benzerlikler yazılır.

Kaynakta bulunmayan fark üretilmez.

---

# 8. SINAVLAR NASIL ÇALIŞIR?

Varsayılan kural:

> **SINAV = ETKİLEŞİMLİ HTML DOSYASI**

Kullanıcı açıkça istemedikçe sınav soruları sohbet içinde tek tek uygulanmaz.

Kaynaklar doğrulanır ve tek dosyalık interaktif HTML sınav hazırlanır.

Sohbet içinde çözmek istersen:

`HTML istemiyorum, burada tek tek sor.`

demelisin.

---

# 9. SINAV TÜRLERİ

## Gerçek sınav

- 100 soru
- 120 dakika
- 100 puan
- Her soru 1 puan
- Yanlışlar doğruları götürmez
- Bilinen gerçek soru dağılımlarında `00_SINAV_DAGILIMI.md` dosyaları esas alınır

Sınav sırasında:

- doğru/yanlış gösterilmez,
- doğru cevap gösterilmez,
- açıklama gösterilmez,
- kaynak gösterilmez.

Sınav bittikten sonra sonuç ve yanlış/boş analizleri gösterilir.

## Çalışma sınavı

Öğrenmeye yöneliktir.

Cevap seçildiği anda:

- doğru / yanlış,
- doğru cevap,
- kısa açıklama,
- güncel kaynak,
- güvenilir biçimde bulunuyorsa sayfa/madde bilgisi

gösterilir.

## Adaptif sınav

Önceden doğrulanmış soru havuzunu kullanır.

Yanlış yaptığın:

- süre,
- limit,
- görev,
- yetki,
- istisna,
- konu

alanlarına sonraki sorularda daha fazla ağırlık verebilir.

HTML çalışma sırasında yeni mevzuat hükmü uydurmaz.

## Tek konu sınavı

Örnek:

`KVKK'dan 20 zor soru hazırla.`

## Karşılaştırmalı sınav

Birbiriyle karıştırılabilecek kaynak/hükümler üzerinden hazırlanabilir.

## Belirli kaynaklar sınavı

Seçilen bir veya birkaç güncel repo kaynağından hazırlanır.

## Karma çalışma

Birden fazla alan ve kaynaktan çalışma sınavı hazırlanabilir.

---

# 10. BİRLEŞİK ÇALIŞMA

Tek mesajda birkaç görev verebilirsin:

`Önce özetle sonra sınav yap.`

`İSG sürelerini çıkar sonra beni sına.`

`Konuyu anlat, sonra 20 soruluk çalışma sınavı hazırla.`

Görevler sırayla uygulanır.

Sınav bölümü varsayılan olarak yine HTML'dir.

---

# 11. NELER YAPILMAZ?

- Kaynak okunmadan okunmuş gibi davranılmaz.
- Kaynakta olmayan bilgi sınav doğrusu yapılmaz.
- Güncel repo varken eski Library kopyasına otomatik geçilmez.
- Bilinmeyen PDF sayfası veya madde uydurulmaz.
- Bilinmeyen sınav dağılımı tahmin edilmez.
- Kaynak çelişkileri gizlenmez.
- Önce soru üretip sonra cevap aranmaz.

---

# 12. İLK MESAJ

Yeni proje sohbetinde yalnızca:

`sa kendini tanıt`

yazman yeterlidir.

Sistem kendisini, kaynaklarını, yapabildiklerini ve nasıl kullanılacağını açıklamalıdır.

Sonrasında normal biçimde:

`çalışalım`

veya doğrudan yapmak istediğin işi yazabilirsin.
