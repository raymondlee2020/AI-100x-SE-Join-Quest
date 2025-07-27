from typing import Dict, Optional, Tuple

from src.piece import Position, PieceColor, ChessPiece


class ChineseChessBoard:
    def __init__(self):
        self.board: Dict[Tuple[int, int], ChessPiece] = {}
        self.current_turn: PieceColor = PieceColor.RED
        self.game_over: bool = False
        self.winner: Optional[PieceColor] = None

    def init(self) -> None:
        # Will initialize the board with all pieces in their starting positions
        self.board.clear()
        self.current_turn = PieceColor.RED
        self.game_over = False
        self.winner = None

    def place_piece(self, position: Position, piece: ChessPiece) -> None:
        # Place a piece at the given position
        self.board[(position.get_row(), position.get_column())] = piece

    def get_piece(self, position):
        """Get the piece at the given position"""
        if isinstance(position, Position):
            pos_key = (position.get_row(), position.get_column())
        else:
            # Assume it's a tuple (row, col)
            pos_key = position
        return self.board.get(pos_key)

    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another, if the move is valid"""
        # Convert tuple positions to Position objects if needed
        if isinstance(from_pos, tuple):
            from_row, from_col = from_pos
            from_position = Position(from_row, from_col)
        else:
            from_position = from_pos
            from_row, from_col = from_pos.get_row(), from_pos.get_column()

        if isinstance(to_pos, tuple):
            to_row, to_col = to_pos
            to_position = Position(to_row, to_col)
        else:
            to_position = to_pos
            to_row, to_col = to_pos.get_row(), to_pos.get_column()

        # Get piece at from_position
        piece = self.get_piece(from_position)
        if not piece:
            return False

        # Check if it's the piece's turn to move
        if piece.get_color() != self.current_turn:
            return False

        # Check if move is valid according to piece rules
        if not piece.is_valid_move(self, from_position, to_position):
            return False

        # Check if target position has a piece that can be captured
        if not piece.can_capture(self, to_position):
            return False

        # Capture target piece if it exists (or just move if empty)
        target_piece = self.get_piece(to_position)

        # Move the piece
        self.board[(to_row, to_col)] = piece
        del self.board[(from_row, from_col)]

        # Check if the game is over (e.g., General captured)
        if target_piece and target_piece.get_type().name == "GENERAL":
            self.game_over = True
            self.winner = piece.get_color()

        return True

    def switch_turn(self):
        """Switch the current turn to the other player"""
        self.current_turn = PieceColor.BLACK if self.current_turn == PieceColor.RED else PieceColor.RED

    def is_game_over(self):
        """Check if the game is over"""
        return self.game_over

    def get_winner(self):
        """Get the winner of the game"""
        return self.winner

    def is_general_facing_general(self):
        """Check if the two generals are facing each other with no pieces in between"""
        # Stub implementation for now
        return False