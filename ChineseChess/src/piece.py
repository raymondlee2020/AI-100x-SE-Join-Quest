from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional, Tuple


class PieceType(Enum):
    GENERAL = 1
    GUARD = 2
    ELEPHANT = 3
    HORSE = 4
    ROOK = 5
    CANNON = 6
    SOLDIER = 7


class PieceColor(Enum):
    RED = 1
    BLACK = 2


class Position:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def get_row(self) -> int:
        return self.row

    def get_column(self) -> int:
        return self.column
        
    def is_inside_palace(self, color: PieceColor) -> bool:
        # Palace boundaries:
        # Red palace is within rows 1-3, columns 4-6
        # Black palace is within rows 8-10, columns 4-6
        if self.column < 4 or self.column > 6:
            return False
            
        if color == PieceColor.RED:
            return 1 <= self.row <= 3
        else:  # BLACK
            return 8 <= self.row <= 10
        
    def is_within_board(self) -> bool:
        # Board size is 9x10 (columns x rows)
        # Rows are 1-10, columns are 1-9
        return 1 <= self.row <= 10 and 1 <= self.column <= 9
        
    def is_beyond_river(self, color: PieceColor) -> bool:
        # For RED pieces, beyond river means row >= 6
        # For BLACK pieces, beyond river means row <= 5
        if color == PieceColor.RED:
            return self.row >= 6
        else:  # BLACK
            return self.row <= 5


class ChessPiece(ABC):
    def __init__(self, piece_type: PieceType, color: PieceColor):
        self.type = piece_type
        self.color = color
        
    def get_type(self) -> PieceType:
        return self.type
        
    def get_color(self) -> PieceColor:
        return self.color
    
    @abstractmethod
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        pass
        
    def can_capture(self, board: 'ChineseChessBoard', to_pos: Position) -> bool:
        # Check if a piece can capture at the target position
        target_piece = board.get_piece(to_pos)
        if not target_piece:
            return True  # No piece to capture, move is allowed
        return target_piece.get_color() != self.color  # Can only capture opponent's pieces


class General(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.GENERAL, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # General can only move within the palace
        if not to_pos.is_inside_palace(self.color):
            return False
        
        # General can only move one step horizontally or vertically
        row_diff = abs(to_pos.get_row() - from_pos.get_row())
        col_diff = abs(to_pos.get_column() - from_pos.get_column())
        
        # Must move exactly one step in one direction only
        if not ((row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)):
            return False
            
        # Check if this move would result in generals facing each other
        if self._would_generals_be_facing(board, from_pos, to_pos):
            return False
            
        # If we passed all checks, the move is valid
        return True
    
    def _would_generals_be_facing(self, board, from_pos, to_pos):
        # Create a temporary copy of board state
        temp_board = dict(board.board)
        from_key = (from_pos.get_row(), from_pos.get_column())
        to_key = (to_pos.get_row(), to_pos.get_column())
        
        # Simulate move
        piece = temp_board.get(from_key)
        if piece:
            temp_board[to_key] = piece
            del temp_board[from_key]
            
            # Find both generals
            red_general_pos = None
            black_general_pos = None
            
            for pos, p in temp_board.items():
                if p.get_type() == PieceType.GENERAL:
                    if p.get_color() == PieceColor.RED:
                        red_general_pos = pos
                    else:
                        black_general_pos = pos
                        
            # If both generals exist and are in the same column
            if red_general_pos and black_general_pos:
                if red_general_pos[1] == black_general_pos[1]:
                    # Check if there are pieces between them
                    min_row = min(red_general_pos[0], black_general_pos[0])
                    max_row = max(red_general_pos[0], black_general_pos[0])
                    col = red_general_pos[1]
                    
                    # Check each position between the generals
                    for r in range(min_row + 1, max_row):
                        if (r, col) in temp_board:
                            # There's a piece between them, so not facing
                            return False
                    
                    # No pieces between generals in the same column
                    return True
        
        return False


class Guard(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.GUARD, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # Guard can only move within the palace
        if not to_pos.is_inside_palace(self.color):
            return False
            
        # Guard can only move diagonally one step
        row_diff = abs(to_pos.get_row() - from_pos.get_row())
        col_diff = abs(to_pos.get_column() - from_pos.get_column())
        
        # Must move exactly one step diagonally
        if not (row_diff == 1 and col_diff == 1):
            return False
            
        # If we passed all checks, the move is valid
        return True


class Elephant(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.ELEPHANT, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # Elephant moves exactly 2 steps diagonally
        row_diff = abs(to_pos.get_row() - from_pos.get_row())
        col_diff = abs(to_pos.get_column() - from_pos.get_column())
        
        # Check if the move is exactly 2 steps diagonally
        if not (row_diff == 2 and col_diff == 2):
            return False
            
        # Elephant cannot cross the river
        if to_pos.is_beyond_river(self.color):
            return False
            
        # Check if the midpoint is blocked (Elephant can't jump over pieces)
        # Calculate the midpoint position
        mid_row = (from_pos.get_row() + to_pos.get_row()) // 2
        mid_col = (from_pos.get_column() + to_pos.get_column()) // 2
        mid_pos = (mid_row, mid_col)
        
        # If there's a piece at the midpoint, the Elephant is blocked
        if board.get_piece(mid_pos):
            return False
            
        # If we passed all checks, the move is valid
        return True


class Horse(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.HORSE, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # Horse moves in an "L" shape: 2 steps in one direction, then 1 step perpendicular
        row_diff = abs(to_pos.get_row() - from_pos.get_row())
        col_diff = abs(to_pos.get_column() - from_pos.get_column())
        
        # Check if the move forms an "L" shape (2+1)
        if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
            return False
        
        # Check if the Horse is blocked (legs blocked)
        # For a Horse move, we need to check if there's a piece in the way
        # If moving 2 steps horizontally, check the adjacent horizontal cell
        # If moving 2 steps vertically, check the adjacent vertical cell
        blocking_pos = None
        if row_diff == 2:  # Moving 2 steps vertically
            # Check the adjacent vertical cell
            block_row = from_pos.get_row() + (1 if to_pos.get_row() > from_pos.get_row() else -1)
            block_col = from_pos.get_column()
            blocking_pos = (block_row, block_col)
        else:  # row_diff == 1, col_diff == 2, moving 2 steps horizontally
            # Check the adjacent horizontal cell
            block_row = from_pos.get_row()
            block_col = from_pos.get_column() + (1 if to_pos.get_column() > from_pos.get_column() else -1)
            blocking_pos = (block_row, block_col)
        
        # If there's a piece at the blocking position, the move is invalid
        if board.get_piece(blocking_pos):
            return False
        
        # If we passed all checks, the move is valid
        return True


class Rook(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.ROOK, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # Rook can move horizontally or vertically any number of steps
        row_diff = to_pos.get_row() - from_pos.get_row()
        col_diff = to_pos.get_column() - from_pos.get_column()
        
        # Must move either horizontally or vertically (not both)
        if not ((row_diff == 0 and col_diff != 0) or (row_diff != 0 and col_diff == 0)):
            return False
            
        # Check if there are pieces in the path
        if row_diff == 0:  # Moving horizontally
            start_col = min(from_pos.get_column(), to_pos.get_column()) + 1
            end_col = max(from_pos.get_column(), to_pos.get_column())
            
            row = from_pos.get_row()
            for col in range(start_col, end_col):
                if board.get_piece((row, col)):
                    return False
                    
        else:  # Moving vertically
            start_row = min(from_pos.get_row(), to_pos.get_row()) + 1
            end_row = max(from_pos.get_row(), to_pos.get_row())
            
            col = from_pos.get_column()
            for row in range(start_row, end_row):
                if board.get_piece((row, col)):
                    return False
            
        # If we passed all checks, the move is valid
        return True


class Cannon(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.CANNON, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # Cannon moves like a Rook (horizontally or vertically)
        row_diff = to_pos.get_row() - from_pos.get_row()
        col_diff = to_pos.get_column() - from_pos.get_column()
        
        # Must move either horizontally or vertically (not both)
        if not ((row_diff == 0 and col_diff != 0) or (row_diff != 0 and col_diff == 0)):
            return False
            
        # Count pieces in the path to determine if it's a valid move
        pieces_in_path = 0
        target_piece = board.get_piece(to_pos)
        
        if row_diff == 0:  # Moving horizontally
            start_col = min(from_pos.get_column(), to_pos.get_column()) + 1
            end_col = max(from_pos.get_column(), to_pos.get_column())
            
            row = from_pos.get_row()
            for col in range(start_col, end_col):
                if board.get_piece((row, col)):
                    pieces_in_path += 1
        else:  # Moving vertically
            start_row = min(from_pos.get_row(), to_pos.get_row()) + 1
            end_row = max(from_pos.get_row(), to_pos.get_row())
            
            col = from_pos.get_column()
            for row in range(start_row, end_row):
                if board.get_piece((row, col)):
                    pieces_in_path += 1
                    
        # Cannon can move like a Rook if there are no pieces in the path and no piece at the target
        if pieces_in_path == 0 and not target_piece:
            return True
        
        # Cannon can capture by jumping exactly one piece (pieces_in_path == 1) and target is an opponent piece
        if pieces_in_path == 1 and target_piece and target_piece.get_color() != self.color:
            return True
            
        # All other situations are invalid
        return False
    
    def can_capture(self, board: 'ChineseChessBoard', to_pos: Position) -> bool:
        # Cannon's capture is handled in is_valid_move, since it's more complex
        # This method is still needed, but we just return True to let is_valid_move
        # handle the actual capturing logic
        return True


class Soldier(ChessPiece):
    def __init__(self, color: PieceColor):
        super().__init__(PieceType.SOLDIER, color)
        
    def is_valid_move(self, board: 'ChineseChessBoard', from_pos: Position, to_pos: Position) -> bool:
        # Calculate direction based on color
        # For RED, forward is increasing row
        # For BLACK, forward is decreasing row
        forward_direction = 1 if self.color == PieceColor.RED else -1
        
        # Calculate row and column differences
        row_diff = to_pos.get_row() - from_pos.get_row()
        col_diff = to_pos.get_column() - from_pos.get_column()
        
        # Check if the Soldier has crossed the river
        crossed_river = from_pos.is_beyond_river(self.color)
        
        # Soldiers can only move one step at a time
        if abs(row_diff) > 1 or abs(col_diff) > 1:
            return False
            
        # Soldiers cannot move diagonally
        if row_diff != 0 and col_diff != 0:
            return False
            
        # Before crossing the river, Soldiers can only move forward
        if not crossed_river:
            # Can only move forward
            if row_diff != forward_direction or col_diff != 0:
                return False
        else:  # After crossing the river
            # Can move forward or sideways, but not backward
            if row_diff == -forward_direction:  # Trying to move backward
                return False
            
            # Can move forward or sideways, but only one step at a time
            if abs(row_diff) + abs(col_diff) != 1:
                return False
        
        # If we passed all checks, the move is valid
        return True