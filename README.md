# cold-call-ready

**Beautiful, bookmarked PDF class notes with one Python script.**

Upload your casebook pages to Claude, paste a prompt, and get a polished, color-coded study guide with case briefs, cold-call Q&A boxes, problem answers, rule text, and confidence scores -- all in Palatino on letter-sized pages with PDF bookmarks.

Built for law school, works for any class.

## Features

- **Case Brief Boxes** -- structured briefs with posture, facts, holding, reasoning
- **Cold-Call Q&A** -- italic questions with bullet-point answers, ready to recite
- **Problem Boxes** -- restate the facts, state the question, deliver the answer
- **Rule Boxes** -- styled containers for statutes, FRE rules, constitutional text
- **Colored Tables** -- teal headers, alternating row shading, auto-width columns
- **Section Headers** -- maroon (major) and teal (sub) headers with PDF bookmarks
- **Header/Footer Bars** -- navy top bar with class/topic info, gray footer with page numbers
- **Confidence Scores** -- rate your coverage section by section
- **Palatino Typography** -- register all four variants (roman, italic, bold, bold-italic)
- **No Page Splits** -- `KeepTogether` wraps every logical block

---

## Quick Start: AI Workflow (Recommended)

The fastest way to use cold-call-ready is with an AI assistant like Claude. You don't need to write any code yourself.

### Step 1: Install the dependency

```bash
pip install reportlab
```

### Step 2: Font (usually automatic)

cold-call-ready auto-detects Palatino on your system. **On macOS, it just works** -- Palatino ships at `/System/Library/Fonts/Palatino.ttc`.

If Palatino isn't found, it falls back to **Times** (built into ReportLab) automatically with a warning. Your notes will still look good -- just not quite as polished.

To override the auto-detection or point to a custom font:

```bash
# Optional -- only needed if auto-detection fails or you want a different path
export NOTE_GEN_FONT_PATH="/path/to/Palatino.ttc"
```

### Step 3: Upload your reading to Claude

Open [Claude](https://claude.ai) (or Claude Code) and attach the PDF or DOCX of your casebook reading.

### Step 4: Paste the prompt

Copy the **Master Prompt** from [`PROMPT_TEMPLATE.md`](PROMPT_TEMPLATE.md) into the chat. Fill in the placeholders:

| Placeholder | What to put | Example |
|---|---|---|
| `[CLASS NAME]` | Your course name | `Evidence` |
| `[PAGES/FILE DESCRIPTION]` | What the reading covers | `pp. 747-755 of the casebook` |
| `[PALATINO FONT PATH]` | Your font path from Step 2 | `/System/Library/Fonts/Palatino.ttc` |
| `[CLASS-SPECIFIC INSTRUCTIONS]` | Optional -- copy a block from the bottom of `PROMPT_TEMPLATE.md` | *(see below)* |

Pre-built class-specific instruction blocks are included for:

| Class | Key emphasis |
|---|---|
| **Evidence** | Problems first, admissibility verdicts with FRE subsections, amendment tracking |
| **Immigration Law** | Step-by-step walkthroughs, all visa types/INA sections, doctrinal timelines |
| **Internet Law** | Full case summaries with judge names, dissents at full depth, policy Qs |
| **Wills, Trusts & Estates** | Heavy charts/diagrams, financial data tables, statutory cross-references |

You can also write your own block for any class using the **Custom / Other Classes** template at the bottom of `PROMPT_TEMPLATE.md`.

### Step 5: Run it

Claude will generate a Python script. Say **"Run it."** (In Claude Code, it runs automatically.) The PDF appears in your working directory.

### Step 6: Review

Open the PDF and check:
- [ ] Every case has a full brief with cold-call points
- [ ] Every problem/question is answered with talking points
- [ ] Bookmarks work in the PDF sidebar
- [ ] No content is split across pages
- [ ] Confidence score is at the end

---

## Manual Usage: Build a PDF Yourself

If you prefer to write the script by hand (or want to customize beyond what the AI generates), use the `NoteBuilder` API directly.

### Example

```python
from note_generator import NoteBuilder

nb = NoteBuilder(
    output_path="my_notes.pdf",
    class_name="Evidence",
    topic_title="Hearsay Exceptions",
    page_range="pp. 400-430",
    semester="Fall 2025"
)

nb.add_title_page(
    subtitle="Exceptions to the Rule Against Hearsay",
    page_ref="Casebook pp. 400-430 | FRE 803, 804",
    toc_data=[["A", "Present Sense Impression", "What makes it reliable?"]],
    why_title="Why You're Reading These Cases",
    why_text="<b>Big Picture.</b> This unit covers ..."
)

nb.add_section("A. Present Sense Impression")
nb.add_text("Under FRE 803(1), a statement describing an event ...")

nb.add_case_brief(
    "Crawford v. Washington",
    "541 U.S. 36 (2004) -- Scalia, J.",
    [
        ("Posture.", "Defendant's wife made statements to police ..."),
        ("Holding.", "Testimonial statements require confrontation ..."),
        ("Reasoning.", [
            "The Confrontation Clause bars admission of testimonial hearsay unless the declarant is unavailable and was previously cross-examined.",
            "The Roberts reliability test gave courts too much discretion.",
        ]),
    ]
)

nb.add_cold_call("COLD-CALL POINTS -- Crawford", [
    ("What did Crawford change?", [
        "Replaced the Roberts reliability test with a bright-line rule.",
    ]),
])

nb.add_problem("8.1", "The Neighbor's Account",
    "A neighbor told police she saw the defendant leave the house carrying a bag.",
    "Is the neighbor's statement admissible after Crawford?",
    [
        "NO -- testimonial statement, no prior cross-examination.",
        "Must be excluded regardless of reliability.",
    ]
)

nb.add_confidence_score([
    ["Crawford", "95%", "Strong coverage."],
    ["OVERALL", "93%", "Review forfeiture-by-wrongdoing."],
])

nb.build()
```

```bash
python my_notes.py
```

---

## API Reference

| Method | Description |
|---|---|
| `NoteBuilder(output_path, class_name, topic_title, page_range, font_path=None, semester=None)` | Create a new PDF builder |
| `.add_title_page(subtitle, page_ref, toc_data, why_title, why_text)` | Title + TOC + "Why" box |
| `.add_section(title)` | Maroon section header with bookmark |
| `.add_subsection(title)` | Teal subsection header with bookmark |
| `.add_text(text)` | Body paragraph (supports `<b>`, `<i>` HTML) |
| `.add_case_brief(title, citation, fields)` | Bordered case brief; `fields` = list of `(label, content_or_bullet_list)` |
| `.add_cold_call(title, qa_pairs)` | Cold-call Q&A box; `qa_pairs` = list of `(question, [answer_bullets])` |
| `.add_problem(number, title, facts, question, answer_bullets)` | Problem with answer |
| `.add_table(headers, rows, col_widths=None)` | Colored info table |
| `.add_rule_box(rule_title, rule_text_parts)` | Styled rule/statute box |
| `.add_info_box(title, text)` | Bordered info box |
| `.add_confidence_score(rows)` | Confidence score table; `rows` = `[component, score, notes]` |
| `.add_page_break()` | Insert page break |
| `.add_spacer(height=6)` | Vertical spacer |
| `.build()` | Build the PDF with bookmarks; returns output path |

All `add_*` methods return `self` for fluent chaining:

```python
nb.add_section("A. Intro").add_text("...").add_page_break()
```

---

## Colors

| Name | Hex | Usage |
|---|---|---|
| Navy | `#1B2A4A` | Header bar, title text |
| Teal | `#2E6B62` | Subsection headers, table headers |
| Maroon | `#8B1A1A` | Section headers, cold-call titles |
| Cream | `#FDF8F0` | Case brief backgrounds |
| Teal Light | `#E8F4F2` | Alternating table rows |

Access them programmatically:

```python
from note_generator import COLORS
print(COLORS["NAVY"])  # HexColor('#1B2A4A')
```

---

## Contributing

PRs welcome. If you add a new component (e.g., `add_flowchart()`, `add_timeline()`), follow the existing pattern: return a ReportLab `Flowable`, accept an optional `content_w` parameter, and add a corresponding `NoteBuilder` method that appends it to the story.

## License

[MIT](LICENSE)
