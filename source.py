from threading import Thread, Lock
from queue import Queue
import time
import threading, time, random

mutex = Lock()

class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def isValidNode(maze, node):
	if maze[node.position[0]][node.position[1]] != 0:
		return False
	else:
		return True

def createPath(current_node, t_number):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # if t_number == 1:
    #     return path[::-1] # Return reversed path
    # else:
    return path

def BiAStar(maze, start, end):
    # t1 = ThreadWithResult(target=sayHello, args=("Mariano",1))
    # t2 = ThreadWithResult(target=sayHello, args=("Mariano",2,))
    list1 = []
    list2 = []
    t1 = ThreadWithResult(target=aStar, args=(maze, start, end, list1, list2, 1))
    t2 = ThreadWithResult(target=aStar, args=(maze, end, start, list2, list1, 2))
    t1.start()
    t2.start()
    
    print(t1.result)
    print(t2.result)

def aStar(maze, start, end, self_list, other_list, t_number):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
	
    if(not isValidNode(maze, start_node) or not isValidNode(maze, end_node)):
      print("The start and end nodes are not walkable nodes.")
      return 
    
    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    counter = 1

    # Loop until you find the end
    while len(open_list) > 0:
        
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        
        # Loop until open list is empty
        if(len(open_list) > 1):
            
            # Loop through all nodes in open list
            for index, item in enumerate(open_list):
                    
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
                    
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        self_list.append(current_node.position)
        
        """Check if they have found the same node"""
        mutex.acquire()
        if current_node.position in other_list:
            print("WE FOUND THE SAME NODE")
            path = createPath(current_node, t_number)
            mutex.release()
            return path
        mutex.release()
        
        # Found the goal
        if current_node == end_node:
            path = createPath(current_node, t_number)
            return path
            
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the closed list
            if child in closed_list:
                continue
            
            # Child is already in the open list
            if child in open_list:
                continue
          
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            
            # Add the child to the open list
            open_list.append(child)

        # Keeps track of the number of iterations
        counter+=1


def sayHello(name, thread_number):
    """This funtion was created with the intention of showing when a
    thread would be created to divide the problem into subproblems"""
    time.sleep(1.0)
    print(f"Hello from thread #{thread_number} {name}!")
    return "Hello from outiside a thread !"

def main():
		#    0  1  2  3  4  5  6  7  8  9  10	
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 1
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 2
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 3
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 4
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 5
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 6
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 7
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 8
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] # 10

    start = (5, 0)
    end = (5,10)
    
    BiAStar(maze, start, end)


if __name__ == '__main__':
    main()