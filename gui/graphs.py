import ttkbootstrap as ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphPanel(ttk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Performance Analytics",
        )

        self.metric = ttk.StringVar(
            value="Average Waiting Time"
        )

        top = ttk.Frame(self)
        top.pack(
            fill="x",
            padx=15,
            pady=(10, 5)
        )

        ttk.Label(
            top,
            text="Select Metric",
            font=("Segoe UI Semibold", 11)
        ).pack(side="left")

        combo = ttk.Combobox(
            top,
            textvariable=self.metric,
            state="readonly",
            width=30,
            style="Graph.TCombobox",
            values=[
                "Average Waiting Time",
                "Average Turnaround Time",
                "Average Response Time",
                "CPU Utilization",
                "Throughput"
            ]
        )

        combo.pack(
            side="left",
            padx=15
        )

        combo.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_graph()
        )

        self.figure = Figure(
            figsize=(8, 5),
            dpi=100,
            facecolor="#09070A"
        )
        
        self.figure.subplots_adjust(
            left=0.09,
            right=0.98,
            top=0.90,
            bottom=0.15
        )

        self.axis = self.figure.add_subplot(111)

        self.initialize_blank_graph()

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        
        self.canvas.draw()

        self.results = None  
        
    def setup_axis_style(self):
        self.axis.set_facecolor("#2A1240")

        self.axis.tick_params(
            axis="x",
            colors="#EBE3F2"
        )

        self.axis.tick_params(
            axis="y",
            colors="#EBE3F2"
        )

        self.axis.spines["left"].set_color("#C8B8DD")
        self.axis.spines["bottom"].set_color("#C8B8DD")

        self.axis.spines["top"].set_visible(False)
        self.axis.spines["right"].set_visible(False)

        self.axis.xaxis.get_offset_text().set_color("#EBE3F2")
        self.axis.yaxis.get_offset_text().set_color("#EBE3F2")
        
    def initialize_blank_graph(self):

        self.axis.clear()

        self.setup_axis_style()

        self.axis.set_ylabel(
            "Value",
            fontsize=11,
            color="#EBE3F2"
        )

        # No title on blank graph
        self.axis.set_title("")

        self.axis.grid(False)

        self.axis.tick_params(
            axis="x",
            colors="#EBE3F2",
            rotation=0,
            labelsize=9
        )

        self.axis.tick_params(
            axis="y",
            colors="#EBE3F2",
            labelsize=9
        )

        self.axis.margins(y=0.18)      
                    

    def display(self, comparison_results):

        self.results = comparison_results

        self.update_graph()
        

    def update_graph(self):

        if self.results is None:
            return

        self.axis.clear()
        self.setup_axis_style()

        metric = self.metric.get()

        algorithms = list(self.results.keys())

        values = [
            self.results[name][metric]
            for name in algorithms
        ]

        reverse = metric in (
            "CPU Utilization",
            "Throughput"
        )

        ranked = sorted(
            zip(algorithms, values),
            key=lambda x: x[1],
            reverse=reverse
        )

        best_algorithm = ranked[0][0]

        colors = []

        for algorithm in algorithms:

            if algorithm == best_algorithm:
                colors.append("#B57EDC")
            else:
                colors.append("#5D3A87")

        bars = self.axis.bar(
            algorithms,
            values,
            width=0.55,
            color=colors,
            edgecolor="#EBE3F2",
            linewidth=1.2
        )

        maximum = max(values)

        for bar in bars:

            height = bar.get_height()

            self.axis.text(
                bar.get_x() + bar.get_width()/2,
                height + maximum*0.02,
                f"{height:.2f}",
                ha="center",
                fontsize=9,
                fontweight="bold",
                color="#EBE3F2"
            )

        self.axis.set_title(
            metric,
            fontsize=15,
            fontweight="bold",
            color="#EBE3F2",
            pad=15
        )

        self.axis.set_ylabel(
            "Value",
            fontsize=11,
            color="#EBE3F2"
        )

        self.axis.grid(
            axis="y",
            linestyle="--",
            linewidth=0.7,
            color="#6B5A80",
            alpha=0.5
        )

        self.axis.set_axisbelow(True)

        self.axis.tick_params(
            axis="x",
            colors="#EBE3F2",
            rotation=15,
        )

        self.axis.tick_params(
            axis="y",
            colors="#EBE3F2",
            labelsize=9
        )

        self.axis.margins(y=0.18)
        # Ensure all tick labels are white
        for label in self.axis.get_xticklabels():
            label.set_color("#EBE3F2")

        for label in self.axis.get_yticklabels():
            label.set_color("#EBE3F2")

        self.canvas.draw()
        
        
    def save_metric_graph(self, metric, filename):
        self.metric.set(metric)
        self.update_graph()

        self.figure.savefig(
            filename,
            dpi=300,
            bbox_inches="tight",
            facecolor=self.figure.get_facecolor()
        )
        
    def clear_graph(self):

        self.results = None

        self.initialize_blank_graph()

        self.canvas.draw()
        
    
    
    