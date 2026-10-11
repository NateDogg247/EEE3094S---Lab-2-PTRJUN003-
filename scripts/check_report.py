"""Verify the user's page-count rule and all report hyperlinks."""

from pathlib import Path
from urllib.parse import urlparse
import json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "report/PTRJUN003_Lab2_Report.pdf"
REPO = "https://github.com/NateDogg247/EEE3094S---Lab-2-PTRJUN003-"


def check():
    reader = PdfReader(PDF)
    labels = reader.page_labels
    reference_index = labels.index("R1")
    intro_index = reference_index - 14
    main_labels = labels[intro_index:reference_index]
    assert main_labels == [str(i) for i in range(1, 15)], main_labels
    assert "Introduction" in reader.pages[intro_index].extract_text()
    assert "Final Remarks" in reader.pages[reference_index - 1].extract_text()
    assert labels[reference_index + 1] == "A1"
    assert "List of Figures" in reader.pages[intro_index - 2].extract_text()
    assert "List of Tables" in reader.pages[intro_index - 1].extract_text()
    internal_count = github_count = 0
    destinations = reader.named_destinations
    github_urls = set()
    for page in reader.pages:
        for item in page.get("/Annots", []):
            annotation = item.get_object()
            action = annotation.get("/A", {})
            if action.get("/S") == "/URI":
                uri = str(action["/URI"])
                if uri.startswith(REPO):
                    assert urlparse(uri).scheme == "https"
                    github_count += 1
                    github_urls.add(uri)
                    for prefix in (REPO + "/tree/main/", REPO + "/blob/main/"):
                        if uri.startswith(prefix):
                            assert (ROOT / uri[len(prefix) :]).exists(), uri
            if action.get("/S") == "/GoTo":
                destination = action["/D"]
                if isinstance(destination, str):
                    assert destination in destinations, destination
                internal_count += 1
            assert action.get("/S") != "/Launch"
    assert github_count > 10
    assert internal_count > 50
    assert not any("??" in page.extract_text() for page in reader.pages)
    result = {
        "main_pages": 14,
        "excluded_title_pages": 1,
        "front_matter_pages": intro_index - 1,
        "reference_pages": 1,
        "appendix_pages": len(reader.pages) - reference_index - 1,
        "total_pages": len(reader.pages),
        "internal_links": internal_count,
        "github_links": github_count,
        "github_urls": sorted(github_urls),
    }
    (ROOT / "results/report_checks.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    check()
