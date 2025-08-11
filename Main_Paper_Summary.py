
import os
import pymupdf4llm
from llm_agents import (
    AuthorExtractorAgent,
    AbstractExtractorAgent,
    TitleExtractorAgent,
    IntroExtractorAgent,
    ConclusionExtractorAgent,
    PaperSummaryWriterAgent,
)

def load_pdf_text_pages(file_path, start_page=0, end_page=None):
    """
    Extract text from PDF pages in markdown format using pymupdf4llm.to_markdown.
    Args:
        file_path (str): Path to the PDF file.
        start_page (int): Zero-based start page index (inclusive).
        end_page (int or None): Zero-based end page index (exclusive). If None, extract till last page.
    Returns:
        str: Concatenated markdown text of the specified page range.
    """
    # Prepare pages list for pymupdf4llm
    if end_page is None:
        pages = None
    else:
        pages = list(range(start_page, end_page))
    md_text = pymupdf4llm.to_markdown(file_path, pages=pages)
    return md_text

def save_summary_to_md(summary: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

def RunPaperSummaryPipeline(pdf_file: str):
    # Check if the PDF file exists
    
    if not os.path.exists(pdf_file):
        raise FileNotFoundError(f"PDF file '{pdf_file}' does not exist.")

    # Instantiate agents
    author_agent = AuthorExtractorAgent()
    abstract_agent = AbstractExtractorAgent()
    title_agent = TitleExtractorAgent()
    intro_agent = IntroExtractorAgent()
    conclusion_agent = ConclusionExtractorAgent()
    summary_agent = PaperSummaryWriterAgent()

    # Extract authors, abstract, title from page 0 (first page)
    first_page_md = load_pdf_text_pages(pdf_file, start_page=0, end_page=1)
    authors = author_agent.extract_authors(first_page_md)
    abstract = abstract_agent.extract_abstract(first_page_md)
    title = title_agent.extract_title(first_page_md)

    # Extract intro summary from first 5 pages
    intro_md = load_pdf_text_pages(pdf_file, start_page=0, end_page=5)
    intro_summary = intro_agent.extract_intro_summary(intro_md)

    # Extract conclusion summary from last 5 pages
    # Get total pages count using pymupdf4llm (fallback to PyMuPDF if needed)
    import fitz
    doc = fitz.open(pdf_file)
    total_pages = len(doc)
    doc.close()
    last_5_start = max(0, total_pages - 5)
    conclusion_md = load_pdf_text_pages(pdf_file, start_page=last_5_start, end_page=total_pages)
    conclusion_summary = conclusion_agent.extract_conclusion_summary(conclusion_md)

    # Compile comprehensive summary
    paper_summary = summary_agent.compile_summary(authors, abstract, title, intro_summary, conclusion_summary)

    # Save summary to markdown file
    output_md = "test_paper_summary.md"
    save_summary_to_md(paper_summary, output_md)
    print(f"Paper summary saved to {output_md}")

def main():
    # Example usage
    pdf_file = "test_paper.pdf"  # Replace with your PDF file path
    try:
        RunPaperSummaryPipeline(pdf_file)
    except Exception as e:
        print(f"Error during paper summary pipeline: {e}")

if __name__ == "__main__":
    main()