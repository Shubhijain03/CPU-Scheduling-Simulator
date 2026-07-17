import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class MetricsPanel(ttk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Performance Metrics"
        )

        self.avg_wt = ttk.StringVar(value="--")
        self.avg_tat = ttk.StringVar(value="--")
        self.avg_rt = ttk.StringVar(value="--")
        self.cpu = ttk.StringVar(value="--")
        self.tp = ttk.StringVar(value="--")

        container = ttk.Frame(self)
        container.pack(
            fill=X,
            expand=True,
            padx=12,
            pady=12
        )

        metrics = [

            ("Average Waiting Time", self.avg_wt, "ms"),

            ("Average Turnaround Time", self.avg_tat, "ms"),

            ("Average Response Time", self.avg_rt, "ms"),

            ("CPU Utilization", self.cpu, "%"),

            ("Throughput", self.tp, "Processes / Time Unit") 

        ]

        for index, (title, variable, unit) in enumerate(metrics):

            container.columnconfigure(index, weight=1)

            card = ttk.Frame(
                container
            )

            card.grid(
                row=0,
                column=index,
                padx=12,
                pady=10,
                sticky="nsew"
            )
            
            card.grid_columnconfigure(0, weight=1)

            ttk.Separator(
                card
            ).pack(
                fill=X,
                padx=10,
                pady=(0, 10 )
            )

            ttk.Label(
                card,
                text=title,
                font=("Segoe UI Semibold", 10),
                foreground="#C8B8DD",
                justify=CENTER
            ).pack(
                pady=(2, 8)
            )

            ttk.Label(
                card,
                textvariable=variable,
                font=("Segoe UI Semibold", 26),
                foreground="#B57EDC",
                justify=CENTER
            ).pack()

            ttk.Label(
                card,
                text=unit,
                font=("Segoe UI", 9),
                foreground="#945BB7"
            ).pack(
                pady=(6, 2)
            )

    # ==================================================
    # UPDATE METRICS
    # ==================================================

    def update_metrics(
        self,
        avg_wt,
        avg_tat,
        avg_rt,
        cpu,
        throughput
    ):

        self.avg_wt.set(f"{avg_wt:.2f}")
        self.avg_tat.set(f"{avg_tat:.2f}")
        self.avg_rt.set(f"{avg_rt:.2f}")
        self.cpu.set(f"{cpu:.2f}")
        self.tp.set(f"{throughput:.2f}")
        
    def clear(self):

        self.avg_wt.set("--")
        self.avg_tat.set("--")
        self.avg_rt.set("--")
        self.cpu.set("--")
        self.tp.set("--")