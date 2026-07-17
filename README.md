# CPU Scheduling Simulator

A modern desktop application built using **Python**, **Tkinter**, and **ttkbootstrap** for simulating and comparing CPU Scheduling Algorithms. The simulator provides an intuitive dark-themed graphical interface for process management, execution visualization, performance analysis, and professional report generation.

---

# Features

## CPU Scheduling Algorithms

The simulator supports the following scheduling algorithms:

- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Shortest Remaining Time First (SRTF)
- Priority Scheduling (Non-Preemptive)
- Priority Scheduling (Preemptive)
- Round Robin (RR)
- Highest Response Ratio Next (HRRN)

---

# Application Features

- Professional desktop GUI built with Tkinter and ttkbootstrap
- Modern dark-themed interface
- Interactive process input table
- Dynamic process addition and deletion
- Automatic input validation
- CSV (.csv) file import
- Excel (.xlsx) file import
- Export comparison results to Excel
- Professional Gantt Chart visualization
- Execution results table
- Performance Metrics Dashboard
- Best Algorithm Recommendation Panel
- Algorithm comparison table
- Performance analytics graphs
- Professional PDF report generation
- Reset functionality
- Comprehensive error handling

---

# Application Preview

## Complete Application

![Complete Window](screenshots/complete_window.png)

---

## Process Management

### Process Input

![Process Input](screenshots/process_input.png)

### Control Panel

![Control Panel](screenshots/control_panel.png)

### Algorithm Configuration

![Algorithm Configuration](screenshots/algorithm_configuration.png)

---

## Scheduling Results

### Execution Results

![Scheduling Results](screenshots/scheduling_result.png)

### Execution Timeline

![Execution Timeline](screenshots/execution_timeline.png)

### Gantt Chart

![Gantt Chart](screenshots/gantt_chart.png)

---

## Performance Analysis

### Performance Metrics

![Performance Metrics](screenshots/performance_metrics.png)

### Best Algorithm Recommendation

![Best Algorithm](screenshots/best_algorithm.png)

---

## Import & Export

### CSV / Excel Import

![Import CSV](screenshots/import_csv.png)

### PDF Report Export

![PDF Export](screenshots/pdf_export.png)

### Excel Export

![Excel Export](screenshots/excel_export.png)

---

# Performance Metrics

The simulator automatically calculates:

- Completion Time (CT)
- Turnaround Time (TAT)
- Waiting Time (WT)
- Response Time (RT)
- Average Waiting Time
- Average Turnaround Time
- Average Response Time
- CPU Utilization
- Throughput

---

# Technologies Used

- Python 3
- Tkinter
- ttkbootstrap
- Matplotlib
- ReportLab
- OpenPyXL
- CSV Module

---

# Project Structure

```text
CPU_Scheduling_Simulator/
│
├── algorithms/
│   ├── fcfs.py
│   ├── hrrn.py
│   ├── priority.py
│   ├── priority_preemptive.py
│   ├── round_robin.py
│   ├── sjf.py
│   └── srtf.py
│
├── gui/
│   ├── app.py
│   ├── best_algorithm.py
│   ├── comparison_table.py
│   ├── csv_handler.py
│   ├── gantt_chart.py
│   ├── graphs.py
│   ├── metrics_panel.py
│   ├── process_parser.py
│   ├── process_table.py
│   └── results_table.py
│
├── models/
│   └── process.py
│
├── utils/
│   ├── comparison.py
│   ├── csv_reader.py
│   ├── metrics.py
│   └── pdf_export.py
│
├── screenshots/
├── requirements.txt
├── README.md
└── sample_processes.csv
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/CPU_Scheduling_Simulator.git
```

Navigate to the project directory:

```bash
cd CPU_Scheduling_Simulator
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Launch the simulator using:

```bash
python -m gui.app
```

---

# Sample Input File

The simulator supports both **CSV (.csv)** and **Excel (.xlsx)** files.

Example:

```csv
PID,Arrival,Burst,Priority
P1,0,5,2
P2,1,3,1
P3,2,6,4
P4,4,2,3
```

The application also accepts common column name variations such as:

- Process ID
- Arrival Time
- Burst Time
- Priority Level
- AT
- BT
- PR

---

# Visualizations

The simulator provides:

- CPU Execution Gantt Chart
- Average Waiting Time Comparison
- Average Turnaround Time Comparison
- Average Response Time Comparison
- CPU Utilization Comparison
- Throughput Comparison

---

# Export Options

The application supports:

- PDF Report Export
- Excel Export (Algorithm Comparison)

---

# PDF Report

The generated report includes:

- Execution Summary
- Process Execution Details
- Performance Metrics
- Professional Formatting
- Page Numbers
- Styled Footer

---

# Learning Outcomes

This project demonstrates:

- CPU Scheduling Algorithms
- Operating System Concepts
- Process Scheduling Simulation
- Object-Oriented Programming
- GUI Development using Tkinter
- Data Visualization
- File Handling (CSV & Excel)
- PDF Report Generation
- Desktop Application Development
- Modular Software Design

---

# Future Enhancements

Potential future improvements include:

- Multi-Level Queue Scheduling
- Multi-Level Feedback Queue (MLFQ)
- Aging Technique
- Timeline Animation
- Additional Scheduling Algorithms
- Custom Theme Support

---

# Author

**Shubhi Jain**

BCA Graduate | Python Developer | Operating Systems | Desktop Application Development

---
