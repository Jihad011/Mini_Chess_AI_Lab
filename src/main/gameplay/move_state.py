


class MoveState:
    def __init__(self, pre_pos, new_pos, moved_piece, captured_piece=None, is_promoted=False):
        self.pre_pos = pre_pos
        self.new_pos = new_pos
        self.moved_piece = moved_piece
        self.captured_piece = captured_piece
        self.is_promoted = is_promoted

    def __eq__(self, other):
        if not isinstance(other, MoveState):
            return False
        return self.pre_pos == other.pre_pos and self.new_pos == other.new_pos

    def copy(self):
        return MoveState(self.pre_pos, self.new_pos, self.moved_piece, self.captured_piece, self.is_promoted)


    def __repr__(self):
        return (f"MoveState(pre_pos={self.pre_pos}, new_pos={self.new_pos}, "
                f"moved_piece={self.moved_piece}, captured_piece={self.captured_piece}, "
                f"is_promoted={self.is_promoted})")

    def __str__(self):
        # For debugging purposes
        captured = f"captured {self.captured_piece}" if self.captured_piece else "no capture"
        promoted = " and promoted to Queen" if self.is_promoted else ""
        return f"Moved {self.moved_piece} from {self.pre_pos} to {self.new_pos}, {captured}{promoted}."


    def same_pos(self):
        return self.pre_pos == self.new_pos
