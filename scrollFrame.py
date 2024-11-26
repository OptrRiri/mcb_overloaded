import platform
import tkinter as tk
import tkinter.ttk as ttk

import mcb.src.tkBind as tkBind

class ScrollFrame(ttk.Frame):
    def __init__(
        self,
        master: ttk.Frame
    ) -> None:
        super().__init__(
            master=master
        )
        
        self.canvas = tk.Canvas(
            master=self,
            borderwidth=0,
            background="#ffffff"
        )
        self.viewPort = ttk.Frame(
            master=self.canvas
        )
        self.verticalScrollBar = tk.Scrollbar(
            master=self,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )
        self.canvas.configure(
            yscrollcommand=self.verticalScrollBar.set
        )
        self.verticalScrollBar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )
        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )
        self.canvas_window = self.canvas.create_window(
            (4, 4),
            window=self.viewPort,
            anchor=tk.NW,
            tags="self.viewPort"
        )
        self.viewPort.bind(
            sequence=tkBind.WIDGET_CONFIGURE, 
            func=self.onFrameConfigure
        )
        self.canvas.bind(
            sequence=tkBind.WIDGET_CONFIGURE, 
            func=self.onCanvasConfigure
        )

        self.viewPort.bind(
            sequence=tkBind.WIDGET_ENTER, 
            func=self.onEnter
        )
        self.viewPort.bind(
            sequence=tkBind.WIDGET_LEAVE, 
            func=self.onLeave
        )

        self.onFrameConfigure(event=None)
    
    def onFrameConfigure(
        self,
        event: tk.Event
    ):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def onCanvasConfigure(
        self,
        event: tk.Event
    ):
        canvas_width = event.width
        self.canvas.itemconfig(
            tagOrId=self.canvas_window,
            width=canvas_width
        )

    def onMouseWheel(
        self,
        event: tk.Event
    ):
        if platform.system() == "Windows":
            self.canvas.yview_scroll(
                number=int(-1 * (event.delta/120)),
                what=tk.UNITS
            )
        
        elif platform.system() == "Darwin":
            self.canvas.yview_scroll(
                number=int(-1 * event.delta),
                what=tk.UNITS
            )
        
        else:
            if event.num == 4:
                self.canvas.yview_scroll(
                    number=-1,
                    what=tk.UNITS
                )
            
            elif event.num == 5:
                self.canvas.yview_scroll(
                    number=1,
                    what=tk.UNITS
                )

    def onEnter(
        self,
        event: tk.Event
    ):
        if platform.system() == "Linux":
            self.canvas.bind_all(
                sequence=tkBind.SCROLLWHEEL_UP,
                func=self.onMouseWheel
            )
            self.canvas.bind_all(
                sequence=tkBind.SCROLLWHEEL_DOWN,
                func=self.onMouseWheel
            )

        else:
            self.canvas.bind_all(
                sequence=tkBind.SCROLLWHEEL,
                func=self.onMouseWheel
            )

    def onLeave(
        self,
        event: tk.Event
    ): 
        if platform.system() == 'Linux':
            self.canvas.unbind_all(tkBind.SCROLLWHEEL_UP)
            self.canvas.unbind_all(tkBind.SCROLLWHEEL_DOWN)
        else:
            self.canvas.unbind_all(tkBind.SCROLLWHEEL)