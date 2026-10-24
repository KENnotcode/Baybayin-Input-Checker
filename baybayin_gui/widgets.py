"""Reusable Tk widgets for the checker workspace."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from baybayin.models import CheckResult

from . import theme


class SourceEditor(tk.Text):
    """Baybayin input editor with a visible error mark style."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(
            parent, height=7, wrap=tk.WORD, font=(theme.FONT_BAYBAYIN, 24),
            undo=True, background=theme.FIELD, foreground=theme.TEXT,
            insertbackground=theme.ACCENT, selectbackground=theme.FIELD_ACTIVE,
            relief=tk.FLAT, padx=12, pady=12, highlightthickness=1,
            highlightbackground=theme.FIELD, highlightcolor=theme.FOCUS,
        )
        self.tag_configure("offending", background=theme.MARK)


class MarkedPreview(tk.Text):
    """Read-only source preview with offending indexes highlighted."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(
            parent, height=2, wrap=tk.WORD, font=(theme.FONT_BAYBAYIN, 18),
            state=tk.DISABLED, background=theme.FIELD, foreground=theme.TEXT,
            relief=tk.FLAT, padx=8, pady=7, highlightthickness=0,
        )
        self.tag_configure("offending", background=theme.MARK)

    def show(self, text: str, result: CheckResult) -> None:
        self.configure(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        indexes = {error.index for error in result.errors}
        for index, character in enumerate(text):
            start = self.index("end-1c")
            self.insert(tk.END, character)
            if index in indexes:
                self.tag_add("offending", start, "end-1c")
        self.configure(state=tk.DISABLED)


class StatusBadge(tk.Label):
    """Compact state badge for empty, valid, and invalid results."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(
            parent, anchor=tk.W, padx=12, pady=9, background=theme.FIELD,
            foreground=theme.MUTED, font=(theme.FONT_UI, 11, "bold"),
        )

    def show(self, result: CheckResult) -> None:
        if result.valid and result.warnings:
            label, color = "Valid with warnings", theme.WARNING
        elif result.valid:
            label, color = "Valid", theme.SUCCESS
        else:
            label, color = "Invalid", theme.ERROR
        self.configure(text=label, background=color, foreground="white")


class ErrorList(tk.Text):
    """Read-only, wrapped diagnostic messages."""

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(
            parent, height=8, wrap=tk.WORD, state=tk.DISABLED,
            background=theme.FIELD, foreground=theme.TEXT,
            relief=tk.FLAT, borderwidth=0, highlightthickness=0,
            font=(theme.FONT_UI, 9), padx=10, pady=8,
        )

    def show(self, text: str, result: CheckResult) -> None:
        self.configure(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        for error in result.errors:
            character = text[error.index] if error.index < len(text) else "?"
            self.insert(
                tk.END,
                f"Character {error.index + 1} ({character}) — {error.message}",
            )
            self.insert(tk.END, "\n\n")
        if not result.errors:
            self.insert("1.0", "No structural or word-shape errors.")
        self.configure(state=tk.DISABLED)
