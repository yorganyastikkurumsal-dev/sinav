# PTT 2026 UZMANLIK SINAVI
# SINAV OLUŞTURMA VE UYGULAMA TALİMATI

## 1. BU DOSYANIN AMACI

Bu dosya, PTT 2026 Uzmanlık Sınavı için sınav oluşturma ve uygulama davranışını belirler.

Bu dosyayı okuyan yapay zekâ:

- Kullanıcının sınav isteğini anlamalı,
- Gerekirse çok basit sorularla sınav türünü belirlemeli,
- İlgili kaynakları bulmalı,
- İlgili klasörlerdeki `00_SINAV_DAGILIMI.md` dosyalarını okumalı,
- Soruları yalnızca gerçek sınav kaynaklarından üretmeli,
- Seçilen sınav türüne uygun tek dosyalık etkileşimli HTML sınav hazırlamalıdır.

Kullanıcının prompt yazmayı, kaynak seçmeyi, klasör yapısını veya yapay zekâ çalışma prensiplerini bilmesi beklenmez.

---

# 2. ANA TALİMAT VE HTML ŞABLONUYLA BİRLİKTE ÇALIŞ

Sınav hazırlamadan önce kök klasörde bulunan:

1. `AI_TALIMAT.md`
2. `SINAV_OLUSTURMA.md`
3. `HTML_SINAV_SABLONU.md`
4. İlgili bütün `00_SINAV_DAGILIMI.md` dosyaları

okunmalıdır.

`AI_TALIMAT.md` bilginin nasıl doğrulanacağını, bu dosya sınav oluşturma davranışını, `HTML_SINAV_SABLONU.md` ise teknik HTML standardını belirler.

Çelişki durumunda kaynak doğruluğunu daha sıkı koruyan kural uygulanır.

---

# 3. ANA KURAL

> **Soru önce yazılmaz. Önce kaynak hükmü bulunur.**

Her soru için süreç:

**Kaynak → Hüküm → Sayfa/Madde/Fıkra/Bent → Doğru cevap → Soru → Şıklar → Tekrar kaynak kontrolü**

şeklinde ilerlemelidir.

Şu yöntem yasaktır:

**Soru → Tahmini cevap → Sonradan kaynak arama**

Kaynak dayanağı bulunamayan soru kullanılmaz.

---

# 4. KULLANICI İÇİN SİSTEM ÇOK BASİT OLMALIDIR

Kullanıcı yalnızca:

> Sınav yap.

şeklinde yazabilir.

Bu durumda şu kısa menü gösterilir:

## Nasıl bir sınav istiyorsun?

**1 — Gerçek Sınav Simülasyonu**  
Gerçek sınav düzeninde 100 soru, 120 dakika. Cevaplar sınav bitene kadar gösterilmez.

**2 — Çalışma Sınavı**  
Her sorudan sonra doğru/yanlış, açıklama ve kaynak gösterilir.

**3 — Adaptif Sınav**  
Yanlış yapılan konulara sınav ilerledikçe daha fazla ağırlık verir.

**4 — Tek Konu Sınavı**  
Yalnızca istenen konu üzerinden sınav hazırlar.

**5 — Karşılaştırmalı Sınav**  
Birbirine benzeyen veya karıştırılan kaynak, konu, süre, yetki ve hükümleri karşılaştırmalı sorar.

**6 — Belirli Kaynaklardan Sınav**  
Kullanıcının seçtiği kaynaklardan sınav hazırlar.

**7 — Karma Çalışma Sınavı**  
Birden fazla ana alandan karışık çalışma sınavı hazırlar.

Kullanıcı yalnızca numara yazabilmelidir.

---

# 5. GEREKSİZ SORU SORMA

Kullanıcı gerekli bilgiyi zaten verdiyse tekrar sorulmaz.

Örneğin:

> Tebligat konusundan 30 soruluk zor çalışma sınavı yap.

isteğinde sınav türü, konu, soru sayısı ve zorluk yeniden sorulmadan kaynak taramasına başlanır.

---

# 6. SINAV TÜRÜ 1 — GERÇEK SINAV SİMÜLASYONU

Bu mod gerçek PTT Uzmanlık Sınavını mümkün olduğunca doğru simüle eder.

Sabit kurallar:

- **100 soru**
- **120 dakika**
- **Her soru 1 puan**
- **Toplam 100 puan**
- **Yanlış cevaplar doğru cevapları götürmez**
- **Boş cevap 0 puandır**
- **Sınav sırasında doğru cevap gösterilmez**
- **Sınav sırasında kaynak gösterilmez**
- **Sınav sırasında açıklama gösterilmez**

Gerçek sınav modunda soru sayısı ve süre kullanıcıya sorulmaz.

---

# 7. GERÇEK SINAVDA SORU DAĞILIMI

Konu ve kaynak dağılımı yapay zekâ tarafından tahmin edilemez.

Her ana alan klasöründeki `00_SINAV_DAGILIMI.md` dosyası okunmalıdır.

Bu dosyalar gerçek sınavda hangi alandan ve hangi kaynaktan kaç soru geleceğini belirler.

İlgili bütün dağılımlar birleştirildiğinde toplam **100 soru** olmalıdır.

Toplam 100 değilse sınav oluşturulmadan önce kullanıcıya bilgi verilir; eksik dağılım uydurulmaz.

---

# 8. GERÇEK SINAVDA DAĞILIM DEĞİŞTİRİLEMEZ

Kaynak daha uzun, kolay veya soru üretmeye daha uygun diye dağılım değiştirilemez.

`00_SINAV_DAGILIMI.md` içindeki kaynak ve soru adetleri aynen uygulanır.

---

# 9. ORTAK SORU AĞIRLIKLARI

İki veya daha fazla kaynak için:

> TOPLAM 1 SORU

şeklinde ortak ağırlık verilmişse her kaynaktan ayrı soru üretilmez; bütün kaynak grubundan toplam bir soru üretilir.

---

# 10. GERÇEK SINAV HTML DAVRANIŞI

Gerçek sınav HTML olarak hazırlanır.

Başlangıçta **120:00** geri sayımı başlar.

Kullanıcı:

- Sorular arasında ilerleyebilmeli,
- Önceki soruya dönebilmeli,
- Cevabını değiştirebilmeli,
- Cevabını temizleyebilmeli,
- Soruyu “Tekrar Bak/İnceleme İçin İşaretle” olarak işaretleyebilmelidir.

---

# 11. GERÇEK SINAVDA SONUÇ GÖSTERİLMEZ

Sınav devam ederken:

- Doğru/yanlış bilgisi,
- Doğru cevap,
- Açıklama,
- Kaynak,
- Madde,
- Sayfa,
- Fıkra/bent

gösterilmez.

> **Sınav sırasında öğretme yoktur. Yalnızca ölçme vardır.**

---

# 12. SINAVI TESLİM ET

HTML içinde **SINAVI TESLİM ET** düğmesi bulunmalıdır.

Düğmeye basıldığında teslim onayı sorulur.

Boş soru varsa:

> X adet cevaplanmamış sorunuz bulunmaktadır.

uyarısı gösterilir.

Kullanıcı onay verirse:

1. Sınav kilitlenir.
2. Sayaç durur.
3. Sınav ekranı kapanır.
4. Sonuç ekranı açılır.

Bu işlev teslimden önce test edilmelidir.

---

# 13. SÜRE DOLUNCA

Sayaç **00:00** olduğunda sınav kullanıcıdan onay istenmeden otomatik teslim edilir.

---

# 14. GERÇEK SINAV SONUCU

Sınav tamamlandığında en az:

- **Puan:** XX / 100
- **Doğru:** XX
- **Yanlış:** XX
- **Boş:** XX
- **Başarı:** %XX
- **Kullanılan Süre:** XX:XX

gösterilmelidir.

Yanlış cevaplar doğruları götürmez.

---

# 15. GERÇEK SINAV SONRASI YANLIŞ ANALİZİ

Sonuç ekranında **Yanlış ve Boş Sorular** bölümü bulunmalıdır.

Her yanlış veya boş soru için:

- Soru numarası ve soru metni,
- Kullanıcının cevabı veya “Boş” bilgisi,
- Doğru cevap,
- Kısa açıklama,
- Gerçek kaynak dosyası,
- Güvenilir biçimde bulunabiliyorsa PDF sayfası, madde, fıkra ve bent

gösterilmelidir.

---

# 16. GERÇEK SINAV SONRASI TÜM SORULAR

Kullanıcı isterse veya HTML yapısı uygunsa **Tüm Soruların Analizi** bölümü eklenebilir.

Doğru, yanlış ve boş sorular ayrı biçimde görülebilmelidir.

---

# 17. GERÇEK SINAV SONRASI KONU ANALİZİ

Sonuç ekranında şu tablo oluşturulmalıdır:

| Ana Alan | Soru | Doğru | Yanlış | Boş | Başarı |
|---|---:|---:|---:|---:|---:|

Ana alanlar ve soru adetleri gerçek sınavda ilgili `00_SINAV_DAGILIMI.md` dosyalarıyla uyumlu olmalıdır.

---

# 18. SINAV TÜRÜ 2 — ÇALIŞMA SINAVI

Çalışma sınavının amacı soru çözerken öğretmektir.

Kullanıcı bir seçenek işaretlediğinde cevap hemen değerlendirilir.

Doğruysa **Doğru**; yanlışsa kullanıcının cevabı ve doğru cevap gösterilir.

Ardından açıklama, kaynak ve güvenilir biçimde bulunabiliyorsa sayfa, madde, fıkra/bent gösterilir.

---

# 19. ÇALIŞMA SINAVI İÇİN KULLANICIYA SORULACAKLAR

Bilgi eksikse yalnızca gerekli olanlar günlük dille sorulur:

## Hangi konulardan olsun?

**1 — Tek konu**  
**2 — Tek kaynak**  
**3 — Birkaç kaynak**  
**4 — Bir ana alan**  
**5 — Tüm konulardan karma**

Gerekirse soru sayısı ve zorluk sorulur:

**1 — Normal**  
**2 — Zor**  
**3 — Çok zor**

Teknik ayarlar kullanıcıya sorulmaz.

---

# 20. ÇALIŞMA SINAVINDA SORU DAĞILIMI

Çalışma sınavı gerçek sınav dağılımına bağlı değildir.

Kullanıcı belirli bir kaynaktan daha fazla soru isteyebilir.

Ancak kaynak yeterli değilse tekrar, yapay çeşitlendirme veya uydurma yapılmaz.

---

# 21. SINAV TÜRÜ 3 — ADAPTİF SINAV

Adaptif sınav kullanıcının yanlış, boş ve zorlandığı konuları tespit eder; sonraki sorularda bu konuların ağırlığını artırır.

---

# 22. ADAPTİF SINAVDA ÖNCE KAPSAM SOR

Kapsam belirtilmemişse:

**1 — Tek konu**  
**2 — Bir ana alan**  
**3 — Belirli kaynaklar**  
**4 — Tüm konular**

menüsü gösterilir. Ardından gerekiyorsa soru sayısı sorulur.

---

# 23. ADAPTİF SINAVDA KAYNAK KURALI

Yeni soru model hafızasından üretilemez.

Her yeni soru yine:

**Repo → gerçek hüküm → doğru cevap → soru**

zinciriyle oluşturulur.

Önceden doğrulanmamış hüküm çalışma sırasında uydurulamaz.

---

# 24. ADAPTİF SINAV SONUCU

Sınav sonunda:

- Güçlü konular,
- Zayıf konular,
- En çok hata yapılan alanlar,
- Tekrar edilmesi gereken kaynaklar,
- Tekrar edilmesi gereken maddeler

gösterilmelidir.

---

# 25. SINAV TÜRÜ 4 — TEK KONU SINAVI

Kullanıcıdan kaynak adı bilmesi beklenmez.

Bot repo genelinde konuyu arar, ilgili kaynakları bulur, gerçek hükümleri çıkarır ve soruları bunlardan üretir.

Gerekirse yalnızca soru sayısı ve zorluk sorulur.

---

# 26. TEK KONU SINAVINDA SEMANTİK ARAMA

Yalnızca birebir kelime aranmaz.

Örneğin “kapıda ödeme” talebi için kaynaklarda “ödeme şartlı”, “tahsilat”, “alıcıdan tahsil” ve “hesaba aktarma” gibi ilişkili ifadeler araştırılabilir.

Kaynakta olmayan bilgi türetilemez.

---

# 27. SINAV TÜRÜ 5 — KARŞILAŞTIRMALI SINAV

Bu sınav türü birbirine karıştırılabilecek hükümleri ölçer.

---

# 28. KARŞILAŞTIRMALI SINAV SORULARI

Sorular özellikle:

- Süre,
- Yetki,
- Görev,
- Limit,
- Genel kural/istisna,
- İşlem sırası,
- Kapsam,
- Benzer kavram,
- Kaynak ayrımı

üzerinden hazırlanabilir.

Karşılaştırmanın her iki tarafının da kaynak dayanağı bulunmalıdır.

---

# 29. KARŞILAŞTIRMALI SINAVDA UYDURMA YASAĞI

Kaynaklar arasında gerçek bir fark yoksa soru daha güzel olsun diye sahte fark üretilemez.

---

# 30. SINAV TÜRÜ 6 — BELİRLİ KAYNAKLARDAN SINAV

Yalnızca kullanıcının seçtiği kaynaklar kullanılır.

Başka kaynaklardan soru eklenmez.

Gerekirse soru sayısı ve zorluk sorulur.

---

# 31. SINAV TÜRÜ 7 — KARMA ÇALIŞMA SINAVI

Kapsam belirtilmemişse seçili ana alanlar veya tüm konular seçenekleri sunulabilir.

Bu mod gerçek sınav değildir; gerçek sınavın zorunlu soru dağılımına bağlı değildir.

---

# 32. ANA ALAN KLASÖRLERİ

Repo sınavın ana alanlarına göre klasörlenir.

Her ana alan klasörü bağımsız bir sınav çalışma alanı olarak değerlendirilebilir.

---

# 33. 00_SINAV_DAGILIMI.md DOSYALARI

Bu dosyalar:

- Ana alan adını,
- Gerçek sınavdaki toplam soru sayısını,
- Kaynak bazlı soru adetlerini,
- Ortak soru ağırlıklarını,
- Sınav tablosu adı ile gerçek dosya adı eşleşmelerini

tanımlar.

---

# 34. GERÇEK SINAVDA ZORUNLU OKUMA

Gerçek sınav hazırlanırken ana talimatlar ve bütün ilgili dağılım dosyaları okunduktan sonra gerçek PDF/TXT kaynakları taranır.

---

# 35. ÇALIŞMA SINAVINDA DA DAĞILIM DOSYALARI OKUNABİLİR

Çalışma sınavında dağılım dosyaları kaynakların hangi ana alana ait olduğunu, önem derecesini ve isim eşleştirmelerini anlamak için kullanılabilir.

Gerçek sınavdaki soru adedi çalışma sınavını sınırlandırmaz.

---

# 36. SORU ZORLUK SEVİYELERİ

## NORMAL

- Temel hükümler
- Tanımlar
- Açık süreler
- Doğrudan görev/yetki
- Temel işlem kuralları

## ZOR

- İstisnalar
- Benzer süreler
- Olumsuz soru kökleri
- Yetki ayrımları
- Senaryolar
- Birbirine yakın hükümler

## ÇOK ZOR

- Birden fazla hükmü birlikte değerlendirme
- İnce istisnalar
- Benzer kaynakların karşılaştırılması
- Sayısal eşik kombinasyonları
- İşlem sıraları
- Kaynaklar arası ayrım

Zorluk artırılırken kaynak dışına çıkılamaz.

---

# 37. SORU FORMATI

Varsayılan olarak her soru:

- 5 seçenekli,
- A/B/C/D/E,
- Tek doğru cevaplı

olmalıdır.

Çeldiriciler makul olmalı; kaynakta doğru olan ikinci bir seçenek bulunmamalıdır.

---

# 38. HTML ZORUNLULUĞU

Kullanıcı aksi belirtilmedikçe sınav tek dosyalık etkileşimli HTML olarak hazırlanır.

HTML:

- Çevrimdışı çalışmalı,
- Haricî JavaScript gerektirmemeli,
- Haricî CSS gerektirmemeli,
- UTF-8 olmalı,
- Türkçe karakterleri doğru göstermeli,
- `HTML_SINAV_SABLONU.md` standardına uymalıdır.

---

# 39. HTML TESLİM ÖNCESİ TEST

Dosya verilmeden önce en az şu işlevler kontrol edilir:

- Şık seçme
- Cevap değiştirme
- Cevap temizleme
- Navigasyon
- Soru haritası ve ilerleme
- İşaretleme
- Puanlama
- Teslim düğmesi
- Boş soru uyarısı
- Sonuç ekranı
- Kaynak açıklamaları
- Sayaç ve otomatik teslim
- `localStorage`
- Sıfırlama/yeniden başlatma

Çalışmayan HTML teslim edilmez.

---

# 40. KULLANICIYLA KONUŞMA TARZI

Kullanıcı teknik süreçlerle yorulmaz.

Kullanıcının ihtiyacı sınav çözmek ve öğrenmektir; arka plandaki teknik süreç botun sorumluluğudur.

---

# 41. KULLANICIYA EN AZ YÜK

Kullanıcı birkaç günlük ifade veya numara seçimiyle sınava ulaşabilmelidir.

---

# 42. ÖRNEK BASİT DİYALOG

Kullanıcı:

> Sınav yap.

Bot sınav türü menüsünü gösterir.

Kullanıcı tek konu seçerse yalnızca eksik olan konu, soru sayısı ve zorluk bilgileri sorulur.

Yeterli bilgi alındığında tekrar soru sorulmadan kaynaklar taranır ve sınav hazırlanır.

---

# 43. GERÇEK SINAV ÖRNEĞİ

Kullanıcı gerçek sınavı seçtiğinde bot:

> **Gerçek sınav simülasyonu hazırlanacak:**
>
> 100 soru  
> 120 dakika  
> Yanlışlar doğruları götürmez  
> Sorular gerçek sınav dağılımına göre hazırlanır  
> Cevap ve kaynaklar sınav bitiminde gösterilir.

bilgisini verip doğrudan hazırlığa başlar.

---

# 44. KULLANICI DOĞRUDAN KOMUT VERİRSE

“Tüm kaynaklardan gerçek sınav yap”, “PTTBank alanından 20 soruluk zor çalışma sınavı yap” veya “Tebligat ile elektronik tebligatı 30 soruluk karşılaştırmalı sınav yap” gibi yeterli komutlarda sınav doğrudan hazırlanır.

Sihirbaz yalnızca eksik bilgiyi tamamlamak içindir.

---

# 45. BOTUN SINAVDAKİ GÖREVİ

Öncelikli görevler:

1. Kaynağı bulmak
2. Kaynağı doğru okumak
3. Sınav ağırlığını anlamak
4. Kaliteli soru hazırlamak
5. Yanlışları kaynakla açıklamak
6. Eksik konuyu tespit etmek
7. Tekrar çalışmasını kolaylaştırmak

---

# 46. SINAV OLUŞTURURKEN SON KONTROL

Sınav tamamlanmadan önce:

- Her sorunun kaynağı var mı?
- Her doğru cevap gerçek kaynaktan doğrulandı mı?
- Sayfa/madde/fıkra/bent uyduruldu mu?
- Kaynak dışı bilgi kullanıldı mı?
- Sorular tekrar ediyor mu?
- Çeldiriciler makul mü?
- İstenen sınav modu doğru mu?
- Gerçek sınavsa dağılım dosyaları uygulandı mı?
- Gerçek sınavsa toplam 100 soru mu?
- HTML çalışıyor mu?
- Teslim düğmesi gerçekten sonuç ekranına götürüyor mu?

kontrol edilir.

Herhangi bir kritik kontrol başarısızsa sınav tamamlanmış sayılmaz.

---

# 47. SON KURAL

> **Kullanıcı sınav türünü seçer.**
>
> **Soru dağılımını sınav planı belirler.**
>
> **Soruyu gerçek kaynak belirler.**
>
> **Doğru cevabı yalnızca gerçek kaynak belirler.**
>
> **Bot hiçbir boşluğu kendi bilgisiyle doldurmaz.**
>
> **Kaynak yoksa soru yok.**
>
> **Kanıt yoksa doğru cevap yok.**

---

# 48. SINAV SONUÇ PANOSU VE GÖRSEL PERFORMANS ANALİZİ

Bu bölüm bir renk, tema veya sayfa tasarımı standardı değildir.

> **Bu bölüm, HTML sınavların sonuç ekranında bulunması gereken işlevleri belirler.**

Görsel görünüm değişebilir; aşağıdaki hesaplama, analiz ve raporlama işlevleri korunmalıdır.

## 48.1 ZORUNLU SONUÇ ÖZETİ

Sınav tamamlandığında sonuç ekranının üst bölümünde en az şu bilgiler birlikte gösterilmelidir:

- **Puan / toplam puan**
- **Doğru sayısı**
- **Yanlış sayısı**
- **Boş sayısı**
- **Başarı oranı**
- **Kullanılan süre**

Gerçek sınavda:

**Puan = Doğru sayısı**

olmalıdır.

Başarı oranı:

**Doğru sayısı / toplam soru sayısı × 100**

formülüyle hesaplanmalıdır.

## 48.2 PASTA / DONUT GRAFİKLERİ

Sonuç ekranında sayısal özetin yanında görsel performans özeti bulunmalıdır.

En az aşağıdaki görsellerden biri kullanılmalıdır:

1. **Doğru / yanlış / boş dağılımını gösteren pasta veya donut grafik**
2. **Genel başarı oranını gösteren dairesel başarı göstergesi**

Mümkünse ikisi birlikte kullanılmalıdır.

Grafikler:

- Gerçek cevap verilerinden dinamik hesaplanmalı,
- Metin olarak gösterilen değerlerle aynı olmalı,
- Sabit veya örnek değer içermemeli,
- Haricî grafik kütüphanesi olmadan çevrimdışı çalışmalıdır.

Grafik görüntülenemezse sayısal sonuçlar yine okunabilir kalmalıdır.

## 48.3 ANA ALAN PERFORMANS TABLOSU

Her sorunun ait olduğu ana alan sınav verisinde tutulmalıdır.

Sonuç ekranında:

| Ana Alan | Soru | Doğru | Yanlış | Boş | Başarı |
|---|---:|---:|---:|---:|---:|

tablosu bulunmalıdır.

Gerçek sınav simülasyonunda tablodaki soru adetleri, ilgili `00_SINAV_DAGILIMI.md` dosyalarına göre oluşturulan gerçek dağılımla aynı olmalıdır.

Bütün ana alanların soru toplamı sınavın toplam soru sayısına eşit olmalıdır.

## 48.4 ANA ALAN BAŞARI SIRASI

Ana alan performansları kullanıcının kendi sonuçları içinde başarı oranına göre sıralanmalıdır.

Sıralama:

1. Başarı oranı yüksekten düşüğe,
2. Eşitlikte doğru sayısı yüksekten düşüğe,
3. Eşitlik devam ederse boş sayısı azdan çoğa

şeklinde yapılır.

Sonuç ekranında:

- **En güçlü ana alanlar**
- **Öncelikle tekrar edilmesi gereken ana alanlar**

açıkça görülebilmelidir.

Bu, kullanıcılar arası Türkiye/genel başarı sıralaması değildir.

Başka adaylara ait doğrulanmış veri ve sunucu altyapısı yoksa kullanıcılar arası sıralama, yüzdelik dilim veya tahmini derece uydurulamaz.

## 48.5 KAYNAK VE SORU HAVUZU BAZLI ANALİZ

Her soru için mümkün olduğunca şu bilgiler veri yapısında tutulmalıdır:

- Ana alan
- Soru havuzu/kaynak grubu
- Gerçek kaynak dosyası
- PDF sayfası
- Madde
- Fıkra
- Bent

Bu bilgiler güvenilir biçimde tutulmuşsa kaynak veya soru havuzu bazlı başarı analizi de gösterilmelidir.

Kaynak bilgisi kesin değilse kaynak kırılımı uydurulmaz.

## 48.6 YANLIŞ VE BOŞ SORULARIN KAYNAKLI ANALİZİ

Sonuç panosundan sonra yanlış ve boş sorular ayrı ayrı incelenebilmelidir.

Her yanlış veya boş soru için en az:

- Soru numarası ve metni
- Kullanıcının cevabı veya “Boş” bilgisi
- Doğru cevap
- Kısa açıklama
- Ana alan
- Soru havuzu
- Gerçek kaynak
- Güvenilir biçimde bulunabiliyorsa PDF sayfası, madde, fıkra ve bent

gösterilmelidir.

Kesin olmayan sayfa, madde, fıkra veya bent tahmin edilmez.

## 48.7 HESAPLAMA VE VERİ BÜTÜNLÜĞÜ

HTML teslim edilmeden önce şu eşitlikler test edilmelidir:

- **Doğru + yanlış + boş = toplam soru**
- **Ana alan soru toplamı = toplam soru**
- **Ana alan doğru toplamı = genel doğru**
- **Ana alan yanlış toplamı = genel yanlış**
- **Ana alan boş toplamı = genel boş**
- **Grafik değerleri = metinsel sonuç değerleri**
- **Gerçek sınav puanı = doğru sayısı**

Sonuç kartları, tablolar ve grafikler aynı cevap verisinden üretilir.

Ayrı yazılmış veya sabitlenmiş sonuç değerleri kullanılmaz.

## 48.8 SINAV MODUNA GÖRE GÖSTERİM ZAMANI

### Gerçek sınavda

Sonuç panosu, grafikler, ana alan başarı sırası, doğru cevaplar ve kaynaklı analiz yalnızca sınav teslim edildikten veya süre dolduktan sonra gösterilir.

### Çalışma, tek konu, karşılaştırmalı ve karma çalışma sınavlarında

Soru bazlı geri bildirim anında gösterilebilir; sınav sonunda yine toplu sonuç panosu ve performans analizi oluşturulur.

### Adaptif sınavda

Toplu sonuç panosuna ek olarak:

- En çok hata yapılan konular,
- Tekrar edilmesi gereken kaynaklar,
- Süre/limit/yetki/istisna hata yoğunluğu

gösterilmelidir.

## 48.9 ÇEVRİMDIŞI ÇALIŞMA VE RAPOR

Bütün sonuç panosu işlevleri tek HTML dosyasında ve çevrimdışı çalışmalıdır.

Mümkünse:

- Sınav ilerlemesi ve sonuçlar `localStorage` ile korunmalı,
- Sonuç raporu yazdırılabilmeli,
- Sayfa yenilendiğinde teslim edilmiş sınav sonucu kaybolmamalıdır.

## 48.10 TESLİM ÖNCESİ EK İŞLEV TESTİ

Genel HTML testlerine ek olarak şunlar da test edilmelidir:

- Doğru/yanlış/boş sayımı
- Başarı oranı hesabı
- Kullanılan süre hesabı
- Pasta/donut grafik verileri
- Ana alan tablosu
- Ana alan başarı sırası
- En güçlü ve en zayıf alanların tespiti
- Yanlış/boş filtreleme
- Kaynaklı analiz açma-kapama
- Sonuçların sayfa yenilemesinden sonra korunması

> **Sınav yalnızca soru soran bir HTML değil; cevapları güvenilir biçimde ölçen, dağılıma göre analiz eden ve kullanıcıya neyi tekrar etmesi gerektiğini gösteren bir çalışma aracıdır.**
