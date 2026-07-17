import heapq

def priority_preemptive(processes):

    # Sort according to arrival time
    processes = sorted(processes, key=lambda x: x.arrival_time)

    heap = []      # (priority, arrival_time, pid, process)
    current_time = 0
    i = 0
    completed = 0
    n = len(processes)

    while completed < n:

        # Add all arrived processes
        while i < n and processes[i].arrival_time <= current_time:
            heapq.heappush(
                heap,
                (
                    processes[i].priority,
                    processes[i].arrival_time,
                    processes[i].pid,
                    processes[i]
                )
            )
            i += 1

        # CPU Idle
        if not heap:
            current_time = processes[i].arrival_time
            continue

        # Get highest priority process
        priority, _, _, process = heapq.heappop(heap)

        # Response time
        if process.response_time == -1:
            process.response_time = current_time - process.arrival_time

        # Execute for 1 unit
        start = current_time
        process.remaining_time -= 1
        current_time += 1
        end = current_time
        process.execution_log.append((start, end))
       

        # Add newly arrived processes
        while i < n and processes[i].arrival_time <= current_time:
            heapq.heappush(
                heap,
                (
                    processes[i].priority,
                    processes[i].arrival_time,
                    processes[i].pid,
                    processes[i]
                )
            )
            i += 1

        # Process not finished
        if process.remaining_time > 0:
            heapq.heappush(
                heap,
                (
                    process.priority,
                    process.arrival_time,
                    process.pid,
                    process
                )
            )
        else:
            # Completion Time
            process.completion_time = current_time

            # Turnaround Time
            process.turnaround_time = (
                process.completion_time - process.arrival_time
            )

            # Waiting Time
            process.waiting_time = (
                process.turnaround_time - process.burst_time
            )

            completed += 1

    return processes