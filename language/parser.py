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
#to VP I added V PP such as 'sat in the home'; else 'holmes sat in the home' cannot be parsed 

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main(filename):

    # If filename specified, read sentence from file
    #with open(f"sentences", encoding="utf-8") as f:
    if len(filename) < 6: 
        with open(f"sentences/{filename}") as f: #you CAN'T OPEN A DIRECTORY BUT MUST SPECIFY A FILE WITHIN IT 
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


def hasnp(phrase):
    trees = list(parser.parse(phrase))
    for tree in trees: 
        tree.pretty_print()
        tree = nltk.tree.ParentedTree.convert(tree)
        parented_tree = nltk.tree.ParentedTree.convert(tree)  
        for subtree in parented_tree.subtrees(lambda t: t.label() == 'NP'):
            for tree in subtree.subtrees(lambda t: t.label() == 'NP'):
                if not tree == subtree: 
                    return False
    return True

def hasnp2(trees): 
    for tree in trees: 
        #tree.pretty_print()
        tree = nltk.tree.ParentedTree.convert(tree)
        parented_tree = nltk.tree.ParentedTree.convert(tree)  
        for subtree in parented_tree.subtrees(lambda t: t.label() == 'NP'):
            for tree in subtree.subtrees(lambda t: t.label() == 'NP'):
                if not tree == subtree: 
                    return False
    return True 
            
def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #print("SENTENCE: ",sentence, type(sentence)); sentence = sentence.strip('#,!@$%^&*()~`.?,<>{}[]":;')
    #print("SENTENCE: ",sentence, type(sentence))
    sentence = (nltk.word_tokenize(sentence.lower()))   #a weakness: this won't strip a single apostrophe(try it to see why) 
    #print("SENTENCE: ",sentence) 
    return sentence 

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    parented_tree = nltk.tree.ParentedTree.convert(tree)
    
    for subtree in parented_tree.subtrees(lambda t: t.label() == 'N'):
        np_chunks.append(subtree)

    return np_chunks

#print (hasnp(['armchair'])) 
if  __name__ == "__main__":
    main('the armchair in the home smiled') #must write 1.txt and NOT 1 

#in the home 
