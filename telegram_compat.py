"""
Compatibility helpers for python-telegram-bot on newer Python runtimes.

python-telegram-bot<=20.7 defines __slots__ on telegram.ext.Updater but forgets
to reserve one for ``__polling_cleanup_cb``. Python 3.13 enforces slots more
strictly and raises AttributeError when that attribute is assigned.
"""


def patch_updater_slots() -> bool:
    """Ensure the Updater class has a slot for __polling_cleanup_cb."""
    try:
        from telegram.ext import _updater as _telegram_updater  # type: ignore
    except Exception:
        return False

    missing_slot = "__polling_cleanup_cb"
    slots = getattr(_telegram_updater.Updater, "__slots__", ())

    if isinstance(slots, tuple) and missing_slot not in slots:
        _telegram_updater.Updater.__slots__ = slots + (missing_slot,)
        return True

    return False


__all__ = ["patch_updater_slots"]
