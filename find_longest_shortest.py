from collections import deque
from main import build_player_adjacency

def find_longest_shortest(graph):
    nodes = list(graph.keys())
    longest_path = []

    for i, start_node in enumerate(nodes):
        q = deque([(start_node, [start_node])])
        visited = {start_node}
        

        furthest_node_path = [start_node]
        while q:
            current_node, path = q.popleft()
            
            if len(path) > len(furthest_node_path):
                furthest_node_path = path

            for neighbor in graph.get(current_node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append((neighbor, path + [neighbor]))
        
        if len(furthest_node_path) > len(longest_path):
            longest_path = furthest_node_path
            
    return longest_path

if __name__ == "__main__":
    player_graph = build_player_adjacency("nba_rosters_1999_to_present_working.json")
    final_path = find_longest_shortest(player_graph)
    if final_path:
        print(final_path[0])
        print(final_path[-1])