# -*- encoding: utf-8 -*-

CATEGORY_CHOICES = (
    ('FICTION', 'Fiction'),
    ('NONFICTION', 'Non-Fiction'),
)

CATEGORY_CHOICES_WITH_BLANK = [('', '')] + list(CATEGORY_CHOICES)

CATEGORY_CODE_MAP = {
    'FICTION': 'Fiction',
    'NONFICTION': 'Non-Fiction',
}
