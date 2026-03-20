# anthropic-document-skills

Anthropic's official document processing skills, imported from
[anthropics/skills](https://github.com/anthropics/skills).

## License

These skills are **source-available** (not open source). See LICENSE.txt in each skill
directory for complete terms. They are shared as reference for complex skill patterns.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| **docx** | `.docx`, Word document, report, memo | Create, read, edit Word documents with tracked changes, comments, and professional formatting |
| **pdf** | `.pdf`, merge PDFs, fill form | Full PDF processing — read, merge, split, rotate, watermark, OCR, form filling |
| **pptx** | `.pptx`, slides, presentation, deck | Create and edit PowerPoint presentations with design system and color palettes |
| **xlsx** | `.xlsx`, spreadsheet, Excel | Spreadsheet operations with financial formatting, formula validation |

## Dependencies

- **docx**: `docx-js` (creation), `pandoc` (reading)
- **pdf**: `pypdf`, `pdfplumber`, `reportlab`, `pytesseract` (OCR)
- **pptx**: `pptxgenjs`, `markitdown`, `LibreOffice`, `Pillow`
- **xlsx**: `pandas`, `openpyxl`
