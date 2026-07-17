import heapq

def srtf(processes):
    # Sort by arrival time
    processes = sorted(processes, key=lambda x: x.arrival_time)

    heap = []      # (remaining_time, arrival_time, pid, process)
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
                    processes[i].remaining_time,
                    processes[i].arrival_time,
                    processes[i].pid,
                    processes[i]
                )
            )
            i += 1

        # If no process has arrived
        if not heap:
            current_time = processes[i].arrival_time
            continue

        # Process with shortest remaining time
        remaining_time, _, _, process = heapq.heappop(heap)

        # Response time
        if process.response_time == -1:
            process.response_time = current_time - process.arrival_time

        # Execute for 1 unit
        process.remaining_time -= 1
        
        start = current_time
        current_time += 1
        end = current_time
        process.execution_log.append((start, end))

        # Add newly arrived processes during this 1 unit
        while i < n and processes[i].arrival_time <= current_time:
            heapq.heappush(
                heap,
                (
                    processes[i].remaining_time,
                    processes[i].arrival_time,
                    processes[i].pid,
                    processes[i]
                )
            )
            i += 1

        # If process still has work left
        if process.remaining_time > 0:
            heapq.heappush(
                heap,
                (
                    process.remaining_time,
                    process.arrival_time,
                    process.pid,
                    process
                )
            )
        else:
            # Completion time
            process.completion_time = current_time

            # Turnaround time
            process.turnaround_time = (
                process.completion_time - process.arrival_time
            )

            # Waiting time
            process.waiting_time = (
                process.turnaround_time - process.burst_time
            )

            completed += 1

    return processes