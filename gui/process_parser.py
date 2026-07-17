from models.process import Process
import ttkbootstrap as ttk


def get_processes_from_table(process_table):

    processes = []

    for row in process_table.rows:

        try:
            pid = row["pid"]

            arrival = int(row["arrival"].get())
            burst = int(row["burst"].get())
            priority = int(row["priority"].get())

            if arrival < 0:
                raise ValueError("Arrival Time cannot be negative.")

            if burst <= 0:
                raise ValueError("Burst Time must be greater than 0.")

            if priority < 0:
                raise ValueError("Priority cannot be negative.")

            process = Process(
                pid=pid,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            )

            processes.append(process)

        except ValueError as e:

            ttk.Messagebox.show_error(
                f"{pid}: {e}",
                "Invalid Input"
            )

            return None

    return processes