from __future__ import annotations
import tkinter as tk
from baybayin_gui.window import BaybayinWindow

BaybayinApp = BaybayinWindow
def main() -> None:
    root = tk.Tk()
    BaybayinWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()