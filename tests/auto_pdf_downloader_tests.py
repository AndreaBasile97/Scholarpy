import unittest
from unittest.mock import patch, MagicMock
from scholarpy.auto_pdf_downloader import (
    get_paper_details_batch,
    download_pdfs,
)
from scholarpy.utils import clean_filename


class AutoPdfDownloader(unittest.TestCase):
    @patch("requests.post")
    def test_get_paper_details_success(self, mock_post):
        # Definisci il comportamento simulato del mock
        expected_response = {
            "status_code": 200,
            "json": lambda: [{"paper_id": 1, "title": "Paper 1"}],
        }
        mock_post.return_value = MagicMock(**expected_response)

        # Chiamata alla funzione da testare
        result = get_paper_details_batch([1, 2, 3])

        # Verifica dell'output atteso
        self.assertEqual(result, [{"paper_id": 1, "title": "Paper 1"}])

    @patch("requests.post")
    def test_get_paper_details_failure(self, mock_post):
        # Definisci il comportamento simulato del mock per un errore nella risposta
        expected_response = {"status_code": 500}
        mock_post.return_value = MagicMock(**expected_response)

        # Chiamata alla funzione da testare
        result = get_paper_details_batch([1, 2, 3])

        # Verifica che la funzione restituisca None in caso di errore
        self.assertIsNone(result)

    @patch("requests.get")
    def test_download_pdfs_success(self, mock_get):
        # Simula una risposta HTTP di successo
        mock_response = MagicMock(status_code=200, content=b"Fake PDF content")
        mock_get.return_value = mock_response

        # Chiamata alla funzione da testare
        pdf_urls = ["http://example.com/pdf1", "http://example.com/pdf2"]
        pdf_titles = ["Paper 1", "Paper 2"]
        download_path = "test_downloads"
        download_pdfs(pdf_urls, pdf_titles, download_path)

        # Verifica che la funzione abbia chiamato requests.get con i parametri corretti
        expected_calls = [
            unittest.mock.call(pdf_urls[0], timeout=2),
            unittest.mock.call(pdf_urls[1], timeout=2),
        ]
        mock_get.assert_has_calls(expected_calls, any_order=True)

        # Verifica che il file sia stato scritto correttamente
        expected_file_path = f"{download_path}/{clean_filename(pdf_titles[0])}.pdf"
        with open(expected_file_path, "rb") as pdf_file:
            content = pdf_file.read()
        self.assertEqual(content, b"Fake PDF content")

    @patch("requests.get")
    def test_download_pdfs_retry_on_5xx_error(self, mock_get):
        # Simula una risposta HTTP con codice di stato 503 (5xx error)
        mock_response = MagicMock(status_code=503)
        mock_get.return_value = mock_response

        # Chiamata alla funzione da testare
        pdf_urls = ["http://example.com/pdf1.pdf"]
        pdf_titles = ["Paper 1"]
        download_path = "test_downloads"
        download_pdfs(pdf_urls, pdf_titles, download_path, max_retries=3)

        # Verifica che la funzione abbia ritentato il download per 3 volte
        self.assertEqual(mock_get.call_count, 3)


if __name__ == "__main__":
    unittest.main()
