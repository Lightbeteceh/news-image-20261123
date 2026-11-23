"""Entry point: render the 23 November 2026 news image.

Reads stories.json next to this file, draws the newspaper page with
render.py and writes entry.png. Deterministic: same input bytes give
the same output bytes. No network, no clocks, no randomness.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import main as _render_main  # noqa: E402


def main():
    _render_main()


if __name__ == "__main__":
    main()
