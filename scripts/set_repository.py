"""Configure actual HTTPS folder links, or restore internal evidence links."""

import argparse, re
from pathlib import Path
from urllib.parse import urlparse

p = argparse.ArgumentParser()
p.add_argument(
    "url", help="Actual HTTPS repository URL, or local for internal PDF links"
)
p.add_argument("--branch", default="main")
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
if not re.fullmatch(r"[A-Za-z0-9._/-]+", a.branch):
    p.error("Unsafe branch name")
if a.url == "local":
    text = (root / "scripts/repository_internal.tex").read_text()
else:
    url = a.url.rstrip("/").removesuffix(".git")
    u = urlparse(url)
    if (
        u.scheme != "https"
        or u.netloc not in ["github.com", "gitlab.com"]
        or u.query
        or u.fragment
    ):
        p.error("Use a plain HTTPS github.com or gitlab.com repository URL")
    if not re.fullmatch(r"/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", u.path):
        p.error("Use the repository root URL")
    tree = "/-/tree/" if u.netloc == "gitlab.com" else "/tree/"
    text = (
        r"\newcommand{\RepoRoot}{"
        + url
        + "}\n"
        + r"\newcommand{\RepoBranch}{"
        + a.branch
        + "}\n"
        + r"\newcommand{\RepoLink}[2]{\href{\RepoRoot"
        + tree
        + r"\RepoBranch/#1}{#2}}"
        + "\n"
        + r"\newcommand{\RepoFile}[2]{\href{\RepoRoot/blob/\RepoBranch/#1}{#2}}"
        + "\n"
        + r"\newcommand{\RepoStatus}{The supporting-folder links open the published repository on the configured branch.}"
        + "\n"
    )
(root / "report/repository.tex").write_text(text)
print("Report links configured. Rebuild the PDF to apply them.")
