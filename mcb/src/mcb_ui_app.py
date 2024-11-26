import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Style

import pyperclip
from typing import Callable

from mcb.src.my_clip_board import MyClipBoard
from mcb.src.scrollFrame import ScrollFrame
import mcb.src.tkBind as tkBind
from mcb.vars.vscode_dark_palette import VsCodeDarkPalette

# to do:
# complete record searching widget
# (done) complete keyword searching widget
# (done) complete record use history widget
# complete keyword creation history widget
# enable deleting record/keyword for all 4 widgets
# enable copying keyword/record itself (without running through mcb) for all 4 widgets
# refresh all button (or on F5)

class McbApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('mcb')
        self.styling()
        self.createWidgets(
            root=self.root
        )
        self.ignoreCaps = True

    def styling(self):
        style = Style()
        style.configure(
            style='result.TButton',
            background=VsCodeDarkPalette.c1,
            foreground="#FFFFFF"
        )
    
    def createWidgets(
        self,
        root: tk.Tk
    ):
        keyword_frm = ttk.Frame(
            master=root
        )
        keyword_frm.grid(
            row=0,
            column=0
        )
        
        keyword_header_lbl = ttk.Label(
            master=keyword_frm,
            text="Keywords",
            background=VsCodeDarkPalette.c4,
            foreground="#FFFFFF"
        )
        keyword_header_lbl.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )
        
        keyword_search_frm = ttk.Frame(
            master=keyword_frm
        )
        keyword_search_frm.grid(
            row=1,
            column=0,
            rowspan=9,
            sticky="w"
        )
        keyword_search_ent, keyword_search_results_srm = self.createSearch(
            master=keyword_search_frm,
            search_enter_func=self.performSearch_keyword
        )

        '''keyword_debug_frm = ttk.Frame(master=root)
        keyword_debug_frm.grid(
            row=0,
            column=1,
            rowspan=9,
            sticky="w"
        )
        keyword_debug_lbl = ttk.Label(master=keyword_debug_frm, text="boop")
        keyword_debug_lbl.grid(
            row=0,
            column=0,
            rowspan=9,
            sticky="w"
        )'''
        keyword_chronoCreate_srm = ScrollFrame(
            master=root
        )
        keyword_chronoCreate_srm.grid(
            row=0,
            column=1,
            rowspan=9,
            sticky="nw"
        )
        self.all_keyword_created(
            results_srm=keyword_chronoCreate_srm
        )

        record_frm = ttk.Frame(
            master=root
        )
        record_frm.grid(
            row=1,
            column=0
        )

        record_header_lbl = ttk.Label(
            master=record_frm,
            text="Records",
            background=VsCodeDarkPalette.c4,
            foreground="#FFFFFF"
        )
        record_header_lbl.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        record_search_frm = ttk.Frame(
            master=record_frm
        )
        record_search_ent, record_search_results_srm = self.createSearch(
            master=record_search_frm,
            search_enter_func=self.performSearch_record
        )
        record_search_frm.grid(
            row=1,
            column=0,
            rowspan=9,
            sticky="w"
        )

        record_chronoUse_srm = ScrollFrame(
            master=root
        )
        record_chronoUse_srm.grid(
            row=1,
            column=1,
            rowspan=9,
            sticky="w"
        )
        self.all_record_used(
            results_srm=record_chronoUse_srm
        )

        self.refresh_all = lambda: self.refresh_all_results(
            keyword_search_ent=keyword_search_ent,
            keyword_search_results_srm=keyword_search_results_srm,
            keyword_chronoCreate_srm=keyword_chronoCreate_srm,
            record_search_ent=record_search_ent,
            record_search_results_srm=record_search_results_srm,
            record_chronoUse_srm=record_chronoUse_srm
        )

    def createSearch(
        self,
        master: ttk.Frame,
        search_enter_func: Callable
    ):
        search_and_options_frm = ttk.Frame(master=master)
        search_and_options_frm.pack()
        
        search_ent = tk.Entry(
            master=search_and_options_frm,
            bg=VsCodeDarkPalette.c2,
            fg="#FFFFFF"
        )
        search_ent.pack()

        results_srm = ScrollFrame(master=master)
        results_srm.pack()
        self.displayResults(
            results_srm=results_srm,
            btn_func=None,
            noExecute_btn_func=None,
            del_btn_func=None
        )

        search_ent.bind(
            tkBind.KEY_ENTER,
            func=lambda event: search_enter_func(
                search_ent=search_ent,
                results_srm=results_srm
            )
        )

        return (search_ent, results_srm)

    def performSearch_keyword(
        self,
        search_ent: tk.Entry,
        results_srm: ScrollFrame
    ):
        search_target = search_ent.get()

        mcb = MyClipBoard()
        results = []
        with mcb.myShelf as myShelf:
            if self.ignoreCaps:
                for key in list(myShelf.keys()):
                    if search_target.lower() in key.lower():
                        results.append(key)
            else:
                for key in list(myShelf.keys()):
                    if search_target in key:
                        results.append(key)
        
        self.displayResults(
            results_srm=results_srm,
            btn_func=self.copy_to_clipboard_keyword,
            noExecute_btn_func=self.noExecute_keyword,
            del_btn_func=self.del_keyword,
            results=results,
        )

    def performSearch_record(
        self,
        search_ent: tk.Entry,
        results_srm: ScrollFrame
    ):
        search_target = search_ent.get()

        mcb = MyClipBoard()
        results = []
        with mcb.recordShelf as recordShelf:
            records: list[str] = recordShelf[list(recordShelf.keys())[0]]
            if self.ignoreCaps:
                for elem in records:
                    if search_target.lower() in elem.lower():
                        results.append(elem)
            else:
                for elem in records:
                    if search_target in elem:
                        results.append(elem)
        
        self.displayResults(
            results_srm=results_srm,
            btn_func=self.copy_to_clipboard_record,
            noExecute_btn_func=self.noExecute_record,
            del_btn_func=self.del_record,
            results=results
        )
    
    def all_keyword_created(
        self,
        results_srm: ScrollFrame
    ):
        mcb = MyClipBoard()
        results = []
        with mcb.myShelf as myShelf:
            for key in list(myShelf.keys())[::-1]:
                results.append(key)
        
        self.displayResults(
            results_srm=results_srm,
            btn_func=self.copy_to_clipboard_keyword,
            noExecute_btn_func=self.noExecute_keyword,
            del_btn_func=self.del_keyword,
            results=results
        )

    def all_record_used(
        self,
        results_srm: ScrollFrame
    ):
        mcb = MyClipBoard()
        results = []
        with mcb.recordShelf as recordShelf:
            records = recordShelf[list(recordShelf.keys())[0]]
            for elem in records[::-1]:
                results.append(elem)
        
        self.displayResults(
            results_srm=results_srm,
            btn_func=self.copy_to_clipboard_record,
            noExecute_btn_func=self.noExecute_record,
            del_btn_func=self.del_record,
            results=results
        )

    def displayResults(
        self,
        results_srm: ScrollFrame,
        btn_func: Callable,
        noExecute_btn_func: Callable,
        del_btn_func: Callable,
        results: list[str] = None
    ):
        for widget in results_srm.viewPort.winfo_children():
            widget.grid_forget()
            widget.destroy()
        
        if results == None or results == []:
            empty_lbl = ttk.Label(
                master=results_srm.viewPort,
                text="No matches found."
            )
            empty_lbl.grid(
                row=0,
                column=0
            )
        else:
            for index in range(len(results)):
                result_text = results[index]
                
                resultHolder_frm = ttk.Frame(
                    master=results_srm.viewPort
                )
                resultHolder_frm.grid(
                    row=index,
                    column=0,
                    sticky="w"
                )
                
                result_btn = ttk.Button(
                    master=resultHolder_frm,
                    text=f"{result_text}",
                    style='result.TButton'
                )
                result_btn.grid(
                    row=0,
                    column=0
                )
                result_btn.bind(
                    sequence=tkBind.CLICK_LEFT,
                    func=lambda event, restext=result_text: btn_func(input_str=restext)
                )

                noExceute_btn = ttk.Button(
                    master=resultHolder_frm,
                    text=f"NE",
                    style='result.TButton'
                )
                noExceute_btn.bind(
                    sequence=tkBind.CLICK_LEFT,
                    func=lambda event, restext=result_text: noExecute_btn_func(input_str=restext)
                )

                delete_btn = ttk.Button(
                    master=resultHolder_frm,
                    text=f"X",
                    style='result.TButton'
                )
                delete_btn.bind(
                    sequence=tkBind.CLICK_LEFT,
                    func=lambda event, restext=result_text: del_btn_func(input_str=restext)
                )

                resultHolder_frm.bind(
                    sequence=tkBind.WIDGET_ENTER,
                    func=lambda event, temp_noExceute_btn=noExceute_btn: temp_noExceute_btn.grid(
                        row=0,
                        column=1
                    ),
                    add="+"
                )
                resultHolder_frm.bind(
                    sequence=tkBind.WIDGET_ENTER,
                    func=lambda event, temp_delete_btn=delete_btn: temp_delete_btn.grid(
                        row=0,
                        column=2
                    ),
                    add="+"
                )
                resultHolder_frm.bind(
                    sequence=tkBind.WIDGET_LEAVE,
                    func=lambda event, temp_noExceute_btn=noExceute_btn: temp_noExceute_btn.grid_forget(),
                    add="+"
                )
                resultHolder_frm.bind(
                    sequence=tkBind.WIDGET_LEAVE,
                    func=lambda event, temp_delete_btn=delete_btn: temp_delete_btn.grid_forget(),
                    add="+"
                )      

    def copy_to_clipboard_keyword(
        self,
        input_str: str
    ):
        mcb = MyClipBoard()
        sys.argv = [
            "mcb",
            input_str,
            "-uv"
        ]
        nmsp = mcb.parse_args(
            manual_args=sys.argv[1::]
        )
        mcb.decision_tree(
            args=nmsp
        )
    
    def copy_to_clipboard_record(
        self,
        input_str: str
    ):
        split_args = input_str.split(" ")
        
        mcb = MyClipBoard()
        sys.argv = [
            "mcb"
        ] + split_args
        nmsp = mcb.parse_args(
            manual_args=sys.argv[1::]
        )
        mcb.decision_tree(
            args=nmsp
        )

    def noExecute_keyword(
        self,
        input_str: str
    ):
        pyperclip.copy(input_str)

    def noExecute_record(
        self,
        input_str: str
    ):
        pyperclip.copy(input_str)

    def del_keyword(
        self,
        input_str: str
    ):
        keyword = input_str
        mcb = MyClipBoard()
        sys.argv = [
            "mcb"
        ] + keyword + [
            "-d"
        ]
        nmsp = mcb.parse_args(
            manual_args=sys.argv[1::]
        )
        mcb.decision_tree(
            args=nmsp
        )
        self.refresh_all_wrapper()

    def del_record(
        self,
        input_str: str
    ):
        split_args = input_str.split(" ")
        mcb = MyClipBoard()
        sys.argv = [
            "mcb"
        ] + split_args + [
            "-dr"
        ]
        nmsp = mcb.parse_args(
            manual_args=sys.argv[1::]
        )
        mcb.decision_tree(
            args=nmsp
        )
        self.refresh_all_wrapper()

    def refresh_both_keyword_results(
        self,
        keyword_search_ent: tk.Entry,
        keyword_search_results_srm: ScrollFrame,
        keyword_chronoCreate_srm: ScrollFrame
    ):
        self.performSearch_keyword(
            search_ent=keyword_search_ent,
            results_srm=keyword_search_results_srm
        )
        self.all_keyword_created(
            results_srm=keyword_chronoCreate_srm
        )

    def refresh_both_record_results(
        self,
        record_search_ent: tk.Entry,
        record_search_results_srm: ScrollFrame,
        record_chronoUse_srm: ScrollFrame
    ):
        self.performSearch_record(
            search_ent=record_search_ent,
            results_srm=record_search_results_srm
        )
        self.all_record_used(
            results_srm=record_chronoUse_srm
        )

    def refresh_all_results(
        self,
        keyword_search_ent: tk.Entry,
        keyword_search_results_srm: ScrollFrame,
        keyword_chronoCreate_srm: ScrollFrame,
        record_search_ent: tk.Entry,
        record_search_results_srm: ScrollFrame,
        record_chronoUse_srm: ScrollFrame
    ):
        self.performSearch_keyword(
            search_ent=keyword_search_ent,
            results_srm=keyword_search_results_srm
        )
        self.all_keyword_created(
            results_srm=keyword_chronoCreate_srm
        )
        self.performSearch_record(
            search_ent=record_search_ent,
            results_srm=record_search_results_srm
        )
        self.all_record_used(
            results_srm=record_chronoUse_srm
        )

    def refresh_all(self):
        pass

    def refresh_all_wrapper(self):
        self.refresh_all()

    

    
