# PageRank Implementation

This project implements the PageRank algorithm in Python for provided dataset (containing links to webpages). The goal is to compute PageRank scores for web pages based on their link structure.

## Running application:
Run src/pagerank.py file

## Files:

### links.srt.gz

- **Description:** Compressed file containing a large corpus of web page links.
- **Format:** Each line represents a link from a source page to a target page, separated by a tab character.
- **Usage:** Input dataset to compute PageRank scores.

### inlinks.txt

- **Description:** Output file where the program writes the list of pages with their number of in-links.
- **Format:** Each line follows the format `PageName<TAB>Rank<TAB>inlink_Count`.
- **Sorting:** Sorted in descending order of in-link count, with ties sorted alphabetically by page name.
- **Purpose:** Provides insights into the popularity and connectivity of each page within the web graph.

### pagerank.txt

- **Description:** Output file where the program writes the list of pages with their calculated PageRank scores.
- **Format:** Each line follows the format `PageName<TAB>Rank<TAB>PageRank score`.
- **Sorting:** Sorted in descending order of PageRank score, with ties sorted alphabetically by page name.
- **Purpose:** Represents the importance of each page based on the PageRank algorithm, considering both direct links and random jumps.
