"""
Example: Building a Constitutional Law study guide with note_generator.

Demonstrates every component available in the NoteBuilder library using a
hypothetical Con Law class so it is clear the tool works for any subject.

Usage:
    python example_usage.py

Output:
    /tmp/example_notes.pdf
"""

from note_generator import NoteBuilder

# ── 1. Create a NoteBuilder instance ────────────────────────────────────────

notes = NoteBuilder(
    course_name="Constitutional Law",
    subtitle="Separation of Powers & Executive Authority",
    school="Example Law School",
    pages="pp. 210-238",
    topics=["Executive Power", "Non-Delegation Doctrine"],
    date="September 15, 2025",
)

# ── 2. Title page with table of contents and "Why" box ──────────────────────

notes.add_title_page(
    toc=[
        ("I",   "Executive Power -- Constitutional Framework",   "pp. 210-218"),
        ("",    "A. Youngstown Sheet & Tube Co. v. Sawyer -- Full Case Brief", ""),
        ("",    "B. The Jackson Concurrence Framework (Chart)",  ""),
        ("",    "C. Textbook Questions -- Answered",             ""),
        ("II",  "The Non-Delegation Doctrine",                   "pp. 219-238"),
        ("",    "A. Overview & Historical Development",          ""),
        ("",    "B. Gundy v. United States -- Full Case Brief",  ""),
        ("III", "Master Comparison Charts",                      ""),
    ],
    why_box=(
        "These readings set up the central tension of executive power: the "
        "President must be strong enough to act decisively, but constrained "
        "enough to preserve the separation of powers.  Understanding the "
        "Youngstown framework is essential -- it appears in virtually every "
        "exam and provides the analytical structure for all executive-action "
        "questions."
    ),
)

# ── 3. Section header ───────────────────────────────────────────────────────

notes.add_section_header(
    number="I",
    title="Executive Power -- Constitutional Framework",
    page_range="pp. 210-218",
)

# ── 4. Body text ────────────────────────────────────────────────────────────

notes.add_body_text(
    "Article II, Section 1 vests 'the executive Power' in the President.  "
    "Unlike Article I's careful enumeration of congressional powers, Article "
    "II's vesting clause is broad and undefined.  This textual asymmetry fuels "
    "the ongoing debate between proponents of a 'unitary executive' (who read "
    "the clause as a substantive grant of all traditionally executive powers) "
    "and those who view the President's authority as limited to powers "
    "specifically enumerated elsewhere in Article II.",
)

# ── 5. Case brief ───────────────────────────────────────────────────────────

notes.add_case_brief(
    case_name="Youngstown Sheet & Tube Co. v. Sawyer",
    citation="343 U.S. 579 (1952)",
    facts=(
        "During the Korean War, a labor dispute threatened to shut down the "
        "nation's steel mills.  President Truman issued Executive Order 10340 "
        "directing the Secretary of Commerce to seize and operate the mills to "
        "ensure continued steel production for the war effort.  Truman cited "
        "no statutory authority; he relied solely on his inherent executive "
        "power as Commander-in-Chief.  Congress had previously considered and "
        "rejected seizure as a remedy in the Taft-Hartley Act."
    ),
    issue=(
        "Whether the President has inherent constitutional authority to seize "
        "private property during wartime without congressional authorization."
    ),
    rule=(
        "The President's power to issue an executive order must stem either "
        "from an act of Congress or from the Constitution itself.  The "
        "Commander-in-Chief power does not extend to seizing domestic private "
        "property, even during wartime."
    ),
    application=(
        "The Court found no statute authorizing the seizure.  Congress had "
        "explicitly rejected seizure as a tool in the Taft-Hartley Act, "
        "choosing instead less drastic remedies.  The President's military "
        "power as Commander-in-Chief did not extend to labor disputes on the "
        "home front.  The order was legislative in nature -- only Congress may "
        "make such policy."
    ),
    holding=(
        "Affirmed the injunction.  The executive order was unconstitutional.  "
        "The President cannot seize private property without congressional "
        "authorization, even in wartime.  6-3 decision (Black, J.)."
    ),
    key_quotes=[
        "The President's power, if any, to issue the order must stem either "
        "from an act of Congress or from the Constitution itself.",
        "In the framework of our Constitution, the President's power to see "
        "that the laws are faithfully executed refutes the idea that he is to "
        "be a lawmaker.",
    ],
)

# ── 6. Cold-call points ────────────────────────────────────────────────────

notes.add_cold_call_points(
    label="Youngstown",
    points=[
        "Why did Black's majority opinion take such a rigid approach?  Because "
        "a formalist bright line prevents incremental expansion of executive "
        "power.  Each exception becomes a precedent.",
        "What is the significance of Congress rejecting seizure in Taft-Hartley?  "
        "It shows Congress considered and refused this exact remedy -- the "
        "President cannot do what Congress deliberately chose not to authorize.",
        "Could Truman have invoked Taft-Hartley's cooling-off provisions instead?  "
        "Yes, but he chose not to, weakening any argument that the situation "
        "was too urgent for the statutory process.",
    ],
)

# ── 7. Problem with answer (textbook question) ──────────────────────────────

notes.add_problem(
    number="Q1",
    question=(
        "If Congress had been silent on steel seizure (no Taft-Hartley "
        "provision at all), would the outcome change under the Jackson "
        "framework?"
    ),
    answer=(
        "Likely yes.  Under Jackson's Category 2 ('zone of twilight'), "
        "congressional silence creates a concurrent authority where the "
        "President may act if the subject matter is not inherently "
        "legislative.  Without Congress's explicit rejection of seizure, "
        "the President's action would fall into Category 2 rather than "
        "Category 3, and the Court would balance the competing interests.  "
        "The wartime emergency might tip the balance in the President's "
        "favor, though the domestic nature of the seizure would still weigh "
        "against executive authority."
    ),
)

# ── 8. Info table (chart) ───────────────────────────────────────────────────

notes.add_info_table(
    title="Jackson Concurrence -- Three Categories of Presidential Power",
    headers=["Category", "Congressional Posture", "Presidential Power", "Example"],
    rows=[
        [
            "1 -- Maximum",
            "Congress has authorized the action",
            "Strongest presumption of validity; "
            "President acts with all federal authority",
            "AUMF authorizing military force",
        ],
        [
            "2 -- Twilight Zone",
            "Congress is silent",
            "Uncertain; concurrent authority; "
            "depends on the specific circumstances",
            "Executive agreements on matters "
            "Congress has not addressed",
        ],
        [
            "3 -- Minimum",
            "Congress has prohibited the action",
            "Weakest; can prevail only if Congress "
            "lacks constitutional power over the matter",
            "Youngstown -- seizure after Congress "
            "rejected it in Taft-Hartley",
        ],
    ],
)

# ── 9. Rule box ─────────────────────────────────────────────────────────────

notes.add_rule_box(
    title="The Youngstown Principle",
    content=(
        "When the President acts contrary to the expressed or implied will of "
        "Congress, presidential power is at its lowest ebb.  The executive may "
        "prevail only by showing that Congress itself lacks constitutional "
        "authority over the subject -- a nearly impossible burden in the "
        "domestic sphere."
    ),
)

# ── 10. Confidence score ───────────────────────────────────────────────────

notes.add_confidence_score(
    score=9,
    max_score=10,
    explanation=(
        "Landmark case with a clear rule.  Focus on Jackson's three-part "
        "framework -- it is the analytical tool that appears on every exam.  "
        "Be ready to classify hypothetical presidential actions into the "
        "correct category and explain why."
    ),
)

# ── 11. Build the PDF ──────────────────────────────────────────────────────

output_path = "/tmp/example_notes.pdf"
notes.build(output_path)
print(f"PDF saved to {output_path}")
