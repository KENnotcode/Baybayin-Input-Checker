"""Main checker window with an editorial desktop workspace."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from baybayin.models import CheckResult

from . import theme
from .controller import CheckerController
from .widgets import ErrorList, MarkedPreview, SourceEditor, StatusBadge


class BaybayinWindow:
    """Compose the checker as a writing workspace, not a dashboard."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Baybayin / Read the script clearly")
        root.geometry("1080x760")
        root.minsize(800, 620)
        theme.configure(root)
        self.controller = CheckerController(self._render_result)

        main = ttk.Frame(root, padding=(42, 30, 42, 34), style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True)
        self._build_header(main)
        self._build_editor(main)
        self._build_results(main)
        root.bind("<Control-Return>", self._check_from_keyboard)

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="App.TFrame")
        header.pack(fill=tk.X)
        brand = tk.Canvas(header, width=34, height=34, bg=theme.BG,
                          highlightthickness=0)
        brand.pack(side=tk.LEFT, padx=(0, 12))
        brand.create_oval(3, 3, 31, 31, fill=theme.ACCENT, outline="")
        brand.create_text(17, 17, text="ᜊ", fill="#FFFFFF",
                          font=(theme.FONT_BAYBAYIN, 16))
        ttk.Label(header, text="BAYBAYIN / CHECKER",
                  style="Eyebrow.TLabel").pack(side=tk.LEFT)
        ttk.Label(header, text="Ctrl + Enter  to check",
                  style="Body.TLabel").pack(side=tk.RIGHT)

        ttk.Label(parent, text="Read the script clearly.",
                  style="Title.TLabel").pack(anchor=tk.W, pady=(42, 4))
        ttk.Label(
            parent,
            text="A focused workspace for structural validation and transliteration.",
            style="Body.TLabel",
        ).pack(anchor=tk.W)

    def _build_editor(self, parent: ttk.Frame) -> None:
        editor_header = ttk.Frame(parent, style="App.TFrame")
        editor_header.pack(fill=tk.X, pady=(34, 8))
        ttk.Label(editor_header, text="YOUR TEXT",
                  style="Eyebrow.TLabel").pack(side=tk.LEFT)
        ttk.Label(editor_header, text="Baybayin Unicode",
                  style="Body.TLabel").pack(side=tk.RIGHT)

        editor_surface = ttk.Frame(parent, padding=2, style="Panel.TFrame")
        editor_surface.pack(fill=tk.X)
        self.input_text = SourceEditor(editor_surface)
        self.input_text.configure(height=6)
        self.input_text.pack(fill=tk.X)

        actions = ttk.Frame(parent, style="App.TFrame")
        actions.pack(fill=tk.X, pady=(12, 0))
        ttk.Label(
            actions,
            text="Marks, vowels, and consonant clusters are checked in one pass.",
            style="Body.TLabel",
        ).pack(side=tk.LEFT)
        ttk.Button(actions, text="CHECK TEXT", style="Accent.TButton",
                   command=self.check_input).pack(side=tk.RIGHT)

    def _build_results(self, parent: ttk.Frame) -> None:
        divider = tk.Frame(parent, height=1, bg=theme.FIELD)
        divider.pack(fill=tk.X, pady=(38, 22))

        results = ttk.Frame(parent, style="App.TFrame")
        results.pack(fill=tk.BOTH, expand=True)
        results.columnconfigure(0, weight=2)
        results.columnconfigure(1, weight=3)
        results.columnconfigure(2, weight=4)
        results.rowconfigure(1, weight=1)

        ttk.Label(results, text="STATUS", style="Eyebrow.TLabel").grid(
            row=0, column=0, sticky=tk.W
        )
        ttk.Label(results, text="TRANSLITERATION", style="Eyebrow.TLabel").grid(
            row=0, column=1, sticky=tk.W, padx=(28, 0)
        )
        ttk.Label(results, text="DIAGNOSTICS", style="Eyebrow.TLabel").grid(
            row=0, column=2, sticky=tk.W, padx=(28, 0)
        )

        self.status = StatusBadge(results)
        self.status.grid(row=1, column=0, sticky="new", pady=(10, 0))
        self.transliteration = tk.Label(
            results, text="Nothing checked yet", anchor=tk.NW, justify=tk.LEFT,
            wraplength=300, background=theme.BG, foreground=theme.TEXT,
            font=(theme.FONT_MONO, 14),
        )
        self.transliteration.grid(row=1, column=1, sticky="new",
                                  padx=(28, 0), pady=(10, 0))
        self.errors = ErrorList(results)
        self.errors.grid(row=1, column=2, sticky="nsew", padx=(28, 0), pady=(10, 0))
        self.highlighted = MarkedPreview(results)
        self.highlighted.grid(row=2, column=0, columnspan=3, sticky="ew",
                              pady=(22, 0))

    def _check_from_keyboard(self, _event: tk.Event) -> str:
        self.check_input()
        return "break"

    def check_input(self) -> None:
        text = self.input_text.get("1.0", "end-1c")
        self.controller.check_text(text)

    def _render_result(self, result: CheckResult) -> None:
        text = self.input_text.get("1.0", "end-1c")
        self.status.show(result)
        self.transliteration.configure(text=result.transliteration or "No readable syllables")
        self.highlighted.show(text, result)
        self.errors.show(text, result)
