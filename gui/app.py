import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.process_table import ProcessTable
from ttkbootstrap.dialogs import Messagebox
from gui.process_parser import get_processes_from_table

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority
from algorithms.priority_preemptive import priority_preemptive
from algorithms.round_robin import round_robin
from algorithms.hrrn import hrrn

from gui.results_table import ResultsTable
from gui.metrics_panel import MetricsPanel
from gui.gantt_chart import GanttChart
from gui.csv_handler import open_csv
from gui.comparison_table import ComparisonTable
from gui.best_algorithm import BestAlgorithm
from gui.graphs import GraphPanel

from utils.comparison import compare_all
from utils.pdf_export import export_results

from utils.metrics import (
    average_waiting_time,
    average_turnaround_time,
    average_response_time,
    cpu_utilization,
    throughput,
)

from tkinter import filedialog


class CPUSchedulerGUI:

    def __init__(self):

        self.root = ttk.Window(
            title="CPU Scheduling Simulator",
            themename="darkly",
            size=(1550, 1000),
            resizable=(True, True)
        )

        self.root.configure(bg="#09070A")
        self.root.minsize(1350, 920)
        self.apply_style()
        self.create_layout()
        self.enable_mouse_scroll()
    # ==================================================
    # PREMIUM DARK THEME
    # ==================================================

    def apply_style(self):

        style = self.root.style

        style.configure(
            ".",
            background="#09070A",
            foreground="#EBE3F2",
            font=("Segoe UI", 10)
        )
        
        style.configure(
            "Purple.TButton",
            background="#945BB7",
            foreground="#FFFFFF",
            borderwidth=0,
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Purple.TButton",
            background=[
                ("active", "#B57EDC"),
                ("pressed", "#7B4FA1")
            ]
        )

        style.configure(
            "TFrame",
            background="#09070A"
        )

        style.configure(
            "TLabelframe",
            background="#2A1240",
            borderwidth=2,
            relief="solid"
        )

        style.configure(
            "TLabelframe.Label",
            background="#2A1240",
            foreground="#EBE3F2",
            font=("Segoe UI Semibold", 12)
        )

        style.configure(
            "TLabel",
            background="#09070A",
            foreground="#EBE3F2"
        )

        style.configure(
            "Header.TLabel",
            background="#09070A",
            foreground="#EBE3F2",
            font=("Segoe UI Semibold", 30)
        )

        style.configure(
            "SubHeader.TLabel",
            background="#09070A",
            foreground="#C8B8DD",
            font=("Segoe UI", 13)
        )

        style.configure(
            "Section.TLabel",
            background="#2A1240",
            foreground="#D8C3F0",
            font=("Segoe UI Semibold", 10)
        )

        style.configure(
            "TEntry",
            fieldbackground="#1B1027",
            foreground="#EBE3F2",
            insertcolor="#EBE3F2"
        )
        
        style.configure(
            "TSpinbox",
            fieldbackground="#1B1027",
            foreground="#EBE3F2",
            bordercolor="#5D3A87",
            lightcolor="#5D3A87",
            darkcolor="#5D3A87",
            arrowcolor="#EBE3F2",
            insertcolor="#EBE3F2"
        )

        style.map(
            "TSpinbox",
            bordercolor=[
                ("focus", "#945BB7"),
                ("hover", "#B57EDC")
            ],
            lightcolor=[
                ("focus", "#945BB7"),
                ("hover", "#B57EDC")
            ],
            darkcolor=[
                ("focus", "#945BB7"),
                ("hover", "#B57EDC")
            ]
        )
        
        style = ttk.Style()

        style.configure(
            "TCombobox",
            fieldbackground="#1B1027",
            foreground="#EBE3F2"
        )
        
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#2A1240")],
            foreground=[("readonly", "#EBE3F2")],
            selectbackground=[("readonly", "#945BB7")],
            selectforeground=[("readonly", "#FFFFFF")]
        )
    # ==================================================
    # MAIN LAYOUT
    # ==================================================

    def create_layout(self):

        ###################################################
        ## HEADER
        ###################################################

        header = ttk.Frame(self.root)
        header.pack(
            fill=X,
            padx=20,
            pady=(15, 10)
        )

        title = ttk.Label(
            header,
            text="CPU Scheduling Simulator",
            font=("Segoe UI Semibold", 30),
            foreground="#B57EDC"
        )

        title.pack()

        subtitle = ttk.Label(
            header,
            text="Visual Analysis • Performance Comparison • Gantt Timeline • Metrics Dashboard",
            font=("Segoe UI", 11),
            foreground="#BDB4CC"
        )

        subtitle.pack(pady=(6, 10))

        ttk.Separator(self.root).pack(
            fill=X,
            padx=20,
            pady=(0, 15)
        )

        ###################################################
        ## MAIN CONTENT
        ###################################################

        self.content = ttk.Frame(self.root)
        self.content.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        ###################################################
        ## MAIN CONTAINER
        ###################################################

        self.main_container = ttk.Frame(self.content)
        self.main_container.pack(fill=BOTH, expand=True)

        ###################################################
        ## LEFT PANEL
        ###################################################

        self.left_panel = ttk.LabelFrame(
            self.main_container,
            text="CONTROL PANEL"
        )

        self.left_panel.pack(
            side=LEFT,
            fill=Y,
            anchor="n",
            padx=(0, 30 ), 
            pady=5
        )

        self.left_panel.configure(width=320 )
        self.left_panel.pack_propagate(False)
       
        ###################################################
        ## CONFIGURATION
        ###################################################

        config = ttk.LabelFrame(
            self.left_panel,
            text="Scheduling Configuration"
        )

        config.pack(
            fill=X,
            padx=16,
            pady=(12, 10)
        )

        config_inner = ttk.Frame(config)
        config_inner.pack(
            fill=X,
            padx=16,
            pady=12
        )

        ttk.Label(
            config_inner,
            text="Scheduling Algorithm",
            style="Section.TLabel"
        ).pack(anchor="w")

        self.algorithm = ttk.StringVar(value="FCFS")

        algorithm_box = ttk.Combobox(
            config_inner,
            textvariable=self.algorithm,
            state="readonly",
            values=[
                "FCFS",
                "SJF",
                "SRTF",
                "Priority",
                "Priority Preemptive",
                "Round Robin",
                "HRRN"
            ]
        )

        algorithm_box.pack(
            fill=X,
            pady=(8,16)
        )

        algorithm_box.bind(
            "<<ComboboxSelected>>",
            self.toggle_quantum
        )

        ttk.Label(
            config_inner,
            text="Time Quantum",
            style="Section.TLabel"
        ).pack(anchor="w")

        self.quantum = ttk.StringVar()

        self.quantum_entry = ttk.Entry(
            config_inner,
            textvariable=self.quantum
        )

        self.quantum_entry.pack(
            fill=X,
            pady=(8,16)
        )

        self.quantum_entry.configure(state="disabled")

        ttk.Label(
            config_inner,
            text="Number of Processes",
            style="Section.TLabel"
        ).pack(anchor="w")

        self.process_count = ttk.StringVar(value="3")
        
        validate_command = (
            self.root.register(
                self.validate_process_count
            ),
            "%P"
        )

        ttk.Combobox(
            config_inner,
            textvariable=self.process_count,
            state="readonly",
            values=[str(i) for i in range(1, 101)]
        ).pack(
            fill=X,
            pady=(8,16)
        )

        ###################################################
        ## EXECUTION CONTROLS
        ###################################################

        action_frame = ttk.LabelFrame(
            self.left_panel,
            text="Execution Controls"
        )

        action_frame.pack(
            fill=X,
            padx=18,
            pady=(0, 12)
        )

        button_area = ttk.Frame(action_frame)
        button_area.pack(
            fill=X,
            padx=12,
            pady=10
        )

        buttons = [
            ("Generate Process Table", "primary", self.generate_process_table),
            ("Run Scheduler", "primary", self.run_algorithm),
            ("Compare Algorithms", "primary", self.compare_algorithms),
            ("Import CSV", "primary", self.upload_csv),
            ("Export Report", "primary", self.export_pdf),
            ("Export Comparison", "primary", self.export_comparison),
            ("Reset Application", "primary", self.reset_app),
        ]

        for text, style, command in buttons:

            ttk.Button(
                button_area,
                text=text,
                style="Purple.TButton",
                command=command
            ).pack(
                fill=X,
                pady=(0,6),
                ipady=5
            )

        ##################################################
        ## RIGHT SIDE (Scrollable)
        ###################################################

        right_container = ttk.Frame(self.main_container)
        right_container.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        right_scroll = ttk.Scrollbar(
            right_container,
            orient=VERTICAL
        )
        right_scroll.pack(side=RIGHT, fill=Y)

        from tkinter import Canvas

        self.right_canvas = Canvas(
            right_container,
            bg="#09070A",
            highlightthickness=0,
            yscrollcommand=right_scroll.set
        )

        self.right_canvas.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        right_scroll.config(command=self.right_canvas.yview)

        self.right_panel = ttk.Frame(self.right_canvas)

        self.right_canvas_window = self.right_canvas.create_window(
            (0, 0),
            window=self.right_panel,
            anchor="nw"
        )

        self.right_panel.bind(
            "<Configure>",
            lambda e: self.right_canvas.configure(
                scrollregion=self.right_canvas.bbox("all")
            )
        )

        self.right_canvas.bind(
            "<Configure>",
            lambda e: self.right_canvas.itemconfigure(
                self.right_canvas_window,
                width=e.width
            )
        )

        ###################################################
        ## PROCESS INPUT
        ###################################################

        self.process_frame = ttk.LabelFrame(
            self.right_panel,
            text="PROCESS INPUT"
        )

        self.process_frame.pack(
            fill=X,
            pady=(0,12)
        )
        # -------------------------------
        # Scrollable Process Area
        # -------------------------------
        
        process_area = ttk.Frame(
            self.process_frame
        )

        process_area.pack(
            fill=BOTH,
            expand=True,
            padx=18,
            pady=(4,10)
        )
        self.process_area = process_area
        self.process_area.pack_propagate(False)

        from tkinter import Canvas


        self.process_canvas = Canvas(
            process_area,
            bg="#09070A",
            highlightthickness=0,
            bd=0
        )


        process_scrollbar = ttk.Scrollbar(
            process_area,
            orient=VERTICAL,
            command=self.process_canvas.yview
        )


        self.process_canvas.configure(
            yscrollcommand=process_scrollbar.set
        )


        self.process_canvas.pack(
            side=LEFT,
            fill=BOTH,
            expand=True,
            pady=(0,0)
        )


        process_scrollbar.pack(
            side=RIGHT,
            fill=Y
        )


        self.process_table_frame = ttk.Frame(
            self.process_canvas
        )


        self.process_canvas_window = self.process_canvas.create_window(
            (0,0),
            window=self.process_table_frame,
            anchor="nw"
        )


        self.process_table_frame.bind(
            "<Configure>",
            lambda e:
            self.process_canvas.configure(
                scrollregion=self.process_canvas.bbox("all")
            )
        )

        self.process_canvas.bind(
            "<Configure>",
            lambda e:
            self.process_canvas.itemconfigure(
                self.process_canvas_window,
                width=e.width
            )
        )


        self.process_table = ProcessTable(
            self.process_table_frame
        )


        self.process_table.pack(
            fill=BOTH,
            expand=True
        )


        self.process_table.generate_rows(
            3,
            default_values=True
        )
            
        self.adjust_process_area()
        
        ###################################################
        ## PERFORMANCE OVERVIEW
        ###################################################

        self.dashboard_frame = ttk.LabelFrame(
            self.right_panel,
            text="PERFORMANCE OVERVIEW"
        )

        self.dashboard_frame.pack(
            fill=X,
            pady=(0,18)
        )

        dashboard_container = ttk.Frame(self.dashboard_frame)
        dashboard_container.pack(
            fill=BOTH,
            expand=True,
            padx=15,
            pady=15
        )

        dashboard_left = ttk.Frame(dashboard_container)
        dashboard_left.pack(
            side=LEFT,
            fill=BOTH,
            expand=True,
            padx=(0,15)
        )

        dashboard_right = ttk.Frame(dashboard_container)
        dashboard_right.pack(
            side=RIGHT,
            fill=Y
        )

        dashboard_right.configure(width=430 )
        dashboard_right.pack_propagate(False)

        self.results_table = ResultsTable(dashboard_left)

        self.results_table.pack(
            fill=BOTH,
            expand=True,
            pady=(0,12)
        )

        self.metrics_panel = MetricsPanel(dashboard_left)

        self.metrics_panel.pack(fill=X)

        self.best_algorithm = BestAlgorithm(dashboard_right)

        self.best_algorithm.pack(
            fill=BOTH,
            expand=True,
            padx=5,
            pady=5,
            ipady=15
        )

        ###################################################
        ## NOTEBOOK
        ###################################################

        self.notebook = ttk.Notebook(self.right_panel)

        self.notebook.pack(
            fill=BOTH,
            expand=True,
            pady=(12,10 )
        )

        # ---------------- GANTT ----------------

        self.gantt_tab = ttk.Frame(self.notebook)
        self.notebook.add(
            self.gantt_tab,
            text="Execution Timeline"
        )

        self.gantt_chart = GanttChart(self.gantt_tab)

        self.gantt_chart.pack(
            fill=BOTH,
            expand=True,
            padx=12,
            pady=12
        )

        # ---------------- COMPARISON ----------------

        self.comparison_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.comparison_tab,
            text="Algorithm Comparison"
        )

        self.comparison_table = ComparisonTable(
            self.comparison_tab
        )

        self.comparison_table.pack(
            fill=BOTH,
            expand=True,
            padx=12,
            pady=12
        )

        # ---------------- GRAPH ----------------

        self.graph_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.graph_tab,
            text="Performance Analysis"
        )

        self.graph_panel = GraphPanel(self.graph_tab)

        self.graph_panel.pack(
            fill=BOTH,
            expand=True,
            padx=12,
            pady=12
        )

        # ==================================================
        # STATUS BAR
        # ==================================================

        self.status = ttk.StringVar(
            value="Status : Ready"
        )
        status_bar = ttk.Label(
                self.root,
                textvariable=self.status,
                anchor="w",
                foreground="#C8B8DD"
        )

        status_bar.pack(
                fill=X,
                side=BOTTOM,
                padx=15,
                pady=8
        )
    # ==================================================
    # MOUSE SCROLL SUPPORT
    # ==================================================
    
    def enable_mouse_scroll(self):
        self.root.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

    def mouse_scroll(self, event):

        widget = self.root.winfo_containing(
            event.x_root,
            event.y_root
        )

        if widget is None:
            return

       # Scroll only the Process Input area
        if str(widget).startswith(str(self.process_canvas)):
            self.process_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

         # Everywhere else scroll the main page
        else:
            self.right_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
    # ==================================================
    # ADJUST PROCESS AREA
    # ==================================================
        
    def adjust_process_area(self):
        fixed_height =300

        self.process_area.configure(
            height=fixed_height
        )

    # ==================================================
    # GENERATE PROCESS TABLE
    # ==================================================

    def generate_process_table(self):

        try:

            count = int(self.process_count.get())

            if count <= 0:
                raise ValueError

            self.process_table.generate_rows(count)
            self.root.after(
                10,
                self.adjust_process_area
            )
            self.process_canvas.yview_moveto(0)            
            self.status.set("Status : Process table generated successfully")

        except ValueError:

            ttk.Messagebox.show_error(
                "Enter a valid positive number of processes.",
                "Invalid Input"
            )

    # ==================================================
    # IMPORT CSV
    # ==================================================

    def upload_csv(self):

        processes = open_csv()

        if processes is None:
            return

        self.process_count.set(str(len(processes)))

        self.process_table.generate_rows(len(processes))

        for row, process in zip(self.process_table.rows, processes):

            row["arrival"].delete(0, END)
            row["arrival"].insert(0, process.arrival_time)

            row["burst"].delete(0, END)
            row["burst"].insert(0, process.burst_time)

            row["priority"].delete(0, END)
            row["priority"].insert(0, process.priority)

        self.status.set("Status : CSV imported successfully")

    # ==================================================
    # RUN SCHEDULER
    # ==================================================

    def run_algorithm(self):

        processes = get_processes_from_table(self.process_table)

        if processes is None:
            return

        algorithm = self.algorithm.get()

        if algorithm == "FCFS":

            result = fcfs(processes)

        elif algorithm == "SJF":

            result = sjf(processes)

        elif algorithm == "SRTF":

            result = srtf(processes)

        elif algorithm == "Priority":

            result = priority(processes)

        elif algorithm == "Priority Preemptive":

            result = priority_preemptive(processes)

        elif algorithm == "Round Robin":

            if not self.quantum.get().strip():

                ttk.Messagebox.show_error(
                    "Please enter Time Quantum.",
                    "Missing Input"
                )
                return

            result = round_robin(
                processes,
                int(self.quantum.get())
            )

        else:

            result = hrrn(processes)

        self.last_result = result

        self.results_table.display_results(result)

        self.metrics_panel.update_metrics(
            average_waiting_time(result),
            average_turnaround_time(result),
            average_response_time(result),
            cpu_utilization(result),
            throughput(result)
        )

        self.gantt_chart.draw(result)

        self.status.set(f"Status : {algorithm} executed successfully")

    # ==================================================
    # COMPARE ALGORITHMS
    # ==================================================

    def compare_algorithms(self):

        processes = get_processes_from_table(self.process_table)

        if processes is None:
            return

        comparison_results = compare_all(processes, 2)
        
        self.comparison_results = comparison_results

        self.best_algorithm.display(comparison_results)

        self.comparison_table.display(comparison_results)

        self.graph_panel.display(comparison_results)

        self.status.set("Status : Comparison completed")

    # ==================================================
    # EXPORT REPORT
    # ==================================================

    def export_pdf(self):

        if not hasattr(self, "last_result"):
            Messagebox.show_warning(
                "Run any scheduling algorithm before exporting.",
                "No Results"
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")]
        )

        if not filename:
            return

        metrics = {

            "Average Waiting Time":
                f"{average_waiting_time(self.last_result):.2f}",

            "Average Turnaround Time":
                f"{average_turnaround_time(self.last_result):.2f}",

            "Average Response Time":
                f"{average_response_time(self.last_result):.2f}",

            "CPU Utilization":
                f"{cpu_utilization(self.last_result):.2f}%",

            "Throughput":
                f"{throughput(self.last_result):.2f}"
        }


        graph_paths = []

        metrics_list = [
            "Average Waiting Time",
            "Average Turnaround Time",
            "Average Response Time",
            "CPU Utilization",
            "Throughput"
        ]


        for metric in metrics_list:

            path = metric.replace(" ", "_") + ".png"

            self.graph_panel.save_metric_graph(
                metric,
                path
            )

            graph_paths.append(path)


        export_results(
            filename,
            self.algorithm.get(),
            self.last_result,
            metrics,
            graph_paths
        )


        self.status.set(
            "Status : Report exported successfully"
        )
    # ==================================================
    # EXPORT COMPARISON (CSV)
    # ==================================================

    def export_comparison(self):

        if not hasattr(self, "comparison_results"):
            Messagebox.show_warning(
                "Run Compare Algorithms before exporting.",
                "No Comparison Available"
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")]
        )

        if not filename:
            return

        import csv

        with open(filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Algorithm",
                "Average Waiting Time",
                "Average Turnaround Time",
                "Average Response Time",
                "CPU Utilization",
                "Throughput"
            ])

            for algorithm, values in self.comparison_results.items():

                writer.writerow([
                    algorithm,
                    values["Average Waiting Time"],
                    values["Average Turnaround Time"],
                    values["Average Response Time"],
                    values["CPU Utilization"],
                    values["Throughput"]
                ])

        self.status.set("Status : Comparison exported successfully")

    # ==================================================
    # TOGGLE QUANTUM
    # ==================================================

    def toggle_quantum(self, event=None):

        if self.algorithm.get() == "Round Robin":

            self.quantum_entry.configure(state="normal")

        else:

            self.quantum.set("")

            self.quantum_entry.configure(state="disabled")

    # ==================================================
    # RESET APPLICATION
    # ==================================================

    def reset_app(self):

        # Reset configuration
        self.algorithm.set("FCFS")
        self.quantum.set("")
        self.quantum_entry.configure(state="disabled")

        self.process_count.set("3")

        # Reset process table
        self.process_table.generate_rows(3)

        # Reset result table
        self.results_table.display_results([])

        # Reset metrics dashboard
        self.metrics_panel.clear()
        # Reset best algorithm panel
        self.best_algorithm.reset()

        # Reset comparison table
        self.comparison_table.display({})

        # Reset graph
        self.graph_panel.clear_graph()

        # Reset gantt chart
        self.gantt_chart.draw([])

        # Remove stored data
        if hasattr(self, "last_result"):
            del self.last_result

        if hasattr(self, "comparison_results"):
            del self.comparison_results

        self.status.set(
            "Status : Application reset successfully"
        )
    # ==================================================
    # VALIDATE PROCESS COUNT
    # ==================================================
    def validate_process_count(self, value):
            if value == "":
                return True

            if value.isdigit():

                number = int(value)

                if 1 <= number <= 100:
                    return True

            return False

    # ==================================================
    # START APPLICATION
    # ==================================================

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    app = CPUSchedulerGUI()

    app.run()