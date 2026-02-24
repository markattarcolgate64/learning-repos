# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Cursor-based Pagination
========================

System:
    A cursor-based paginator for an API that returns pages of results from a
    sorted dataset. Instead of page numbers, callers pass an opaque cursor
    string to fetch the next page. The cursor encodes the index of the last
    item returned so the server knows where to resume.

    The paginator provides:
        - items: the list of items for the current page
        - next_cursor: an opaque cursor to fetch the next page (None if no more)
        - has_next_page: boolean

Expected behavior:
    - Paginating through the full dataset should return every item exactly once.
    - No item should be duplicated across pages.
    - No item should be skipped.
    - has_next_page should be True when more items exist, False on the last page.
    - next_cursor should be None on the last page.

Symptoms:
    Tests are failing because paginating through the dataset produces
    duplicate items (the last item of one page appears again as the first
    item of the next page). Additionally, has_next_page may report incorrectly
    on the final page.
"""

import base64
import json
import unittest


class Page:
    """Represents a single page of results."""

    def __init__(self, items, next_cursor, has_next_page):
        self.items = items
        self.next_cursor = next_cursor
        self.has_next_page = has_next_page

    def __repr__(self):
        return (
            f"Page(items={self.items!r}, next_cursor={self.next_cursor!r}, "
            f"has_next_page={self.has_next_page})"
        )


def encode_cursor(index):
    """Encode an integer index into an opaque cursor string."""
    payload = json.dumps({"idx": index})
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_cursor(cursor):
    """Decode an opaque cursor string back to an integer index."""
    payload = base64.urlsafe_b64decode(cursor.encode()).decode()
    data = json.loads(payload)
    return data["idx"]


def paginate(dataset, page_size, cursor=None):
    """
    Return a Page of results from `dataset`.

    Args:
        dataset:   a list of items (assumed sorted/stable order).
        page_size: maximum number of items per page.
        cursor:    opaque cursor from a previous Page, or None for the first page.

    Returns:
        A Page object.
    """
    if cursor is None:
        start = 0
    else:
        # The cursor stores the index of the last item we returned.
        # We should start from the NEXT item.
        last_index = decode_cursor(cursor)
        start = last_index  # resume from this index

    end = start + page_size
    items = dataset[start:end]

    # Determine if there is a next page
    has_next_page = end < len(dataset)

    if has_next_page:
        # Store the last index we returned so the next call can resume after it
        next_cursor = encode_cursor(end - 1)
    else:
        next_cursor = None

    return Page(items=items, next_cursor=next_cursor, has_next_page=has_next_page)


# ---------------------------------------------------------------------------
# Tests -- these should PASS once the bug is fixed
# ---------------------------------------------------------------------------

class TestCursorPagination(unittest.TestCase):

    def _collect_all(self, dataset, page_size):
        """Helper: paginate through the entire dataset collecting all items."""
        all_items = []
        cursor = None
        pages = 0
        max_pages = len(dataset) + 1  # safety limit

        while True:
            page = paginate(dataset, page_size, cursor)
            all_items.extend(page.items)
            pages += 1

            if not page.has_next_page:
                break
            cursor = page.next_cursor
            if pages > max_pages:
                self.fail("Infinite loop detected in pagination")

        return all_items, pages

    def test_paginate_exact_fit(self):
        """Dataset size is an exact multiple of page_size."""
        dataset = list(range(10))
        items, pages = self._collect_all(dataset, page_size=5)
        self.assertEqual(items, dataset, "All items should be returned in order")
        self.assertEqual(pages, 2)

    def test_paginate_with_remainder(self):
        """Dataset size is NOT a multiple of page_size."""
        dataset = list(range(7))
        items, pages = self._collect_all(dataset, page_size=3)
        self.assertEqual(items, dataset, "All items should be returned in order")
        self.assertEqual(pages, 3)  # 3 + 3 + 1

    def test_no_duplicates(self):
        """No item should appear on more than one page."""
        dataset = list(range(20))
        items, _ = self._collect_all(dataset, page_size=6)
        self.assertEqual(
            len(items),
            len(set(items)),
            f"Duplicate items found: {items}",
        )
        self.assertEqual(len(items), 20)

    def test_has_next_page_false_on_last(self):
        """has_next_page should be False on the very last page."""
        dataset = list(range(5))
        page = paginate(dataset, page_size=5)
        self.assertFalse(
            page.has_next_page,
            "Only one page of data; has_next_page should be False",
        )
        self.assertIsNone(page.next_cursor)

    def test_single_item_pages(self):
        """page_size=1 should work correctly."""
        dataset = ["a", "b", "c"]
        items, pages = self._collect_all(dataset, page_size=1)
        self.assertEqual(items, dataset)
        self.assertEqual(pages, 3)

    def test_empty_dataset(self):
        """Empty dataset should return one empty page with no next."""
        page = paginate([], page_size=5)
        self.assertEqual(page.items, [])
        self.assertFalse(page.has_next_page)
        self.assertIsNone(page.next_cursor)

    def test_cursor_round_trip(self):
        """Fetching page 1, then using its cursor for page 2, gives correct items."""
        dataset = list(range(10))
        page1 = paginate(dataset, page_size=4)
        self.assertEqual(page1.items, [0, 1, 2, 3])

        page2 = paginate(dataset, page_size=4, cursor=page1.next_cursor)
        self.assertEqual(page2.items, [4, 5, 6, 7])

        page3 = paginate(dataset, page_size=4, cursor=page2.next_cursor)
        self.assertEqual(page3.items, [8, 9])
        self.assertFalse(page3.has_next_page)


if __name__ == "__main__":
    unittest.main()
