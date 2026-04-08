"""Pydantic models for chonkster output tables."""

from __future__ import annotations

from typing import Optional

from pydantic import Field, BaseModel


class PageRecord(BaseModel):
    """One row per (document, page). Analytics-ready grain."""

    # identifiers
    doc_id: str = Field(description="Document identifier (filename without extension)")
    doc_hash: Optional[int] = Field(default=None, description="Binary hash of source document")
    source_mimetype: Optional[str] = Field(default=None, description="MIME type of source document")
    page_num: int = Field(description="1-indexed page number")
    page_count: int = Field(description="Total pages in the document")

    # page dimensions
    page_width: Optional[float] = None
    page_height: Optional[float] = None

    # markdown text
    md_text: str = Field(default="", description="Markdown rendering of page content")

    # content flags
    has_header: bool = False
    has_table: bool = False
    has_figure: bool = False

    # content counts
    header_count: int = 0
    table_count: int = 0
    figure_count: int = 0
    text_block_count: int = 0

    # text metrics
    char_count: int = 0
    word_count: int = 0
