import requests
import csv
import argparse
from scholarpy.utils import clean_filename, create_folder_if_not_exists, make_api_request, read_and_split_lines
import os
import time
import os


from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")

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


def extract_citation_info(entry, forward=True):
    if forward:
        citing_paper = entry["citingPaper"]
    else:
        citing_paper = entry["citedPaper"]

    titolo = citing_paper["title"]
    citing_paper_id = citing_paper["paperId"]
    journal_info = citing_paper.get("journal", {})
    journal_name = journal_info.get("name", "N/A") if journal_info else "N/A"
    fields_of_study = citing_paper.get("fieldsOfStudy")
    citation_styles = citing_paper.get("citationStyles", {})
    bibTex = citation_styles.get("bibtex", "N/A") if citation_styles else "N/A"
    external_ids = citing_paper.get("externalIds", {})
    doi = external_ids.get("DOI", "N/A") if external_ids else "N/A"
    link = citing_paper["url"]
    year = citing_paper["year"]
    autori = citing_paper.get("authors", [])
    author_names = [author["name"] for author in autori] if autori else ["N/A"]
    fields_of_study_str = ", ".join(fields_of_study) if fields_of_study else "N/A"

    return {
        "Id": citing_paper_id,
        "Title": titolo,
        "BibTex": bibTex,
        "DOI": doi,
        "Authors": author_names,
        "Year": year,
        "Fields": fields_of_study_str,
        "Link": link,
    }

def write_to_csv(csv_path, fieldnames, data):
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def get_citations_info(paper_id, csv_filename, limit=1000, forward=True):
    if forward:
        snowballing_type = "citations"
        folder_name = "forward"
    else:
        snowballing_type = "references"
        folder_name = "backward"

    create_folder_if_not_exists(folder_name)

    if csv_filename is None:
        csv_filename = f"{paper_id}.csv"

    csv_path = os.path.join(folder_name, csv_filename)

    base_url = "https://api.semanticscholar.org/graph/v1/paper/"
    citations_url = f"{base_url}{paper_id}/{snowballing_type}?fields=paperId,title,authors,journal,url,externalIds,year,fieldsOfStudy,citationStyles&limit={limit}"
    
    response = make_api_request(citations_url, api_key=api_key)

    if response.status_code == 200:
        data = response.json()["data"]
        fieldnames = ["Id", "Title", "BibTex", "DOI", "Authors", "Year", "Fields", "Link"]

        citation_info_list = [extract_citation_info(entry, forward) for entry in data]
        write_to_csv(csv_path, fieldnames, citation_info_list)

    else:
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
        "--batch_path",
        help="This should contain the path to txt file containing paper titles one under the other",
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
    if args.batch_path:
        paper_list = read_and_split_lines(args.batch_path)

        for paper in paper_list:
            time.sleep(2)
            paper_id = search_paper_id(paper)
            try:
                get_citations_info(
                    paper_id=paper_id,
                    csv_filename=f"{paper_id}.csv",
                    limit=1000,
                    forward=args.forward,
                )
            except:
                print(f"paper :{paper} non trovato")
