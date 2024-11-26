from tkinter.messagebox import showerror
from traceback import format_exc

from mcb.src.my_clip_board import MyClipBoard

def main():
    mcb = MyClipBoard()
    nmsp = mcb.parse_args()
    mcb.decision_tree(
        args=nmsp
    )

try:
    main()
except Exception as e:
    print(format_exc())
    showerror(
        title="Exception occured",
        message=f"{type(e)}: {e}"
    )