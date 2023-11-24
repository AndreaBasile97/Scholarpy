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

## Contributing 🤝

Feel free to contribute to Scholarpy by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
