


class Stats:
    def __init__(self):
        self.nodes_visited = 0
        self.q_nodes_visited = 0
        self.evaluation = 0.0

    def reset(self):
        """Reset the statistics to their initial state."""
        self.nodes_visited = 0
        self.q_nodes_visited = 0
        self.evaluation = 0.0

    def __str__(self):
        """Return a formatted string for the statistics."""
        return f"Nodes Visited: {self.nodes_visited}\nQ Nodes Visited: {self.q_nodes_visited}\nEvaluation: {self.evaluation:.2f}"
