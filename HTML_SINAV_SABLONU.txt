# PTT 2026 UZMANLIK SINAVI — HTML ŞABLON TALİMATI

Bu dosya, sınav üreten botun **HTML sınavı nasıl hazırlayacağını** tanımlar.

## Zorunlu okuma sırası

Sınav hazırlanırken bot şu sırayı izlemelidir:

1. `AI_TALIMAT.md`
2. `SINAV_OLUSTURMA.md`
3. `HTML_SINAV_SABLONU.md`
4. İlgili klasörlerdeki `00_SINAV_DAGILIMI.md`
5. İlgili gerçek PDF/TXT kaynakları

## Ana kural

**Bu şablon soru kaynağı değildir.**  
Sorular ve doğru cevaplar yalnızca gerçek PDF/TXT kaynaklarından doğrulanır.

> Önce kaynak → sonra hüküm → sonra doğru cevap → sonra soru → en son HTML.

---

# SINAV MODLARI

## 1. Gerçek Sınav

- 100 soru
- 120 dakika
- Yanlışlar doğruları götürmez
- Sınav sırasında doğru/yanlış gösterilmez
- Kaynak ve açıklama sınav sırasında gösterilmez
- Kullanıcı cevap değiştirebilir
- Kullanıcı soruyu `Tekrar Bak` olarak işaretleyebilir
- `SINAVI TESLİM ET` butonu bulunur
- Boş soru varsa teslimden önce uyarılır
- Süre 00:00 olduğunda otomatik teslim edilir
- Sayfa yenilendiğinde sayaç sıfırlanmaz
- Sonuçtan sonra doğru/yanlış/boş, kaynak ve açıklamalar gösterilir
- Gerçek sınavda `00_SINAV_DAGILIMI.md` dosyalarındaki soru adetleri zorunludur

## 2. Çalışma Sınavı

- Kullanıcı cevap verir vermez doğru/yanlış gösterilir
- Doğru cevap gösterilir
- Açıklama gösterilir
- Kaynak dosyası gösterilir
- Biliniyorsa PDF sayfası, madde, fıkra ve bent gösterilir
- Cevap gösterildikten sonra soru kilitlenebilir
- Gerçek sınavdaki kaynak soru sayısı sınırı uygulanmaz

## 3. Adaptif Sınav

- HTML kendi başına yeni soru uydurmaz
- Önceden kaynakla doğrulanmış daha büyük bir soru havuzu hazırlanır
- Kullanıcının yanlış yaptığı `category`, `skill` veya ana alanlara sonraki seçimlerde ağırlık verilebilir
- Aynı soru aynı oturumda tekrar sorulmaz

## 4. Karşılaştırmalı Sınav

- Bir soruda birden fazla kaynak olabilir
- `sources` dizisinde kaynaklar ayrı ayrı tutulur
- Karşılaştırma yalnızca kaynakların gerçekten desteklediği farklar üzerinden yapılır

---

# HTML TASARIM STANDARDI

HTML:

- Tek dosya olmalıdır
- Çevrimdışı çalışmalıdır
- Haricî CSS/JS/font kullanmamalıdır
- UTF-8 olmalıdır
- Mobil ve masaüstünde çalışmalıdır
- 5 seçenekli A-B-C-D-E soru düzeni kullanılmalıdır
- Sade ve profesyonel görünmelidir
- Sorular arasında navigasyon bulunmalıdır
- localStorage ile sınav durumu korunmalıdır
- Gerçek sınavda sayaç yenilemede sıfırlanmamalıdır
- Sonuç ekranında ana alan performansı gösterilmelidir
- Yanlış ve boş sorular özellikle öne çıkarılmalıdır

---

# SORU VERİ STANDARDI

Her soru mümkün olduğunca şu yapıyı kullanmalıdır:

```javascript
{
  id: 1,
  question: "Soru metni",
  options: ["A", "B", "C", "D", "E"],
  correct: 0,
  explanation: "Kaynağa dayalı açıklama",

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
  sourcePool: "Kaynak veya ortak havuz",
  skill: "Süre / Yetki / İstisna / Limit / vb.",
  difficulty: "Normal / Zor / Çok Zor"
}
```

`correct` alanında:

- `0 = A`
- `1 = B`
- `2 = C`
- `3 = D`
- `4 = E`

Kaynakta güvenilir biçimde bulunmayan sayfa/madde/fıkra/bent **uydurulmaz**, `null` bırakılır.

---

# HTML MOTORU

Aşağıdaki kod sınav üretirken temel şablon olarak kullanılmalıdır.

```html
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PTT 2026 Uzmanlık Sınavı</title>
<style>
:root{
  --bg:#f4f6f9;
  --card:#ffffff;
  --text:#1f2937;
  --muted:#6b7280;
  --line:#e5e7eb;
  --primary:#b91c1c;
  --primary-dark:#991b1b;
  --success:#15803d;
  --danger:#b91c1c;
  --warning:#b45309;
  --shadow:0 10px 30px rgba(15,23,42,.08);
}
*{box-sizing:border-box}
body{
  margin:0;
  font-family:Arial,Helvetica,sans-serif;
  background:var(--bg);
  color:var(--text);
}
button,input{font:inherit}
.app{max-width:1180px;margin:auto;padding:18px}
.topbar{
  position:sticky;top:0;z-index:20;
  background:rgba(244,246,249,.96);
  backdrop-filter:blur(8px);
  padding:10px 0 14px;
}
.header-card,.card{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:18px;
  box-shadow:var(--shadow);
}
.header-card{padding:18px 20px}
.header-grid{
  display:grid;
  grid-template-columns:1fr auto;
  gap:18px;
  align-items:center;
}
h1{font-size:24px;margin:0 0 8px}
.meta{color:var(--muted);font-size:14px;line-height:1.5}
.timer{
  min-width:140px;text-align:center;padding:12px 16px;
  border-radius:14px;background:#111827;color:white;
  font-weight:700;font-size:22px;letter-spacing:.5px;
}
.progress-wrap{margin-top:14px}
.progress-line{
  height:9px;background:#eef0f3;border-radius:999px;overflow:hidden
}
.progress-line span{
  display:block;height:100%;width:0;background:var(--primary);transition:.2s
}
.progress-text{font-size:13px;color:var(--muted);margin-top:6px}
.layout{
  display:grid;
  grid-template-columns:minmax(0,1fr) 270px;
  gap:18px;
  margin-top:18px;
}
.card{padding:24px}
.question-number{
  font-weight:700;color:var(--primary);font-size:14px;margin-bottom:10px
}
.question{
  font-size:20px;line-height:1.55;font-weight:700;margin-bottom:20px
}
.options{display:grid;gap:11px}
.option{
  display:flex;gap:12px;align-items:flex-start;
  width:100%;text-align:left;
  border:1px solid var(--line);
  background:#fff;border-radius:13px;
  padding:14px 15px;cursor:pointer;
  transition:.15s;
}
.option:hover{border-color:#9ca3af;transform:translateY(-1px)}
.option.selected{border-color:var(--primary);background:#fff7f7}
.option.correct{border-color:var(--success);background:#f0fdf4}
.option.wrong{border-color:var(--danger);background:#fef2f2}
.option-letter{
  flex:0 0 32px;height:32px;border-radius:9px;
  background:#f3f4f6;display:grid;place-items:center;font-weight:700
}
.option.selected .option-letter{background:var(--primary);color:white}
.option.correct .option-letter{background:var(--success);color:white}
.option.wrong .option-letter{background:var(--danger);color:white}
.feedback{
  display:none;margin-top:18px;border-radius:14px;padding:16px;
  border:1px solid var(--line);line-height:1.55
}
.feedback.show{display:block}
.feedback.good{background:#f0fdf4;border-color:#bbf7d0}
.feedback.bad{background:#fef2f2;border-color:#fecaca}
.source-box{
  margin-top:12px;padding-top:12px;border-top:1px dashed #d1d5db;
  color:#374151;font-size:14px
}
.controls{
  display:flex;flex-wrap:wrap;gap:10px;
  justify-content:space-between;margin-top:20px
}
.controls-left,.controls-right{display:flex;gap:10px;flex-wrap:wrap}
.btn{
  border:0;border-radius:11px;padding:11px 15px;cursor:pointer;font-weight:700
}
.btn-primary{background:var(--primary);color:white}
.btn-primary:hover{background:var(--primary-dark)}
.btn-soft{background:#eef2f7;color:#111827}
.btn-warn{background:#fff7ed;color:#9a3412}
.btn-danger{background:#111827;color:white}
.sidebar{position:sticky;top:150px;height:max-content}
.sidebar h3{margin-top:0}
.nav-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:7px
}
.nav-btn{
  border:1px solid var(--line);background:#fff;border-radius:9px;
  height:38px;cursor:pointer;font-weight:700
}
.nav-btn.current{outline:2px solid var(--primary)}
.nav-btn.answered{background:#f3f4f6}
.nav-btn.review{box-shadow:inset 0 -4px 0 #f59e0b}
.legend{font-size:12px;color:var(--muted);line-height:1.7;margin-top:14px}
.result{display:none}
.result.show{display:block}
.score-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:18px 0
}
.stat{
  border:1px solid var(--line);border-radius:14px;padding:16px;text-align:center
}
.stat strong{display:block;font-size:24px;margin-top:6px}
.review-card{
  border:1px solid var(--line);border-radius:14px;padding:16px;margin-top:12px
}
.review-card h4{margin:0 0 10px}
.tag{
  display:inline-block;padding:4px 8px;border-radius:999px;
  background:#f3f4f6;font-size:12px;margin:2px 4px 2px 0
}
.hidden{display:none!important}
.small{font-size:13px;color:var(--muted)}
hr{border:0;border-top:1px solid var(--line);margin:20px 0}
@media(max-width:850px){
  .layout{grid-template-columns:1fr}
  .sidebar{position:static}
  .header-grid{grid-template-columns:1fr}
  .timer{width:100%}
  .score-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:520px){
  .app{padding:10px}
  .card{padding:17px}
  h1{font-size:20px}
  .question{font-size:18px}
  .nav-grid{grid-template-columns:repeat(5,1fr)}
  .score-grid{grid-template-columns:1fr 1fr}
}
@media print{
  .topbar,.sidebar,.controls{display:none!important}
  body{background:white}
  .card,.header-card{box-shadow:none}
}
</style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="header-card">
      <div class="header-grid">
        <div>
          <h1 id="examTitle">PTT 2026 Uzmanlık Sınavı</h1>
          <div class="meta" id="examMeta"></div>
        </div>
        <div class="timer" id="timer">--:--</div>
      </div>
      <div class="progress-wrap">
        <div class="progress-line"><span id="progressBar"></span></div>
        <div class="progress-text" id="progressText"></div>
      </div>
    </div>
  </div>

  <div id="examView">
    <div class="layout">
      <main class="card">
        <div class="question-number" id="questionNumber"></div>
        <div class="question" id="questionText"></div>
        <div class="options" id="options"></div>

        <div class="feedback" id="feedback"></div>

        <div class="controls">
          <div class="controls-left">
            <button class="btn btn-soft" id="prevBtn">← Önceki</button>
            <button class="btn btn-warn" id="reviewBtn">☆ Tekrar Bak</button>
            <button class="btn btn-soft" id="clearBtn">Cevabı Temizle</button>
          </div>
          <div class="controls-right">
            <button class="btn btn-primary" id="nextBtn">Sonraki →</button>
          </div>
        </div>
      </main>

      <aside class="card sidebar">
        <h3>Sorular</h3>
        <div class="nav-grid" id="navGrid"></div>
        <div class="legend">
          <div>● Cevaplanan</div>
          <div>▬ Turuncu çizgi: Tekrar Bak</div>
        </div>
        <hr>
        <button class="btn btn-danger" style="width:100%" id="submitBtn">
          SINAVI TESLİM ET
        </button>
      </aside>
    </div>
  </div>

  <section class="card result" id="resultView">
    <h2>Sınav Sonucu</h2>
    <div class="score-grid" id="scoreGrid"></div>
    <div id="topicAnalysis"></div>
    <hr>
    <h3>Yanlış ve Boş Sorular</h3>
    <div id="wrongList"></div>
    <hr>
    <h3>Tüm Soruların Analizi</h3>
    <div id="allReview"></div>
    <hr>
    <button class="btn btn-danger" id="resetBtn">Sınavı Sıfırla</button>
  </section>
</div>

<script>
/*
============================================================
PTT 2026 UZMANLIK SINAVI - TEK DOSYALIK HTML MOTORU
============================================================

MODLAR:
- "real"     : Gerçek sınav. Sınav sırasında cevap/kaynak göstermez.
- "study"    : Çalışma sınavı. Cevap seçilince açıklama ve kaynak gösterir.
- "adaptive" : Önceden doğrulanmış soru havuzundan zayıf etiketlere ağırlık verir.

ÖNEMLİ:
Bu dosya soru ÜRETMEZ. Aşağıdaki QUESTIONS dizisine yalnızca
PDF/TXT kaynaktan doğrulanmış sorular yerleştirilmelidir.
*/

const EXAM = {
  id: "ptt_2026_ornek_v1",
  title: "PTT 2026 Uzmanlık Sınavı",
  mode: "study", // "real" | "study" | "adaptive"
  durationMinutes: 30,

  // Gerçek sınav için:
  // mode: "real",
  // durationMinutes: 120,
  // questions dizisinde 100 doğrulanmış soru bulunmalıdır.

  wrongCancelsCorrect: false
};

/*
SORU VERİ ŞABLONU

{
  id: 1,
  question: "SORU METNİ",
  options: ["A", "B", "C", "D", "E"],
  correct: 0, // 0=A, 1=B, 2=C, 3=D, 4=E

  explanation: "Kaynağa dayalı açıklama.",

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
  sourcePool: "Kaynak veya ortak havuz",
  skill: "Süre",       // örn: Süre, Yetki, İstisna, Limit
  difficulty: "Zor"    // Normal, Zor, Çok Zor
}

Karşılaştırmalı soruda sources dizisine iki veya daha fazla kaynak eklenebilir.
Kaynakta bulunmayan sayfa/madde bilgisi UYDURULMAZ; null bırakılır.
*/

const QUESTIONS = [
  {
    id: 1,
    question: "BURAYA KAYNAKTAN DOĞRULANMIŞ 1. SORU GELECEK.",
    options: [
      "A seçeneği",
      "B seçeneği",
      "C seçeneği",
      "D seçeneği",
      "E seçeneği"
    ],
    correct: 0,
    explanation: "Buraya kaynak hükmüne dayalı açıklama gelecek.",
    sources: [
      {
        file: "Kaynak Dosya.pdf",
        page: null,
        article: null,
        paragraph: null,
        clause: null
      }
    ],
    mainArea: "Örnek Ana Alan",
    category: "Örnek Konu",
    sourcePool: "Örnek Kaynak",
    skill: "Bilgi",
    difficulty: "Normal"
  },
  {
    id: 2,
    question: "BURAYA KAYNAKTAN DOĞRULANMIŞ 2. SORU GELECEK.",
    options: [
      "A seçeneği",
      "B seçeneği",
      "C seçeneği",
      "D seçeneği",
      "E seçeneği"
    ],
    correct: 1,
    explanation: "Buraya ikinci sorunun kaynak açıklaması gelecek.",
    sources: [
      {
        file: "Kaynak Dosya.pdf",
        page: null,
        article: null,
        paragraph: null,
        clause: null
      }
    ],
    mainArea: "Örnek Ana Alan",
    category: "Örnek Konu",
    sourcePool: "Örnek Kaynak",
    skill: "Bilgi",
    difficulty: "Normal"
  },
  {
    id: 3,
    question: "BURAYA KAYNAKTAN DOĞRULANMIŞ 3. SORU GELECEK.",
    options: [
      "A seçeneği",
      "B seçeneği",
      "C seçeneği",
      "D seçeneği",
      "E seçeneği"
    ],
    correct: 2,
    explanation: "Buraya üçüncü sorunun kaynak açıklaması gelecek.",
    sources: [
      {
        file: "Kaynak Dosya.pdf",
        page: null,
        article: null,
        paragraph: null,
        clause: null
      }
    ],
    mainArea: "Örnek Ana Alan",
    category: "Örnek Konu",
    sourcePool: "Örnek Kaynak",
    skill: "Bilgi",
    difficulty: "Normal"
  }
];

const LETTERS = ["A","B","C","D","E"];
const storageKey = "PTT_EXAM_" + EXAM.id;

let state = {
  current: 0,
  answers: Array(QUESTIONS.length).fill(null),
  review: Array(QUESTIONS.length).fill(false),
  locked: Array(QUESTIONS.length).fill(false),
  startedAt: null,
  endsAt: null,
  submitted: false,
  submittedAt: null
};

function loadState(){
  try{
    const raw = localStorage.getItem(storageKey);
    if(raw){
      const parsed = JSON.parse(raw);
      if(parsed.answers?.length === QUESTIONS.length){
        state = {...state, ...parsed};
      }
    }
  }catch(e){}
}

function saveState(){
  localStorage.setItem(storageKey, JSON.stringify(state));
}

function initTiming(){
  if(!state.startedAt){
    state.startedAt = Date.now();
    state.endsAt = state.startedAt + EXAM.durationMinutes * 60 * 1000;
    saveState();
  }
}

function formatTime(ms){
  ms = Math.max(0, ms);
  const total = Math.floor(ms/1000);
  const m = Math.floor(total/60);
  const s = total%60;
  return String(m).padStart(2,"0")+":"+String(s).padStart(2,"0");
}

function renderHeader(){
  document.getElementById("examTitle").textContent = EXAM.title;

  const modeLabel =
    EXAM.mode === "real" ? "Gerçek Sınav Simülasyonu" :
    EXAM.mode === "adaptive" ? "Adaptif Çalışma Sınavı" :
    "Çalışma Sınavı";

  document.getElementById("examMeta").textContent =
    `${modeLabel} • ${QUESTIONS.length} Soru • ${EXAM.durationMinutes} Dakika` +
    (EXAM.mode === "real" ? " • Yanlışlar doğruları götürmez" : "");

  const answered = state.answers.filter(x => x !== null).length;
  document.getElementById("progressText").textContent =
    `${answered} / ${QUESTIONS.length} soru cevaplandı`;

  document.getElementById("progressBar").style.width =
    `${(answered/QUESTIONS.length)*100}%`;
}

function renderNav(){
  const nav = document.getElementById("navGrid");
  nav.innerHTML = "";

  QUESTIONS.forEach((q,i)=>{
    const b = document.createElement("button");
    b.className = "nav-btn";
    if(i === state.current) b.classList.add("current");
    if(state.answers[i] !== null) b.classList.add("answered");
    if(state.review[i]) b.classList.add("review");
    b.textContent = i+1;
    b.onclick = ()=>{state.current=i;saveState();render();};
    nav.appendChild(b);
  });
}

function sourceHtml(q){
  if(!q.sources || !q.sources.length) return "";

  return q.sources.map((s,idx)=>{
    const lines = [];
    if(s.file) lines.push(`<strong>Kaynak${q.sources.length>1 ? " "+(idx+1) : ""}:</strong> ${escapeHtml(s.file)}`);
    if(s.page) lines.push(`<strong>PDF Sayfası:</strong> ${escapeHtml(String(s.page))}`);
    if(s.article) lines.push(`<strong>Madde:</strong> ${escapeHtml(String(s.article))}`);
    if(s.paragraph) lines.push(`<strong>Fıkra:</strong> ${escapeHtml(String(s.paragraph))}`);
    if(s.clause) lines.push(`<strong>Bent:</strong> ${escapeHtml(String(s.clause))}`);
    return lines.join("<br>");
  }).join("<br><br>");
}

function renderQuestion(){
  const q = QUESTIONS[state.current];

  document.getElementById("questionNumber").textContent =
    `SORU ${state.current+1} / ${QUESTIONS.length}`;

  document.getElementById("questionText").textContent = q.question;

  const box = document.getElementById("options");
  box.innerHTML = "";

  q.options.forEach((text,idx)=>{
    const btn = document.createElement("button");
    btn.className = "option";

    if(state.answers[state.current] === idx) btn.classList.add("selected");

    if(EXAM.mode !== "real" && state.locked[state.current]){
      if(idx === q.correct) btn.classList.add("correct");
      if(state.answers[state.current] === idx && idx !== q.correct){
        btn.classList.add("wrong");
      }
    }

    btn.innerHTML =
      `<span class="option-letter">${LETTERS[idx]}</span>`+
      `<span>${escapeHtml(text)}</span>`;

    btn.disabled = EXAM.mode !== "real" && state.locked[state.current];
    btn.onclick = ()=>answer(idx);
    box.appendChild(btn);
  });

  renderFeedback();

  document.getElementById("prevBtn").disabled = state.current === 0;
  document.getElementById("nextBtn").textContent =
    state.current === QUESTIONS.length-1 ? "Son Soru" : "Sonraki →";

  document.getElementById("reviewBtn").textContent =
    state.review[state.current] ? "★ Tekrar Bak İşaretli" : "☆ Tekrar Bak";

  document.getElementById("clearBtn").classList.toggle(
    "hidden",
    EXAM.mode !== "real" && state.locked[state.current]
  );
}

function answer(idx){
  const i = state.current;
  if(EXAM.mode !== "real" && state.locked[i]) return;

  state.answers[i] = idx;

  if(EXAM.mode === "study" || EXAM.mode === "adaptive"){
    state.locked[i] = true;
  }

  saveState();
  render();

  // Adaptif mod burada YENİ SORU ÜRETMEZ.
  // Gelişmiş kullanımda önceden doğrulanmış büyük bir havuzdan
  // q.category / q.skill etiketlerine göre sonraki soru sırası seçilebilir.
}

function renderFeedback(){
  const fb = document.getElementById("feedback");
  const q = QUESTIONS[state.current];

  if(EXAM.mode === "real" || !state.locked[state.current]){
    fb.className = "feedback";
    fb.innerHTML = "";
    return;
  }

  const selected = state.answers[state.current];
  const good = selected === q.correct;

  fb.className = "feedback show " + (good ? "good" : "bad");

  fb.innerHTML = `
    <strong>${good ? "✅ DOĞRU" : "❌ YANLIŞ"}</strong>
    ${good ? "" : `
      <div style="margin-top:8px">
        <strong>Senin cevabın:</strong> ${LETTERS[selected]}<br>
        <strong>Doğru cevap:</strong> ${LETTERS[q.correct]}
      </div>
    `}
    <div style="margin-top:10px">
      <strong>Açıklama:</strong><br>
      ${escapeHtml(q.explanation || "Açıklama eklenmemiş.")}
    </div>
    <div class="source-box">${sourceHtml(q)}</div>
  `;
}

function render(){
  if(state.submitted){
    showResult();
    return;
  }
  renderHeader();
  renderNav();
  renderQuestion();
}

function go(delta){
  state.current = Math.max(0, Math.min(QUESTIONS.length-1, state.current+delta));
  saveState();
  render();
}

function toggleReview(){
  state.review[state.current] = !state.review[state.current];
  saveState();
  render();
}

function clearAnswer(){
  if(EXAM.mode !== "real" && state.locked[state.current]) return;
  state.answers[state.current] = null;
  saveState();
  render();
}

function submitExam(auto=false){
  if(state.submitted) return;

  const blanks = state.answers.filter(x=>x===null).length;

  if(!auto){
    const msg =
      `Sınavı teslim etmek istediğinize emin misiniz?`+
      (blanks ? `\n\n${blanks} adet cevaplanmamış sorunuz bulunmaktadır.` : "");
    if(!confirm(msg)) return;
  }

  state.submitted = true;
  state.submittedAt = Date.now();
  saveState();
  showResult();
}

function getStats(){
  let correct=0, wrong=0, blank=0;

  QUESTIONS.forEach((q,i)=>{
    const a = state.answers[i];
    if(a === null) blank++;
    else if(a === q.correct) correct++;
    else wrong++;
  });

  const score = QUESTIONS.length
    ? Math.round((correct/QUESTIONS.length)*10000)/100
    : 0;

  return {correct,wrong,blank,score};
}

function usedTime(){
  const end = state.submittedAt || Date.now();
  return formatTime(end - state.startedAt);
}

function showResult(){
  document.getElementById("examView").classList.add("hidden");
  document.querySelector(".topbar").classList.add("hidden");

  const result = document.getElementById("resultView");
  result.classList.add("show");

  const s = getStats();
  const sg = document.getElementById("scoreGrid");

  sg.innerHTML = `
    <div class="stat"><span>Puan</span><strong>${s.score}</strong></div>
    <div class="stat"><span>Doğru</span><strong>${s.correct}</strong></div>
    <div class="stat"><span>Yanlış</span><strong>${s.wrong}</strong></div>
    <div class="stat"><span>Boş</span><strong>${s.blank}</strong></div>
    <div class="stat"><span>Süre</span><strong style="font-size:19px">${usedTime()}</strong></div>
  `;

  renderTopicAnalysis();
  renderReviews();
}

function renderTopicAnalysis(){
  const map = {};

  QUESTIONS.forEach((q,i)=>{
    const key = q.mainArea || q.category || "Diğer";
    if(!map[key]) map[key]={total:0,correct:0,wrong:0,blank:0};
    map[key].total++;

    const a=state.answers[i];
    if(a===null) map[key].blank++;
    else if(a===q.correct) map[key].correct++;
    else map[key].wrong++;
  });

  let rows="";
  Object.entries(map).forEach(([name,x])=>{
    const pct = x.total ? Math.round((x.correct/x.total)*100) : 0;
    rows += `
      <tr>
        <td>${escapeHtml(name)}</td>
        <td>${x.total}</td>
        <td>${x.correct}</td>
        <td>${x.wrong}</td>
        <td>${x.blank}</td>
        <td>%${pct}</td>
      </tr>
    `;
  });

  document.getElementById("topicAnalysis").innerHTML = `
    <h3>Ana Alan Performansı</h3>
    <div style="overflow:auto">
      <table style="width:100%;border-collapse:collapse">
        <thead>
          <tr>
            <th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Ana Alan</th>
            <th>Soru</th><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Başarı</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function reviewHtml(q,i){
  const a = state.answers[i];
  const status =
    a===null ? "BOŞ" :
    a===q.correct ? "DOĞRU" : "YANLIŞ";

  return `
    <div class="review-card">
      <h4>Soru ${i+1} — ${status}</h4>
      <div>${escapeHtml(q.question)}</div>
      <div style="margin-top:10px">
        <strong>Senin cevabın:</strong>
        ${a===null ? "Cevaplanmadı" : LETTERS[a]+" — "+escapeHtml(q.options[a])}
        <br>
        <strong>Doğru cevap:</strong>
        ${LETTERS[q.correct]} — ${escapeHtml(q.options[q.correct])}
      </div>
      <div style="margin-top:10px">
        <strong>Açıklama:</strong><br>
        ${escapeHtml(q.explanation || "")}
      </div>
      <div class="source-box">${sourceHtml(q)}</div>
      <div style="margin-top:10px">
        ${q.mainArea ? `<span class="tag">${escapeHtml(q.mainArea)}</span>` : ""}
        ${q.category ? `<span class="tag">${escapeHtml(q.category)}</span>` : ""}
        ${q.skill ? `<span class="tag">${escapeHtml(q.skill)}</span>` : ""}
        ${q.difficulty ? `<span class="tag">${escapeHtml(q.difficulty)}</span>` : ""}
      </div>
    </div>
  `;
}

function renderReviews(){
  let wrong="";
  let all="";

  QUESTIONS.forEach((q,i)=>{
    const block = reviewHtml(q,i);
    all += block;

    if(state.answers[i]===null || state.answers[i]!==q.correct){
      wrong += block;
    }
  });

  document.getElementById("wrongList").innerHTML =
    wrong || `<div class="small">Yanlış veya boş soru bulunmuyor.</div>`;

  document.getElementById("allReview").innerHTML = all;
}

function escapeHtml(value){
  return String(value ?? "")
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;")
    .replaceAll('"',"&quot;")
    .replaceAll("'","&#039;");
}

function tick(){
  if(state.submitted) return;

  const timer = document.getElementById("timer");

  if(EXAM.durationMinutes <= 0){
    timer.textContent = "SÜRESİZ";
    return;
  }

  const left = state.endsAt - Date.now();
  timer.textContent = formatTime(left);

  if(left <= 0){
    submitExam(true);
  }
}

document.getElementById("prevBtn").addEventListener("click",()=>go(-1));
document.getElementById("nextBtn").addEventListener("click",()=>go(1));
document.getElementById("reviewBtn").addEventListener("click",toggleReview);
document.getElementById("clearBtn").addEventListener("click",clearAnswer);
document.getElementById("submitBtn").addEventListener("click",()=>submitExam(false));

document.getElementById("resetBtn").addEventListener("click",()=>{
  if(confirm("Bu sınavın tüm kayıtları silinsin ve yeniden başlatılsın mı?")){
    localStorage.removeItem(storageKey);
    location.reload();
  }
});

loadState();
initTiming();
render();
tick();
setInterval(tick,1000);
</script>
</body>
</html>
```

---

# BOT İÇİN SON KONTROL

HTML kullanıcıya teslim edilmeden önce:

- [ ] Soru sayısı doğru mu?
- [ ] Her soruda 5 şık var mı?
- [ ] Her soruda tek doğru cevap var mı?
- [ ] Doğru cevap gerçekten kaynakta mı?
- [ ] Kaynak referansı doğru soruya mı bağlı?
- [ ] Gerçek sınavsa `00_SINAV_DAGILIMI.md` dağılımları uygulandı mı?
- [ ] Şık seçme çalışıyor mu?
- [ ] Önceki / sonraki çalışıyor mu?
- [ ] `Tekrar Bak` çalışıyor mu?
- [ ] `Cevabı Temizle` gerçek sınavda çalışıyor mu?
- [ ] `SINAVI TESLİM ET` çalışıyor mu?
- [ ] Boş soru uyarısı çalışıyor mu?
- [ ] Sonuç hesabı doğru mu?
- [ ] Süre dolunca otomatik teslim oluyor mu?
- [ ] Sayfa yenilenince süre korunuyor mu?
- [ ] Türkçe karakterler doğru mu?
- [ ] Sonuç ekranında yanlış ve boş soruların kaynakları görünüyor mu?

## Değişmez felsefe

> **Soru dağılımını dağılım MD'si belirler.**  
> **Soru içeriğini gerçek kaynak belirler.**  
> **Doğru cevabı gerçek kaynak belirler.**  
> **HTML yalnızca doğrulanmış sınavı uygular.**  
> **Kaynak yoksa soru yok.**
