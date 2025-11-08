from collections import defaultdict
import json
from collections import deque


def build_player_adjacency(json_file):
    adj = defaultdict(set)
    with open(json_file) as f:
        data = json.load(f)
        for season in data:
            for team in data[season].get("teams"):
                roster_names = [p.get("player_name") for p in team.get("roster") if p.get("player_name")]
                for i in range(len(roster_names)):
                    for j in range(i + 1, len(roster_names)):
                        p1 = roster_names[i]
                        p2 = roster_names[j]
                        adj[p1].add(p2)
                        adj[p2].add(p1)
    return adj

def resolve_name_to_ids(name, name_to_ids):
    """ Given a player name (case insensitive), yield all matching player_ids from name_to_ids dict."""
    return name_to_ids.get(name.lower(), set())

def bfs_shortest_path(graph, src_id, dst_id):
    """ Returns list of player_ids representing the shortest path from src_id to dst_id ,"""
    if src_id == dst_id:
        return [src_id]
    if src_id not in graph or dst_id not in graph:
        return []

    q = deque([src_id])
    parent = {src_id: None}
    seen = {src_id}

    while q:
        u = q.popleft()
        for v in graph.get(u, []):
            if v in seen: 
                continue
            parent[v] = u
            if v == dst_id:
                # reconstruct
                path = [v]
                while parent[path[-1]] is not None:
                    path.append(parent[path[-1]])
                path.reverse()
                return path
            seen.add(v)
            q.append(v)
    return []

def annotate_path_edges(path, edge_meta):
    """
    Given a list of player_ids representing a path, return a list of dicts for each edge in the path,
    """
    info = []
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]
        key = (min(a, b), max(a, b))
        info.append({
            "a": a, "b": b,
            "seasons_teams": edge_meta.get(key)
        })
    return info


