"""Tests for the Chonk class."""

from __future__ import annotations

from unittest.mock import patch

import pandas as pd
from docling_core.types.doc.base import Size

from chonkster import Chonk
from chonkster._models import PageRecord


class TestChonkInit:
    """Tests for Chonk initialization."""

    @patch("chonkster._chonk.DocumentConverter")
    def test_converter_created_once(self, mock_dc_cls):
        """DocumentConverter is instantiated at init time."""
        ck = Chonk()
        mock_dc_cls.assert_called_once()
        assert ck._converter is mock_dc_cls.return_value


class TestChonkParse:
    """Tests for Chonk.parse()."""

    @patch("chonkster._chonk.DocumentConverter")
    def test_nonexistent_path(self, mock_dc_cls, tmp_path):  # noqa: ARG002
        """Returns empty DataFrame for a path that doesn't exist."""
        ck = Chonk()
        df = ck.parse(tmp_path / "nonexistent")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert list(df.columns) == list(PageRecord.model_fields.keys())

    @patch("chonkster._chonk.DocumentConverter")
    def test_empty_directory(self, mock_dc_cls, tmp_path):  # noqa: ARG002
        """Returns empty DataFrame for a directory with no supported files."""
        ck = Chonk()
        df = ck.parse(tmp_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    @patch("chonkster._chonk.DocumentConverter")
    def test_single_file(self, mock_dc_cls, tmp_path, mock_docling_document):
        """Parses a single file correctly."""
        mock_docling_document.add_page(page_no=1, size=Size())

        mock_instance = mock_dc_cls.return_value
        mock_result = mock_instance.convert.return_value
        mock_result.document = mock_docling_document

        pdf = tmp_path / "test.pdf"
        pdf.touch()

        ck = Chonk()
        df = ck.parse(pdf)
        assert len(df) == 1
        mock_instance.convert.assert_called_once_with(str(pdf))

    @patch("chonkster._chonk.DocumentConverter")
    def test_directory_with_files(self, mock_dc_cls, tmp_path, mock_docling_document):
        """Discovers and parses all supported files in a directory."""
        mock_docling_document.add_page(page_no=1, size=Size())

        mock_instance = mock_dc_cls.return_value
        mock_result = mock_instance.convert.return_value
        mock_result.document = mock_docling_document

        (tmp_path / "a.pdf").touch()
        (tmp_path / "b.docx").touch()
        (tmp_path / "skip.txt").touch()

        ck = Chonk()
        df = ck.parse(tmp_path)
        assert mock_instance.convert.call_count == 2

    @patch("chonkster._chonk.DocumentConverter")
    def test_skips_unsupported_extensions(self, mock_dc_cls, tmp_path, mock_docling_document):
        """Files with unsupported extensions are ignored."""
        mock_docling_document.add_page(page_no=1, size=Size())

        mock_instance = mock_dc_cls.return_value
        mock_result = mock_instance.convert.return_value
        mock_result.document = mock_docling_document

        (tmp_path / "data.csv").touch()
        (tmp_path / "notes.txt").touch()

        ck = Chonk()
        df = ck.parse(tmp_path)
        assert len(df) == 0
        mock_instance.convert.assert_not_called()

    @patch("chonkster._chonk.DocumentConverter")
    def test_conversion_error_skips_file(self, mock_dc_cls, tmp_path):
        """Files that fail conversion are skipped with a warning."""
        mock_instance = mock_dc_cls.return_value
        mock_instance.convert.side_effect = RuntimeError("bad file")

        (tmp_path / "bad.pdf").touch()

        ck = Chonk()
        df = ck.parse(tmp_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    @patch("chonkster._chonk.DocumentConverter")
    def test_recursive_discovery(self, mock_dc_cls, tmp_path, mock_docling_document):
        """Discovers files in subdirectories."""
        mock_docling_document.add_page(page_no=1, size=Size())

        mock_instance = mock_dc_cls.return_value
        mock_result = mock_instance.convert.return_value
        mock_result.document = mock_docling_document

        subdir = tmp_path / "nested"
        subdir.mkdir()
        (subdir / "deep.pdf").touch()

        ck = Chonk()
        df = ck.parse(tmp_path)
        assert mock_instance.convert.call_count == 1

    @patch("chonkster._chonk.DocumentConverter")
    def test_string_path_accepted(self, mock_dc_cls, tmp_path, mock_docling_document):
        """parse() accepts string paths, not just Path objects."""
        mock_docling_document.add_page(page_no=1, size=Size())

        mock_instance = mock_dc_cls.return_value
        mock_result = mock_instance.convert.return_value
        mock_result.document = mock_docling_document

        pdf = tmp_path / "test.pdf"
        pdf.touch()

        ck = Chonk()
        df = ck.parse(str(pdf))
        assert len(df) == 1
