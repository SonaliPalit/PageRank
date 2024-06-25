import gzip
import sys
from collections import defaultdict


def read_links_file(input_file):

    links = []
    with gzip.open(input_file, 'rt') as file:
        for line in file:
            source, target = line.strip().split('\t')
            links.append((source, target))
    return links


def compute_inlinks(links):

    inlinks_count = defaultdict(int)
    for _, target in links:
        inlinks_count[target] += 1
    for source, _ in links:
        if source not in inlinks_count:
            inlinks_count[source] = 0
    return inlinks_count

def page_inlinks(links):
    inlinks = defaultdict(set)
    for source, target in links:
        inlinks[target].add(source)
    for source, _ in links:
        if source not in inlinks:
            inlinks[source] = set()
    return inlinks

def page_outlinks(links):
    out_links = defaultdict(set)
    for source, target in links:
        out_links[source].add(target)
    for _, target in links:
        if target not in out_links:
            out_links[target] = set()
    return out_links


def compute_pagerank(links, pages, out_links, in_links, lamb, tau, N=-1):

    # pages = set([page for link in links for page in link])
    num_pages = len(pages)
    # page_to_index = {page: i for i, page in enumerate(pages)}
    I = {page: 1 / num_pages for page in pages}
    R = {}

    # out_links = page_outlinks(links)
    # in_links = page_inlinks(links)

    if N == -1: #convergence case
        while True:
            R = {page: lamb / num_pages for page in pages}
            sink_pages_weight = 0
            for page in pages:
                Q = in_links[page]
                for q in Q:
                    R[page] += (1 - lamb) * I[q] / len(out_links[q])
                if (len(out_links[page]) == 0):
                    sink_pages_weight += (1 - lamb) * I[page] / num_pages
            
            for q in pages:
                R[q] += sink_pages_weight
            
            
            if sum((R[page] - I[page]) ** 2 for page in pages) ** 0.5 < tau:
                break
            I = R 

    else:
        for _ in range(N):
            R = {page: lamb / num_pages for page in pages}
            sink_pages_weight = 0
            for page in pages:
                Q = in_links[page]
                for q in Q:
                    R[page] += (1 - lamb) * I[q] / len(out_links[q])
                if (len(out_links[page]) == 0):
                    sink_pages_weight += (1 - lamb) * I[page] / num_pages

           
            for q in pages:
                R[q] += sink_pages_weight
                
            I = R 

    return R



def write_inlinks_file(inlinks_count, inlinks_file, k, page_to_index_dict, index_to_page_dict):
    reverted_inlinks = {}
    for key in inlinks_count:
        value = inlinks_count[key]
        reverted_inlinks[index_to_page_dict[key]] = value

    sorted_inlinks = sorted(reverted_inlinks.items(), key=lambda x: (-x[1], x[0]))
    with open(inlinks_file, 'w') as file:
        for i, (page, count) in enumerate(sorted_inlinks[:k], start=1):
            file.write(f"{page}\t{i}\t{count}\n")


def write_pagerank_file(pagerank, pagerank_file, k, page_to_index_dict, index_to_page_dict):
    reverted_pagerank = {}
    for key in pagerank:
        value = pagerank[key]
        reverted_pagerank[index_to_page_dict[key]] = value

    sorted_pagerank = sorted(reverted_pagerank.items(), key=lambda x: (-x[1], x[0]))
    with open(pagerank_file, 'w') as file:
        for i, (page, score) in enumerate(sorted_pagerank[:k], start=1):
            file.write(f"{page}\t{i}\t{score:.12f}\n")

def do_pagerank_to_convergence(input_file: str, lamb: float, tau: float,
                               inlinks_file: str, pagerank_file: str, k: int):
    
    
    links = []
    inlinks_count = defaultdict(int)
    inlinks = defaultdict(set)
    out_links = defaultdict(set)
     # pages = sorted(set([page for link in links for page in link]))
    pages = set()
    page_to_index_dict = {}
    index_to_page_dict = {}
    cur_index = 0
    with gzip.open(input_file, 'rt') as file:
        for line in file:
            source, target = line.strip().split('\t')
            if (source in page_to_index_dict): 
                s = page_to_index_dict[source]
            else:
                s = cur_index
                cur_index += 1
                page_to_index_dict[source] = s
                index_to_page_dict[s] = source

            if (target in page_to_index_dict):
                t = page_to_index_dict[target]
            else:
                t = cur_index
                cur_index += 1
                page_to_index_dict[target] = t
                index_to_page_dict[t] = target
            links.append((s, t))


            inlinks_count[t] += 1
            inlinks[t].add(s)
            out_links[s].add(t)

            pages.add(s)
            pages.add(t)
    
    for source, target in links:
        if source not in inlinks:
            inlinks[source] = set()
        if source not in inlinks_count:
            inlinks_count[source] = 0
        if target not in out_links:
            out_links[target] = set()
    
    pages = sorted(list(pages))
    pagerank = compute_pagerank(links, pages, out_links, inlinks, lamb, tau)
    write_inlinks_file(inlinks_count, inlinks_file, k, page_to_index_dict, index_to_page_dict)
    write_pagerank_file(pagerank, pagerank_file, k, page_to_index_dict, index_to_page_dict)


def do_pagerank_n_times(input_file: str, N: int, inlinks_file: str,
                        pagerank_file: str, k: int):
    
    links = []
    inlinks_count = defaultdict(int)
    inlinks = defaultdict(set)
    out_links = defaultdict(set)

    pages = set()

    page_to_index_dict = {}
    index_to_page_dict = {}
    cur_index = 0
    with gzip.open(input_file, 'rt') as file:
        for line in file:
            source, target = line.strip().split('\t')
            if (source in page_to_index_dict): 
                s = page_to_index_dict[source]
            else:
                s = cur_index
                cur_index += 1
                page_to_index_dict[source] = s
                index_to_page_dict[s] = source

            if (target in page_to_index_dict):
                t = page_to_index_dict[target]
            else:
                t = cur_index
                cur_index += 1
                page_to_index_dict[target] = t
                index_to_page_dict[t] = target
            links.append((s, t))


            inlinks_count[t] += 1
            inlinks[t].add(s)
            out_links[s].add(t)

            pages.add(s)
            pages.add(t)
    
    for source, target in links:
        if source not in inlinks:
            inlinks[source] = set()
        if source not in inlinks_count:
            inlinks_count[source] = 0
        if target not in out_links:
            out_links[target] = set()
    
    pages = sorted(list(pages))
    
    pagerank = compute_pagerank(links, pages, out_links, inlinks, lamb=0.20, tau=0.005, N=N)
    write_inlinks_file(inlinks_count, inlinks_file, k, page_to_index_dict, index_to_page_dict)
    write_pagerank_file(pagerank, pagerank_file, k, page_to_index_dict, index_to_page_dict)


def main():
    argc = len(sys.argv)
    input_file = sys.argv[1] if argc > 1 else 'links.srt.gz'
    lamb = float(sys.argv[2]) if argc > 2 else 0.2
    
    tau = 0.005
    N = -1  # signals to run until convergence
    if argc > 3:
        arg = sys.argv[3]
        if arg.lower().startswith('exactly'):
            N = int(arg.split(' ')[1])
        else:
            tau = float(arg)
    
    inlinks_file = sys.argv[4] if argc > 4 else 'inlinks.txt'
    pagerank_file = sys.argv[5] if argc > 5 else 'pagerank.txt'
    k = int(sys.argv[6]) if argc > 6 else 100
    
    if N == -1:
        do_pagerank_to_convergence(input_file, lamb, tau, inlinks_file, pagerank_file, k)
    else:
        do_pagerank_n_times(input_file, N, inlinks_file, pagerank_file, k)
    

if __name__ == '__main__':
    main()
