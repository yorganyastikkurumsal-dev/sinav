from __future__ import annotations

import hashlib
import html
import json
import math
import random
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

from pypdf import PdfReader

ROOT = Path.cwd()
OUTPUT = ROOT / "generated_learning_exams"
TARGET_PER_AREA = 100

AREAS = [
    ("PTT ile İlgili Genel Mevzuat", "01_PTT_ile_Ilgili_Genel_Mevzuat_100_Soru.html"),
    ("Posta - Kargo - Elektronik Posta ve Regülasyon", "02_Posta_Kargo_Elektronik_Posta_Regulasyon_100_Soru.html"),
    ("PTTBank - Ödeme Sistemleri - Finansal Hizmetler", "03_PTTBank_Odeme_Sistemleri_Finansal_Hizmetler_100_Soru.html"),
    ("İnsan Kaynakları - İSG", "04_Insan_Kaynaklari_ISG_100_Soru.html"),
    ("Finans - Muhasebe", "05_Finans_Muhasebe_100_Soru.html"),
    ("Satınalma - Destek", "06_Satinalma_Destek_100_Soru.html"),
    ("Yapı - İş Yerleri", "07_Yapi_Is_Yerleri_100_Soru.html"),
    ("Bilgi Teknolojileri ve Güvenliği - Bilişim", "08_Bilgi_Teknolojileri_Guvenligi_Bilisim_100_Soru.html"),
    ("Diğer Önemli Operasyonel Alanlar", "09_Diger_Onemli_Operasyonel_Alanlar_100_Soru.html"),
    ("Genel İlgili Mevzuat", "10_Genel_Ilgili_Mevzuat_100_Soru.html"),
]

SKIP_PHRASES = [
    "Bu dokümanın güncelliği",
    "Basılı kopyalar",
    "Dokümanın Adı",
    "Erişilebilirlik Derecesi",
    "İlk Yayım Tarihi",
    "Revizyon Tarihi",
    "Revizyon No",
    "Sayfa Sayısı",
    "Hazırlayan Birim Onayı",
    "EYS Onayı",
    "Kontrol Onayı",
    "Yürürlük Onayı",
    "Yayımlandığı Resmî Gazete",
    "Yayımlandığı Düstur",
    "Kanun Numarası",
    "Kabul Tarihi",
    "Karar Sayısı",
]

PAGE_MARKER = re.compile(r"=+\s*SAYFA\s+(\d+)\s*=+", re.I)
NUMBER_PATTERN = re.compile(
    r"(?<![\w./])"
    r"(?P<prefix>yılda en az|ayda en az|en az|en çok|azami|asgari|yaklaşık|her)?\s*"
    r"(?P<num>\d+(?:[.,]\d+)?)"
    r"(?:\s*(?P<unit>iş günü|takvim günü|gün|ay|yıl|saat|dakika|hafta|defa|kez|kişi|adet|işçi|personel|puan|soru|oranında|yüzde|%|TL|Türk lirası|kilogram|kg|gram|metre|cm|mm|m²|m3|desimetreküp|günlük|aylık|yıllık))?",
    re.I,
)


def stable_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def clean_text(value: str) -> str:
    value = value.replace("\ufeff", "")
    value = re.sub(r"[\u00ad\u200b\u200c\u200d]", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    return value


def normalized_tokens(value: str) -> list[str]:
    value = unicodedata.normalize("NFKD", value.casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return [x for x in re.findall(r"[a-z0-9]+", value) if len(x) >= 4]


def parse_pages(path: Path) -> list[tuple[int | None, str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    parts = PAGE_MARKER.split(text)
    if len(parts) == 1:
        return [(None, text)]
    pages: list[tuple[int | None, str]] = []
    for i in range(1, len(parts), 2):
        pages.append((int(parts[i]), parts[i + 1]))
    return pages


def sentence_split(page_text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in page_text.splitlines():
        line = clean_text(raw_line)
        if not line:
            continue
        if any(part.casefold() in line.casefold() for part in SKIP_PHRASES):
            continue
        if re.fullmatch(r"\d+(?:/\d+)?", line):
            continue
        lines.append(line)
    text = clean_text(" ".join(lines))
    sentences = re.split(r"(?<=[.!?])\s+(?=(?:[A-ZÇĞİÖŞÜ0-9“\"(]))", text)
    return [clean_text(item) for item in sentences if clean_text(item)]


def useful_sentence(sentence: str) -> bool:
    if len(sentence) < 45 or len(sentence) > 390:
        return False
    if sum(char.isalpha() for char in sentence) < 25:
        return False
    if any(part.casefold() in sentence.casefold() for part in SKIP_PHRASES):
        return False
    if sentence.count("(") > 6 or sentence.count(")") > 6:
        return False
    if re.search(r"_{3,}|-{5,}", sentence):
        return False
    if sentence.casefold().startswith(("not:", "dipnot", "ek-")):
        return False
    if sentence.count("md.") >= 2 or sentence.count("KHK") >= 3:
        return False
    if len(sentence.split()) < 7 and not re.search(r"\d", sentence):
        return False
    return True


def parse_facts(path: Path) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for page, content in parse_pages(path):
        for sentence in sentence_split(content):
            if useful_sentence(sentence):
                facts.append({"sentence": sentence, "page": page})
    return facts


def extract_definitions(source: str, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for fact in facts:
        sentence = fact["sentence"]
        matches: list[tuple[str, str]] = []
        colon = re.match(r"^(?:\d+(?:\.\d+)*\s*)?([^:]{2,90}):\s*(.{25,320})$", sentence)
        if colon:
            matches.append((colon.group(1), colon.group(2)))
        comma = re.match(
            r"^(?:\d+(?:\.\d+)*\s*)?([A-ZÇĞİÖŞÜ][^,]{1,70}),\s+(.{25,320}?\bifade eder\.?)$",
            sentence,
            re.I,
        )
        if comma:
            matches.append((comma.group(1), comma.group(2)))

        for raw_term, raw_definition in matches:
            term = clean_text(raw_term)
            term = re.sub(r"^.*?\b\d+(?:\.\d+)+\s*", "", term)
            term = term.strip(" .-–—“”\"")
            definition = clean_text(raw_definition)
            if not 1 <= len(term.split()) <= 8:
                continue
            if not 2 <= len(term) <= 72:
                continue
            if re.search(r"\b(RG|Ek|Değişik|Mülga|fıkra|bent|madde)\b", term, re.I):
                continue
            if term.startswith("(") or term.endswith(")"):
                continue
            if sum(ch.isdigit() for ch in term) > 2:
                continue
            if ":" in term or ";" in term:
                continue
            if len(definition) < 25 or len(definition) > 290:
                continue
            if definition.count("(") > 3:
                continue
            simple_term = re.sub(r"\([^)]*\)", "", term).strip().casefold()
            if len(simple_term) > 4 and simple_term in definition.casefold():
                continue
            score = 50
            if re.search(r"ifade eder|ifade etmektedir", definition, re.I):
                score += 20
            if len(definition) <= 190:
                score += 10
            output.append(
                {
                    "kind": "definition",
                    "source": source,
                    "page": fact["page"],
                    "support": sentence,
                    "term": term,
                    "definition": definition,
                    "score": score,
                }
            )
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for item in output:
        key = (item["source"].casefold(), item["term"].casefold())
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def bad_number_match(sentence: str, match: re.Match[str]) -> bool:
    value = float(match.group("num").replace(",", "."))
    unit = (match.group("unit") or "").casefold()
    prefix = (match.group("prefix") or "").casefold()
    before = sentence[max(0, match.start() - 18) : match.start()].casefold()
    around = sentence[max(0, match.start() - 2) : match.end() + 3]
    if "/" in around:
        return True
    if re.search(r"(madde|fıkra|bent|no|numarası|tarih|sayılı)\s*$", before):
        return True
    if not unit and not prefix:
        return True
    if 1900 <= value <= 2100 and unit in {"yıl", ""}:
        return True
    return False


def extract_numbers(source: str, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for fact in facts:
        sentence = fact["sentence"]
        if len(sentence) > 310:
            continue
        if "RG-" in sentence or "RG -" in sentence:
            continue
        for match in NUMBER_PATTERN.finditer(sentence):
            if bad_number_match(sentence, match):
                continue
            answer = clean_text(match.group(0))
            if not answer or len(answer) > 36:
                continue
            score = 55
            if match.group("unit"):
                score += 15
            if match.group("prefix"):
                score += 10
            output.append(
                {
                    "kind": "numeric",
                    "source": source,
                    "page": fact["page"],
                    "support": sentence,
                    "answer": answer,
                    "prefix": clean_text(match.group("prefix") or ""),
                    "number": match.group("num"),
                    "unit": clean_text(match.group("unit") or ""),
                    "span": match.span(),
                    "score": score,
                }
            )
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict[str, Any]] = []
    for item in output:
        key = (item["source"].casefold(), item["support"].casefold(), item["answer"].casefold())
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def extract_source_statements(source: str, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for fact in facts:
        sentence = fact["sentence"]
        if len(sentence) < 65 or len(sentence) > 245:
            continue
        if sentence.count("(") > 2:
            continue
        if re.search(r"\b(RG|Mülga|Değişik|Ek fıkra|KHK-)\b", sentence, re.I):
            continue
        if not re.search(
            r"(zorundadır|yükümlüdür|yapılır|uygulanır|sağlanır|belirlenir|sorumludur|yetkilidir|kapsar|ifade eder|edilir|olmalıdır|gerçekleştirilir|hazırlanır|bildirilir)",
            sentence,
            re.I,
        ):
            continue
        score = 45
        if 85 <= len(sentence) <= 190:
            score += 15
        output.append(
            {
                "kind": "source",
                "source": source,
                "page": fact["page"],
                "support": sentence,
                "score": score,
            }
        )
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in output:
        key = item["support"].casefold()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


class PdfVerifier:
    def __init__(self, area_dir: Path):
        self.area_dir = area_dir
        self.cache: dict[Path, list[str]] = {}

    def pages(self, pdf_path: Path) -> list[str]:
        if pdf_path in self.cache:
            return self.cache[pdf_path]
        try:
            reader = PdfReader(str(pdf_path))
            pages = [page.extract_text() or "" for page in reader.pages]
        except Exception as exc:
            print(f"PDF okunamadı: {pdf_path} -> {exc}")
            pages = []
        self.cache[pdf_path] = pages
        return pages

    @staticmethod
    def overlap(support: str, page_text: str) -> float:
        wanted = list(dict.fromkeys(normalized_tokens(support)))[:45]
        if not wanted:
            return 0.0
        present = set(normalized_tokens(page_text))
        return sum(token in present for token in wanted) / len(wanted)

    def verify(self, txt_path: Path, support: str, page: int | None) -> tuple[bool, int | None]:
        pdf_path = txt_path.with_suffix(".pdf")
        if not pdf_path.exists():
            return False, page
        pages = self.pages(pdf_path)
        if not pages:
            return False, page
        if page and 1 <= page <= len(pages):
            if self.overlap(support, pages[page - 1]) >= 0.42:
                return True, page
        best_score = 0.0
        best_page: int | None = None
        for index, page_text in enumerate(pages, start=1):
            score = self.overlap(support, page_text)
            if score > best_score:
                best_score = score
                best_page = index
        return best_score >= 0.50, best_page


def numeric_options(candidate: dict[str, Any]) -> list[str]:
    number_text = candidate["number"]
    number = float(number_text.replace(",", "."))
    prefix = candidate["prefix"]
    unit = candidate["unit"]

    if number.is_integer():
        integer = int(number)
        values = [
            max(1, integer - 1),
            integer + 1,
            max(1, integer // 2),
            integer * 2,
            integer + (5 if integer >= 5 else 2),
            max(1, integer - (5 if integer >= 10 else 2)),
        ]
    else:
        values = [max(0.01, number - 0.5), number + 0.5, number * 2, max(0.01, number / 2), number + 1]

    def render(value: float) -> str:
        if float(value).is_integer():
            core = str(int(value))
        else:
            core = (f"{value:.2f}".rstrip("0").rstrip(".")).replace(".", ",")
        return clean_text(" ".join(part for part in [prefix, core, unit] if part))

    correct = candidate["answer"]
    choices = [correct]
    for value in values:
        option = render(value)
        if option.casefold() != correct.casefold() and option not in choices:
            choices.append(option)
        if len(choices) == 5:
            break
    while len(choices) < 5:
        extra = render(number + len(choices) + 2)
        if extra not in choices:
            choices.append(extra)
    return choices


def shuffle_options(options: list[str], correct_value: str, rng: random.Random) -> tuple[list[str], int]:
    options = list(dict.fromkeys(options))
    if len(options) != 5:
        raise ValueError(f"Beş benzersiz seçenek üretilemedi: {options}")
    rng.shuffle(options)
    return options, options.index(correct_value)


def interleave(groups: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    queues = {key: sorted(value, key=lambda item: (-item["score"], len(item["support"]))) for key, value in groups.items()}
    order = ["definition", "numeric", "source"]
    output: list[dict[str, Any]] = []
    while any(queues.get(key) for key in order):
        for key in order:
            if queues.get(key):
                output.append(queues[key].pop(0))
    return output


def build_question(
    candidate: dict[str, Any],
    area: str,
    definitions: list[dict[str, Any]],
    source_names: list[str],
    rng: random.Random,
) -> dict[str, Any] | None:
    kind = candidate["kind"]
    source = candidate["source"]
    support = candidate["support"]
    if kind == "definition":
        correct_value = candidate["term"]
        same_source = [
            item["term"]
            for item in definitions
            if item["source"] == source and item["term"].casefold() != correct_value.casefold()
        ]
        area_terms = [
            item["term"]
            for item in definitions
            if item["term"].casefold() != correct_value.casefold()
        ]
        pool = list(dict.fromkeys(same_source + area_terms))
        rng.shuffle(pool)
        distractors = []
        for term in pool:
            if term.casefold() != correct_value.casefold() and term not in distractors:
                distractors.append(term)
            if len(distractors) == 4:
                break
        if len(distractors) < 4:
            return None
        options, correct = shuffle_options([correct_value] + distractors, correct_value, rng)
        question = f'“{candidate["definition"]}” ifadesi aşağıdaki kavramlardan hangisini tanımlar?'
        explanation = f'{correct_value}: {candidate["definition"]}'
        category = "Tanım"
        difficulty = "Normal"
    elif kind == "numeric":
        choices = numeric_options(candidate)
        correct_value = candidate["answer"]
        options, correct = shuffle_options(choices, correct_value, rng)
        start, end = candidate["span"]
        masked = support[:start] + "[ … ]" + support[end:]
        question = f'{source} kaynağındaki aşağıdaki hükümde boş bırakılan yere hangisi gelmelidir?\n“{masked}”'
        explanation = f"Kaynak hükmü: {support}"
        category = "Süre / Sayı / Limit"
        difficulty = "Zor"
    else:
        if len(source_names) < 5:
            return None
        pool = [name for name in source_names if name != source]
        rng.shuffle(pool)
        correct_value = source
        options, correct = shuffle_options([correct_value] + pool[:4], correct_value, rng)
        question = f'Aşağıdaki hüküm hangi repo kaynağında yer almaktadır?\n“{support}”'
        explanation = f"Bu hüküm {source} kaynağında yer almaktadır."
        category = "Kaynak Eşleştirme"
        difficulty = "Normal"

    return {
        "question": question,
        "options": options,
        "correct": correct,
        "explanation": explanation,
        "support": support,
        "source": source + ".pdf",
        "page": candidate.get("page"),
        "mainArea": area,
        "sourcePool": source,
        "category": category,
        "difficulty": difficulty,
        "kind": kind,
    }


def generate_area_questions(area: str, area_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(stable_seed(area))
    verifier = PdfVerifier(area_dir)
    source_records: list[dict[str, Any]] = []

    for txt_path in sorted(area_dir.glob("*.txt"), key=lambda path: path.name.casefold()):
        if txt_path.name.startswith("00_"):
            continue
        pdf_path = txt_path.with_suffix(".pdf")
        if not pdf_path.exists():
            print(f"PDF çifti bulunamadı, kaynak atlandı: {txt_path}")
            continue
        source = txt_path.stem
        facts = parse_facts(txt_path)
        definitions = extract_definitions(source, facts)
        numbers = extract_numbers(source, facts)
        statements = extract_source_statements(source, facts)
        source_records.append(
            {
                "source": source,
                "txt": txt_path,
                "facts": facts,
                "definitions": definitions,
                "numbers": numbers,
                "statements": statements,
            }
        )

    source_names = [record["source"] for record in source_records]
    all_definitions = [item for record in source_records for item in record["definitions"]]
    if len(source_names) < 5:
        raise RuntimeError(f"{area}: en az beş kaynak gerekli")

    usable_records = [
        record
        for record in source_records
        if record["definitions"] or record["numbers"] or record["statements"]
    ]
    if not usable_records:
        raise RuntimeError(f"{area}: soru üretilebilecek kaynak bulunamadı")

    base = TARGET_PER_AREA // len(usable_records)
    remainder = TARGET_PER_AREA % len(usable_records)
    targets = {
        record["source"]: base + (1 if index < remainder else 0)
        for index, record in enumerate(usable_records)
    }

    selected: list[dict[str, Any]] = []
    used_support: set[tuple[str, str]] = set()
    rejected_pdf = 0
    candidate_queues: dict[str, list[dict[str, Any]]] = {}
    source_path = {record["source"]: record["txt"] for record in usable_records}

    for record in usable_records:
        groups = {
            "definition": record["definitions"],
            "numeric": record["numbers"],
            "source": record["statements"],
        }
        candidate_queues[record["source"]] = interleave(groups)

    def take_from(source: str) -> dict[str, Any] | None:
        nonlocal rejected_pdf
        queue = candidate_queues[source]
        while queue:
            candidate = queue.pop(0)
            key = (source.casefold(), candidate["support"].casefold())
            if key in used_support:
                continue
            verified, actual_page = verifier.verify(
                source_path[source], candidate["support"], candidate.get("page")
            )
            if not verified:
                rejected_pdf += 1
                continue
            candidate = dict(candidate)
            candidate["page"] = actual_page
            question = build_question(candidate, area, all_definitions, source_names, rng)
            if not question:
                continue
            used_support.add(key)
            return question
        return None

    for record in usable_records:
        source = record["source"]
        for _ in range(targets[source]):
            question = take_from(source)
            if question:
                selected.append(question)
            else:
                break

    while len(selected) < TARGET_PER_AREA:
        progress = False
        ordered_sources = sorted(
            usable_records,
            key=lambda record: len(candidate_queues[record["source"]]),
            reverse=True,
        )
        for record in ordered_sources:
            if len(selected) >= TARGET_PER_AREA:
                break
            question = take_from(record["source"])
            if question:
                selected.append(question)
                progress = True
        if not progress:
            break

    if len(selected) < TARGET_PER_AREA:
        raise RuntimeError(
            f"{area}: PDF doğrulamasından sonra yalnızca {len(selected)} soru üretilebildi"
        )

    selected = selected[:TARGET_PER_AREA]
    rng.shuffle(selected)
    for index, question in enumerate(selected, start=1):
        question["id"] = index

    source_counts = defaultdict(int)
    type_counts = defaultdict(int)
    for question in selected:
        source_counts[question["sourcePool"]] += 1
        type_counts[question["kind"]] += 1

    report = {
        "area": area,
        "questions": len(selected),
        "sources_in_folder": len(source_records),
        "sources_used": len(source_counts),
        "source_counts": dict(sorted(source_counts.items())),
        "type_counts": dict(type_counts),
        "pdf_rejections": rejected_pdf,
    }
    return selected, report


def exam_html(area: str, questions: list[dict[str, Any]], storage_slug: str) -> str:
    data = json.dumps(questions, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    title = html.escape(area)
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#07111f">
<title>{title} — 100 Soruluk Çalışma Sınavı</title>
<style>
:root{{--bg:#07111f;--panel:#0e1d30;--panel2:#142941;--line:#294861;--text:#eff7ff;--muted:#a9bdd0;--accent:#27c8b9;--ok:#43d17f;--bad:#ff6b6b;--warn:#f4b860;--shadow:0 18px 48px rgba(0,0,0,.36)}}
*{{box-sizing:border-box}}html{{width:100%;overflow-x:hidden;-webkit-text-size-adjust:100%;scroll-behavior:smooth}}body{{margin:0;width:100%;min-height:100vh;min-height:100dvh;overflow-x:hidden;background:radial-gradient(circle at 10% 0%,rgba(39,200,185,.13),transparent 30%),var(--bg);color:var(--text);font-family:Inter,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;line-height:1.5}}button{{font:inherit;cursor:pointer;touch-action:manipulation;-webkit-tap-highlight-color:transparent}}button:focus-visible,a:focus-visible{{outline:3px solid rgba(39,200,185,.7);outline-offset:2px}}.hidden{{display:none!important}}.shell{{width:min(1400px,100%);margin:auto;padding:clamp(10px,2vw,20px)}}.card{{background:linear-gradient(180deg,rgba(20,41,65,.98),rgba(14,29,48,.98));border:1px solid rgba(77,112,145,.45);border-radius:18px;box-shadow:var(--shadow)}}.top{{position:sticky;top:0;z-index:40;background:rgba(7,17,31,.94);backdrop-filter:blur(15px);border-bottom:1px solid rgba(77,112,145,.4);padding-top:env(safe-area-inset-top)}}.topin{{width:min(1400px,100%);margin:auto;padding:10px 18px;display:flex;align-items:center;gap:14px}}.brand{{min-width:0;flex:1}}.brand b{{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.brand span{{font-size:.76rem;color:var(--muted)}}.elapsed{{font-weight:900;font-variant-numeric:tabular-nums;padding:8px 12px;background:var(--panel);border:1px solid var(--line);border-radius:12px}}.progressbox{{min-width:180px}}.progresslabel{{font-size:.72rem;color:var(--muted);text-align:right;margin-bottom:4px}}.progress{{height:7px;background:#13263b;border-radius:99px;overflow:hidden}}.progress i{{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--accent),#62e1d7);transition:.2s}}.start{{width:min(900px,100%);margin:5vh auto;padding:clamp(25px,5vw,55px);text-align:center}}.pill{{display:inline-block;padding:6px 11px;border-radius:99px;background:rgba(39,200,185,.13);color:#7aeee5;font-weight:900;font-size:.78rem}}h1{{font-size:clamp(1.9rem,5vw,3.5rem);line-height:1.07;letter-spacing:-1px;margin:16px 0}}.lead{{color:var(--muted);font-size:1rem;max-width:720px;margin:0 auto 24px}}.stats{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:24px 0}}.stat{{flex:1 1 150px;max-width:210px;padding:16px;background:rgba(7,17,31,.55);border:1px solid var(--line);border-radius:14px}}.stat b{{display:block;font-size:1.35rem}}.stat span{{font-size:.78rem;color:var(--muted)}}.notice{{text-align:left;padding:15px 17px;border-left:4px solid var(--accent);background:rgba(39,200,185,.08);border-radius:12px;margin:20px 0}}.btn{{border:0;border-radius:13px;padding:12px 17px;font-weight:850;color:var(--text);background:var(--panel2);min-height:46px}}.btn.primary{{background:linear-gradient(135deg,var(--accent),#69e1d7);color:#031018}}.btn.danger{{background:linear-gradient(135deg,#d94c56,var(--bad))}}.btn.outline{{background:transparent;border:1px solid var(--line)}}.layout{{display:flex;align-items:flex-start;gap:20px;padding-top:18px;padding-bottom:95px}}.qcard{{flex:1 1 0;min-width:0;padding:clamp(18px,3vw,34px)}}.qmeta{{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:.85rem;margin-bottom:16px}}.qmeta b{{color:#74e8df}}.qtext{{font-size:clamp(1.08rem,2vw,1.38rem);line-height:1.48;margin:0 0 20px;white-space:pre-line;overflow-wrap:anywhere}}.options{{display:grid;gap:10px}}.option{{width:100%;min-height:58px;display:grid;grid-template-columns:42px minmax(0,1fr);align-items:center;gap:11px;text-align:left;padding:13px 14px;border-radius:13px;border:1px solid var(--line);background:rgba(7,17,31,.58);color:var(--text);overflow-wrap:anywhere}}.option:hover:not(:disabled){{border-color:#5484aa;background:#13304b}}.option .letter{{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:#17324d;color:#79e9e0;font-weight:900}}.option.chosen{{border-color:var(--accent);background:rgba(39,200,185,.11)}}.option.correct{{border-color:var(--ok);background:rgba(67,209,127,.13)}}.option.wrong{{border-color:var(--bad);background:rgba(255,107,107,.13)}}.option.correct .letter{{background:var(--ok);color:#04140b}}.option.wrong .letter{{background:var(--bad);color:#210506}}.option:disabled{{cursor:default;opacity:1}}.feedback{{margin-top:18px;padding:17px;border-radius:14px;border:1px solid var(--line);background:#0a192a}}.feedback.ok{{border-left:5px solid var(--ok)}}.feedback.bad{{border-left:5px solid var(--bad)}}.feedback h3{{margin:0 0 8px}}.feedback p{{margin:8px 0}}.source{{padding:11px;border-radius:10px;background:rgba(39,200,185,.08);color:#c5f2ee;font-size:.86rem;overflow-wrap:anywhere}}.actions{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}}.side{{flex:0 0 315px;width:315px;position:sticky;top:86px;padding:17px}}.sidehead{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}.grid{{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:6px}}.cell{{aspect-ratio:1;min-width:0;border:1px solid var(--line);border-radius:7px;background:#091827;color:var(--muted);font-size:.68rem;font-weight:850;padding:0}}.cell.done{{background:rgba(39,200,185,.2);border-color:rgba(39,200,185,.7);color:#c5f8f3}}.cell.bad{{box-shadow:inset 0 0 0 2px var(--bad)}}.cell.current{{background:var(--accent);color:#041018;transform:scale(1.08)}}.summary{{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin:14px 0}}.mini{{padding:8px 3px;text-align:center;background:#091827;border:1px solid var(--line);border-radius:10px}}.mini b{{display:block}}.mini span{{font-size:.66rem;color:var(--muted)}}.closemap,.backdrop,.dock{{display:none}}.result{{padding-top:20px;padding-bottom:60px}}.hero{{padding:27px;display:flex;align-items:center;gap:24px}}.hero>div:first-child{{flex:1}}.resultstats{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}}.rstat{{flex:1 1 110px;padding:12px;text-align:center;background:#091827;border:1px solid var(--line);border-radius:12px}}.rstat b{{display:block;font-size:1.2rem}}.rstat span{{font-size:.72rem;color:var(--muted)}}.donut{{width:155px;height:155px;border-radius:50%;display:grid;place-items:center;position:relative;background:conic-gradient(var(--ok) 0 var(--okdeg),var(--bad) var(--okdeg) var(--baddeg),var(--warn) var(--baddeg) 360deg)}}.donut:after{{content:"";position:absolute;inset:14px;border-radius:50%;background:var(--panel)}}.donut b{{position:relative;z-index:1;font-size:1.8rem}}.section{{margin-top:18px;padding:22px}}.section h2{{margin:0 0 13px;font-size:1.22rem}}.scroll{{overflow-x:auto;-webkit-overflow-scrolling:touch}}table{{width:100%;border-collapse:collapse;min-width:650px}}th,td{{padding:10px 8px;border-bottom:1px solid var(--line);font-size:.84rem;text-align:left}}th:not(:first-child),td:not(:first-child){{text-align:center}}th{{color:var(--muted)}}details{{border:1px solid var(--line);border-radius:13px;background:#091827;margin:9px 0;overflow:hidden}}summary{{cursor:pointer;padding:13px 15px;font-weight:800}}.detail{{padding:0 15px 15px}}.modalwrap{{position:fixed;inset:0;z-index:120;display:grid;place-items:center;padding:15px;background:rgba(0,0,0,.72)}}.modal{{width:min(520px,100%);padding:23px}}.modalactions{{display:flex;justify-content:flex-end;gap:9px;margin-top:18px}}
@media(max-width:1024px){{.layout{{display:block;padding-bottom:calc(92px + env(safe-area-inset-bottom))}}.side{{position:fixed;z-index:90;top:0;right:0;bottom:0;width:min(92vw,390px);height:100dvh;overflow:auto;padding:calc(15px + env(safe-area-inset-top)) 16px calc(20px + env(safe-area-inset-bottom));border-radius:19px 0 0 19px;transform:translateX(105%);transition:.22s}}body.mapopen{{overflow:hidden}}body.mapopen .side{{transform:translateX(0)}}.closemap{{display:grid;place-items:center;width:44px;height:44px;border:1px solid var(--line);border-radius:12px;background:#091827;color:white}}.backdrop{{display:block;position:fixed;inset:0;z-index:80;background:rgba(0,0,0,.65);opacity:0;pointer-events:none;border:0}}body.mapopen .backdrop{{opacity:1;pointer-events:auto}}.dock{{display:flex;position:fixed;z-index:70;left:0;right:0;bottom:0;gap:7px;padding:9px max(9px,env(safe-area-inset-right)) calc(9px + env(safe-area-inset-bottom)) max(9px,env(safe-area-inset-left));background:rgba(7,17,31,.97);border-top:1px solid var(--line)}}.dock button{{flex:1;min-width:0;min-height:52px;padding:6px;border-radius:12px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-weight:800;font-size:.72rem}}.dock .primary{{background:var(--accent);color:#041018}}.actions{{display:none}}.hero{{flex-direction:column}}.donut{{flex:0 0 auto}}}}
@media(max-width:680px){{.topin{{padding:8px 10px;flex-wrap:wrap;gap:7px}}.brand{{width:calc(100% - 95px)}}.brand span{{display:none}}.elapsed{{font-size:.9rem;padding:6px 8px}}.progressbox{{order:3;width:100%}}.progresslabel{{text-align:left}}.start{{margin:2vh auto;padding:23px 15px}}.qcard{{padding:17px 13px}}.qtext{{font-size:1.04rem}}.option{{grid-template-columns:37px minmax(0,1fr);padding:11px;font-size:.92rem}}.grid{{grid-template-columns:repeat(7,1fr);gap:7px}}.hero,.section{{padding:17px 13px}}.modalwrap{{align-items:end;padding-bottom:max(10px,env(safe-area-inset-bottom))}}.modalactions{{flex-direction:column-reverse}}.modalactions .btn{{width:100%}}}}
@media(max-width:390px){{.grid{{grid-template-columns:repeat(6,1fr)}}.dock button{{font-size:.65rem}}}}
@media(hover:none) and (pointer:coarse){{.btn,.option,.cell{{min-height:48px}}}}
</style>
</head>
<body>
<header id="top" class="top hidden"><div class="topin"><div class="brand"><b>{title}</b><span>100 soruluk kaynaklı çalışma sınavı</span></div><div id="elapsed" class="elapsed">00:00</div><div class="progressbox"><div id="progressLabel" class="progresslabel">0 / 100 cevaplandı</div><div class="progress"><i id="progressBar"></i></div></div></div></header>
<main>
<section id="start" class="shell"><div class="card start"><span class="pill">YANLIŞLARLA ÖĞRENME MODU</span><h1>{title}</h1><p class="lead">Bu sınav gerçek sınav simülasyonu değildir. Her cevap seçildiğinde doğru/yanlış bilgisi, doğru cevap, kaynak hükmü ve ilgili PDF sayfası anında gösterilir.</p><div class="stats"><div class="stat"><b>100</b><span>Soru</span></div><div class="stat"><b>Süre sınırı yok</b><span>Çalışma modu</span></div><div class="stat"><b>5 seçenek</b><span>A–B–C–D–E</span></div><div class="stat"><b>Anında</b><span>Kaynaklı açıklama</span></div></div><div class="notice"><b>Kaynak ilkesi:</b> Sorular güncel repo PDF/TXT çiftlerinden üretilmiş ve destek cümlesi PDF metninde doğrulanmıştır. Yanlış yaptığında doğru hüküm ekranda kalır.</div><div style="display:flex;gap:9px;justify-content:center;flex-wrap:wrap"><button id="startBtn" class="btn primary">Çalışmaya Başla</button><button id="resumeBtn" class="btn outline hidden">Kaldığım Yerden Devam Et</button><button id="resetBtn" class="btn danger hidden">Kaydı Sil</button></div></div></section>
<section id="exam" class="shell hidden"><div class="layout"><article class="card qcard"><div class="qmeta"><b id="qnum">Soru 1 / 100</b><span id="qcat"></span></div><h2 id="qtext" class="qtext"></h2><div id="options" class="options"></div><div id="feedback" class="feedback hidden"></div><div class="actions"><button id="prev" class="btn outline">← Önceki</button><button id="next" class="btn primary">Sonraki →</button></div></article><aside class="card side"><div class="sidehead"><b>Soru Haritası</b><div style="display:flex;align-items:center;gap:8px"><span id="mapCount">1/100</span><button id="closeMap" class="closemap" aria-label="Soru haritasını kapat">×</button></div></div><div id="grid" class="grid"></div><div class="summary"><div class="mini"><b id="correctMini">0</b><span>Doğru</span></div><div class="mini"><b id="wrongMini">0</b><span>Yanlış</span></div><div class="mini"><b id="blankMini">100</b><span>Boş</span></div></div><button id="finish" class="btn danger" style="width:100%">Çalışmayı Bitir</button></aside></div><button id="backdrop" class="backdrop" aria-label="Soru haritasını kapat"></button><nav class="dock"><button id="mPrev">←<br>Önceki</button><button id="mMap">▦<br>Harita</button><button id="mNext" class="primary">→<br>Sonraki</button><button id="mFinish">✓<br>Bitir</button></nav></section>
<section id="result" class="shell result hidden"><div class="card hero"><div><span class="pill">ÇALIŞMA TAMAMLANDI</span><h1 style="font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:6px">Sonuç ve Tekrar Raporu</h1><p id="resultText" class="lead" style="margin:0;max-width:none"></p><div class="resultstats"><div class="rstat"><b id="score">0</b><span>Doğru</span></div><div class="rstat"><b id="wrong">0</b><span>Yanlış</span></div><div class="rstat"><b id="blank">0</b><span>Boş</span></div><div class="rstat"><b id="percent">0%</b><span>Başarı</span></div><div class="rstat"><b id="used">00:00</b><span>Kullanılan süre</span></div></div></div><div id="donut" class="donut" style="--okdeg:0deg;--baddeg:0deg"><b id="donutText">0%</b></div></div><div class="card section"><h2>Kaynak Bazlı Başarı Sırası</h2><div class="scroll"><table><thead><tr><th>Kaynak</th><th>Soru</th><th>Doğru</th><th>Yanlış</th><th>Boş</th><th>Başarı</th></tr></thead><tbody id="sourceRows"></tbody></table></div></div><div class="card section"><h2>Yanlış ve Boş Soruların Kaynaklı Tekrarı</h2><p id="analysisIntro" style="color:var(--muted)"></p><div id="analysis"></div></div><div style="display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin-top:18px"><button id="print" class="btn outline">Raporu Yazdır</button><button id="restart" class="btn danger">Baştan Çöz</button></div></section>
</main>
<div id="modalWrap" class="modalwrap hidden"><div class="card modal"><h3>Çalışmayı bitir</h3><p id="modalText"></p><div class="modalactions"><button id="cancelModal" class="btn outline">Devam Et</button><button id="confirmModal" class="btn danger">Bitir ve Sonucu Göster</button></div></div></div>
<script>
"use strict";
const Q={data};
const KEY="ptt2026_learning_{storage_slug}_v1";
const L=["A","B","C","D","E"];
const $=id=>document.getElementById(id);
const E=s=>String(s??"").replace(/[&<>"']/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}}[c]));
const els={{top:$("top"),start:$("start"),exam:$("exam"),result:$("result"),elapsed:$("elapsed"),progressLabel:$("progressLabel"),progressBar:$("progressBar"),qnum:$("qnum"),qcat:$("qcat"),qtext:$("qtext"),options:$("options"),feedback:$("feedback"),prev:$("prev"),next:$("next"),grid:$("grid"),mapCount:$("mapCount"),correctMini:$("correctMini"),wrongMini:$("wrongMini"),blankMini:$("blankMini"),finish:$("finish"),closeMap:$("closeMap"),backdrop:$("backdrop"),mPrev:$("mPrev"),mMap:$("mMap"),mNext:$("mNext"),mFinish:$("mFinish"),startBtn:$("startBtn"),resumeBtn:$("resumeBtn"),resetBtn:$("resetBtn"),modalWrap:$("modalWrap"),modalText:$("modalText"),cancelModal:$("cancelModal"),confirmModal:$("confirmModal"),score:$("score"),wrong:$("wrong"),blank:$("blank"),percent:$("percent"),used:$("used"),donut:$("donut"),donutText:$("donutText"),resultText:$("resultText"),sourceRows:$("sourceRows"),analysisIntro:$("analysisIntro"),analysis:$("analysis"),print:$("print"),restart:$("restart")}};
let state={{started:false,completed:false,current:0,answers:{{}},startedAt:null,finishedAt:null}};let timer=null;
function load(){{try{{return Object.assign(state,JSON.parse(localStorage.getItem(KEY)||"{{}}"))}}catch{{return state}}}}
function save(){{localStorage.setItem(KEY,JSON.stringify(state))}}
function fmt(sec){{sec=Math.max(0,Math.floor(sec));return String(Math.floor(sec/60)).padStart(2,"0")+":"+String(sec%60).padStart(2,"0")}}
function elapsed(){{return state.startedAt?Math.floor(((state.finishedAt||Date.now())-state.startedAt)/1000):0}}
function screen(name){{els.start.classList.toggle("hidden",name!=="start");els.exam.classList.toggle("hidden",name!=="exam");els.result.classList.toggle("hidden",name!=="result");els.top.classList.toggle("hidden",name!=="exam");closeMap();window.scrollTo(0,0)}}
function openMap(){{document.body.classList.add("mapopen")}}function closeMap(){{document.body.classList.remove("mapopen")}}
function counts(){{let c=0,w=0;Object.entries(state.answers).forEach(([i,a])=>{{if(Number(a)===Q[Number(i)].correct)c++;else w++}});return{{c,w,b:Q.length-c-w}}}}
function tick(){{els.elapsed.textContent=fmt(elapsed())}}
function buildGrid(){{els.grid.innerHTML="";Q.forEach((q,i)=>{{const b=document.createElement("button");b.className="cell";b.textContent=i+1;b.setAttribute("aria-label",`Soru ${{i+1}}`);b.onclick=()=>{{state.current=i;save();render();closeMap();window.scrollTo(0,0)}};els.grid.appendChild(b)}})}}
function startNew(){{state={{started:true,completed:false,current:0,answers:{{}},startedAt:Date.now(),finishedAt:null}};save();begin()}}
function begin(){{screen("exam");if(!els.grid.children.length)buildGrid();render();clearInterval(timer);tick();timer=setInterval(tick,1000)}}
function select(i){{if(Object.prototype.hasOwnProperty.call(state.answers,state.current))return;state.answers[state.current]=i;save();render()}}
function render(){{const i=state.current,q=Q[i],has=Object.prototype.hasOwnProperty.call(state.answers,i),chosen=has?Number(state.answers[i]):null;els.qnum.textContent=`Soru ${{i+1}} / ${{Q.length}}`;els.qcat.textContent=q.category+" · "+q.difficulty;els.qtext.textContent=q.question;els.mapCount.textContent=`${{i+1}}/100`;els.options.innerHTML="";q.options.forEach((o,oi)=>{{const b=document.createElement("button");b.className="option";b.innerHTML=`<span class="letter">${{L[oi]}}</span><span>${{E(o)}}</span>`;if(has){{b.disabled=true;if(oi===q.correct)b.classList.add("correct");if(oi===chosen&&chosen!==q.correct)b.classList.add("wrong");if(oi===chosen)b.classList.add("chosen")}}b.onclick=()=>select(oi);els.options.appendChild(b)}});if(has){{const ok=chosen===q.correct;els.feedback.className="feedback "+(ok?"ok":"bad");els.feedback.innerHTML=`<h3>${{ok?"✅ Doğru":"❌ Yanlış"}}</h3><p><b>Doğru cevap:</b> ${{L[q.correct]}}) ${{E(q.options[q.correct])}}</p><p><b>Açıklama:</b> ${{E(q.explanation)}}</p><div class="source"><b>Kaynak:</b> ${{E(q.source)}}${{q.page?" · PDF s. "+E(q.page):""}}<br><b>Kaynak hükmü:</b> ${{E(q.support)}}</div>`}}else{{els.feedback.className="feedback hidden";els.feedback.innerHTML=""}}els.prev.disabled=i===0;els.mPrev.disabled=i===0;els.next.textContent=i===Q.length-1?"Haritaya Bak":"Sonraki →";els.mNext.innerHTML=i===Q.length-1?"▦<br>Harita":"→<br>Sonraki";overview()}}
function overview(){{const x=counts(),answered=x.c+x.w;els.correctMini.textContent=x.c;els.wrongMini.textContent=x.w;els.blankMini.textContent=x.b;els.progressLabel.textContent=`${{answered}} / 100 cevaplandı`;els.progressBar.style.width=answered+"%";[...els.grid.children].forEach((b,i)=>{{const has=Object.prototype.hasOwnProperty.call(state.answers,i);b.classList.toggle("done",has);b.classList.toggle("bad",has&&Number(state.answers[i])!==Q[i].correct);b.classList.toggle("current",i===state.current)}})}}
function go(d){{state.current=Math.max(0,Math.min(Q.length-1,state.current+d));save();render();window.scrollTo(0,0)}}
function finishAsk(){{const x=counts();els.modalText.innerHTML=x.b?`<b>${{x.b}} boş sorun var.</b> Yine de bitirmek istediğine emin misin?`:"Tüm sorular cevaplandı. Sonuç raporunu açmak istiyor musun?";els.modalWrap.classList.remove("hidden")}}
function finish(){{state.completed=true;state.finishedAt=Date.now();save();clearInterval(timer);els.modalWrap.classList.add("hidden");showResult()}}
function showResult(){{screen("result");const x=counts(),pct=Math.round(x.c/Q.length*100);els.score.textContent=x.c;els.wrong.textContent=x.w;els.blank.textContent=x.b;els.percent.textContent=pct+"%";els.used.textContent=fmt(elapsed());els.donutText.textContent=pct+"%";const okdeg=x.c/Q.length*360,baddeg=(x.c+x.w)/Q.length*360;els.donut.style.setProperty("--okdeg",okdeg+"deg");els.donut.style.setProperty("--baddeg",baddeg+"deg");els.resultText.textContent=`${{x.c}} doğru, ${{x.w}} yanlış, ${{x.b}} boş. Yanlış ve boş sorular aşağıda kaynaklarıyla tekrar edilebilir.`;const map={{}};Q.forEach((q,i)=>{{map[q.source]??={{t:0,c:0,w:0,b:0}};const z=map[q.source];z.t++;if(!Object.prototype.hasOwnProperty.call(state.answers,i))z.b++;else if(Number(state.answers[i])===q.correct)z.c++;else z.w++}});els.sourceRows.innerHTML="";Object.entries(map).sort((a,b)=>(b[1].c/b[1].t)-(a[1].c/a[1].t)||b[1].c-a[1].c).forEach(([s,z])=>{{const tr=document.createElement("tr");tr.innerHTML=`<td>${{E(s)}}</td><td>${{z.t}}</td><td>${{z.c}}</td><td>${{z.w}}</td><td>${{z.b}}</td><td>%${{Math.round(z.c/z.t*100)}}</td>`;els.sourceRows.appendChild(tr)}});const bad=Q.map((q,i)=>({{q,i}})).filter(o=>!Object.prototype.hasOwnProperty.call(state.answers,o.i)||Number(state.answers[o.i])!==o.q.correct);els.analysisIntro.textContent=bad.length?`${{bad.length}} soru için doğru cevap ve kaynak hükmü aşağıdadır.`:"Tebrikler, yanlış veya boş sorun yok.";els.analysis.innerHTML="";bad.forEach(({q,i})=>{{const has=Object.prototype.hasOwnProperty.call(state.answers,i),u=has?`${{L[state.answers[i]]}}) ${{q.options[state.answers[i]]}}`:"Boş";const d=document.createElement("details");d.innerHTML=`<summary>${{i+1}}. ${{E(q.question)}}</summary><div class="detail"><p><b>Senin cevabın:</b> ${{E(u)}}</p><p><b>Doğru cevap:</b> ${{L[q.correct]}}) ${{E(q.options[q.correct])}}</p><p><b>Açıklama:</b> ${{E(q.explanation)}}</p><div class="source"><b>Kaynak:</b> ${{E(q.source)}}${{q.page?" · PDF s. "+E(q.page):""}}<br><b>Kaynak hükmü:</b> ${{E(q.support)}}</div></div>`;els.analysis.appendChild(d)}})}}
function init(){{state=load();if(state.completed){{showResult();return}}if(state.started){{els.resumeBtn.classList.remove("hidden");els.resetBtn.classList.remove("hidden")}}screen("start")}}
els.startBtn.onclick=startNew;els.resumeBtn.onclick=begin;els.resetBtn.onclick=()=>{{localStorage.removeItem(KEY);location.reload()}};els.prev.onclick=()=>go(-1);els.next.onclick=()=>state.current===Q.length-1?openMap():go(1);els.mPrev.onclick=()=>go(-1);els.mNext.onclick=()=>state.current===Q.length-1?openMap():go(1);els.mMap.onclick=openMap;els.closeMap.onclick=closeMap;els.backdrop.onclick=closeMap;els.finish.onclick=finishAsk;els.mFinish.onclick=finishAsk;els.cancelModal.onclick=()=>els.modalWrap.classList.add("hidden");els.confirmModal.onclick=finish;els.modalWrap.onclick=e=>{{if(e.target===els.modalWrap)els.modalWrap.classList.add("hidden")}};els.print.onclick=()=>window.print();els.restart.onclick=()=>{{localStorage.removeItem(KEY);startNew()}};document.addEventListener("keydown",e=>{{if(e.key==="Escape"){{closeMap();els.modalWrap.classList.add("hidden")}}if(!els.exam.classList.contains("hidden")){{if(e.key==="ArrowLeft")go(-1);if(e.key==="ArrowRight")go(1);const k=L.indexOf(e.key.toUpperCase());if(k>=0)select(k)}}}});window.addEventListener("resize",()=>{{if(innerWidth>1024)closeMap()}});init();
</script>
</body>
</html>'''


def index_html(entries: list[dict[str, Any]]) -> str:
    cards = "\n".join(
        f'<a class="card" href="{html.escape(item["file"])}"><span>{index:02d}</span><div><b>{html.escape(item["area"])}</b><small>100 kaynaklı çalışma sorusu · anında açıklama</small></div></a>'
        for index, item in enumerate(entries, start=1)
    )
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#07111f"><title>PTT 2026 Çalışma Sınavları</title><style>*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;background:#07111f;color:#eff7ff;font-family:Inter,system-ui,-apple-system,"Segoe UI",Arial,sans-serif}}main{{width:min(1050px,100%);margin:auto;padding:clamp(16px,4vw,44px)}}h1{{font-size:clamp(2rem,6vw,4rem);line-height:1.05;margin:10px 0}}p{{color:#a9bdd0;max-width:780px}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:28px}}.card{{display:flex;align-items:center;gap:14px;padding:18px;border:1px solid #294861;border-radius:16px;background:linear-gradient(180deg,#142941,#0e1d30);color:#eff7ff;text-decoration:none;box-shadow:0 15px 38px rgba(0,0,0,.28);min-width:0}}.card:hover{{border-color:#27c8b9}}.card span{{flex:0 0 44px;height:44px;border-radius:12px;display:grid;place-items:center;background:#27c8b9;color:#041018;font-weight:900}}.card div{{min-width:0}}.card b{{display:block;overflow-wrap:anywhere}}.card small{{display:block;margin-top:5px;color:#a9bdd0}}.note{{margin-top:22px;padding:15px;border-left:4px solid #27c8b9;background:#0e1d30;border-radius:12px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}.card{{padding:15px}}}}</style></head><body><main><div style="display:inline-block;padding:6px 10px;border-radius:99px;background:rgba(39,200,185,.13);color:#77e8df;font-weight:900;font-size:.78rem">PTT 2026 UZMANLIK ÇALIŞMA MERKEZİ</div><h1>Ana Alan Çalışma Sınavları</h1><p>Her ana alanda 100 soru bulunur. Cevap seçildiği anda doğru/yanlış, doğru cevap, açıklama, repo PDF kaynağı ve sayfa bilgisi gösterilir. Sınavlar telefonda, tablette ve bilgisayarda çevrimdışı çalışır.</p><div class="grid">{cards}</div><div class="note"><b>Kullanım:</b> Bu klasörü ZIP dosyasından tamamen çıkarın ve <code>00_ACILIS_MENUSU.html</code> dosyasını tarayıcıda açın. Mesajlaşma uygulamasının önizlemesi JavaScript çalıştırmazsa dosyayı telefonun tarayıcısıyla açın.</div></main></body></html>'''


def main() -> None:
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    entries: list[dict[str, Any]] = []
    reports: list[dict[str, Any]] = []

    for area, filename in AREAS:
        area_dir = ROOT / area
        if not area_dir.exists():
            raise FileNotFoundError(f"Ana alan klasörü bulunamadı: {area_dir}")
        print(f"\n--- {area} ---")
        questions, report = generate_area_questions(area, area_dir)
        storage_slug = hashlib.sha1(area.encode("utf-8")).hexdigest()[:12]
        target = OUTPUT / filename
        target.write_text(exam_html(area, questions, storage_slug), encoding="utf-8")
        entries.append({"area": area, "file": filename})
        reports.append(report)
        print(json.dumps(report, ensure_ascii=False, indent=2))

    (OUTPUT / "00_ACILIS_MENUSU.html").write_text(index_html(entries), encoding="utf-8")
    readme = """PTT 2026 ANA ALAN ÇALIŞMA SINAVLARI\n\n- 10 ana alanın her biri için ayrı 100 soruluk HTML bulunur.\n- Toplam 1.000 soru vardır.\n- Cevap seçilince doğru/yanlış, doğru cevap, açıklama, PDF kaynağı ve sayfa bilgisi anında açılır.\n- Dosyalar tek başına ve çevrimdışı çalışır.\n- Telefon, tablet ve bilgisayar ekranlarına uyumludur.\n- Başlamak için 00_ACILIS_MENUSU.html dosyasını tarayıcıda açın.\n- Mesajlaşma uygulaması önizlemesinde düğmeler çalışmazsa dosyayı indirip Chrome, Edge, Firefox veya Safari ile açın.\n"""
    (OUTPUT / "README.txt").write_text(readme, encoding="utf-8")
    (OUTPUT / "URETIM_RAPORU.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Final integrity checks.
    html_files = sorted(OUTPUT.glob("[0-9][0-9]_*.html"))
    exam_files = [path for path in html_files if path.name != "00_ACILIS_MENUSU.html"]
    if len(exam_files) != 10:
        raise RuntimeError(f"Beklenen 10 sınav dosyası yerine {len(exam_files)} dosya üretildi")
    for path in exam_files:
        content = path.read_text(encoding="utf-8")
        if content.count('"question":') != 100:
            raise RuntimeError(f"{path.name}: 100 soru doğrulanamadı")
        if "const Q=" not in content or "Kaynak hükmü" not in content:
            raise RuntimeError(f"{path.name}: çalışma sınavı işlevleri eksik")
    print("\nÜretim tamamlandı: 10 HTML, 1.000 soru, açılış menüsü ve rapor.")


if __name__ == "__main__":
    main()
