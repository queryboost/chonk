"""Tests for PageRecord Pydantic model."""

from __future__ import annotations

from chonkster._models import PageRecord


class TestPageRecord:
    """Tests for the PageRecord model."""

    def test_minimal_fields(self):
        """PageRecord can be created with only required fields."""
        record = PageRecord(doc_id="doc1", page_num=1, page_count=5)
        assert record.doc_id == "doc1"
        assert record.page_num == 1
        assert record.page_count == 5

    def test_defaults(self):
        """Optional fields have sensible defaults."""
        record = PageRecord(doc_id="doc1", page_num=1, page_count=1)
        assert record.doc_hash is None
        assert record.source_mimetype is None
        assert record.page_width is None
        assert record.page_height is None
        assert record.md_text == ""
        assert record.has_header is False
        assert record.has_table is False
        assert record.has_figure is False
        assert record.header_count == 0
        assert record.table_count == 0
        assert record.figure_count == 0
        assert record.text_block_count == 0
        assert record.char_count == 0
        assert record.word_count == 0

    def test_all_fields(self):
        """PageRecord accepts all fields."""
        record = PageRecord(
            doc_id="report",
            doc_hash=42,
            source_mimetype="application/pdf",
            page_num=3,
            page_count=10,
            page_width=612.0,
            page_height=792.0,
            md_text="# Hello\n\nWorld",
            has_header=True,
            has_table=False,
            has_figure=True,
            header_count=1,
            table_count=0,
            figure_count=2,
            text_block_count=3,
            char_count=15,
            word_count=2,
        )
        assert record.doc_id == "report"
        assert record.doc_hash == 42
        assert record.page_width == 612.0
        assert record.has_header is True
        assert record.figure_count == 2

    def test_model_dump(self):
        """model_dump() returns a dict with all fields."""
        record = PageRecord(doc_id="doc1", page_num=1, page_count=1)
        d = record.model_dump()
        assert isinstance(d, dict)
        assert "doc_id" in d
        assert "md_text" in d
        assert len(d) == 17

    def test_model_fields_keys(self):
        """model_fields contains all expected column names."""
        keys = list(PageRecord.model_fields.keys())
        assert "doc_id" in keys
        assert "page_num" in keys
        assert "word_count" in keys
