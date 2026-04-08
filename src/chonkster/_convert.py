"""Transform DoclingDocument into a page-grain analytics table."""

from __future__ import annotations

from docling_core.types.doc.document import (
    DocItem,
    TextItem,
    TableItem,
    TitleItem,
    PictureItem,
    DoclingDocument,
    SectionHeaderItem,
)

from chonkster._models import PageRecord


def to_page_table(doc: DoclingDocument) -> list[PageRecord]:
    """Convert a DoclingDocument to a list of PageRecords (one per page).

    Args:
        doc: A parsed DoclingDocument.

    Returns:
        List of PageRecord, one per page, sorted by page_num.
    """
    page_count = len(doc.pages)
    if page_count == 0:
        return []

    # pre-compute per-page stats by iterating items once
    page_stats: dict[int, dict] = {
        pn: {
            "header_count": 0,
            "table_count": 0,
            "figure_count": 0,
            "text_block_count": 0,
        }
        for pn in doc.pages
    }

    for item, _level in doc.iterate_items():
        if not isinstance(item, DocItem) or not item.prov:
            continue
        pn = item.prov[0].page_no
        if pn not in page_stats:
            continue

        stats = page_stats[pn]
        if isinstance(item, (SectionHeaderItem, TitleItem)):
            stats["header_count"] += 1
        elif isinstance(item, TableItem):
            stats["table_count"] += 1
        elif isinstance(item, PictureItem):
            stats["figure_count"] += 1

        if isinstance(item, TextItem):
            stats["text_block_count"] += 1

    # build one record per page
    records: list[PageRecord] = []
    for pn in sorted(doc.pages):
        page_item = doc.pages[pn]
        md_text = doc.export_to_markdown(page_no=pn)
        stats = page_stats[pn]

        records.append(
            PageRecord(
                doc_id=doc.name,
                doc_hash=doc.origin.binary_hash if doc.origin else None,
                source_mimetype=doc.origin.mimetype if doc.origin else None,
                page_num=pn,
                page_count=page_count,
                page_width=page_item.size.width if page_item.size else None,
                page_height=page_item.size.height if page_item.size else None,
                md_text=md_text,
                has_header=stats["header_count"] > 0,
                has_table=stats["table_count"] > 0,
                has_figure=stats["figure_count"] > 0,
                header_count=stats["header_count"],
                table_count=stats["table_count"],
                figure_count=stats["figure_count"],
                text_block_count=stats["text_block_count"],
                char_count=len(md_text),
                word_count=len(md_text.split()) if md_text.strip() else 0,
            )
        )

    return records


def to_dataframe(doc: DoclingDocument):
    """Convert a DoclingDocument to a pandas DataFrame with page grain.

    Args:
        doc: A parsed DoclingDocument.

    Returns:
        pandas.DataFrame with one row per page.
    """
    import pandas as pd

    records = to_page_table(doc)
    return pd.DataFrame([r.model_dump() for r in records])
