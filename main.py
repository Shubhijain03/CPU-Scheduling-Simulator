import copy
import sys
from utils.csv_reader import read_csv

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority
from algorithms.priority_preemptive import priority_preemptive
from algorithms.round_robin import round_robin
from algorithms.hrrn import hrrn
from utils.comparison import compare_all

from utils.metrics import (
    average_waiting_time,
    average_turnaround_time,
    average_response_time,
    cpu_utilization,
    throughput,
)
from utils.graph import (
    plot_average_waiting_time,
    plot_average_turnaround_time,
    plot_average_response_time,
    plot_cpu_utilization,
    plot_throughput,
)
from utils.gantt_chart import display_gantt_chart

def print_table(processes):
    print("-" * 70)
    print(f"{'PID':<6}{'AT':<6}{'BT':<6}{'PR':<6}{'CT':<6}{'TAT':<8}{'WT':<6}{'RT':<6}")
    print("-" * 70)

    for process in processes:
        print(
            f"{process.pid:<6}"
            f"{process.arrival_time:<6}"
            f"{process.burst_time:<6}"
            f"{process.priority:<6}"
            f"{process.completion_time:<6}"
            f"{process.turnaround_time:<8}"
            f"{process.waiting_time:<6}"
            f"{process.response_time:<6}"
        )
processes = copy.deepcopy(read_csv("processes.csv"))
comparison_results = {}

print("1. FCFS")
print("2. SJF")
print("3. SRTF")
print("4. Priority")
print("5. Priority Preemptive")
print("6. Round Robin")
print("7. HRRN")
print("8. Compare All Algorithms")

choice = int(input("Enter your choice: "))

if choice == 6:
    quantum = int(input("Enter Time Quantum: "))
    
if choice == 1:
    result = fcfs(processes)

elif choice == 2:
    result = sjf(processes)

elif choice == 3:
    result = srtf(processes)

elif choice == 4:
    result = priority(processes)

elif choice == 5:
    result = priority_preemptive(processes)

elif choice == 6:
    result = round_robin(processes, quantum)

elif choice == 7:
    result = hrrn(processes)
elif choice == 8:
    quantum = int(input("Enter Time Quantum for Round Robin: "))
    comparison_results = compare_all(processes, quantum)
    
    print("\nAlgorithm Comparison")
    print("-" * 90)

    print(
        f"{'Algorithm':<25}"
        f"{'Avg WT':<12}"
        f"{'Avg TAT':<12}"
        f"{'Avg RT':<12}"
        f"{'CPU Util':<12}"
        f"{'Throughput':<12}"
    )

    print("-" * 90)

    for name, metrics in comparison_results.items():
        print(
            f"{name:<25}"
            f"{metrics['Average Waiting Time']:<12.2f}"
            f"{metrics['Average Turnaround Time']:<12.2f}"
            f"{metrics['Average Response Time']:<12.2f}"
            f"{metrics['CPU Utilization']:<12.2f}"
            f"{metrics['Throughput']:<12.2f}"
        )
    plot_average_waiting_time(comparison_results)
    plot_average_turnaround_time(comparison_results)
    plot_average_response_time(comparison_results)
    plot_cpu_utilization(comparison_results)
    plot_throughput(comparison_results)
    sys.exit()
else:
    print("Invalid Choice")
    sys.exit()
    

print_table(result)

print()

display_gantt_chart(result)

print("\nPerformance Metrics")
print("-------------------")
print(f"Average Waiting Time    : {average_waiting_time(result):.2f}")
print(f"Average Turnaround Time : {average_turnaround_time(result):.2f}")
print(f"Average Response Time   : {average_response_time(result):.2f}")
print(f"CPU Utilization         : {cpu_utilization(result):.2f}%")
print(f"Throughput              : {throughput(result):.2f}")