import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class BestAlgorithm(ttk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="BEST ALGORITHM ANALYSIS"
        )

        #################################################
        # Main Container
        #################################################

        container = ttk.Frame(self)
        container.pack_propagate(False)
        container.pack(
            fill=BOTH,
            expand=True,
            padx=8,
            pady=10
        )

        #################################################
        # Header
        #################################################

        ttk.Label(
            container,
            text="BEST SCHEDULER",
            font=("Segoe UI Semibold", 11),
            foreground="#B57EDC"
        ).pack(pady=(0, 8))

        #################################################
        # Algorithm Name
        #################################################

        self.algorithm = ttk.Label(
            container,
            text="Run Comparison",
            font=("Segoe UI Semibold", 22),
            foreground="#B57EDC",
            anchor="center"
        )

        self.algorithm.pack(
            fill=X,
            pady=(8, 10)
        )

        #################################################
        # Reason
        #################################################

        self.reason = ttk.Label(
            container,
            text="Compare all scheduling algorithms to generate the best recommendation.",
            justify=LEFT,
            wraplength=420,
            font=("Segoe UI", 10),
            foreground="#C8B8DD"
        )

        self.reason.pack(
            fill=X,
            padx=6,
            pady=(0, 15)
        )

        ttk.Separator(container).pack(
            fill=X,
            pady=10
        )

        #################################################
        # Performance Metrics
        #################################################

        ttk.Label(
            container,
            text="Performance Metrics",
            font=("Segoe UI Semibold", 13),
            foreground="#B57EDC"
        ).pack(
            fill=X,
            padx=12,
            pady=(0, 12)
        )

        metrics = ttk.Frame(container)

        metrics.pack(
            fill=X,
            padx=6
        )

        self.awt_label = ttk.Label(
            metrics,
            font=("Segoe UI", 10),
            foreground="#EBE3F2"
        )
        self.awt_label.pack(anchor="w", pady=3)

        self.tat_label = ttk.Label(
            metrics,
            font=("Segoe UI", 10),
            foreground="#EBE3F2"
        )
        self.tat_label.pack(anchor="w", pady=3)

        self.rt_label = ttk.Label(
            metrics,
            font=("Segoe UI", 10),
            foreground="#EBE3F2"
        )
        self.rt_label.pack(anchor="w", pady=3)

        self.cpu_label = ttk.Label(
            metrics,
            font=("Segoe UI", 10),
            foreground="#EBE3F2"
        )
        self.cpu_label.pack(anchor="w", pady=3)

        self.tp_label = ttk.Label(
            metrics,
            font=("Segoe UI", 10),
            foreground="#EBE3F2"
        )
        self.tp_label.pack(anchor="w", pady=3)

        ttk.Separator(container).pack(
            fill=X,
            pady=15
        )

        #################################################
        # Recommendation
        #################################################

        ttk.Label(
            container,
            text="Recommendation",
            font=("Segoe UI Semibold", 13),
            foreground="#B57EDC"
        ).pack(
            fill=X,
            padx=6,
            pady=(0, 8)
        )

        self.recommendation = ttk.Label(
            container,
            text="Run Compare Algorithms to receive an automatic recommendation.",
            justify=LEFT,
            anchor="w",
            wraplength=400,
            font=("Segoe UI", 10),
            foreground="#EBE3F2"
        )

        self.recommendation.pack(
            fill=X,
            padx=6,
            pady=(4, 0)
        )
    #################################################
    # Display
    #################################################

    def display(self, comparison_results):
        
        if not comparison_results:
            return

        best_algorithm, metrics = min(
            comparison_results.items(),
            key=lambda item: item[1]["Average Waiting Time"]
        )

        self.algorithm.config(
            text=best_algorithm
        )

        self.reason.config(
            text="Selected because it achieved the lowest Average Waiting Time."
        )

        self.awt_label.config(
            text=f"Average Waiting Time : {metrics['Average Waiting Time']:.2f} ms"
        )

        self.tat_label.config(
            text=f"Average Turnaround : {metrics['Average Turnaround Time']:.2f} ms"
        )

        self.rt_label.config(
            text=f"Average Response : {metrics['Average Response Time']:.2f} ms"
        )

        self.cpu_label.config(
            text=f"CPU Utilization : {metrics['CPU Utilization']:.2f}%"
        )

        self.tp_label.config(
            text=f"Throughput : {metrics['Throughput']:.2f}"
        )

        self.recommendation.config(
            text=(
                f"{best_algorithm} is recommended because it achieved the lowest "
                "average waiting time while maintaining competitive turnaround "
                "time, response time, CPU utilization and throughput for the "
                "selected workload."
            )
        )
    # ==================================================
    # RESET DISPLAY
    # ==================================================

    def reset(self):

        self.algorithm.config(
            text="Run Comparison"
        )

        self.reason.config(
            text="Compare all scheduling algorithms to generate the best recommendation."
        )

        self.awt_label.config(
            text=""
        )

        self.tat_label.config(
            text=""
        )

        self.rt_label.config(
            text=""
        )

        self.cpu_label.config(
            text=""
        )

        self.tp_label.config(
            text=""
        )

        self.recommendation.config(
            text="Run Compare Algorithms to receive an automatic recommendation."
        )
        
    # ==================================================
    # RESPONSIVE RESIZE
    # ==================================================

    def _resize_text(self, event=None):

        width = self.winfo_width()

        # Keep recommendation inside the panel
        self.recommendation.configure(
            wraplength=max(220, width - 60)
        )

        # Keep reason text inside the panel
        self.reason.configure(
            wraplength=max(220, width - 60)
        )

        # Algorithm title shrinks slightly on smaller widths
        if width < 320:
            self.algorithm.configure(font=("Segoe UI Semibold", 18))
        elif width < 420:
            self.algorithm.configure(font=("Segoe UI Semibold", 20))
        else:
            self.algorithm.configure(font=("Segoe UI Semibold", 24))