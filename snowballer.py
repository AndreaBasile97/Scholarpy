import requests
import csv
import argparse
from utils import clean_filename
import os


def search_paper_id(paper_title):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    search_url = f"{base_url}?query={paper_title}"

    response = requests.get(search_url)

    if response.status_code == 200:
        search_data = response.json()
        papers = search_data.get("data", [])

        if papers:
            # Restituisci il paper ID del primo risultato della ricerca
            return papers[0].get("paperId", None)
        else:
            print(f"Nessun risultato trovato per '{paper_title}'.")
            return None
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None


def get_citations_info(paper_id, csv_filename, limit=1000, forward=True):
    if forward:
        snowballing_type = "citations"
        folder_name = "forward"
    else:
        snowballing_type = "references"
        folder_name = "backward"

    # Create the folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if csv_filename is None:
        csv_filename = f"{paper_id}.csv"

    csv_path = os.path.join(folder_name, csv_filename)

    base_url = "https://api.semanticscholar.org/graph/v1/paper/"
    citations_url = f"{base_url}{paper_id}/{snowballing_type}?fields=paperId,title,authors,journal,url,externalIds,year,fieldsOfStudy,citationStyles&limit={limit}"

    # Effettua la richiesta all'API
    response = requests.get(citations_url)

    # Verifica se la richiesta è andata a buon fine (status code 200)
    if response.status_code == 200:
        # Apri un file CSV in modalità scrittura
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            # Definisci i nomi delle colonne nel file CSV
            fieldnames = ["Id","Title", "BibTex", "DOI", "Authors", "Year", "Fields", "Link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Scrivi l'intestazione nel file CSV
            writer.writeheader()

            # Estrai la parte di dati dalla risposta
            data = response.json()["data"]

            # Itera attraverso ogni elemento nella lista "data"
            for entry in data:
                # Estrai le informazioni da ogni "citingPaper"
                if forward:
                    citing_paper = entry["citingPaper"]
                else:
                    citing_paper = entry["citedPaper"]
                titolo = citing_paper["title"]
                citing_paper_id = citing_paper["paperId"]
                journal = citing_paper.get("journal", {})
                fields_of_study = citing_paper.get("fieldsOfStudy")
                try:
                    bibTex = citing_paper.get("citationStyles", {}).get("bibtex")
                except:
                    pass
                try:
                    journal = journal.get("name", "N/A")
                except:
                    pass
                try:
                    doi = external_ids.get("DOI", "N/A")
                except:
                    doi = "N/A"
                external_ids = citing_paper.get("externalIds", {})
                link = citing_paper["url"]
                year = citing_paper["year"]
                autori = citing_paper.get("authors", [])

                # Extract all author names
                author_names = (
                    [author["name"] for author in autori] if autori else ["N/A"]
                )

                # Join the elements of fields_of_study list into a string
                fields_of_study_str = (
                    ", ".join(fields_of_study) if fields_of_study else "N/A"
                )

                # Scrivi le informazioni nel file CSV
                writer.writerow(
                    {
                        "Id": citing_paper_id,
                        "Title": titolo,
                        "BibTex": bibTex,
                        "DOI": doi,
                        "Authors": author_names,
                        "Year": year,
                        "Fields": fields_of_study_str,
                        "Link": link,
                    }
                )

        print(f"Dati salvati correttamente nel file CSV: {csv_path}")

    else:
        # Stampa un messaggio di errore se la richiesta non è andata a buon fine
        print(f"Errore nella richiesta API. Codice di stato: {response.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retrieve citation information for a paper."
    )
    parser.add_argument(
        "--paper_title",
        help="Title of the paper for which to retrieve citations.",
    )
    parser.add_argument(
        "--forward",
        help="forward True -> get the citations, else get the references (backward).",
    )
    parser.add_argument("--csv_filename", help="Filename for the CSV output.")
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Limit on the number of citations to retrieve.",
    )
    parser.add_argument(
        "--paper_id", help="ID of the paper for which to retrieve citations."
    )

    args = parser.parse_args()

    if args.paper_title:
        # Pulisci il titolo del paper prima di utilizzarlo
        args.paper_title = args.paper_title
    if args.paper_id is None:
        # If paper_id is not provided, search for it using paper_title
        args.paper_id = search_paper_id(args.paper_title)
    if args.paper_id:
        get_citations_info(args.paper_id, args.csv_filename, args.limit, args.forward)
