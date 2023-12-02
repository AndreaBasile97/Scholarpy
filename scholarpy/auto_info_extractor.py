import argparse
from scholarpy.utils import (
    paper_details_batch_wrapper,
    search_paper_id,
    get_paper_details_batch,
    extract_paper_details_batch,
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve informations for a paper.")
    parser.add_argument(
        "--batch_path",
        help="This should contain the path to txt file containing paper titles one under the other",
    )
    parser.add_argument(
        "--paper_title",
        help="This should contain the path to txt file containing paper titles one under the other",
    )
    parser.add_argument(
        "--fields", nargs="+", help="fields to retrive from the papers inside the path"
    )

    args = parser.parse_args()

    if not args.fields:
        args.fields = [
            "title",
            "citationStyles",
            "authors",
            "year",
            "journal",
            "externalIds",
        ]
    if args.batch_path:
        paper_details_batch_wrapper(args.batch_path, fields=args.fields)
    elif args.paper_title:
        id = search_paper_id(args.paper_title)
        paper_details = get_paper_details_batch(paper_ids=[id, id], fields=args.fields)
        extract_paper_details_batch(paper_details)
