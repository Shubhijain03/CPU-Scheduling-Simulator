from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

from utils.csv_reader import read_process_file


def open_csv():

    path = filedialog.askopenfilename(
        title="Select Process File",
       filetypes=[
            ("Supported Files", "*.csv *.xlsx"),
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx"),
            ("All Files", "*.*")
        ]
    )

    if not path:
        return None

    try:
        processes = read_process_file(path)

        if not processes:
            Messagebox.show_warning(
                "The selected file does not contain any process data.",
                "Empty File"
            )
            return None

        return processes

    except FileNotFoundError:

        Messagebox.show_error(
            "The selected file could not be found.",
            "File Error"
        )
        
    except ValueError as error:

        Messagebox.show_error(
           f"Invalid file format.\n\n{error}"
        )

    except Exception as error:

        Messagebox.show_error(
            f"Unexpected error while reading CSV.\n\n{error}",
            "Error"
        )

    return None