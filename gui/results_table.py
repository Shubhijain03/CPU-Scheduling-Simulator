import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ResultsTable(ttk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Scheduling Results"
        )

        style = ttk.Style()

        # ==================================================
        # TREEVIEW STYLE
        # ==================================================

        style.configure(
            "Results.Treeview",
            background="#2A1240",
            foreground="#EBE3F2",
            fieldbackground="#2A1240",
            borderwidth=0,
            rowheight=48,
            font=("Segoe UI", 11)
        )

        style.configure(
            "Results.Treeview.Heading",
            background="#945BB7",
            foreground="#EBE3F2",
            relief="flat",
            font=("Segoe UI Semibold", 12)
        )

        style.map(
            "Results.Treeview",
            background=[("selected", "#945BB7")],
            foreground=[("selected", "#FFFFFF")]
        )

        # ==================================================
        # TABLE FRAME
        # ==================================================

        table_frame = ttk.Frame(self)
        table_frame.pack(
            fill=BOTH,
            expand=True,
            padx=16,
            pady=16
        )

        columns = (
            "PID",
            "AT",
            "BT",
            "PR",
            "CT",
            "TAT",
            "WT",
            "RT"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=13,
            style="Results.Treeview"
        )
        
        self.tree["displaycolumns"] = (
            "PID",
            "AT",
            "BT",
            "PR",
            "CT",
            "TAT",
            "WT",
            "RT"
        )

        # ==================================================
        # ROW COLORS
        # ==================================================

        self.tree.tag_configure(
            "normal",
            background="#2A1240",
            foreground="#EBE3F2"
        )

        self.tree.tag_configure(
            "alternate",
            background="#311A47",
            foreground="#EBE3F2"
        )

        self.tree.tag_configure(
            "best",
            background="#7B4FA1",
            foreground="#FFFFFF"
        )

        self.tree.tag_configure(
            "worst",
            background="#5A2D72",
            foreground="#EBE3F2"
        )

        # ==================================================
        # HEADINGS
        # ==================================================

        for column in columns:

            self.tree.heading(
                column,
                text=column,
                anchor=CENTER
            )

            if column == "PID":
                width = 95
            elif column in ("AT", "BT", "PR"):
                width = 85
            else:
                width = 110

            self.tree.column(
                column,
                anchor=CENTER,
                width=width,
                stretch=True
            )

        # ==================================================
        # SCROLLBARS
        # ==================================================

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL,
            command=self.tree.yview
        )

        x_scroll = ttk.Scrollbar(
            table_frame,
            orient=HORIZONTAL,
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(5, 0)
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(5, 0)
        )

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    def display_results(self, processes):

        self.tree.delete(*self.tree.get_children())

        if not processes:
            return

        min_wt = min(
            process.waiting_time
            for process in processes
        )

        max_wt = max(
            process.waiting_time
            for process in processes
        )

        for index, process in enumerate(processes):

            if process.waiting_time == min_wt:
                tag = "best"

            elif process.waiting_time == max_wt:
                tag = "worst"

            else:
                tag = "alternate" if index % 2 else "normal"

            self.tree.insert(
                "",
                END,
                values=(
                    process.pid,
                    process.arrival_time,
                    process.burst_time,
                    process.priority,
                    process.completion_time,
                    process.turnaround_time,
                    process.waiting_time,
                    process.response_time
                ),
                tags=(tag,)
            )