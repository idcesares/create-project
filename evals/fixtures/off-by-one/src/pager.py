def page(items, number, size):
    """Return page `number` (1-based) of `items`, `size` items per page."""
    start = number * size
    return items[start:start + size]
