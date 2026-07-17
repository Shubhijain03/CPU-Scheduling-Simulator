def hrrn(processes):

    processes = sorted(processes, key=lambda x: x.arrival_time)

    current_time = 0
    completed = 0
    n = len(processes)

    visited = [False] * n

    while completed < n:

        idx = -1
        highest_ratio = -1

        # Find process with highest response ratio
        for i in range(n):

            if not visited[i] and processes[i].arrival_time <= current_time:

                waiting = current_time - processes[i].arrival_time

                ratio = (waiting + processes[i].burst_time) / processes[i].burst_time

                if ratio > highest_ratio:
                    highest_ratio = ratio
                    idx = i

        # CPU Idle
        if idx == -1:
            current_time += 1
            continue

        process = processes[idx]

        process.response_time = current_time - process.arrival_time

        start = current_time
        current_time += process.burst_time
        end = current_time
        process.execution_log.append((start, end))

        process.completion_time = current_time

        process.turnaround_time = (
            process.completion_time - process.arrival_time
        )

        process.waiting_time = (
            process.turnaround_time - process.burst_time
        )

        process.remaining_time = 0

        visited[idx] = True
        completed += 1

    return processes