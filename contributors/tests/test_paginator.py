from django.test import SimpleTestCase

from contributors.views.mixins import (
    INNER_VISIBLE_PAGES,
    MAX_PAGES_WITHOUT_SHRINKING,
    PAGES_VISIBLE_AT_BOUNDARY,
    get_page_slice,
)


class PaginatorTests(SimpleTestCase):
    """A test suite for paginator slices."""

    def test_returns_all_pages_at_small_num_of_them(self):
        num_pages = MAX_PAGES_WITHOUT_SHRINKING
        self.assertEqual(
            get_page_slice(current_page=3, num_pages=num_pages),
            slice(0, num_pages),
        )

    def test_returns_first_several_pages(self):
        self.assertEqual(
            get_page_slice(
                current_page=PAGES_VISIBLE_AT_BOUNDARY // 2,
                num_pages=MAX_PAGES_WITHOUT_SHRINKING + 1,
            ),
            slice(0, PAGES_VISIBLE_AT_BOUNDARY),
        )

    def test_returns_last_several_pages(self):
        num_pages = MAX_PAGES_WITHOUT_SHRINKING + 1
        self.assertEqual(
            get_page_slice(
                current_page=num_pages - PAGES_VISIBLE_AT_BOUNDARY // 2,
                num_pages=num_pages,
            ),
            slice(
                num_pages - PAGES_VISIBLE_AT_BOUNDARY,
                num_pages,
            ),
        )

    def test_returns_some_inner_pages(self):
        current_page = MAX_PAGES_WITHOUT_SHRINKING
        start_index = current_page - 1 - INNER_VISIBLE_PAGES // 2
        self.assertEqual(
            get_page_slice(
                current_page=current_page,
                num_pages=MAX_PAGES_WITHOUT_SHRINKING * 2,
            ),
            slice(start_index, start_index + INNER_VISIBLE_PAGES),
        )

    def test_returns_inner_at_boundary_minus_one(self):
        self.assertEqual(
            get_page_slice(
                current_page=5,
                num_pages=10,
                max_pages_without_shrinking=8,
                pages_visible_at_boundary=5,
                inner_visible_pages=3,
            ),
            slice(3, 6),
        )
