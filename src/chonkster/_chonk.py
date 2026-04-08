"""Chonk: the main entry point for document-to-table conversion."""

from __future__ import annotations

import logging
from typing import Union
from pathlib import Path

import pandas as pd
from docling.document_converter import DocumentConverter  # type: ignore[import-untyped]

from chonkster._models import PageRecord
from chonkster._convert import to_dataframe

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS: set[str] = {
    ".pdf",
    ".docx",
    ".pptx",
    ".html",
    ".md",
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".bmp",
}


def _empty_dataframe() -> pd.DataFrame:
    """Return an empty DataFrame with the correct PageRecord columns."""
    return pd.DataFrame(columns=pd.Index(PageRecord.model_fields.keys()))


class Chonk:
    """Turn documents into an analytics-ready wide table."""

    def __init__(self) -> None:
        self._converter = DocumentConverter()

    def parse(self, source: Union[str, Path]) -> pd.DataFrame:
        """Parse one file or a folder of documents into a page-grain DataFrame.

        Args:
            source: Path to a single file or a directory containing documents.

        Returns:
            pandas DataFrame with one row per (document, page).
        """
        source = Path(source)

        if source.is_dir():
            files = sorted(f for f in source.rglob("*") if f.suffix.lower() in SUPPORTED_EXTENSIONS)
        elif source.is_file():
            files = [source]
        else:
            logger.warning("Source path does not exist: %s", source)
            return _empty_dataframe()

        if not files:
            logger.warning("No supported documents found in %s", source)
            return _empty_dataframe()

        frames: list[pd.DataFrame] = []

        for filepath in files:
            try:
                result = self._converter.convert(str(filepath))
                df = to_dataframe(result.document)
                frames.append(df)
            except Exception:
                logger.warning("Failed to convert %s, skipping", filepath, exc_info=True)

        if not frames:
            return _empty_dataframe()

        return pd.concat(frames, ignore_index=True)
