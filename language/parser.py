import nltk
import sys
import string 

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
D -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"

"""

NONTERMINALS = """ 
S -> NP VP | NP

AP -> A | A AP
NP -> N | D NP | AP NP | N PP 
PP -> P NP
VP -> V | V NP | V NP PP | V PP 
"""  

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main(filename):

    #If filename specified, read sentence from file
    #otherwise, read the sentence as the filename 
    if len(filename) < 6: #all the filenames in sentences have a smaller length 
        with open(f"sentences/{filename}") as f:  
            s = f.read().strip('#,!@$%^&*()~`.?,<>{}[]":;')

        s = s.translate(str.maketrans('', '', string.punctuation))
    else:
        s = filename
        
    print ("s: ", s.strip('.')) 
    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence 
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

 
            
def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """ 
    sentence = (nltk.word_tokenize(sentence.lower()))   #a weakness: this won't strip a single apostrophe(try it to see why) 
    return sentence 

def hasnounphrase(subtree):
    for subt in subtree.subtrees():
        if subt == subtree:
            continue
        elif subt.label() == 'NP':
            return True
    return False

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = [] 
    
    for subtree in parented_tree.subtrees(lambda t: t.label() == 'N'):
        if not hasnounphrase(subtree):
            np_chunks.append(subtree)
    return np_chunks
 
if  __name__ == "__main__":
    main('the armchair in the home smiled') 
