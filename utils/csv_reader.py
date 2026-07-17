import csv
import os

from openpyxl import load_workbook

from models.process import Process


def read_process_file(file_name):

    extension = os.path.splitext(file_name)[1].lower()

    if extension == ".csv":
        rows = _read_csv(file_name)

    elif extension == ".xlsx":
        rows = _read_excel(file_name)

    else:
        raise ValueError(
            "Only CSV (.csv) and Excel (.xlsx) files are supported."
        )

    return _parse_processes(rows)


def _read_csv(file_name):

    with open(
        file_name,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(
                "The selected file is empty."
            )

        return list(reader)


def _read_excel(file_name):

    workbook = load_workbook(
        file_name,
        data_only=True
    )

    sheet = workbook.active

    rows = list(sheet.values)

    if not rows:
        raise ValueError(
            "The selected file is empty."
        )

    headers = [
        str(header).strip()
        if header is not None else ""
        for header in rows[0]
    ]

    data = []

    for values in rows[1:]:

        row = {}

        for header, value in zip(headers, values):

            row[header] = (
                ""
                if value is None
                else str(value).strip()
            )

        data.append(row)

    return data

def normalize_row(row, aliases):

    normalized = {}

    lower_row = {
        str(key).strip().lower(): value
        for key, value in row.items()
    }

    for standard_name, possible_names in aliases.items():

        for name in possible_names:

            key = name.strip().lower()

            if key in lower_row:
                normalized[standard_name] = lower_row[key]
                break

    return normalized


def _parse_processes(rows):

    column_aliases = {
        "PID": [
            "PID",
            "Process ID",
            "ProcessID",
            "Process",
            "Id",
            "ID"
        ],

        "Arrival": [
            "Arrival",
            "Arrival Time",
            "ArrivalTime",
            "AT"
        ],

        "Burst": [
            "Burst",
            "Burst Time",
            "BurstTime",
            "BT",
            "CPU Burst"
        ],

        "Priority": [
            "Priority",
            "Priority Level",
            "PriorityLevel",
            "PR"
        ]
    }

    if not rows:
        raise ValueError(
            "The selected file contains no process data."
        )

    rows = [
        normalize_row(row, column_aliases)
        for row in rows
    ]

    required_columns = {
        "PID",
        "Arrival",
        "Burst",
        "Priority"
    }

    if not required_columns.issubset(rows[0].keys()):
        raise ValueError(
            "File must contain one of the supported column names for:\n"
            "PID, Arrival, Burst and Priority."
        )

    processes = []

    pids = set()

    for row_number, row in enumerate(rows, start=2):

        if any(
            row.get(column, "").strip() == ""
            for column in required_columns
        ):
            raise ValueError(
                f"Missing value found in row {row_number}."
            )

        pid = row["PID"].strip()

        if pid in pids:
            raise ValueError(
                f"Duplicate Process ID '{pid}' found in row {row_number}."
            )

        pids.add(pid)

        try:
            arrival = int(row["Arrival"])
            burst = int(row["Burst"])
            priority = int(row["Priority"])

        except ValueError:
            raise ValueError(
                f"Row {row_number} contains non-numeric values."
            )

        if arrival < 0:
            raise ValueError(
                f"Arrival Time cannot be negative (row {row_number})."
            )

        if burst <= 0:
            raise ValueError(
                f"Burst Time must be greater than 0 (row {row_number})."
            )

        if priority < 0:
            raise ValueError(
                f"Priority cannot be negative (row {row_number})."
            )

        processes.append(
            Process(
                pid=pid,
                arrival_time=arrival,
                burst_time=burst,
                priority=priority
            )
        )

    return processes