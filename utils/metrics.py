def average_waiting_time(processes):
    # Returns the average waiting time.
    total = 0
    for process in processes:
        total += process.waiting_time

    return total / len(processes)


def average_turnaround_time(processes):
    # Returns the average turnaround time.
    total = 0

    for process in processes:
        total += process.turnaround_time

    return total / len(processes)


def average_response_time(processes):
    # Returns the average response time.
    total = 0

    for process in processes:
        total += process.response_time

    return total / len(processes)


def cpu_utilization(processes):
    #CPU Utilization (%)
    total_burst = 0

    for process in processes:
        total_burst += process.burst_time

    finish_time = max(
        process.completion_time
        for process in processes
    )
    return (total_burst / finish_time) * 100


def throughput(processes):
    # Processes completed per unit time.
    finish_time = max(
        process.completion_time
        for process in processes
    )
    return len(processes) / finish_time