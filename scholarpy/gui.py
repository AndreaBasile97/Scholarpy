import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from snowballer import search_paper_id, get_citations_info
from utils import clean_filename, read_and_split_lines
import time
from auto_pdf_downloader import get_paper_details, get_pdf_urls, download_pdfs


class SnowballerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Creazione e posizionamento degli elementi dell'interfaccia
        tk.Label(self, text="Paper Title:").grid(row=0, column=0, padx=10, pady=5)
        self.paper_title_entry = tk.Entry(self)
        self.paper_title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="Paper ID:").grid(row=1, column=0, padx=10, pady=5)
        self.paper_id_entry = tk.Entry(self)
        self.paper_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="CSV Filename:").grid(row=2, column=0, padx=10, pady=5)
        self.csv_filename_entry = tk.Entry(self)
        self.csv_filename_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="Limit:").grid(row=3, column=0, padx=10, pady=5)
        self.limit_entry = tk.Entry(self)
        self.limit_entry.grid(row=3, column=1, padx=10, pady=5)

        # Radio buttons for Forward and Backward
        self.snowball_direction = tk.IntVar()
        self.snowball_direction.set(1)  # default to Forward

        forward_radio = tk.Radiobutton(
            self, text="Forward", variable=self.snowball_direction, value=1
        )
        forward_radio.grid(row=4, column=0, padx=10, pady=5)

        backward_radio = tk.Radiobutton(
            self, text="Backward", variable=self.snowball_direction, value=0
        )
        backward_radio.grid(row=4, column=1, padx=10, pady=5)

        self.snowball_button = tk.Button(self, text="Snowball", command=self.snowball)
        self.snowball_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Aggiungo un unico label per mostrare il risultato
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)

    def snowball(self):
        # Ottieni i valori inseriti dall'utente
        paper_title = self.paper_title_entry.get()
        paper_id = self.paper_id_entry.get()
        csv_filename = self.csv_filename_entry.get()
        limit = int(self.limit_entry.get()) if self.limit_entry.get() else 1000

        # Controlla che almeno uno tra paper_title e paper_id sia stato fornito
        if not paper_title and not paper_id:
            messagebox.showerror("Errore", "Inserisci almeno Paper Title o Paper ID")
            return

        # Se il paper_id non è fornito, esegui la ricerca
        if not paper_id:
            paper_id = search_paper_id(paper_title)

        if paper_id:
            try:
                # Ottieni le informazioni sulle citazioni e salva nel file CSV
                forward = bool(self.snowball_direction.get())
                get_citations_info(
                    paper_id, clean_filename(csv_filename), limit, forward
                )
                self.result_label.config(
                    text=f"Dati salvati correttamente in {csv_filename}", fg="green"
                )
            except Exception as e:
                self.result_label.config(
                    text=f"Errore durante l'esecuzione: {str(e)}", fg="red"
                )
        else:
            self.result_label.config(
                text=f"Nessun paper ID trovato per '{paper_title}'", fg="red"
            )


class BulkSnowballerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Creazione e posizionamento degli elementi dell'interfaccia
        tk.Label(self, text="Upload Txt File:").grid(row=0, column=0, padx=10, pady=5)
        self.upload_button = tk.Button(self, text="Upload", command=self.upload_file)
        self.upload_button.grid(row=0, column=1, padx=10, pady=5)

        # Radio buttons for Forward and Backward
        self.snowball_direction = tk.IntVar()
        self.snowball_direction.set(1)  # default to Forward

        forward_radio = tk.Radiobutton(
            self, text="Forward", variable=self.snowball_direction, value=1
        )
        forward_radio.grid(row=1, column=0, padx=10, pady=5)

        backward_radio = tk.Radiobutton(
            self, text="Backward", variable=self.snowball_direction, value=0
        )
        backward_radio.grid(row=1, column=1, padx=10, pady=5)

        self.snowball_button = tk.Button(
            self, text="Bulk Snowball", command=self.bulk_snowball
        )
        self.snowball_button.grid(row=2, column=0, columnspan=2, pady=10)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a TXT file")

    def bulk_snowball(self):
        if not hasattr(self, "file_path"):
            messagebox.showerror("Errore", "Seleziona prima un file TXT.")
            return

        paper_list = read_and_split_lines(self.file_path)
        forward = bool(self.snowball_direction.get())

        for paper in paper_list:
            print(paper)
            time.sleep(2)
            paper_id = search_paper_id(paper)
            print(paper_id)
            try:
                get_citations_info(
                    paper_id=paper_id,
                    csv_filename=f"{paper_id}.csv",
                    limit=1000,
                    forward=forward,
                )
            except:
                print(f"paper :{paper} non trovato")


class AutoPDFdownloader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Creazione e posizionamento degli elementi dell'interfaccia
        tk.Label(self, text="Upload Txt File containing PDF ids:").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.upload_button = tk.Button(self, text="Upload", command=self.upload_file)
        self.upload_button.grid(row=0, column=1, padx=10, pady=5)

        self.download_button = tk.Button(self, text="Download", command=self.download)
        self.download_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a TXT file")

    def download(self):
        if not hasattr(self, "file_path"):
            messagebox.showerror("Errore", "Seleziona prima un file TXT.")
            return

        paper_list_ids = read_and_split_lines(self.file_path)

        papers_details = get_paper_details(paper_list_ids)
        pdf_urls, pdf_titles = get_pdf_urls(papers_details)
        download_pdfs(pdf_urls, pdf_titles)
        self.result_label.config(
            text=f"Ho salvato i pdf. Puoi trovare quelli scartati in pdf_not_found_titles.txt e pdf_not_downloaded.txt",
            fg="green",
        )


class SnowballerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Scholarpy - by Andrea Basile")
        self.create_menu()
        self.current_frame = None

    def create_menu(self):
        menu_bar = tk.Menu(self)

        # Creazione del menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label="Single Paper Search", command=self.show_single_paper_search
        )
        file_menu.add_command(label="Bulk Search", command=self.show_bulk_search)
        file_menu.add_command(
            label="Auto PDF downloader", command=self.show_pdf_downloader
        )
        menu_bar.add_cascade(label="Menu", menu=file_menu)

        self.config(menu=menu_bar)

    def show_single_paper_search(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SnowballerGUI(self)
        self.current_frame.grid()

    def show_bulk_search(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = BulkSnowballerGUI(self)
        self.current_frame.grid()

    def show_pdf_downloader(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AutoPDFdownloader(self)
        self.current_frame.grid()


if __name__ == "__main__":
    app = SnowballerApp()
    app.mainloop()
