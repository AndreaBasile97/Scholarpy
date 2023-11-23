import requests
import json
import os
from utils import clean_filename, read_and_split_lines
import argparse


def get_paper_details(paper_ids):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/batch"
    fields = "referenceCount,citationCount,title,openAccessPdf"
    
    payload = {
        "ids": paper_ids
    }

    response = requests.post(
        base_url,
        params={'fields': fields},
        json=payload
    )

    if response.status_code == 200:
        paper_details = response.json()

        # Restituisci i dettagli, inclusi gli URL degli articoli in formato PDF
        return paper_details
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return None


def get_pdf_urls(paper_details):
    pdf_urls = []
    pdf_titles = []

    for paper in paper_details:
        if 'openAccessPdf' in paper and paper['openAccessPdf'] is not None:
            pdf_url = paper['openAccessPdf']['url']
            pdf_urls.append(pdf_url)

            pdf_title = paper['title']
            pdf_titles.append(pdf_title)
        else:
            # Se il PDF non è disponibile, aggiungi il titolo al file "pdf_not_found_titles.txt"
            with open("pdf_not_found_titles.txt", "a") as file:
                file.write(paper['title'] + '\n')
    return pdf_urls, pdf_titles


def download_pdfs(pdf_urls, pdf_titles, download_path='pdf_downloads'):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for i, url in enumerate(pdf_urls):
        response = requests.get(url)
        if response.status_code == 200:
            # Download the PDF
            try:
                response_pdf = requests.get(url)
            except:
                print(f'Download failed for {url}')

            if response_pdf.status_code == 200:
                # Use the title in the file name
                download_path = os.path.join(download_path, f'{clean_filename(pdf_titles[i])}.pdf')
                with open(download_path, 'wb') as pdf_file:
                    pdf_file.write(response_pdf.content)

            # Scrivi il contenuto del PDF nel file
            with open(download_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            
            print(f"File {download_path} scaricato con successo.")
        else:
            print(f"Errore nel download del file dal seguente URL: {url}")


def main():

    parser = argparse.ArgumentParser(description='Download PDFs for given paper IDs.')
    parser.add_argument('--bulk_path', type=str, help='File containing a list of paper IDs')
    args = parser.parse_args()

    if args.bulk_path:
        paper_id_list = read_and_split_lines(args.bulk_path)
        papers_details = get_paper_details(paper_id_list)
        pdf_urls, pdf_titles = get_pdf_urls(papers_details)
        download_pdfs(pdf_urls,pdf_titles)

if __name__ == '__main__':
    main()