import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability damping_factor, choose a link at random
    linked to by page. With probability 1 - damping_factor, choose
    a link at random chosen from all pages in the corpus.
    """
    # corpus is your dictionary from crawl with keys of pages and links
    pages = set(corpus.keys())
    linked = corpus[page]

    # Notes: "if a page has no links, we can pretend it has links to all pages in the corpus"
    if not linked:
        linked = pages

    # pages and links will equal the length of the entries within corpus
    n_pages = len(pages)
    n_links = len(linked)
    PR = {}  # start with empty PR (Probabilistic)

    # use PR = 1-d / N where d is defined above 0.85 and N = number of pages
    for i in pages:
        pr = (1 - damping_factor) / n_pages  # dampening to each page
        if i in linked:
            pr += damping_factor / n_links  # dampening to each link in page
        PR[i] = pr

    return PR


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # just as in above - make a list from corpus at random
    page = random.choice(list(corpus.keys()))
    count = {p: 0 for p in corpus}

    # Count the page visits
    for _ in range(n):
        count[page] += 1

        # Probability for next pages
        pr = transition_model(corpus, page, damping_factor)

        # Randomly choose next page based on probabilities
        pages = list(pr.keys())
        weights = list(pr.values())
        page = random.choices(pages, weights=weights, k=1)[0]

    # Converts counts to PageRank values
    rank = {p: count[p] / n for p in count}

    return rank


def iterate_pagerank(corpus, damping_factor, threshold=0.001):
    """
    Compute PageRank values for each page by repeatedly updating
    until values converge (less than threshold change).
    """
    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}

    # Loop until ranks converge
    while True:
        new_ranks = {}
        for page in corpus:
            total = 0
            for possible_page in corpus:
                links = corpus[possible_page]
                if not links:
                    total += pagerank[possible_page] / N
                elif page in links:
                    total += pagerank[possible_page] / len(links)

            # PageRank 
            new_ranks[page] = (1 - damping_factor) / N + damping_factor * total

        # Convergence
        converged = all(
            abs(new_ranks[page] - pagerank[page]) < threshold
            for page in corpus
        )
        pagerank = new_ranks

        if converged:
            break

    return pagerank


if __name__ == "__main__":
    main()
