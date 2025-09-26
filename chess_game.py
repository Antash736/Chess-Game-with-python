import pygame
import sys
import random
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

move_sound = pygame.mixer.Sound("Sounds/move_Sound.mp3")
move_sound.set_volume(0.5)
capture_sound = pygame.mixer.Sound("Sounds/capture_Sound.mp3")
capture_sound.set_volume(0.5)
end_sound = pygame.mixer.Sound("Sounds/win_Sound.mp3")
end_sound.set_volume(0.5)

WIDTH, HEIGHT = 700, 700
SQUARE_SIZE = WIDTH // 8

LIGHT_COLOR = (255, 255, 255)
DARK_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
MOVE_COLOR = (0, 0, 255, 100)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

class ChessPiece:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(f'images/{image}')
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

board = [[None for _ in range(8)] for _ in range(8)]
current_player = "White"
selected_piece = None
selected_position = None
valid_moves = []

def init_board():
    for col in range(8):
        board[1][col] = ChessPiece('Black', 'Pawn', 'black pawn.png')
    board[0][0] = ChessPiece('Black', 'Rook', 'black rook.png')
    board[0][1] = ChessPiece('Black', 'Knight', 'black knight.png')
    board[0][2] = ChessPiece('Black', 'Bishop', 'black bishop.png')
    board[0][3] = ChessPiece('Black', 'Queen', 'black queen.png')
    board[0][4] = ChessPiece('Black', 'King', 'black king.png')
    board[0][5] = ChessPiece('Black', 'Bishop', 'black bishop.png')
    board[0][6] = ChessPiece('Black', 'Knight', 'black knight.png')
    board[0][7] = ChessPiece('Black', 'Rook', 'black rook.png')
    for col in range(8):
        board[6][col] = ChessPiece('White', 'Pawn', 'white pawn.png')
    board[7][0] = ChessPiece('White', 'Rook', 'white rook.png')
    board[7][1] = ChessPiece('White', 'Knight', 'white knight.png')
    board[7][2] = ChessPiece('White', 'Bishop', 'white bishop.png')
    board[7][3] = ChessPiece('White', 'Queen', 'white queen.png')
    board[7][4] = ChessPiece('White', 'King', 'white king.png')
    board[7][5] = ChessPiece('White', 'Bishop', 'white bishop.png')
    board[7][6] = ChessPiece('White', 'Knight', 'white knight.png')
    board[7][7] = ChessPiece('White', 'Rook', 'white rook.png')

def show_start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 60)
    title = font.render("Welcome to Chess!", True, (255, 255, 255))
    instruction = pygame.font.SysFont(None, 36).render("Press any key to start", True, (200, 200, 200))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_end_screen(winner):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 60)
    message = font.render(f"{winner} Wins!", True, (255, 255, 255))
    instruction = pygame.font.SysFont(None, 36).render("Press any key to exit", True, (200, 200, 200))
    screen.blit(message, (WIDTH//2 - message.get_width()//2, HEIGHT//2 - 100))
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
    end_sound.play()
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def is_king_captured(color):
    for row in board:
        for piece in row:
            if piece and piece.type == "King" and piece.color == color:
                return False
    return True

def is_clear_path(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    d_row = end_row - start_row
    d_col = end_col - start_col
    step_row = (d_row // abs(d_row)) if d_row != 0 else 0
    step_col = (d_col // abs(d_col)) if d_col != 0 else 0
    current_row = start_row + step_row
    current_col = start_col + step_col
    while (current_row, current_col) != (end_row, end_col):
        if board[current_row][current_col] is not None:
            return False
        current_row += step_row
        current_col += step_col
    return True

def is_castling(piece, start_pos, end_pos):
    if piece.type == "King" and not piece.has_moved:
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if start_row == end_row and abs(end_col - start_col) == 2:
            if end_col > start_col:
                rook_col = 7
                path = [(start_row, c) for c in range(start_col + 1, rook_col)]
            else:
                rook_col = 0
                path = [(start_row, c) for c in range(rook_col + 1, start_col)]
            for r, c in path:
                if board[r][c] is not None:
                    return False
            rook = board[start_row][rook_col]
            if rook and rook.type == "Rook" and not rook.has_moved and rook.color == piece.color:
                return True
    return False

def perform_castling(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    if end_col > start_col:
        rook_start = (start_row, 7)
        rook_end = (start_row, end_col - 1)
    else:
        rook_start = (start_row, 0)
        rook_end = (start_row, end_col + 1)
    animate_move(start_pos, end_pos, board[start_row][start_col])
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = None
    board[end_row][end_col].has_moved = True
    board[rook_end[0]][rook_end[1]] = board[rook_start[0]][rook_start[1]]
    board[rook_start[0]][rook_start[1]] = None
    board[rook_end[0]][rook_end[1]].has_moved = True
    move_sound.play()

def is_valid_move(piece, start_pos, end_pos):
    if is_castling(piece, start_pos, end_pos):
        return True
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    dx = end_col - start_col
    dy = end_row - start_row
    if piece.type == "Pawn":
        direction = -1 if piece.color == "White" else 1
        start_row_ref = 6 if piece.color == "White" else 1
        if dx == 0 and board[end_row][end_col] is None:
            if dy == direction:
                return True
            if dy == 2 * direction and start_row == start_row_ref and board[start_row + direction][start_col] is None:
                return True
        elif abs(dx) == 1 and dy == direction and board[end_row][end_col] and board[end_row][end_col].color != piece.color:
            return True
    elif piece.type == "Rook":
        if dx == 0 or dy == 0:
            return is_clear_path(start_pos, end_pos)
    elif piece.type == "Knight":
        return (abs(dx), abs(dy)) in [(1, 2), (2, 1)]
    elif piece.type == "Bishop":
        if abs(dx) == abs(dy):
            return is_clear_path(start_pos, end_pos)
    elif piece.type == "Queen":
        if dx == 0 or dy == 0 or abs(dx) == abs(dy):
            return is_clear_path(start_pos, end_pos)
    elif piece.type == "King":
        return max(abs(dx), abs(dy)) == 1
    return False

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if selected_position == (row, col):
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(HIGHLIGHT_COLOR)
                screen.blit(highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            if (row, col) in valid_moves:
                move_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                move_highlight.fill(MOVE_COLOR)
                screen.blit(move_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def animate_move(start_pos, end_pos, piece):
    frames = 10
    start_x = start_pos[1] * SQUARE_SIZE
    start_y = start_pos[0] * SQUARE_SIZE
    end_x = end_pos[1] * SQUARE_SIZE
    end_y = end_pos[0] * SQUARE_SIZE
    dx = (end_x - start_x) / frames
    dy = (end_y - start_y) / frames
    for i in range(1, frames + 1):
        draw_board()
        screen.blit(piece.image, (start_x + dx * i, start_y + dy * i))
        pygame.display.flip()
        pygame.time.delay(40)

def get_all_possible_moves(board, color):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == color:
                for r in range(8):
                    for c in range(8):
                        if is_valid_move(piece, (row, col), (r, c)):
                            target = board[r][c]
                            if target is None or target.color != piece.color:
                                moves.append(((row, col), (r, c), target))
    return moves

def make_move(board, move):
    (start, end, captured) = move
    piece = board[start[0]][start[1]]
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = None
    piece.has_moved = True
    if captured:
        capture_sound.play()
    else:
        move_sound.play()
    return captured

def undo_move(board, move, captured):
    (start, end, _) = move
    piece = board[end[0]][end[1]]
    board[start[0]][start[1]] = piece
    board[end[0]][end[1]] = captured
    piece.has_moved = False

piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 1000}

def evaluate_board(board, color):
    score = 0
    for row in board:
        for piece in row:
            if piece:
                value = piece_values[piece.type.lower()]
                score += value if piece.color == color else -value
    return score

def minimax(board, depth, alpha, beta, maximizing_player, color):
    if depth == 0:
        return evaluate_board(board, color)
    moves = get_all_possible_moves(board, color if maximizing_player else ("Black" if color == "White" else "White"))
    if not moves:
        return evaluate_board(board, color)
    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            captured = make_move(board, move)
            eval = minimax(board, depth - 1, alpha, beta, False, color)
            undo_move(board, move, captured)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            captured = make_move(board, move)
            eval = minimax(board, depth - 1, alpha, beta, True, color)
            undo_move(board, move, captured)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_move(board, color):
    best_move = None
    best_score = float('-inf')
    for move in get_all_possible_moves(board, color):
        captured = make_move(board, move)
        score = minimax(board, 2, float('-inf'), float('inf'), False, color)
        undo_move(board, move, captured)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def delayed_ai_move(board, color):
    time.sleep(0.5)
    return ai_move(board, color)

show_start_screen()
init_board()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            if selected_piece:
                if is_valid_move(selected_piece, selected_position, (row, col)):
                    if is_castling(selected_piece, selected_position, (row, col)):
                        perform_castling(selected_position, (row, col))
                    else:
                        target_piece = board[row][col]
                        if target_piece is None or target_piece.color != selected_piece.color:
                            animate_move(selected_position, (row, col), selected_piece)
                            board[row][col] = selected_piece
                            board[selected_position[0]][selected_position[1]] = None
                            selected_piece.has_moved = True
                            if target_piece:
                                capture_sound.play()
                            else:
                                move_sound.play()
                    selected_piece = None
                    selected_position = None
                    valid_moves = []
                    if is_king_captured("Black"):
                        show_end_screen("White")
                        running = False
                        break
                    current_player = "Black"
                    move = delayed_ai_move(board, "Black")
                    if move:
                        (start, end, _) = move
                        piece = board[start[0]][start[1]]
                        animate_move(start, end, piece)
                        board[end[0]][end[1]] = piece
                        board[start[0]][start[1]] = None
                        piece.has_moved = True
                        if is_king_captured("White"):
                            show_end_screen("Black")
                            running = False
                            break
                        current_player = "White"
                else:
                    selected_piece = None
                    selected_position = None
                    valid_moves = []
            else:
                if board[row][col] and board[row][col].color == current_player:
                    selected_piece = board[row][col]
                    selected_position = (row, col)
                    valid_moves = []
                    for r in range(8):
                        for c in range(8):
                            if is_valid_move(selected_piece, selected_position, (r, c)):
                                target = board[r][c]
                                if target is None or target.color != selected_piece.color:
                                    valid_moves.append((r, c))
    draw_board()
    pygame.display.flip()

pygame.quit()
