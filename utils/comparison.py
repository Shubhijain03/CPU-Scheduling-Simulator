import copy
from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.priority import priority
from algorithms.priority_preemptive import priority_preemptive
from algorithms.round_robin import round_robin
from algorithms.hrrn import hrrn


from utils.metrics import (
    average_waiting_time,
    average_turnaround_time,
    average_response_time,
    cpu_utilization,
    throughput,
)


def compare_all(processes, quantum):

    comparison_results = {}

    algorithms = [
        ("FCFS", fcfs),
        ("SJF", sjf),
        ("SRTF", srtf),
        ("Priority", priority),
        ("Priority Preemptive", priority_preemptive),
        ("HRRN", hrrn),
    ]

    for name, algorithm in algorithms:

        process_copy = copy.deepcopy(processes)

        result = algorithm(process_copy)

        comparison_results[name] = {
            "Average Waiting Time": average_waiting_time(result),
            "Average Turnaround Time": average_turnaround_time(result),
            "Average Response Time": average_response_time(result),
            "CPU Utilization": cpu_utilization(result),
            "Throughput": throughput(result),
        }

    rr_processes = copy.deepcopy(processes)

    rr_result = round_robin(rr_processes, quantum)

    comparison_results["Round Robin"] = {
        "Average Waiting Time": average_waiting_time(rr_result),
        "Average Turnaround Time": average_turnaround_time(rr_result),
        "Average Response Time": average_response_time(rr_result),
        "CPU Utilization": cpu_utilization(rr_result),
        "Throughput": throughput(rr_result),
    }

    return comparison_results