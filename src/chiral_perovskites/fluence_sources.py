"""Pin original Nature 2026 XLSX source workbooks by SHA-256.

Raw files are downloaded locally and are not redistributed with this repo.
"""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

PUBLICATION_PREFIX = (
    "https://media.springernature.com/original/springer-static/esm/"
    "art%3A10.1038%2Fs41586-026-10637-x/MediaObjects/"
)
BACKUP_PREFIX = (
    "https://static-content.springer.com/esm/"
    "art%3A10.1038%2Fs41586-026-10637-x/MediaObjects/"
)
FILES = {
    "nature2026_source_fig2.xlsx": ("41586_2026_10637_MOESM4_ESM.xlsx",
        "7a94679a0f6fdb2b41fd7852915f0d88babbe35efed23a5dd6a0503de870b1fe", PUBLICATION_PREFIX),
    "nature2026_source_fig3.xlsx": ("41586_2026_10637_MOESM5_ESM.xlsx",
        "4f06825a839ba470e96fc45d9587db4d5f42067c41b2d03762e26ed64d217c29", PUBLICATION_PREFIX),
    "nature2026_source_ED6.xlsx": ("41586_2026_10637_MOESM9_ESM.xlsx",
        "d505c422ee49d20255587d8efd55de957d89985c488461b2bc5d78e848ff5e42", PUBLICATION_PREFIX),
    "nature2026_source_ED7.xlsx": ("41586_2026_10637_MOESM10_ESM.xlsx",
        "b1e92e1cef9d8a37908bfc6a10114828420abfb4419447b273921c8074566608", BACKUP_PREFIX),
}


def validate_xlsx(data: bytes, sha: str) -> None:
    digest = hashlib.sha256(data).hexdigest()
    if digest.lower() != sha.lower():
        raise ValueError(f"Publisher workbook checksum mismatch {digest}; manual provenance review required.")
    try:
        with ZipFile(io.BytesIO(data)) as z:
            if "xl/workbook.xml" not in z.namelist():
                raise ValueError("Download is not a valid source Excel workbook")
    except BadZipFile as exc:
        raise ValueError("Publisher returned HTML/error data instead of Excel workbook") from exc


def fetch(folder: Path) -> list[dict]:
    folder.mkdir(parents=True,exist_ok=True)
    records=[]
    for local,(suffix,sha,prefix) in FILES.items():
        path=folder/local
        if not path.exists():
            url=prefix+suffix
            with urlopen(Request(url,headers={"User-Agent":"chiral-pv-research/0.5"}),timeout=90) as response:
                content=response.read()
            validate_xlsx(content,sha)
            path.write_bytes(content)
        validate_xlsx(path.read_bytes(),sha)
        records.append({"filename":local,"sha256":sha,"original_url":prefix+suffix,"bytes":path.stat().st_size})
    return records
