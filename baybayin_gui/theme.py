"""Centralized visual tokens and Tk widget styles."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

BG = "#0D1117"
SURFACE = "#151C24"
FIELD = "#1B2632"
FIELD_ACTIVE = "#293847"
TEXT = "#F2EEE6"
MUTED = "#A4AFB8"
SUBTLE = "#748290"
ACCENT = "#D6A84F"
ACCENT_HOVER = "#E7BB67"
SUCCESS = "#3F8A63"
ERROR = "#B95B50"
WARNING = "#B9853E"
FOCUS = "#D6A84F"
MARK = "#70423D"

FONT_UI = "Segoe UI"
FONT_MONO = "Consolas"
FONT_BAYBAYIN = "Noto Sans Tagalog"


def configure(root: tk.Tk) -> None:
    root.configure(background=BG)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("App.TFrame", background=BG)
    style.configure("Panel.TFrame", background=SURFACE)
    style.configure("Eyebrow.TLabel", background=BG, foreground=ACCENT,
                    font=(FONT_UI, 9, "bold"))
    style.configure("Title.TLabel", background=BG, foreground=TEXT,
                    font=(FONT_UI, 28, "bold"))
    style.configure("Body.TLabel", background=BG, foreground=MUTED,
                    font=(FONT_UI, 10))
    style.configure("PanelTitle.TLabel", background=SURFACE, foreground=TEXT,
                    font=(FONT_UI, 11, "bold"))
    style.configure("PanelMeta.TLabel", background=SURFACE, foreground=SUBTLE,
                    font=(FONT_UI, 9))
    style.configure("Accent.TButton", background=ACCENT, foreground=BG,
                    font=(FONT_UI, 10, "bold"), padding=(24, 12),
                    borderwidth=0, relief=tk.FLAT)
    style.map("Accent.TButton", background=[("active", ACCENT_HOVER),
                                             ("pressed", ACCENT)])
