from collections import deque
def round_robin(processes,quantum):
    q=deque()
    processes=sorted(processes,key=lambda x:x.arrival_time)
    current_time=0
    i=0
    while i<len(processes) or q:
        while i<len(processes) and processes[i].arrival_time <= current_time:
            q.append(processes[i])
            i+=1
        if not q :
            current_time=processes[i].arrival_time
            continue
        process=q.popleft()
        if process.response_time ==-1:
            process.response_time = current_time - process.arrival_time
        execution_time = min(process.remaining_time, quantum)
        
        start = current_time
        current_time += execution_time
        end = current_time
        process.execution_log.append((start, end))
        
        #remaining time
        process.remaining_time -= execution_time
        
        
        while i < len(processes) and processes[i].arrival_time <= current_time:
            q.append(processes[i])
            i += 1
        if process.remaining_time >0:
            q.append(process)
        else:
            #completion time
            process.completion_time=current_time
            
            #turnaround ime
            process.turnaround_time = process.completion_time - process.arrival_time
            
            #waiting time 
            process.waiting_time=process.turnaround_time - process.burst_time  
    return processes   
            
                
        
