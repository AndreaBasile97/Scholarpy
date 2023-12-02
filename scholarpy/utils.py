import re
import pandas
import pandas as pd
import os
import requests
from colorama import Fore, Style
import csv
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def write_to_csv(csv_path, fieldnames, data, modality="w"):
    with open(csv_path, modality, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file is empty, write the header
        if modality == "w":
            writer.writeheader()

        writer.writerows(data)


def get_paper_details_batch(
    paper_ids, fields=["referenceCount", "citationCount", "title", "openAccessPdf"]
):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/batch"
    paper_ids = [id for id in paper_ids if id is not None]
    print(f"get_paper_details_batch({paper_ids}, {fields})")
    payload = {"ids": paper_ids}
    response = make_api_request(
        url=base_url,
        params={"fields": ",".join(fields)},
        payload=payload,
        api_key=api_key,
    )

    if response.status_code == 200:
        paper_details = response.json()
        # Restituisci i dettagli, inclusi gli URL degli articoli in formato PDF
        return paper_details
    else:
        print(f"Errore nella richiesta batch: {response.status_code} per {paper_ids}")
        return None


def extract_paper_details_batch(paper_details):
    extracted_data = []
    for paper in paper_details:
        extracted_paper = {}

        # Estrai i dettagli richiesti
        extracted_paper["title"] = paper.get("title", "")
        extracted_paper["citationStyles"] = paper.get("citationStyles", "")
        extracted_paper["authors"] = ", ".join(
            [author["name"] for author in paper.get("authors", [])]
        )
        extracted_paper["year"] = paper.get("year", "")
        try:
            extracted_paper["journal"] = paper.get("journal", "").get("name", "")
        except:
            extracted_paper["journal"] = "N/A"
        try:
            external_ids = paper.get("externalIds", {})
            extracted_paper["DOI"] = (
                external_ids.get("DOI", "N/A") if external_ids else "N/A"
            )
        except:
            pass

        extracted_data.append(extracted_paper)

    csv_path = "paper_details.csv"
    fieldnames = ["title", "citationStyles", "authors", "year", "journal", "DOI"]
    print(extracted_data)
    write_to_csv(csv_path, fieldnames, extracted_data, modality="a")

    return extracted_data


def search_paper_id(paper_title):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    search_url = f"{base_url}?query={paper_title}"

    response = make_api_request(search_url, api_key=api_key)

    if response.status_code == 200:
        search_data = response.json()
        papers = search_data.get("data", [])

        if papers and papers[0].get("paperId") is not None:
            # Return the paper ID of the first result of the search
            return papers[0].get("paperId")
        else:
            print(f"No results found for '{paper_title}'. Writing to file.")
            filename = f"paper_ids_not_found_for_these_titles.txt"

            with open(filename, "a") as file:
                file.write(f"{paper_title}\n")

    else:
        print(f"Error in single request: {response.status_code}")


def clean_filename(title):
    # Rimuovi tutti i caratteri speciali non consentiti per i nomi di file
    return re.sub(r'[\/:*?"<>|-]', "", title)


def get_csv_names(path_cartella):
    # Verifica se il percorso esiste
    if not os.path.exists(path_cartella):
        raise FileNotFoundError(f"Il percorso '{path_cartella}' non esiste.")

    # Ottieni la lista dei file nella cartella
    files = os.listdir(path_cartella)

    # Filtra solo i file con estensione .csv
    csv_files = [file for file in files if file.endswith(".csv")]

    # Restituisci la lista di file CSV completi di percorso
    csv_paths = [os.path.join(path_cartella, csv_file) for csv_file in csv_files]

    return csv_paths


def csv_appender(csv_files):
    # Check if the list of CSV files is not empty
    if not csv_files:
        print("Error: The list of CSV files is empty.")
        return

    # Read the first CSV file to get the column headers
    first_file = csv_files[0]
    try:
        df_first = pd.read_csv(first_file)
    except pd.errors.EmptyDataError:
        print(f"Error: {first_file} is empty or not a valid CSV file.")
        return

    # Check if all CSV files have the same column headers
    for file in csv_files[1:]:
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            print(f"Error: {file} is empty or not a valid CSV file.")
            return

        if not df.columns.equals(df_first.columns):
            print(f"Error: Column headers in {file} do not match the first CSV file.")
            return

    # Merge the CSV files
    result_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

    # Save the merged DataFrame to a new CSV file
    result_df.to_csv("merged_output.csv", index=False)

    print(f"Merged CSV files successfully. Result saved to 'merged_output.csv'.")


def read_and_split_lines(file_path):
    result = []

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

        # Rimuovi caratteri di nuova linea (\n) e spazi bianchi extra
        cleaned_lines = [line.strip() for line in lines]

        # Aggiungi le stringhe nella lista
        result.extend(cleaned_lines)

    return result


def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def make_api_request(url, params=None, payload={}, api_key=None):
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key
    else:
        print(
            f"{Fore.YELLOW}Warning: API key not provided. Some API calls may be limited.{Style.RESET_ALL}"
        )

    if params is None and payload == {}:
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, params=params, json=payload)

    while response.status_code >= 500:
        response = requests.get(url, headers=headers)

    return response


def paper_details_batch_wrapper(
    paper_titles_txt_path,
    fields=["titles", "citationStyles", "authors", "year", "journal"],
):
    paper_ids = []
    paper_list = read_and_split_lines(paper_titles_txt_path)
    for paper in paper_list:
        paper_ids.append(search_paper_id(paper))
    paper_ids = [id for id in paper_ids if id is not None]

    papers_details = get_paper_details_batch(paper_ids, fields=fields)
    extract_paper_details_batch(papers_details)
