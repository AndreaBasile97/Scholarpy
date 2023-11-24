import re
import pandas
import pandas as pd
import os
import requests
from colorama import Fore, Style

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


def make_api_request(url, api_key=None):
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key
    else:
        print(f"{Fore.YELLOW}Warning: API key not provided. Some API calls may be limited.{Style.RESET_ALL}")

    response = requests.get(url, headers=headers)
    
    while response.status_code >= 500:
        response = requests.get(url, headers=headers)
    
    return response

# Esempio di utilizzo
# file_path = "bulk.txt"
# result = read_and_split_lines(file_path)
# print(result)
# csv_files_list = [
#     "Adversarial attacks on medical machine learning  Science.csv",
#     "Big data and machine learning algorithms for health-care delivery - The Lancet Oncology.csv",
#     "Do no harm a roadmap for responsible machine learning for health care Nature Medicine.csv",
#     "Patient clustering improves efficiency of federated machine learning to predict mortality and hospital stay time using distributed electronic medical records  ScienceDirect.csv",
#     "Preparing Medical Imaging Data for Machine Learning  Radiology (rsna.org).csv",
#     "Secure, privacy-preserving and federated machine learning in medical imaging Nature Machine Intelligence.csv",
#     "Swarm Learning for decentralized and confidential clinical machine learning  Nature.csv",
#     "The importance of interpretability and visualization in machine learning for applications in medicine and health care  SpringerLink.csv",
#     "What Clinicians Want Contextualizing Explainable Machine Learning for Clinical End Use (mlr.press).csv",
# ]
# csv_appender(csv_files_list)


# names_list = get_csv_names("forward")
# csv_appender(names_list)