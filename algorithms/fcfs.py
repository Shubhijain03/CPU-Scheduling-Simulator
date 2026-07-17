def fcfs(processes):
    processes.sort(key=lambda x:x.arrival_time)
    current_time=0
    
    for process in processes:
        if current_time<process.arrival_time :
            current_time=process.arrival_time
            
        #response_time
        process.response_time=current_time-process.arrival_time
        
        start = current_time
        end = current_time + process.burst_time
        process.execution_log.append((start, end))
        
        # Execute the process
        current_time += process.burst_time

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

    return processes
        
        
        