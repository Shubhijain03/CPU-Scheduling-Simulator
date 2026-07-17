import heapq
def priority(processes):
    processes=sorted(processes,key=lambda x:x.arrival_time)
    
    i=0
    heap=[]
    current_time=0
    
    while i<len(processes) or heap:
        while i<len(processes) and processes[i].arrival_time <= current_time:
            #Smaller priority value = Higher priority
            heapq.heappush(heap,(processes[i].priority,processes[i].burst_time,processes[i].arrival_time,processes[i].pid,processes[i]))
            i+=1
            
        if not heap:
            current_time=processes[i].arrival_time
        else:
             _,_,_,_,process=heapq.heappop(heap)
             #response time
             process.response_time=current_time - process.arrival_time
             
             start = current_time
             end = current_time + process.burst_time
             process.execution_log.append((start, end))
             
             #execution time
             current_time += process.burst_time
                
             #compeltion time
             process.completion_time=current_time
                
             #turnaround time
             process.turnaround_time=process.completion_time - process.arrival_time
                
             #waiting time 
             process.waiting_time=process.turnaround_time - process.burst_time
    return processes
                