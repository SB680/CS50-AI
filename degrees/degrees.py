import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names= {}

# Maps ids to a set of corresponding names 
names2 = {} 

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    count = 0; 
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names: 
                names[row["name"].lower()] = {row["id"]} 
            else: 
                names[row["name"].lower()] = {row["id"]}

            if row["name"].lower() not in names2: 
                names2[row["id"].lower()] = {row["name"]} 
            else: 
                names2[row["id"].lower()] = {row["name"]}
    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            #count+=1; 
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
            #if count<20:
            #    print (people[row["person_id"]])
            #    print (people[row["person_id"]]["movies"])



def main():
    print ("ARGV: ", sys.argv)
    sys.argv = ['large','small']
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large" 
    # Load data from files into memory
    #directory = "small" 
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

##    source = person_id_for_name(input("Name: "))
##    if source is None:
##        sys.exit("Person not found.")
##    target = person_id_for_name(input("Name: "))
##    if target is None:
##        sys.exit("Person not found.")
##
##    path = shortest_path(source, target)
##    print ("path: ",path) 
##    if path is None:
##        print("Not connected.")
##    else:
##        degrees = len(path)
##        print(f"{degrees} degrees of separation.")
##        path = [(None, source)] + path
##        for i in range(degrees):
##            person1 = people[path[i][1]]["name"]
##            person2 = people[path[i + 1][1]]["name"]
##            movie = movies[path[i + 1][0]]["title"]
##            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def shortest_path2(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """ 
    
    #raise NotImplementedError
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier() #you could replace with StackFrontier but not guaranteed the shortest path then 
    frontier.add(start)  
    num_explored = 0
 
    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:
        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")
        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # If node is the goal, then we have a solution
        if node.state == target:
            actions = []
            cells = []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            solution = (actions, cells)
            return solution 

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            if state not in explored: #not frontier.contains_state(state) and 
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)  

def shortest_path(source, target):
    num_explored = 0

    # Initialize frontier to just the starting person (source)
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialise an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no solution
        if frontier.empty():
            return None
        
        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # Mark node as explored
        explored.add(node.state)

        # Add neighbours to frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                
                # Check if child node is goal node
                if child.state == target:
                    movies_path = []
                    people_path = []
                    while child.parent is not None:
                        movies_path.append(child.action)
                        people_path.append(child.state)
                        child= child.parent
                    movies_path.reverse()
                    people_path.reverse()
                    return list(zip(movies_path, people_path))

                # Else add child node to frontier
                frontier.add(child)

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    #print ("persons: ",person_ids) 
    #for person_id in person_ids
    #print(person_ids) 
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            #print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """ 
    movie_ids = people[person_id]["movies"]
    #print("MOVIES: ",movie_ids) 
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

if __name__ == "__main__":
    main()
source = list(names['tom hanks'])[0]; target = list(names['dustin hoffman'])[0];
print ("source: ",list(names2[source])[0]," target: ",list(names2[target])[0]) 
path = shortest_path2(source,target)
print ("path: ",path) 
degrees = len(path[0]) 
srcname = names2[source]
degreesofsep = 1  
for i in range(degrees-1):
    if not movies[path[0][i+1]] == movies[path[0][i]]:
        degreesofsep+=1 
        print(list(srcname)[0], " and ",list(names2[path[1][i]])[0]," starred in ", movies[path[0][i]]['title'])    
        srcname = (names2[path[1][i]]) 
print(list(srcname)[0], " and ",list(names2[path[1][degrees-1]])[0]," starred in ", movies[path[0][degrees-1]]['title'])

print ("There are ", degreesofsep, " degrees of separation") 



