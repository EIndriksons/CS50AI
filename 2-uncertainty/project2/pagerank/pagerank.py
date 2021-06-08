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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    dist = {}

    # Determine link count
    link_count = len(corpus[page])
    
    if link_count > 0:
        # Calculate dist probability for all pages
        for key in corpus:
            dist[key] = (1 - damping_factor) / len(corpus)

        # Calculate (and add) dist probability for linked pages
        for key in corpus[page]:
            dist[key] += damping_factor / link_count
    else:
        # Calculate dist probability for all pages (without damping factor)
        for key in corpus:
            dist[key] = 1 / len(corpus)

    return dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initiate ranking dict
    ranking = {}
    for page in corpus:
        ranking[page] = 0

    # Select the first sample with equal random choice
    sample = random.choice(list(corpus.keys()))

    # Loop through all of the samples
    for i in range(1, n):

        # Calculate the new distribution based on the sample page
        dist = transition_model(corpus, sample, damping_factor)

        # Adjust the existing ranking based on the current distribution
        for page in ranking:
            ranking[page] = ((i - 1) * ranking[page] + dist[page]) / i

        # Choose new sample but this time use the existing distributions
        sample = random.choices(list(ranking.keys()), list(ranking.values()), k=1)[0]

    return ranking


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    threshold = 0.001
    page_count = len(corpus)
    
    # Initiate ranking dict
    ranking = {}
    for page in corpus:
        ranking[page] = 1 / page_count

    # While loop should run up until the change in page rank 
    # is not higher than the threshold value for all pages
    repeat = True
    while repeat:

        i = 0
        for page in corpus:

            # Calculate the new probability for a page and initiate delta change
            prob_new = (1 - damping_factor) / page_count
            prob_delta = 0

            # Surf other pages and determine if the page contains links to current page
            for key in corpus:
                if page in corpus[key]:

                    # If the page contains link to the current page adjust prob_delta
                    link_count = len(corpus[key])
                    prob_delta = prob_delta + ranking[key] / link_count

            # Adjust prob_delta by damping factor then assign the delta value to the
            # existing probability measure
            prob_delta = damping_factor * prob_delta
            prob_new += prob_delta

            # Calculate if the change is larger than the set threshold value
            # If so add to the counter to move one step closer to ending the loop
            if abs(ranking[page] - prob_new) < threshold:
                i += 1

            # Assign new probability distribution
            ranking[page] = prob_new

        # If we have met the threshold value page_count of times end the loop
        if i == page_count:
            repeat = False

    return ranking


if __name__ == "__main__":
    main()
