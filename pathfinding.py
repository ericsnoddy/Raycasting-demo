# std lib
from collections import deque

class PathFinding:
    def __init__(self, game) -> None:
        self.game = game
        self.map = game.map.mini_map
        self.routes = [-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]  # start=[0, 0]
        self.moves_dict = {}
        self.get_moves_dict()


    def get_path(self, start, goal):
        # restore bfs path from initial to desired tile (from npc to player); only need to generate the next step
        self.visited_dict = self.bfs(start, goal, self.moves_dict)
        path = [goal]

        # try to retrieve goal from dict; if it doesn't exist return start which ends the algo
        step = self.visited_dict.get(goal, start)

        # build a path list by adding steps until we get to start (we don't add start)
        while step and step != start:
            path.append(step)
            step = self.visited_dict[step]

        # return last element in the path list - our next node
        return path[-1]


    def bfs(self, start, goal, moves_dict):
        # classical "bread-first" search algorithm
        # put the start tile in a queue, form a Dict of visited tiles.
        queue = deque([start])
        visited_dict = {start: None}

        # In a loop until queue is empty...  
        while queue:
            # ... we get the first element from queue, and will look at all adjacent tiles to that
            cur_node = queue.popleft()

            # (we're done when we reach our goal and won't add it to visisted_dict)
            if cur_node == goal:
                break

            # iterate on the list of possible moves
            next_nodes = moves_dict[cur_node]
            for next_node in next_nodes:
                # if we haven't visited the tile yet, and it is not currently occupied, add it to the queue
                if next_node not in visited_dict and next_node not in self.game.object_handler.npc_locations:
                    queue.append(next_node)
                    # then add it as a key to visited dict with value=first item in queue (current node)
                    visited_dict[next_node] = cur_node
        return visited_dict


    def get_next_nodes(self, x, y):
        # builds a list of valid moves relative to current tile as (0,0)
        return [(x + rx, y + ry) for rx, ry in self.routes if (x + rx, y + ry) not in self.game.map.world_map]

    
    def get_moves_dict(self):
        # build a Dict with key=map coord and value=list of available moves
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                # if tile is not an obstacle...
                if not col:
                    # build a list of possible moves by merging with growing list
                    self.moves_dict[(x, y)] = self.moves_dict.get((x, y), []) + self.get_next_nodes(x, y)