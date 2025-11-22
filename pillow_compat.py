"""
Runtime compatibility helpers for Pillow.

Pillow 10 removed ImageDraw.textsize(), but older versions of
Pygments (and potentially other dependencies) still call it.
We monkeypatch a drop-in replacement that proxies to textbbox().
"""

from PIL import ImageDraw


def _add_textsize_backport() -> None:
    """Add a textsize() helper if Pillow no longer exposes it."""
    if hasattr(ImageDraw.ImageDraw, "textsize"):
        return

    def _textsize(self, text, font=None, *args, **kwargs):
        bbox = self.textbbox((0, 0), text, font=font, *args, **kwargs)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    ImageDraw.ImageDraw.textsize = _textsize  # type: ignore[attr-defined]


_add_textsize_backport()
