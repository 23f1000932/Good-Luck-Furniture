import re
from slugify import slugify as _slugify


def generate_slug(text):
    """Generate a URL-friendly slug from text."""
    return _slugify(text, max_length=200, word_boundary=True)


def unique_slug(text, model_class, existing_id=None):
    """
    Generate a unique slug for the given model class.
    If existing_id is given, ignore that record (for edit scenarios).
    """
    base = generate_slug(text)
    slug = base
    counter = 1

    while True:
        query = model_class.query.filter_by(slug=slug)
        if existing_id:
            query = query.filter(model_class.id != existing_id)
        if not query.first():
            return slug
        slug = f'{base}-{counter}'
        counter += 1
