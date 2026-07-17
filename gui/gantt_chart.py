import ttkbootstrap as ttk
from tkinter import Canvas


class GanttChart(ttk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Execution Timeline"
        )

        container = ttk.Frame(self)
        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.canvas = Canvas(
            container,
            bg="#09070A",
            highlightthickness=0,
            height=270
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # DRAW GANTT CHART
    # ==================================================

    def draw(self, processes):

        self.canvas.delete("all")

        timeline = []

        for process in processes:

            for start, end in process.execution_log:

                timeline.append(
                    (
                        start,
                        end,
                        process.pid
                    )
                )

        timeline.sort(key=lambda x: x[0])

        if not timeline:
            return

        total_time = timeline[-1][1]

        self.canvas.update_idletasks()

        canvas_width = max(
            self.canvas.winfo_width(),
            950
        )

        left_margin = 55
        right_margin = 45

        usable_width = canvas_width - left_margin - right_margin

        scale = usable_width / max(total_time, 1)

        top = 70
        bar_height = 65

        colors = [
            "#945BB7",
            "#7B4FA1",
            "#5D3A87",
            "#B57EDC",
            "#8A63C9",
            "#6A4FB5",
            "#A27FD8",
            "#C8B8DD"
        ]

        color_map = {}
        color_index = 0

        # ==========================================
        # Title
        # ==========================================

        self.canvas.create_text(
            left_margin,
            28,
            text="CPU Execution Timeline",
            anchor="w",
            fill="#EBE3F2",
            font=("Segoe UI Semibold", 15)
        )

        # ==========================================
        # Initial Time
        # ==========================================

        self.canvas.create_text(
            left_margin,
            top + bar_height + 22,
            text=str(timeline[0][0]),
            fill="#C8B8DD",
            font=("Segoe UI", 10)
        )

        # ==========================================
        # Draw Processes
        # ==========================================

        for start, end, pid in timeline:

            if pid not in color_map:

                color_map[pid] = colors[
                    color_index % len(colors)
                ]

                color_index += 1

            x1 = left_margin + start * scale
            x2 = left_margin + end * scale

            self.canvas.create_rectangle(
                x1,
                top,
                x2,
                top + bar_height,
                fill=color_map[pid],
                outline="#EBE3F2",
                width=2
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                top + bar_height / 2,
                text=pid,
                fill="#FFFFFF",
                font=("Segoe UI Semibold", 11)
            )

            self.canvas.create_text(
                x2,
                top + bar_height + 22,
                text=str(end),
                fill="#C8B8DD",
                font=("Segoe UI", 10)
            )

        # ==========================================
        # Timeline Line
        # ==========================================

        self.canvas.create_line(
            left_margin,
            top + bar_height,
            canvas_width - right_margin,
            top + bar_height,
            fill="#945BB7",
            width=2
        )

        # ==========================================
        # Legend
        # ==========================================

        legend_y = top + bar_height + 60

        self.canvas.create_text(
            left_margin,
            legend_y,
            text="Legend",
            anchor="w",
            fill="#EBE3F2",
            font=("Segoe UI Semibold", 11)
        )

        x = left_margin + 80

        for pid, color in color_map.items():

            self.canvas.create_rectangle(
                x,
                legend_y - 8,
                x + 18,
                legend_y + 8,
                fill=color,
                outline="#EBE3F2"
            )

            self.canvas.create_text(
                x + 28,
                legend_y,
                text=pid,
                anchor="w",
                fill="#EBE3F2",
                font=("Segoe UI", 10)
            )

            x += 70