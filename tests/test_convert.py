"""Tests for the document conversion functions."""

from __future__ import annotations

import pandas as pd
from docling_core.types.doc.base import Size

from chonkster._models import PageRecord
from chonkster._convert import to_dataframe, to_page_table


class TestToPageTable:
    """Tests for to_page_table()."""

    def test_empty_pages(self, mock_docling_document):
        """Returns empty list when document has no pages."""
        result = to_page_table(mock_docling_document)
        assert result == []

    def test_returns_page_records(self, mock_docling_document):
        """Each element in the result is a PageRecord."""
        # Add a page to the document
        mock_docling_document.add_page(page_no=1, size=Size())
        records = to_page_table(mock_docling_document)
        assert len(records) == 1
        assert isinstance(records[0], PageRecord)

    def test_page_count_matches(self, mock_docling_document):
        """page_count reflects total number of pages."""
        mock_docling_document.add_page(page_no=1, size=Size())
        mock_docling_document.add_page(page_no=2, size=Size())
        records = to_page_table(mock_docling_document)
        assert len(records) == 2
        assert all(r.page_count == 2 for r in records)

    def test_doc_id_from_name(self, mock_docling_document):
        """doc_id comes from the document name."""
        mock_docling_document.add_page(page_no=1, size=Size())
        records = to_page_table(mock_docling_document)
        assert records[0].doc_id == "test-doc"

    def test_origin_fields(self, mock_docling_document):
        """doc_hash and source_mimetype populated from origin."""
        mock_docling_document.add_page(page_no=1, size=Size())
        records = to_page_table(mock_docling_document)
        assert records[0].doc_hash == 123456789
        assert records[0].source_mimetype == "application/pdf"

    def test_pages_sorted_by_page_num(self, mock_docling_document):
        """Records are returned sorted by page number."""
        mock_docling_document.add_page(page_no=3, size=Size())
        mock_docling_document.add_page(page_no=1, size=Size())
        mock_docling_document.add_page(page_no=2, size=Size())
        records = to_page_table(mock_docling_document)
        page_nums = [r.page_num for r in records]
        assert page_nums == [1, 2, 3]


class TestToDataframe:
    """Tests for to_dataframe()."""

    def test_returns_dataframe(self, mock_docling_document):
        """Returns a pandas DataFrame."""
        mock_docling_document.add_page(page_no=1, size=Size())
        df = to_dataframe(mock_docling_document)
        assert isinstance(df, pd.DataFrame)

    def test_empty_document(self, mock_docling_document):
        """Empty document produces empty DataFrame."""
        df = to_dataframe(mock_docling_document)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_columns_match_model(self, mock_docling_document):
        """DataFrame columns match PageRecord fields."""
        mock_docling_document.add_page(page_no=1, size=Size())
        df = to_dataframe(mock_docling_document)
        expected = list(PageRecord.model_fields.keys())
        assert list(df.columns) == expected

    def test_row_count_matches_pages(self, mock_docling_document):
        """One row per page."""
        mock_docling_document.add_page(page_no=1, size=Size())
        mock_docling_document.add_page(page_no=2, size=Size())
        df = to_dataframe(mock_docling_document)
        assert len(df) == 2
