from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal.
# You can find the path to the shortest unexplored room by using a breadth-first search for a room with a `'?'` for an exit. If you use the `bfs` code from the homework, you will need to make a few modifications.
# 1. Instead of searching for a target vertex, you are searching for an exit with a `'?'` as the value. If an exit has been explored, you can put it in your BFS queue like normal.

# 2. Breath First Search will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.

traversal_path = []

# The graph should be a dictionary
mapDictionary = {}

def bfs(starting_room_id):
    # Create an empty Queue
    q = Queue()
    # Enqueue(Add) a path to the starting_vertex to the queue.
    q.enqueue([starting_room_id])
    # Create an empty set to store visited.
    visited = set()
    # Create a while loop: Queue is not empty
    while q.size() > 0:
    # Dequeue(remove) the first path.
        path = q.dequeue()
    # Grab the last vertex from the path.
        current_room = path[-1]
    # Add v to visited.
        visited.add(current_room)
    # For each direction in the map's current_room.
        for direction in mapDictionary[current_room]:
    # Check if the current_room's direction is equal to '?'.
            if mapDictionary[current_room][direction] == '?':
                
                # Return path
                return path
            
            #Else if the current_room's direction has not been visited.
            elif mapDictionary[current_room][direction] not in visited:
            # Create a new path to append(add) the direction.
                new_path = list(path)
                new_path.append(mapDictionary[current_room][direction])
                q.enqueue(new_path)

# Creating the maze by dft.
def search(starting_room):
    
    # Reverse the directions
    opp_directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

    # Create a counter of rooms that the player has been to.
    vistedRoomId = 0

    # While the length of the mapDictionary is not equal to the length of the room_graph.
    while len(mapDictionary) != len(room_graph):
        # The room we are currently in.
        current_room =player.current_room
        # The room_id we are currently in.
        room_id = current_room.id
        # Make a dictionary of rooms
        room_dict = {}
        
        # If the room_id is not in mapDictionary.
        if room_id not in mapDictionary:
            # Repeat to find the possible exits.
            for i in current_room.get_exits():
                # Add the key at [i] and the value = '?'.
                room_dict[i] = '?'
            
            # Update the room
            if traversal_path:
                # prevRoom is equal to the opposite directions of the last travel path.
                prevRoom = opp_directions[traversal_path[-1]]
                # Add the prevRoom to the room_dict and add it to the counter.
                room_dict[prevRoom] = vistedRoomId
            # Make the room_id of the mapDictionary to equal to the room_dict.
            mapDictionary[room_id] = room_dict
        
        # Else room_id is equal to the room_id of the mapDictionary.
        else:
            room_id = mapDictionary[room_id]    

        # We see there is an unexplored '?'
        # Need to see if a room is connected or not
        # Storing the '?'s
        possible_exits = list()

        # Repeat through the room dictionary
        for direction in room_dict:
            # If the direction of the room_dict is equal to '?':
            if room_dict[direction] == '?':
                # Add(append) the direction to the possible_exits.
                possible_exits.append(direction)
                
        # If the length of the possible_exits is not equal to 0:
        if len(possible_exits) != 0:
            # Then we want to randomly shuffle the possible_exits.
            random.shuffle(possible_exits)
            # Set the direction to equal to the possible_exits at index 0.
            direction = possible_exits[0]
            # Append the direction of the traversal_path.
            traversal_path.append(direction)
            
            # Move the player by the travel().
            player.travel(direction)
            
            # Grab the player's current room
            room_move = player.current_room
            
            # Current room.id and direction of the mapDictionary is set to equal to room_move.id.
            mapDictionary[current_room.id][direction] = room_move.id
            
            # Set the visitedRoomId to equal to the current_room.id.
            vistedRoomId = current_room.id
        
        # Else use bfs to search for the next possible rooms and exits by using room_id.
        else:
            next_room = bfs(room_id)
            
            # If next_room is not None and the length of the next_room is greater than 0:
            if next_room is not None and len(next_room) > 0:
                # For loop: Then repeat the length of the room to gain access to the room's id.
                for i in range(len(next_room)-1):
                    # Repeat the mapDictionary's next_room at the index to access the direction.
                    for direction in mapDictionary[next_room[i]]:
                        # If the next_room[i] and direction of the mapDictionary is equal to next_room[i + 1]:
                        if mapDictionary[next_room[i]][direction] == next_room[i + 1]:
                            # Append the direction of the traversal_path
                            traversal_path.append(direction)
                            # Move player
                            player.travel(direction)
            else:
                break
        
search(room_graph)
print("Map Graph Dictionary", mapDictionary) 
print("------------------")
print("Traversal path", traversal_path)
print("------------------")

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
