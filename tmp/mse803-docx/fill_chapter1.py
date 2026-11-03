from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


SOURCE = Path("Assessment/2604MSE803_Assessment1_Report_Draft_v2.docx")
OUTPUT = Path("Assessment/2604MSE803_Assessment1_Report_Draft_v3.docx")


SECTION_TEXT = {
    "1.1 Purpose and Scope of the Report": (
        "Data analytics can support environmental and commercial decisions by converting "
        "observations into evidence while making uncertainty visible. This report examines "
        "two contexts. Task 1 analyses water-quality and fish-population data from the Avon "
        "River to identify environmental challenges and develop conservation recommendations. "
        "This is important because New Zealand’s freshwater ecosystems face interacting "
        "pressures involving water quality, habitat condition and human activity (Ministry for "
        "the Environment & Stats NZ, 2023). Task 2 compares developing an AI-powered customer "
        "relationship management system with improving an existing product through A/B testing "
        "and user-feedback analysis."
    ),
    "1.2 Analytical Approach and Evidence Base": (
        "The report follows a data-to-insight-to-decision process, recognising that analytical "
        "results inform rather than replace professional judgement (Provost & Fawcett, 2013). "
        "For Task 1, the supplied Excel workbook undergoes a structured data-quality audit, "
        "including the development of a data dictionary and the assessment of missing values, "
        "duplicates, inconsistencies and implausible observations. Descriptive and exploratory "
        "analysis is followed by correlation and regression methods to investigate relationships "
        "between temperature, pH, dissolved oxygen, fish count and average size. Python and Power "
        "BI are evaluated as complementary analytical and communication tools. Task 2 uses a "
        "comparative framework covering data availability, bias, predictive uncertainty, privacy, "
        "implementation risk and strategic value."
    ),
    "1.3 Assumptions and Limitations": (
        "The Avon River workbook is treated as the primary empirical source, although it contains "
        "duplicates, missing values, inconsistent records and implausible observations requiring "
        "documented cleaning. It covers only October to December 2023, despite the scenario "
        "referring to several years of data. Varying species composition and missing information "
        "about sampling effort, rainfall, river flow, habitat and pollutants restrict causal "
        "interpretation. Observational associations alone cannot demonstrate that a water-quality "
        "variable caused a change in fish populations (Quinn & Keough, 2002). Task 2 provides no "
        "company-specific financial or operational data; therefore, its recommendation is "
        "conditional on the organisation’s data readiness, resources, risk tolerance and strategic "
        "priorities."
    ),
}


def clear_paragraph(paragraph):
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)


doc = Document(SOURCE)
paragraphs = doc.paragraphs

# Remove the introductory drafting instruction directly below the chapter heading.
for paragraph in paragraphs:
    if paragraph.text.strip() == (
        "[Introduce both assessment scenarios, the report purpose, and the "
        "evidence-to-decision approach]"
    ):
        paragraph._element.getparent().remove(paragraph._element)
        break

for heading, text in SECTION_TEXT.items():
    paragraphs = doc.paragraphs
    for index, paragraph in enumerate(paragraphs):
        if paragraph.text.strip() == heading:
            target = paragraphs[index + 1]
            if not target.text.strip().startswith("["):
                raise RuntimeError(f"Expected placeholder after {heading!r}")
            clear_paragraph(target)
            target.style = doc.styles["Normal"]
            target.add_run(text)
            break
    else:
        raise RuntimeError(f"Heading not found: {heading}")

doc.save(OUTPUT)
print(OUTPUT)
