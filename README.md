# Scholarpy 📚

Author: Andrea Basile

A wrapper for Semantic Scholar APIs, Scholarpy simplifies scholarly research by providing easy access to paper information.

## Guide 📖

### 1. Snowballing ❄️

Snowballing is a technique that involves obtaining all references (backward) or citations (forward) from a specific paper. This process is then repeated for each new reference/citation found. However, these scripts perform a one-step snowballing starting from the seed papers.

Thanks to Scholarpy, you can easily perform snowballing and obtain a CSV file containing essential information about the references, including:

- Paper id
- Title
- BibTeX
- DOI
- Link
- Year
- Authors

**Using command-line arguments for single paper snowballing:**


    python -m scholarpy.snowballer --paper_title '' --paper_id '' --limit 1000 --csv_filename papers.csv --forward True


**Using command-line arguments for multiple papers snowballing:**

    python -m scholarpy.snowballer --batch_path results.txt --forward True


### 2. Auto PDF downloader 📰

Stop downloading manually pdf files! You can write a .txt file filled with paper ids and then using:

    python -m scholarpy.auto_pdf_downloader --batch_path 'path/to/paper_ids.txt'

To automatically download paper pdfs!

### 3. Auto Infos extractor ℹ️

You can extract these infos:

- Paper id
- Title
- BibTeX
- DOI
- Link
- Year
- Authors

Using:


    python -m scholarpy.auto_info_extractor --batch_path 'path/to/paper_titles.txt'

Or:


    python -m scholarpy.auto_info_extractor --paper_title 'Lorem ipsum...'

Note: this feature work with 'Paper titles' and not with 'Paper ids'

## Warning! ⚠️

Scholarpy automatically logs papers not found in order to keep track of the whole operations. Scholarpy may not find papers for two reason:

1. The paper doesn't exists in Semantic Scholar knowledge base.
2. The paper title is not correctly written or contains less/more words than the real title.
3. To unlock the full potential of scholarpy you should get the API from (https://www.semanticscholar.org/) and inserting it in the .env


## Quick Start 🚀

**Using GUI:**

    python -m scholarpy.gui

**Note: the gui may be not updated with all Scholarpy features**

The pdf ids can be fetch using the snowballer.

## Contributing 🤝

Feel free to contribute to Scholarpy by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated!

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
