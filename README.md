# Scholarpy 📚

Author: Andrea Basile

A wrapper for Semantic Scholar APIs, Scholarpy simplifies scholarly research by providing easy access to paper information.

## Guide 📖

### Snowballing ❄️

Snowballing is a technique that involves obtaining all references (backward) or citations (forward) from a specific paper. This process is then repeated for each new reference/citation found. However, these scripts perform a one-step snowballing starting from the seed papers.

Thanks to Scholarpy, you can easily perform snowballing and obtain a CSV file containing essential information about the references, including:

- Paper id
- Title
- BibTeX
- DOI
- Link
- Year
- Authors

## Quick Start 🚀

1. **Using GUI:**

    ```bash
    python -m scholarpy.gui
    ```

2. **Using command-line arguments for single paper snowballing:**

    ```bash
    python -m scholarpy.snowballer --paper_title '' --paper_id '' --limit 1000 --csv_filename papers.csv --forward True
    ```

3. **Using command-line arguments for multiple papers snowballing:**

    ```bash
    python -m scholarpy.snowballer --batch_path results.txt --forward True
    ```

### Auto PDF Downloader 🗃️

1. **Using command-line arguments for multiple paper pdfs downloading:**
You should put the path to the .txt file containing paper_ids. Example:

2437df4f5iny387d57d2377 <br>
s32ny32s4ns4324324231ff <br>
3xdrnnixrnyiwxonxw0732m <br>
...

    python -m scholarpy.auto_pdf_downloader --bulk_path paper_ids.txt 


The pdf ids can be fetch using the snowballer.

## Contributing 🤝

Feel free to contribute to Scholarpy by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
