import heapq
def sjf(processes):
    processes=sorted(processes,key=lambda x:x.arrival_time)
    
    current_time=0
    i=0
    heap=[]
    
    while i<len(processes) or heap:
        while i<len(processes)  and processes[i].arrival_time <= current_time :
            heapq.heappush(heap,(processes[i].burst_time,processes[i].arrival_time,processes[i].pid,processes[i]))
            i +=1
        
        if not heap:
            current_time=processes[i].arrival_time
        else :
            _,_,_,process=heapq.heappop (heap)
        
            #response time
            process.response_time=current_time-process.arrival_time
            
            start = current_time
            end = current_time + process.burst_time
            process.execution_log.append((start, end))
            
            #execution _time
            current_time  += process.burst_time
            
            #completion time
            process.completion_time=current_time
            
            #Turnaround time
            process.turnaround_time=process.completion_time - process.arrival_time
            
            #waiting time
            process.waiting_time=process.turnaround_time-process.burst_time
    return processes
            
            
            
            
         
         
         
         
         
         
         
         
         
         
         
            