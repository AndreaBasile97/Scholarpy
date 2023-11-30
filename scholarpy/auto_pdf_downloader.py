import requests
import json
import os
from scholarpy.utils import (
    clean_filename,
    read_and_split_lines,
    get_paper_details_batch,
)
import argparse
import time


def get_pdf_urls(paper_details):
    pdf_urls = []
    pdf_titles = []
    for paper in paper_details:
        if "openAccessPdf" in paper and paper["openAccessPdf"] is not None:
            pdf_url = paper["openAccessPdf"]["url"]
            pdf_urls.append(pdf_url)

            pdf_title = paper["title"]
            pdf_titles.append(pdf_title)

        else:
            # Se il PDF non è disponibile, aggiungi il titolo al file "pdf_not_found_titles.txt"
            with open("pdf_not_found_titles.txt", "a", encoding="utf-8") as file:
                file.write(paper["title"] + "\n")
    return pdf_urls, pdf_titles


def download_pdfs(pdf_urls, pdf_titles, download_path="pdf_downloads", max_retries=3):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    error_log_path = os.path.join(download_path, "pdf_not_downloaded.txt")

    for i, url in enumerate(pdf_urls):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    try:
                        # Use the title in the file name
                        file_path = os.path.join(
                            download_path, f"{clean_filename(pdf_titles[i])}.pdf"
                        )
                        with open(file_path, "wb") as pdf_file:
                            pdf_file.write(response.content)
                        break  # Break out of the retry loop if successful
                    except Exception as e:
                        print(f"Error saving file: {e}")
                elif 500 <= response.status_code < 600:
                    # Retry for 5xx errors
                    retries += 1
                    print(
                        f"Retrying ({retries}/{max_retries}) after 5xx error for URL: {url}"
                    )
                    time.sleep(2)  # Add a short delay before retrying
                else:
                    # Write the error to the log file
                    with open(error_log_path, "a") as error_log:
                        error_log.write(
                            f"Error downloading file from URL: {url}, Status Code: {response.status_code}\n"
                        )
                    break  # Break out of the retry loop for non-5xx errors
            except Exception as e:
                # Write the error to the log file
                with open(error_log_path, "a") as error_log:
                    error_log.write(
                        f"Error downloading file from URL: {url}, Exception: {e}\n"
                    )
                break  # Break out of the retry loop for other exceptions

    print("Download process completed.")


def main():
    parser = argparse.ArgumentParser(description="Download PDFs for given paper IDs.")
    parser.add_argument(
        "--bulk_path", type=str, help="File containing a list of paper IDs"
    )
    args = parser.parse_args()
    if args.bulk_path:
        paper_id_list = read_and_split_lines(args.bulk_path)
        papers_details = get_paper_details_batch(paper_id_list)
        pdf_urls, pdf_titles = get_pdf_urls(papers_details)
        download_pdfs(pdf_urls, pdf_titles)


if __name__ == "__main__":
    main()
