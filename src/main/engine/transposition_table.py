

class TTEntry:
    def __init__(self, value, depth, flag, best_move=None):
        self.value = value
        self.depth = depth
        self.flag = flag
        self.best_move = best_move
