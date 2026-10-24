"""Centralized visual tokens and Tk widget styles."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

BG = "#F4F0E8"
SURFACE = "#FFFCF5"
FIELD = "#EAE3D6"
FIELD_ACTIVE = "#DDD2C1"
TEXT = "#25221E"
MUTED = "#6D665D"
SUBTLE = "#918779"
ACCENT = "#C85B38"
ACCENT_HOVER = "#A9472B"
SUCCESS = "#3F765A"
ERROR = "#B84E42"
WARNING = "#A26A2D"
FOCUS = "#C85B38"
MARK = "#E9A69A"

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
    style.configure("Accent.TButton", background=ACCENT, foreground="#FFFFFF",
                    font=(FONT_UI, 10, "bold"), padding=(24, 12),
                    borderwidth=0, relief=tk.FLAT)
    style.map("Accent.TButton", background=[("active", ACCENT_HOVER),
                                             ("pressed", ACCENT)])
