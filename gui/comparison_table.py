import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ComparisonTable(ttk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Algorithm Comparison"
        )

        columns = (
            "Algorithm",
            "Avg WT",
            "Avg TAT",
            "Avg RT",
            "CPU Util (%)",
            "Throughput"
        )

        style = ttk.Style()

        # ==================================================
        # TREEVIEW STYLE
        # ==================================================

        style.configure(
            "Comparison.Treeview",
            background="#2A1240",
            foreground="#EBE3F2",
            fieldbackground="#2A1240",
            borderwidth=0,
            rowheight=44,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Comparison.Treeview.Heading",
            background="#945BB7",
            foreground="#EBE3F2",
            relief="flat",
            font=("Segoe UI Semibold", 12)
        )

        style.map(
            "Comparison.Treeview",
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
            padx=15,
            pady=15
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
            style="Comparison.Treeview"
        )

        # ==================================================
        # ROW TAGS
        # ==================================================

        self.tree.tag_configure(
            "best",
            background="#B57EDC",
            foreground="#FFFFFF"
        )

        self.tree.tag_configure(
            "normal",
            background="#2A1240",
            foreground="#EBE3F2"
        )

        self.tree.tag_configure(
            "alternate",
            background="#322046",
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

            if column == "Algorithm":
                width = 240
            else:
                width = 130

            self.tree.column(
                column,
                width=width,
                anchor=CENTER,
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

    def display(self, comparison_results):

        self.tree.delete(*self.tree.get_children())

        if not comparison_results:
            return

        ranked = sorted(
            comparison_results.items(),
            key=lambda x: x[1]["Average Waiting Time"]
        )

        best_algorithm = ranked[0][0]

        for index, (algorithm, metrics) in enumerate(comparison_results.items()):

            if algorithm == best_algorithm:
                tag = "best"
            else:
                tag = "alternate" if index % 2 else "normal"

            self.tree.insert(
                "",
                END,
                values=(
                    algorithm,
                    f"{metrics['Average Waiting Time']:.2f}",
                    f"{metrics['Average Turnaround Time']:.2f}",
                    f"{metrics['Average Response Time']:.2f}",
                    f"{metrics['CPU Utilization']:.2f} %",
                    f"{metrics['Throughput']:.2f}"
                ),
                tags=(tag,)
            )