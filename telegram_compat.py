"""
Compatibility helpers for python-telegram-bot on newer Python runtimes.

python-telegram-bot<=20.7 defines __slots__ on telegram.ext.Updater but forgets
to reserve one for ``__polling_cleanup_cb``. Python 3.13 enforces slots more
strictly and raises AttributeError when that attribute is assigned.
"""

from __future__ import annotations

from typing import Any, Optional
from weakref import WeakKeyDictionary


def patch_updater_slots() -> bool:
    """Ensure the Updater class can store __polling_cleanup_cb on Python 3.13."""
    try:
        from telegram.ext import _updater as _telegram_updater  # type: ignore
    except Exception:
        return False

    updater_cls = getattr(_telegram_updater, "Updater", None)
    if updater_cls is None:
        return False

    missing_slot = "__polling_cleanup_cb"
    slots = getattr(updater_cls, "__slots__", ())

    # First try to append the missing slot like upstream should have done.
    if isinstance(slots, tuple) and missing_slot not in slots:
        try:
            updater_cls.__slots__ = slots + (missing_slot,)
            return True
        except (TypeError, AttributeError):
            # Python refuses to mutate __slots__ post-class-creation; fall back
            # to a descriptor-based emulation below.
            pass

    # If adding to __slots__ failed (or slots are not a tuple), emulate the slot
    # via a descriptor that stores the value in a WeakKeyDictionary.
    mangled_name = f"_{updater_cls.__name__}{missing_slot}"

    if hasattr(updater_cls, mangled_name):
        # Already patched (descriptor exists) or upstream fixed it.
        return False

    _cleanup_store: "WeakKeyDictionary[Any, Optional[Any]]" = WeakKeyDictionary()

    def _get_cleanup_cb(self: Any) -> Optional[Any]:
        return _cleanup_store.get(self)

    def _set_cleanup_cb(self: Any, value: Optional[Any]) -> None:
        _cleanup_store[self] = value

    def _del_cleanup_cb(self: Any) -> None:
        _cleanup_store.pop(self, None)

    setattr(updater_cls, mangled_name, property(
        _get_cleanup_cb, _set_cleanup_cb, _del_cleanup_cb,
        "Compat descriptor injected for python-telegram-bot Updater.__polling_cleanup_cb"
    ))
    return True


__all__ = ["patch_updater_slots"]
