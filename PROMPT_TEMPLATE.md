# Universal Law School Notes Prompt Template

## How to Use This Template

1. **Upload your reading** (PDF or DOCX) to Claude.
2. **Copy the Master Prompt below** into the chat.
3. **Replace the `[BRACKETED PLACEHOLDERS]`** with your class-specific information:
   - `[CLASS NAME]` -- the name of your course (e.g., "Evidence", "Wills, Trusts & Estates")
   - `[PAGES/FILE DESCRIPTION]` -- what the reading covers (e.g., "pp. 747-755 of the casebook")
   - `[PALATINO FONT PATH]` -- path to Palatino font file (default provided; only change if different)
   - `[CLASS-SPECIFIC INSTRUCTIONS]` -- optional block for class-specific emphasis (see examples at bottom)
4. **Send the prompt.** Claude will generate a Python script that outputs a colorful, bookmarked PDF.
5. After Claude generates the script, say: **"Run it."**

**Tip:** You can leave `[CLASS-SPECIFIC INSTRUCTIONS]` empty or delete that line entirely for a general-purpose output. For best results, paste in one of the class-specific instruction blocks from the bottom of this file.

---

## Master Prompt

```
I have uploaded [PAGES/FILE DESCRIPTION] for my [CLASS NAME] class.

=== READING & ANALYSIS ORDER ===

Before writing anything, read the entire uploaded document using this sequence:

1. SCAN the full document to identify its structure: problems/hypotheticals, cases, statutory text, notes, and questions.
2. READ any problems or hypotheticals FIRST so you understand what the reading is building toward.
3. READ the cases, statutes, and doctrinal text, tracking how each one connects to the problems.
4. READ all notes, questions, and commentary -- these often contain cold-call material.
5. PLAN your output: decide on logical section groupings, identify every question that needs an answer, and list every case that needs a summary.

Do NOT begin writing until you have completed all five steps.

=== CONTENT REQUIREMENTS ===

Produce a comprehensive, cold-call-ready study guide covering everything in the uploaded reading. Include ALL of the following:

A. Big-Picture Orientation
   - Open with a "Why You're Reading This" or "This Guide Covers" box explaining the doctrinal theme, how the pieces fit together, and why it matters.
   - Provide a Table of Contents or section-overview table at the top.

B. Case Summaries (for EVERY case mentioned or discussed)
   - Case name, citation, court, year.
   - Facts (enough detail to discuss intelligently if cold-called).
   - Procedural history (if relevant).
   - Issue(s) presented.
   - Holding and reasoning -- include the court's logic, not just the outcome.
   - Key quotes where they illuminate the reasoning.
   - Dissents or concurrences if covered in the reading.
   - Connection to the broader doctrinal theme.

C. Problems & Hypotheticals (answer EVERY question posed)
   - Restate the problem facts.
   - State each question exactly as posed.
   - Provide a clear answer with "Cold-Call Talking Points" -- bullet-pointed arguments a student could articulate aloud.
   - Where the textbook cites a case alongside a problem, connect them explicitly (e.g., "See Paiva, 892 F.2d at 155").
   - Address counterarguments or "close to the line" observations where appropriate.

D. Doctrinal Concepts & Statutory Text
   - Summarize every rule, statute, or doctrinal framework covered.
   - For multi-part rules (e.g., elements tests, multi-factor balancing), break each element out with its own explanation.
   - Use comparison tables when comparing related concepts, competing tests, or majority vs. minority approaches.

E. Notes & Commentary
   - The textbook's numbered "Notes" and "Questions" sections are prime cold-call material. Answer every note question with a substantive response.
   - Where a note cross-references another case or concept, explain that connection.

F. Charts, Tables & Visual Aids
   - Use tables liberally: comparison charts, element breakdowns, timeline tables, side-by-side analyses.
   - If the reading involves numerical data, financial figures, or chronological events, include a data table.
   - Where a visual diagram would aid understanding (e.g., flowcharts for decision trees, relationship maps for parties), describe and include one.

G. Cold-Call Talking Points
   - Attach "Cold-Call Talking Points" or "Cold-Call Q&A" boxes to every major case and every problem answer.
   - Format as Q&A where possible: state a likely professor question, then provide a confident, concise answer with supporting reasoning.
   - Bold the key terms a professor would want to hear.

H. Confidence Scores
   - At the end of each major section or case, include a confidence score (X/10) rating how well the notes capture the material.
   - If confidence is below 7/10 on anything, flag it and explain what may be missing.

[CLASS-SPECIFIC INSTRUCTIONS]

=== FORMATTING REQUIREMENTS ===

Generate a Python script using ReportLab that produces a PDF with these specifications:

Font & Typography:
- Use Palatino font. The note_generator library auto-detects it on macOS/Linux/Windows.
  If auto-detection fails, pass the path explicitly or fall back to Times (built into ReportLab).
- Register all Palatino variants (regular, bold, italic, bold-italic) with subfont indices.
- Body text: 11pt. Section headers: 14-16pt bold. Sub-headers: 12pt bold.
- Case names in italic wherever they appear in running text.

Page Layout:
- Vertical (portrait) US Letter: 612 x 792 points.
- Margins: ~54-72pt on all sides.
- Header bar on every page with class name (left) and topic/page range (right).
- Footer with document title (left) and page number (right).

Color Scheme:
- Use a rich, class-appropriate color palette for headers, table headers, callout boxes, and accent bars.
- Section headers should have colored background bars or underlines.
- Tables should have colored header rows and alternating row shading.
- Cold-call boxes and Q&A sections should have a distinct background tint and left border.
- Confidence score bars should be visually rendered (colored fill bar + numeric score).

Structure & Navigation:
- PDF bookmarks for every major section (accessible in PDF sidebar).
- No content should split awkwardly across pages -- use KeepTogether or equivalent to prevent orphaned headers, split tables, or broken callout boxes.
- Each major section should begin with enough space; start a new page if less than ~120pt remain.

Output:
- Save the PDF to the same directory as the uploaded file.
- Name it descriptively (e.g., "Notes [page range].pdf" or "[Topic] Notes.pdf").

=== QUALITY CHECKS ===

Before finalizing, verify:
[ ] Every case in the reading has a full summary with facts, holding, and reasoning.
[ ] Every problem/hypothetical question is answered with cold-call talking points.
[ ] Every numbered note question is answered substantively.
[ ] All comparison opportunities are captured in tables (e.g., majority vs. dissent, old rule vs. new rule, statute vs. common law).
[ ] Case-to-problem connections are explicit -- no case exists in isolation from the problems it illuminates.
[ ] The Table of Contents / overview table at the top accurately reflects all sections.
[ ] Bookmarks are registered for PDF navigation.
[ ] No section header is orphaned at the bottom of a page.
[ ] Confidence scores are present for each major section.
[ ] The font renders correctly (Palatino, not falling back to Helvetica/Courier).
```

---

## Class-Specific Instruction Blocks

Copy the relevant block below and paste it into the `[CLASS-SPECIFIC INSTRUCTIONS]` placeholder in the master prompt.

---

### Evidence

```
=== CLASS-SPECIFIC: EVIDENCE ===

Reading Order Emphasis: Read ALL problems first (they are the backbone of this casebook). Then read the cases. Then return to answer each problem, connecting cases to problems explicitly.

- For each problem: state whether the evidence is ADMISSIBLE or INADMISSIBLE, then explain why using the specific rule subsections (e.g., 701(a), 701(b), 701(c)).
- When a problem cites a case (e.g., "See United States v. Yazzie"), integrate that case's holding into the problem answer.
- For FRE rule text: break each subsection into its own explanation with the advisory committee notes where relevant.
- Track the "line-drawing" theme: where does lay testimony end and expert testimony begin? Where does relevant evidence become unfairly prejudicial? Make these boundary questions explicit.
- Include a "Five Demands" or equivalent framework table whenever expert testimony is at issue.
- Note any 2000 or 2023 amendments to the FRE and explain what changed and why.
```

---

### Immigration Law

```
=== CLASS-SPECIFIC: IMMIGRATION LAW ===

- Provide a detailed logical walkthrough of all facts and case logic -- do not summarize at a high level; walk through the reasoning step by step.
- Address ALL visa types, immigration forms (e.g., I-130, I-730), and statutory provisions (INA sections, 8 C.F.R. sections) referenced in the reading.
- For each statutory provision: cite the exact section, state what it does, and explain how it applies to the facts or problem at hand.
- Problems should be analyzed from every possible angle: What relief is available? What are the eligibility requirements? What are the bars? What discretionary factors apply?
- Include "Legal Issues Embedded in Problem X" lists that identify every distinct legal question raised.
- When the reading covers a doctrinal evolution (e.g., the PSG standard from Acosta to M-E-V-G-), present it as a chronological progression with a timeline or evolution table.
- Distinguish between mandatory and discretionary relief.
- Note any recent executive actions, BIA decisions, or circuit splits that affect the doctrine.
- Include a "Key Statutes, Regs & Treaties -- Quick Reference" table at the end.
```

---

### Internet Law

```
=== CLASS-SPECIFIC: INTERNET LAW ===

- Every case mentioned or discussed in the reading must receive a full summary with facts, holding (including the judge's name), and the court's decision.
- For each case: include "Key Analytical Points" that break down the court's reasoning into discrete, testable propositions.
- Doctrinal concepts should be presented in definition tables (Concept | Definition | Significance).
- Where multiple cases address the same doctrine (e.g., likelihood of confusion in trademark), include a Master Comparison Chart at the end showing how each case applied the test.
- Pay special attention to Internet-specific adaptations of traditional legal doctrines -- flag where the Internet changes the analysis vs. where traditional rules apply unchanged.
- Include dissents with the same level of detail as majority opinions -- professors frequently cold-call on dissenting reasoning.
- Cold-call questions should include policy-oriented questions (e.g., "Should the standard be the same online and offline?") in addition to doctrinal ones.
- Confidence scores should appear after each case section.
```

---

### Wills, Trusts & Estates

```
=== CLASS-SPECIFIC: WILLS, TRUSTS & ESTATES ===

- Charts and diagrams are ESPECIALLY important for this class. Include comparison tables, flowcharts (described textually and rendered as tables), and data tables wherever possible.
- Answer EVERY question posed in the notes -- these are the primary cold-call targets. Format as Q (in italic or colored header): / A: with substantive analysis.
- For cases involving financial data (e.g., stock prices, trust values, damages calculations), include data tables with the numbers from the opinion.
- When the reading covers competing approaches (e.g., capital lost vs. total return, permissive vs. mandated retention), present them in a side-by-side comparison table with: definition, when applied, key case, result.
- Include statutory cross-references (UTC, UPIA, UPC, Restatement) with exact section numbers and what each provision does.
- For fiduciary duty topics: always identify (1) the duty, (2) the standard of care, (3) what constitutes a breach, (4) the remedy/damages measure, and (5) any exceptions or escape valves.
- Where a trust instrument's language matters, quote the key language and explain how the court interpreted it.
- "Power vs. Duty" distinctions should be flagged and explained whenever they arise.
```

---

### Custom / Other Classes

```
=== CLASS-SPECIFIC: [CLASS NAME] ===

[Add your own class-specific instructions here. Consider:
 - What does your professor emphasize in cold calls?
 - Are there recurring analytical frameworks (elements tests, balancing tests, policy arguments)?
 - Does the casebook use problems, and if so, are they the focus of class discussion?
 - Are there statutes or regulations that need to be broken down section by section?
 - Are there competing approaches (circuit splits, majority/minority rules) to track?
 - Does the class emphasize policy arguments, doctrinal evolution, or practical application?]
```
