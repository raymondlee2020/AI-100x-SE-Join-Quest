from behave import given, when, then
from src.game import ChineseChessGame
from src.board import ChineseChessBoard
from src.piece import General, Guard, Elephant, Horse, Rook, Cannon, Soldier, PieceColor, Position

@given('the board is empty except for a Red General at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, General(PieceColor.RED))
    context.from_pos = position

@given('the board is empty except for a Red Guard at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, Guard(PieceColor.RED))
    context.from_pos = position

@given('the board is empty except for a Red Rook at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, Rook(PieceColor.RED))
    context.from_pos = position

@given('the board is empty except for a Red Horse at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, Horse(PieceColor.RED))
    context.from_pos = position

@given('the board is empty except for a Red Elephant at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, Elephant(PieceColor.RED))
    context.from_pos = position

@given('the board is empty except for a Red Cannon at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, Cannon(PieceColor.RED))
    context.from_pos = position

@given('the board is empty except for a Red Soldier at ({row:d}, {col:d})')
def step_impl(context, row, col):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    position = Position(row, col)
    context.game.board.place_piece(position, Soldier(PieceColor.RED))
    context.from_pos = position

@given('the board has')
def step_impl(context):
    context.game = ChineseChessGame()
    context.game.board = ChineseChessBoard()
    
    for row in context.table:
        piece_type = row['Piece'].split()[0]
        color = row['Piece'].split()[1]
        # Remove parentheses from position and split by comma
        pos_parts = row['Position'].strip('()').split(',')
        row_pos = int(pos_parts[0])
        col_pos = int(pos_parts[1])
        position = Position(row_pos, col_pos)
        
        # Create the appropriate piece based on the type and color
        if piece_type == 'Red':
            piece_color = PieceColor.RED
        else:  # Black
            piece_color = PieceColor.BLACK
            
        if color == 'General':
            piece = General(piece_color)
        elif color == 'Guard':
            piece = Guard(piece_color)
        elif color == 'Elephant':
            piece = Elephant(piece_color)
        elif color == 'Horse':
            piece = Horse(piece_color)
        elif color == 'Rook':
            piece = Rook(piece_color)
        elif color == 'Cannon':
            piece = Cannon(piece_color)
        elif color == 'Soldier':
            piece = Soldier(piece_color)
        
        context.game.board.place_piece(position, piece)
        
        # Store the from_pos if it's the piece that will be moved
        if piece_color == PieceColor.RED:
            context.from_pos = position

@when('Red moves the General from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@when('Red moves the Guard from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@when('Red moves the Rook from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@when('Red moves the Horse from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@when('Red moves the Elephant from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@when('Red moves the Cannon from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@when('Red moves the Soldier from ({from_row:d}, {from_col:d}) to ({to_row:d}, {to_col:d})')
def step_impl(context, from_row, from_col, to_row, to_col):
    context.from_pos = Position(from_row, from_col)
    context.to_pos = Position(to_row, to_col)
    try:
        context.move_result = context.game.make_move(context.from_pos, context.to_pos)
    except Exception as e:
        context.move_error = e

@then('the move is legal')
def step_impl(context):
    assert context.move_result is True, f"Expected move to be legal, but it was not"

@then('the move is illegal')
def step_impl(context):
    assert context.move_result is False, f"Expected move to be illegal, but it was legal"

@then('Red wins immediately')
def step_impl(context):
    assert context.move_result is True, "Expected move to be legal"
    assert context.game.is_game_over() is True, "Expected game to be over"
    assert context.game.get_winner() == PieceColor.RED, "Expected Red to be the winner"

@then('the game is not over just from that capture')
def step_impl(context):
    assert context.move_result is True, "Expected move to be legal"
    assert context.game.is_game_over() is False, "Expected game to not be over"