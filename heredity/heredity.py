import csv
import itertools
import sys
import copy 
PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    sys.argv = ['family0']
    #if len(sys.argv) != 2: --useless line of code 
    #    sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[0])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
     
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene 
        
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
 
                p = joint_probability(people, one_gene, two_genes, have_trait)  
                update(probabilities, one_gene, two_genes, have_trait, p)  
                
    normalize(probabilities) 
    for person in people:
        #print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")

def load_data(filename):
    """
    Load data from CSV files into memory.
    """
    data = dict()
    #HOW TO USE: {} INDICATE A VARIABLE -- IE YOU CAN'T WRITE {data}; you could write family0 but not {family0}; or {filename} not filename  
    with open(f"data/{filename}.csv") as f:
        reader = csv.DictReader(f) 
        for row in reader:
            name = row["name"]
            print("NAME: ",name)
            print("COLUMN NAME: " ,column["name"]) 
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    print ("DATA: ",data) 
    return data
        
        
def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people, one_gene, two_genes, have_trait): 
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
 
    prob = 1   
    prob0 = PROBS["gene"][0]; prob1 = PROBS["gene"][1]; prob2 = PROBS["gene"][2]; #prob0: p(has 0 gene) 

    probtraitgiven0 = PROBS['trait'][0][True]; probtraitgiven1 = PROBS['trait'][1][True]; probtraitgiven2 = PROBS['trait'][2][True];
    pxgene = [prob0,prob1,prob2]
    ptraitgivenxgene = [probtraitgiven0,probtraitgiven1,probtraitgiven2]
    
    pgetsifparenthas1 = 0.5; pgetsifparenthas0 = 0.01; pgetsifparenthas2 = 0.99;  #pgetsif1 = 0.5*(0.01 + 0.99) 
    pgetsifparenthasx = [pgetsifparenthas0,pgetsifparenthas1,pgetsifparenthas2]
    
    for person in people:   
        trait = person in have_trait 
        if trait == None:
            trait = False 
        if not people[person]['mother'] == None: 
            motherhastrait = people[people[person]['mother']]['trait'] #means she has 0 bad genes
            fatherhastrait = people[people[person]['father']]['trait'] #2 bad genes
            mother = people[person]['mother']; father = people[person]['father'];

            numdeffathergene =2*(father in two_genes) + int(father in one_gene); numdefmothergene =2*(mother in two_genes) + int(mother in one_gene);
            
            pgetsfromfather = pgetsifparenthasx[numdeffathergene];  
            pgetsfrommother = pgetsifparenthasx[numdefmothergene]; 
            
            pperson1 = pgetsfrommother*(1-pgetsfromfather) + pgetsfromfather*(1-pgetsfrommother) #p(person has 1 of the bad gene) 
            pperson0 =(1-pgetsfromfather)*(1-pgetsfrommother) 
            pperson2 = pgetsfrommother*pgetsfromfather
            
            if person in one_gene: 
                prob*= pperson1*(1-probtraitgiven1)*(not trait) + pperson1*(probtraitgiven1)*trait 
            elif person in two_genes: 
                prob*= pperson2*(1-probtraitgiven2)*(not trait) + pperson2*(probtraitgiven2)*trait
            else: 
                prob*= pperson0*(1-probtraitgiven0)*(not trait) + pperson0*(probtraitgiven0)*trait 
        else:
            numgens = 2*(person in two_genes) + int(person in one_gene); 
            if not trait: #then find p(not have trait given numgens)
                prob*=pxgene[numgens]*(1-ptraitgivenxgene[numgens]) #probtraitgiven0: probability they have the trait (are in have_trait) with 0 genes -- that of a mutation
            elif trait:  
                prob*=pxgene[numgens]*(ptraitgivenxgene[numgens]) 
    return prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        num = 2 *(person in two_genes) + (person in one_gene); 
        probabilities[person]["gene"][num]+=p
        trait = person in have_trait 
        probabilities[person]['trait'][trait]+=p 

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """ 
    print( "TESTING NORMALIZE USING THIS DICT: ",probabilities) 

    for person in probabilities.keys():
        s = 0; y = 0 
        for numgen in probabilities[person]['gene']:
            s+=probabilities[person]['gene'][numgen]
        for numgen in probabilities[person]['gene']:
            probabilities[person]['gene'][numgen]*=1/s
        for val in probabilities[person]['trait']:
            y+=probabilities[person]['trait'][val]
        for val in probabilities[person]['trait']:
            probabilities[person]['trait'][val]*=1/y 
          

if __name__ == "__main__":
    main()
