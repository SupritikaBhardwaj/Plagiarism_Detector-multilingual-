def graph_similarity(left: dict, right: dict) -> float:
    left_labels = {node["label"] for node in left.get("nodes", [])}
    right_labels = {node["label"] for node in right.get("nodes", [])}
    label_score = len(left_labels & right_labels) / max(len(left_labels | right_labels), 1)
    left_edges = {(edge["type"], edge["source"] < edge["target"]) for edge in left.get("edges", [])}
    right_edges = {(edge["type"], edge["source"] < edge["target"]) for edge in right.get("edges", [])}
    edge_score = len(left_edges & right_edges) / max(len(left_edges | right_edges), 1)
    return (label_score * 0.6) + (edge_score * 0.4)

