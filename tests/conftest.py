"""Pytest configuration and shared fixtures for chonkster tests."""

from __future__ import annotations

from unittest.mock import Mock, MagicMock

import pytest
from docling_core.types.doc.document import DocumentOrigin, DoclingDocument


@pytest.fixture
def mock_docling_document():
    """Create a minimal DoclingDocument for testing conversion logic."""
    doc = DoclingDocument(name="test-doc")
    origin = DocumentOrigin(
        filename="test-doc.pdf",
        mimetype="application/pdf",
        binary_hash=123456789,
    )
    doc.origin = origin
    return doc


@pytest.fixture
def mock_converter():
    """Create a mock DocumentConverter that returns a canned result."""
    converter = MagicMock()
    result = Mock()

    doc = DoclingDocument(name="mock-doc")
    origin = DocumentOrigin(
        filename="mock-doc.pdf",
        mimetype="application/pdf",
        binary_hash=987654321,
    )
    doc.origin = origin
    result.document = doc

    converter.convert.return_value = result
    return converter
