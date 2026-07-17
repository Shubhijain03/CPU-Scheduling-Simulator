import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ProcessTable(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.rows = []
        self.create_table()

    # ==================================================
    # TABLE HEADER
    # ==================================================

    def create_table(self):

        headers = [
            "PROCESS ID",
            "ARRIVAL TIME",
            "BURST TIME",
            "PRIORITY"
        ]

        for column, text in enumerate(headers):

            header = ttk.Label(
                self,
                text=text,
                font=("Segoe UI Semibold", 12),
                anchor="center",
                foreground="#EBE3F2",
                background="#2A1240"
            )

            header.grid(
                row=0,
                column=column,
                padx=10,
                pady=(0, 10),
                ipady=10,
                sticky="ew"
            )

            self.columnconfigure(
                column,
                weight=1,
                minsize=170
            )

    # ==================================================
    # GENERATE ROWS
    # ==================================================

    def generate_rows(self, count, default_values=False):

        for widget in self.winfo_children():

            if int(widget.grid_info()["row"]) != 0:
                widget.destroy()

        self.rows.clear()

        for row in range(count):

            pid = f"P{row + 1}"

            pid_label = ttk.Label(
                self,
                text=pid,
                font=("Segoe UI Semibold", 12),
                anchor="center",
                foreground="#C8B8DD"
            )

            pid_label.grid(
                row=row + 1,
                column=0,
                padx=10,
                pady=10,
                sticky="ew"
            )

            arrival = ttk.Entry(
                self,
                justify="center",
                width=16,
                font=("Segoe UI", 10)
            )

            burst = ttk.Entry(
                self,
                justify="center",
                width=16,
                font=("Segoe UI", 10)
            )

            priority = ttk.Entry(
                self,
                justify="center",
                width=16,
                font=("Segoe UI", 10)
            )

            for column, widget in enumerate(
                [arrival, burst, priority],
                start=1
            ):

                widget.grid(
                    row=row + 1,
                    column=column,
                    padx=10,
                    pady=10,
                    ipady=8,
                    sticky="ew"
                )

            arrival.insert(0, "0")
            burst.insert(0, "1")
            priority.insert(0, "1")

            self.make_editable(arrival, "0")
            self.make_editable(burst, "1")
            self.make_editable(priority, "1")

            self.rows.append(
                {
                    "pid": pid,
                    "arrival": arrival,
                    "burst": burst,
                    "priority": priority
                }
            )

    # ==================================================
    # PLACEHOLDER BEHAVIOUR
    # ==================================================

    def make_editable(self, entry, default_value):

        def clear_default(event):
            if entry.get() == default_value:
                entry.delete(0, END)

        def restore_default(event):
            if entry.get().strip() == "":
                entry.insert(0, default_value)

        entry.bind("<FocusIn>", clear_default)
        entry.bind("<FocusOut>", restore_default)