# PTT 2026 UZMANLIK SINAVI — HTML ŞABLON TALİMATI

Bu dosya, sınav üreten yapay zekânın **HTML sınavı nasıl hazırlayacağını ve hangi işlevleri zorunlu olarak sağlaması gerektiğini** belirler.

Bu dosya soru ve doğru cevap kaynağı değildir.

> **Soru dağılımını ilgili `00_SINAV_DAGILIMI.md` belirler.**
>
> **Soru içeriğini ve doğru cevabı gerçek PDF/TXT kaynakları belirler.**
>
> **Bu dosya yalnızca doğrulanmış sınavın teknik uygulama standardını belirler.**

---

# 1. ZORUNLU OKUMA SIRASI

HTML sınav hazırlanmadan önce:

1. `AI_TALIMAT.md`
2. `SINAV_OLUSTURMA.md`
3. `HTML_SINAV_SABLONU.md`
4. İlgili `00_SINAV_DAGILIMI.md` dosyaları
5. İlgili gerçek PDF/TXT kaynakları

okunmalıdır.

Önce kaynak hükmü bulunur; doğru cevap sabitlenir; soru ve şıklar doğrulanır; en son HTML’e aktarılır.

---

# 2. TEK DOSYALIK HTML ZORUNLULUĞU

Kullanıcı açıkça başka bir format istemedikçe sınav:

> **Tek dosyalık etkileşimli HTML**

olarak hazırlanmalıdır.

HTML:

- UTF-8 olmalı,
- Çevrimdışı çalışmalı,
- Haricî CSS kullanmamalı,
- Haricî JavaScript kullanmamalı,
- Haricî font kullanmamalı,
- Haricî grafik kütüphanesine ihtiyaç duymamalı,
- İnternet bağlantısı olmadan açılmalı,
- Telefon, tablet ve masaüstünde çalışmalı,
- Başka kişilere tek `.html` dosyası olarak gönderilebilmelidir.

---

# 3. SINAV MODLARI

## 3.1 Gerçek Sınav

Sabit kurallar:

- 100 soru
- 120 dakika
- Her soru 1 puan
- Toplam 100 puan
- Yanlışlar doğruları götürmez
- Boş cevap 0 puandır
- Sorular A/B/C/D/E olmak üzere 5 seçeneklidir
- Sınav sırasında doğru/yanlış gösterilmez
- Sınav sırasında doğru cevap gösterilmez
- Sınav sırasında açıklama gösterilmez
- Sınav sırasında kaynak gösterilmez
- Süre bitince sınav otomatik teslim edilir
- Teslimden sonra sonuç ve kaynaklı analiz gösterilir
- İlgili bütün `00_SINAV_DAGILIMI.md` dosyalarındaki dağılım aynen uygulanır

## 3.2 Çalışma Sınavı

- Kullanıcı cevap verdiğinde doğru/yanlış gösterilebilir
- Doğru cevap gösterilir
- Kısa açıklama gösterilir
- Gerçek kaynak gösterilir
- Güvenilir biçimde bulunabiliyorsa PDF sayfası, madde, fıkra ve bent gösterilir
- Gerçek sınav soru sayısı sınırı uygulanmaz

## 3.3 Adaptif Sınav

- HTML kendi başına yeni mevzuat hükmü veya soru uyduramaz
- Önceden kaynakla doğrulanmış geniş soru havuzu kullanılır
- Yanlış, boş ve zorlanılan konu/etiketlere ağırlık verilebilir
- Aynı soru aynı oturumda gereksiz yere tekrar edilmez

## 3.4 Tek Konu / Belirli Kaynak / Karşılaştırmalı / Karma Çalışma

- Yalnızca seçilen kapsam kullanılır
- Karşılaştırmalı sorularda her iki tarafın da gerçek kaynak dayanağı bulunur
- Kaynakta olmayan fark veya istisna üretilmez
- Çalışma sınavı geri bildirim davranışı uygulanabilir

---

# 4. SORU VERİ STANDARDI

Her soru mümkün olduğunca şu veri yapısını taşımalıdır:

```javascript
{
  id: 1,
  question: "Soru metni",
  options: ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği", "E seçeneği"],
  correct: 0,
  explanation: "Kaynağa dayalı kısa açıklama",

  sources: [
    {
      file: "Kaynak.pdf",
      page: "12",
      article: "Madde 7",
      paragraph: "2",
      clause: "b"
    }
  ],

  mainArea: "Ana Alan",
  category: "Konu",
  sourcePool: "Kaynak veya ortak soru havuzu",
  skill: "Süre / Yetki / Görev / Limit / İstisna / İşlem sırası / vb.",
  difficulty: "Normal / Zor / Çok Zor"
}
```

`correct` alanı:

- `0 = A`
- `1 = B`
- `2 = C`
- `3 = D`
- `4 = E`

olarak kullanılmalıdır.

Kaynakta güvenilir biçimde bulunmayan sayfa, madde, fıkra veya bent tahmin edilmez; `null` veya boş bırakılır.

Aynı isimli PDF ve TXT iki ayrı kaynak sayılmaz.

---

# 5. GENEL HTML İŞLEV STANDARDI

Sınav ekranında en az:

- Sınav başlığı
- Sınav modu
- Toplam soru sayısı
- Süre
- Geri sayım sayacı
- Cevaplanan soru sayısı
- İlerleme çubuğu
- Soru numarası
- Soru metni
- Beş seçenek
- Önceki soru
- Sonraki soru
- Cevabı temizle
- Tekrar Bak / İnceleme için işaretle
- Soru haritası
- Sınavı teslim et

işlevleri bulunmalıdır.

Kullanıcı gerçek sınavda:

- Önceki soruya dönebilmeli,
- Sonraki soruya geçebilmeli,
- Cevabını değiştirebilmeli,
- Cevabını temizleyebilmeli,
- Soruyu inceleme için işaretleyebilmeli,
- Soru haritasından istediği soruya gidebilmelidir.

---

# 6. TAM FLEX RESPONSIVE VE MOBİL KULLANIM STANDARDI

Bu bölüm renk, tema veya görsel zevk standardı değildir.

> **Bütün HTML sınavların telefon, tablet ve masaüstünde sorunsuz kullanılmasını sağlayan zorunlu işlev standardıdır.**

Kullanıcının kurum bilgisayarını sürekli meşgul etmesi beklenemez. Sınav, tek HTML dosyası olarak telefona gönderildiğinde de tam işlevli çalışmalıdır.

## 6.1 Desteklenecek ekranlar

HTML sınav en az şu ekran genişliklerinde kullanılabilir olmalıdır:

- **320 px** küçük telefon
- **360 px** standart Android telefon
- **390–430 px** güncel telefonlar
- **768 px** tablet
- **1024 px** tablet veya küçük dizüstü
- **1366 px** standart masaüstü
- **1920 px ve üzeri** geniş ekran

Hem **dikey** hem **yatay** ekran yönü desteklenmelidir.

Hiçbir desteklenen genişlikte:

- Sayfanın tamamında yatay kaydırma oluşmamalı,
- Soru veya şık metni ekrandan taşmamalı,
- Düğmeler üst üste binmemeli,
- Sayaç veya ilerleme çubuğu kesilmemeli,
- Sonuç kartları ve grafikler görünmez hâle gelmemelidir.

## 6.2 Viewport ve telefon güvenli alanı

HTML başlığında en az:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

kullanılmalıdır.

Çentikli ve alt gezinme çubuklu telefonlarda gerekli yerlerde:

- `env(safe-area-inset-top)`
- `env(safe-area-inset-right)`
- `env(safe-area-inset-bottom)`
- `env(safe-area-inset-left)`

kullanılmalıdır.

Sabit üst sayaç ve alt menü telefonun sistem alanlarının altında kalmamalıdır.

## 6.3 Flex tabanlı ana yerleşim

Ana sınav yerleşimi uyarlanabilir `flex` yapısıyla kurulmalıdır.

Masaüstünde:

- Soru alanı kalan genişliği almalı,
- Soru haritası sağ tarafta bulunabilmeli,
- Soru panelinde `min-width: 0` kullanılmalı,
- Uzun metinler ana yerleşimi genişletmemelidir.

Telefon ve tablette:

- Ana yerleşim tek sütuna dönmeli,
- Soru kartı ekran genişliğini aşmamalı,
- Masaüstü kenar çubuğu soru alanını daraltmamalı,
- Soru haritası mobil çekmece, tam ekran panel veya modal biçiminde açılmalıdır.

Örnek temel davranış:

```css
.exam-layout{
  display:flex;
  align-items:flex-start;
  gap:20px;
  min-width:0;
}
.question-panel{
  flex:1 1 0;
  min-width:0;
}
.question-map{
  flex:0 0 315px;
}
@media (max-width:1024px){
  .exam-layout{flex-direction:column}
  .question-panel{width:100%}
}
```

Renk ve ölçüler değişebilir; esnek davranış korunmalıdır.

## 6.4 Metin taşması yasağı

Soru, şık, açıklama, kaynak ve ana alan adlarında uzun metin bulunabileceği kabul edilmelidir.

Gerekli alanlarda:

```css
min-width:0;
overflow-wrap:anywhere;
word-break:normal;
```

kullanılmalıdır.

Metin küçültülerek okunamaz hâle getirilmemeli; gerektiğinde doğal olarak alt satıra geçmelidir.

## 6.5 Dokunmatik kullanım

Telefon ve tablette:

- Şıkların dokunma yüksekliği tercihen en az **48 px**, hiçbir durumda **44 px altında olmamalı**,
- Önceki, sonraki, harita, işaretle ve teslim düğmeleri en az **44 × 44 px** dokunma alanına sahip olmalı,
- Düğmeler yanlış dokunmaya yol açacak kadar yakın olmamalı,
- İşlemler yalnızca `hover` davranışına bağlı olmamalı,
- `touch-action: manipulation` kullanılabilmeli,
- Seçili şık yalnızca renkle değil; kenarlık, simge veya belirgin durum değişikliğiyle de anlaşılmalıdır.

## 6.6 Mobil sabit alt gezinme

Uzun sınavlarda telefonda şu işlemlere sürekli erişim sağlanmalıdır:

- Önceki
- Sonraki
- Soru haritası
- Tekrar Bak / İşaretle
- Teslim et

Bu işlemler mobilde sabit alt gezinme çubuğunda gösterilebilir.

Sabit alt çubuk:

- Soru ve şıkların üzerini kapatmamalı,
- İçerikte kendi yüksekliği kadar alt boşluk bırakmalı,
- Güvenli alt alanı dikkate almalı,
- Yatay telefon görünümünde de kullanılabilir kalmalıdır.

## 6.7 Mobil soru haritası

Masaüstündeki soru haritası telefonda soru metnini daraltmamalıdır.

Mobil soru haritası:

- Sağdan veya alttan açılan çekmece,
- Tam ekran panel,
- Açılır modal

şeklinde uygulanabilir.

Harita açıldığında:

- Arka plan etkileşimi engellenmeli,
- Kapat düğmesi bulunmalı,
- Dış alana dokunarak kapatılabilmeli,
- `Escape` tuşuyla kapatılabilmeli,
- Bir soru seçildiğinde panel kapanıp seçilen soruya gidilmeli,
- Cevaplanmış, boş, aktif ve işaretli sorular ayırt edilebilmelidir.

## 6.8 Üst bilgi, sayaç ve ilerleme

Sayaç ve sınav ilerlemesi mobilde görünür kalmalıdır.

Dar ekranda:

- Başlık kısaltılabilir,
- Alt açıklama gizlenebilir,
- Sayaç küçültülebilir ancak okunabilir kalmalı,
- İlerleme çubuğu ayrı satıra geçebilmelidir.

Sayaç hiçbir genişlikte üst üste binmemeli veya kesilmemelidir.

## 6.9 Modal ve teslim uyarısı

Teslim onayı ve boş soru uyarısı küçük ekranda tamamen kullanılabilir olmalıdır.

Mobil modal:

- Ekran yüksekliğini aşarsa kendi içinde kaydırılmalı,
- Düğmeleri en az 44 px yüksekliğinde olmalı,
- Dikey ekranda düğmeler alt alta geçebilmeli,
- Tarayıcı çubuğu nedeniyle erişilemez hâle gelmemelidir.

## 6.10 Sonuç ekranı ve grafikler

Sonuç kartları telefon ekranında tek veya iki sütuna düşebilmelidir.

Pasta/donut grafikler ve dairesel başarı göstergeleri:

- Ekrandan taşmamalı,
- Genişliğe göre küçülmeli,
- Metinsel sonuçları kapatmamalı,
- Grafik çalışmasa bile sayısal sonuçlar okunabilir kalmalıdır.

Ana alan performans tablosu dar ekranda yalnızca kendi kutusu içinde kontrollü yatay kaydırılabilir. Bütün sayfayı yatay kaydırmamalıdır.

Yanlış/boş soru analizindeki uzun kaynak adları ve açıklamalar ekrandan taşmamalıdır.

## 6.11 Ekran yönü değişikliği

Telefon dikeyden yataya veya yataydan dikeye çevrildiğinde:

- Cevaplar kaybolmamalı,
- Aktif soru değişmemeli,
- Sayaç sıfırlanmamalı,
- Açık mobil harita güvenli biçimde kapanabilmeli,
- Yerleşim yeni genişliğe göre yeniden düzenlenmelidir.

---

# 7. ERİŞİLEBİLİRLİK STANDARDI

- Düğmelerin anlaşılır metni veya `aria-label` değeri bulunmalı,
- Klavye odağı görünür olmalı,
- Modal ve soru haritası klavyeyle kullanılabilmeli,
- Renk tek başına durum göstergesi olmamalı,
- Yazı boyutu büyütüldüğünde yatay taşma oluşmamalı,
- Kullanıcı `Tab`, `Enter`, ok tuşları ve uygun kısayollarla sınavı kullanabilmelidir.

Mobilde ekran okuyucu için anlam taşımayan simge düğmelerine açıklayıcı `aria-label` verilmelidir.

---

# 8. SINAV DURUMUNUN KORUNMASI

Sınav durumu `localStorage` ile korunmalıdır.

En az şu bilgiler saklanmalıdır:

- Başlama zamanı
- Bitiş zamanı / son teslim zamanı
- Aktif soru
- Verilen cevaplar
- İnceleme için işaretlenen sorular
- Teslim durumu
- Teslim zamanı

Sayfa yenilendiğinde:

- Sayaç yeniden başlamamalı,
- Cevaplar silinmemeli,
- İşaretli sorular kaybolmamalı,
- Aktif soru mümkünse korunmalı,
- Teslim edilmiş sınav tekrar çözülebilir hâle gelmemelidir.

Aynı cihaz ve tarayıcıda dosya yeniden açıldığında, tarayıcının yerel dosyalara depolama izni verdiği ölçüde kayıt korunmalıdır.

---

# 9. GERÇEK SINAVDA TESLİM DAVRANIŞI

HTML’de `SINAVI TESLİM ET` düğmesi bulunmalıdır.

Düğmeye basıldığında:

- Teslim onayı sorulmalı,
- Boş soru sayısı gösterilmeli,
- Kullanıcı vazgeçebilmelidir.

Kullanıcı onaylarsa:

1. Sınav kilitlenir
2. Sayaç durur
3. Cevaplar değiştirilemez
4. Sonuç ekranı açılır

Sayaç `00:00` olduğunda sınav onay istenmeden otomatik teslim edilmelidir.

---

# 10. SONUÇ PANOSU VE PERFORMANS ANALİZİ

Sınav sonunda en az:

- Puan / toplam puan
- Doğru
- Yanlış
- Boş
- Başarı oranı
- Kullanılan süre

birlikte gösterilmelidir.

Gerçek sınavda:

> **Puan = doğru sayısı**

olmalıdır.

Başarı oranı:

> **Doğru / toplam soru × 100**

formülüyle hesaplanmalıdır.

## 10.1 Görsel sonuç özeti

Sonuç ekranında en az:

- Doğru/yanlış/boş pasta veya donut grafiği
- Genel başarı oranını gösteren dairesel gösterge

ögelerinden biri bulunmalıdır; mümkünse ikisi birlikte kullanılmalıdır.

Grafikler:

- Gerçek cevap verilerinden dinamik hesaplanmalı,
- Metinsel sonuçlarla aynı değerleri göstermeli,
- Sabit örnek değer içermemeli,
- Çevrimdışı çalışmalıdır.

## 10.2 Ana alan performansı

Her sorunun `mainArea` bilgisi tutulmalıdır.

Sonuç ekranında:

| Ana Alan | Soru | Doğru | Yanlış | Boş | Başarı |
|---|---:|---:|---:|---:|---:|

 tablosu bulunmalıdır.

Gerçek sınavda ana alan soru adetleri ilgili dağılım dosyalarıyla aynı olmalıdır.

Ana alanlar ayrıca başarı oranına göre sıralanmalı; en güçlü ve öncelikle tekrar edilmesi gereken alanlar gösterilmelidir.

Bu sıralama kullanıcının kendi konu alanları arasındadır. Başka adaylara ait doğrulanmış veri yoksa Türkiye sıralaması, yüzdelik dilim veya tahminî derece uydurulamaz.

## 10.3 Yanlış ve boş soruların kaynaklı analizi

Her yanlış veya boş soru için:

- Soru numarası
- Soru metni
- Kullanıcının cevabı veya `Boş`
- Doğru cevap
- Kısa açıklama
- Ana alan
- Soru havuzu
- Gerçek kaynak dosyası
- Güvenilir biçimde bulunabiliyorsa PDF sayfası, madde, fıkra ve bent

 gösterilmelidir.

Gerçek sınavda bu bilgiler yalnızca teslimden sonra açılır.

---

# 11. HESAPLAMA VE VERİ BÜTÜNLÜĞÜ

HTML teslim edilmeden önce:

- Doğru + yanlış + boş = toplam soru
- Ana alan soru toplamı = toplam soru
- Ana alan doğru toplamı = genel doğru
- Ana alan yanlış toplamı = genel yanlış
- Ana alan boş toplamı = genel boş
- Grafik değerleri = metinsel sonuç değerleri
- Gerçek sınav puanı = doğru sayısı

 eşitlikleri test edilmelidir.

Sonuç kartları, tablolar ve grafikler aynı cevap verisinden üretilmelidir. Ayrı ayrı yazılmış veya sabitlenmiş sonuç değerleri kullanılmamalıdır.

---

# 12. PAYLAŞILABİLİR MOBİL DOSYA STANDARDI

Arkadaşa gönderilen tek `.html` dosyası:

- Dosya yöneticisinden tarayıcıyla açılabilmeli,
- İnternet bağlantısı olmadan çalışmalı,
- Soruları ve kaynak analizlerini kendi içinde taşımalı,
- Ek klasör veya dosya gerektirmemeli,
- Telefon ekranında bütün temel işlevleri sunmalıdır.

Kullanıcıya mümkünse dosyayı doğrudan tarayıcıda açması söylenmelidir. Mesajlaşma uygulamalarının önizleme ekranı JavaScript’i çalıştırmıyorsa dosya tarayıcıya aktarılmalıdır.

---

# 13. TESLİM ÖNCESİ ZORUNLU TESTLER

## 13.1 Kaynak ve soru testi

- [ ] Soru sayısı doğru mu?
- [ ] Her soruda 5 seçenek var mı?
- [ ] Her soruda tek doğru cevap var mı?
- [ ] Doğru cevap gerçek kaynakta mı?
- [ ] Kaynak referansı doğru soruya mı bağlı?
- [ ] Sayfa/madde/fıkra/bent uydurulmuş mu?
- [ ] Gerçek sınav dağılım dosyalarına tam uyuyor mu?

## 13.2 Temel işlev testi

- [ ] Şık seçme çalışıyor mu?
- [ ] Cevap değiştirme çalışıyor mu?
- [ ] Önceki/sonraki çalışıyor mu?
- [ ] Cevabı temizleme çalışıyor mu?
- [ ] Tekrar Bak/İşaretle çalışıyor mu?
- [ ] Soru haritası çalışıyor mu?
- [ ] Teslim düğmesi çalışıyor mu?
- [ ] Boş soru uyarısı çalışıyor mu?
- [ ] Süre dolunca otomatik teslim oluyor mu?
- [ ] Yenilemede süre ve cevaplar korunuyor mu?
- [ ] Sonuç hesabı doğru mu?
- [ ] Yanlış/boş kaynak analizi açılıyor mu?

## 13.3 Responsive ve mobil test

- [ ] 320 px genişlikte bütün sayfada yatay taşma yok mu?
- [ ] 360 px genişlikte bütün şıklar rahat seçiliyor mu?
- [ ] 390–430 px genişlikte sayaç ve ilerleme kesilmiyor mu?
- [ ] 768 px tablette yerleşim çalışıyor mu?
- [ ] 1024 px geçiş noktasında soru haritası doğru davranıyor mu?
- [ ] 1366 px masaüstünde soru alanı ve harita dengeli mi?
- [ ] 1920 px geniş ekranda içerik gereksiz yere dağılmıyor mu?
- [ ] Telefon dikey görünüm çalışıyor mu?
- [ ] Telefon yatay görünüm çalışıyor mu?
- [ ] Mobil alt gezinme içeriği kapatmıyor mu?
- [ ] Mobil soru haritası açılıyor, kapanıyor ve soru seçiyor mu?
- [ ] Dokunma alanları en az 44 × 44 px mi?
- [ ] Uzun soru ve uzun şık metni taşmıyor mu?
- [ ] Teslim modalı küçük ekranda kullanılabiliyor mu?
- [ ] Sonuç kartları ve grafikler taşmıyor mu?
- [ ] Ana alan tablosu bütün sayfayı yatay kaydırmıyor mu?
- [ ] Ekran yönü değişince cevaplar ve sayaç korunuyor mu?

## 13.4 Tarayıcı testi

En az:

- [ ] Masaüstü Chrome/Edge
- [ ] Android Chrome

üzerinde kontrol edilmelidir.

Mümkünse ayrıca:

- [ ] iPhone Safari
- [ ] Firefox

üzerinde kontrol edilmelidir.

Kritik testlerden biri başarısızsa HTML tamamlanmış sayılmaz.

---

# 14. SON KURAL

> **Sınav yalnızca masaüstünde açılan bir sayfa değildir.**
>
> **Tek dosya olarak paylaşıldığında çalışanların telefondan, tabletten veya bilgisayardan rahatça çözebileceği tam işlevli bir sınav uygulamasıdır.**
>
> **Tasarım değişebilir; kaynak doğruluğu, sınav davranışı, sonuç analizi ve responsive işlevler değiştirilemez.**
>
> **Kaynak yoksa soru yok. Kanıt yoksa doğru cevap yok.**
