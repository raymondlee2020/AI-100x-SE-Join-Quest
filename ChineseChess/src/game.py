from typing import Optional

# Import from local modules
from .board import ChineseChessBoard
from .piece import PieceColor, Position


class ChineseChessGame:
    def __init__(self):
        self.board = ChineseChessBoard()
    
    def init_game(self) -> None:
        # Will initialize the game by setting up the board
        self.board.init()
    
    def make_move(self, from_pos, to_pos) -> bool:
        """Make a move from the from_position to the to_position
        
        Args:
            from_pos: tuple or Position - Starting position
            to_pos: tuple or Position - Target position
        
        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Convert tuple positions to Position objects if needed
        if isinstance(from_pos, tuple):
            from_row, from_col = from_pos
            from_position = Position(from_row, from_col)
        else:
            from_position = from_pos
            
        if isinstance(to_pos, tuple):
            to_row, to_col = to_pos
            to_position = Position(to_row, to_col)
        else:
            to_position = to_pos
        
        # Try to make the move
        result = self.board.move_piece(from_position, to_position)
        
        # If the move was successful and the game is not over, switch turns
        if result and not self.board.is_game_over():
            self.board.switch_turn()
            
        return result
    
    def get_current_player(self) -> PieceColor:
        """Get the current player's color"""
        return self.board.current_turn
    
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return self.board.is_game_over()
    
    def get_winner(self) -> Optional[PieceColor]:
        """Get the winner of the game"""
        return self.board.get_winner()