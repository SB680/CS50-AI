import os
import random
import re
import sys
import copy 

DAMPING = 0.85
SAMPLES = 10000 


def main():
    #with open('corpus0') as f:
    #    sys.argv = f.read()
    #print ("sys.argv: ",sys.argv) 
    #sys.argv = open('corpus0','r')
    sys.argv = ['corpus1', 'corpus2']
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print ("corpus: ",corpus) 
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
    l = corpus 
    pdist = {}
    if not l[page] == set(): 
        for pages in l.keys():
            pdist[pages] = (1-damping_factor)/len(l)
        numoccurlist = {}  
        
        for pages in l[page]:
            #print ("PAGE: ",page) 
            for pagename in corpus.keys():
                if pages == pagename:
                    if pages in numoccurlist:
                        numoccurlist[pages] +=1    
                    else:
                        numoccurlist[pages]=1 
        
        for pages in l[page]:
            pdist[pages]+=damping_factor*numoccurlist[pages]/len(l[page])  
            
    else:
        for pages in l.keys():
            pdist[pages] = 1/len(l)
    return pdist

print("TESTING TRANSITION MODEL: ")
corp= {'ai.html': {'inference.html', 'algorithms.html'}, 'algorithms.html': {'programming.html', 'recursion.html'}, 'c.html': {'programming.html'},
       'inference.html': {'ai.html'}, 'logic.html': {'inference.html'},
       'programming.html': {'c.html', 'python.html'}, 'python.html': {'programming.html', 'ai.html','programming.html'}, 'recursion.html': set()}
transition_model(corp, 'recursion.html', 0.85)

corpus = {'1.html': {'2.html'}, '2.html': {'3.html', '1.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}} 

def sample_pagerank1(corpus, damping_factor): 
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print ("CALL: ") 
    df = damping_factor; c = corpus  

    #expectation: P(2) = 1/4()
    someint = random.randint(0,len(c.keys())-1)
   # print ("Rand website selected: ",someint)
    randpage = list(c.keys())[someint]
    rand = random.uniform(0,1)
    #print ("random number: ",rand) 
    intervals = {} 
    x = 0
    pdist = transition_model(corpus, randpage, damping_factor)
    #print ("pdist: ",pdist)
    
    for page in pdist.keys():
        x+=pdist[page] 
        intervals[page] = x  
    #print("INTERVALS: ",intervals)

    for page in intervals.keys():
        if intervals[page] >= rand: #this probability corresponds to the values in pdist 
            #print ("PAGE: ",page)
            nextpg  = page 
            break
    
    return nextpg 

def sample_pagerank(corpus,damping_factor,samples):
    pages = []; numoccur = {} 

    for sample in range(samples):
        pagevisited =sample_pagerank1(corpus, damping_factor) 
        pages.append(pagevisited)
        if pagevisited in numoccur:
            numoccur[pagevisited]+=1/samples 
        else:
            numoccur[pagevisited]=1/samples 
         
    actual_pagerank(corpus,damping_factor,samples)
    return numoccur

def actual_pagerank3(corpus,damping_factor,samples): #NOT CORRECT; THE CORRECT ONE IS BELOW 
    actualranks = {} #calculated values
    pagelist = {} 
    for page in corpus.keys():
        actualranks[page] = (1-damping_factor)/len(corpus.keys()) 
        pagelist[page]= 0 
    
    for pagekey in corpus.keys():
        #print ("NEXT ITER: ") 
        pagelistcopy = copy.deepcopy(pagelist) 
        for value in corpus[pagekey]:
            #print("value: ",value)
            for page in pagelist: 
                if value == page:
                    pagelistcopy[page]+=1
        #print("page: ",page) 
        #print ("count ",i, ": ", count)
        #print("KEY: ",pagekey) 
        #print("pages: ",pagelistcopy) 

        for key in corpus.keys():
            #for value in corpus[key]:
            #print ("LENGTH: ", len(corpus[pagekey]))
            if not len(corpus[pagekey]) == 0:
                prob = pagelistcopy[key]/len(corpus[pagekey]) #e.g. 'page1':p2,p3,p3,p1,p2 gives 2/5 for p2 and 2/5 for p3 
            else:
                prob = 0 
            actualranks[key]+=prob *(damping_factor/len(corpus.keys()))  
            #print("page: ",page, " probability: ",prob)
            #print("ACTUAL RANKS: ",actualranks) 
            #damping_factor/len(corpus.keys()) *
    print("ACTUAL RANKS: ",actualranks)
    return actualranks 

def actual_pagerank(corpus,damping_factor,samples): #the samples argument is redundant because these ranks were found analytically NOT USING ITERATION 
    ar = {} #calculated values 
    numel = len(corpus.keys()); df = damping_factor; const = df/numel  
    numempty = 0 
    for page in corpus.keys():  
        if corpus[page] == set():
            numempty+=1 
        ar[page] = 0 #avoids keyerror        
    for page in corpus.keys():
        ar[page] += (numempty)/(pow(numel,2))
        ar[page] +=((numel-numempty)/numel)*(1-df)/numel 
        
    for page in corpus.keys():
        nump = len(corpus[page])
        #print ("Nump: ",nump)
        if not nump == 0: 
            for p in corpus[page]: 
                ar[p]+=const/nump 
    c = 0 
    for key in ar.keys():
        c+=ar[key] 
    return ar
 
def findaccuracy(samplerank,actualrank):
    maxd = 0 
    #it takes very long to obtain accuracy better than 0.01  
    for page in samplerank: 
        maxd = max(abs(samplerank[page]-actualrank[page]),maxd)   
    #print("SAMPLERANK: ",samplerank)  
    return maxd

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = 2000 
    
    actualrank = actual_pagerank(corpus,damping_factor,samples)
    print("ACTUAL RANKS: ",actualrank) 
    maxd = 0 
    while samples < 3900:
        samplerank = sample_pagerank(corpus,damping_factor,samples)
        print("SAMPLES: ",samples)
        print (findaccuracy(samplerank,actualrank))
        samples+=300  
    
    return samplerank 
    
if __name__ == "__main__":
    main()


