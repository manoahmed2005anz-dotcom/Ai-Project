
# **********************************************   2
def check_win(board_instance, piece):
    board_data = board_instance.board

    # 1. أفقيًا
    for r in range(ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = board_data[r][c : c + CONNECT_N]
            if window.count(piece) == CONNECT_N:
                return True

    # 2. عموديًا
    for c in range(COLUMNS):
        for r in range(ROWS - CONNECT_N + 1):
            window = [board_data[r + i][c] for i in range(CONNECT_N)]
            if window.count(piece) == CONNECT_N:
                return True

    # 3. قطريًا (صعوداً لليمين /)
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r - i][c + i] for i in range(CONNECT_N)]
            if window.count(piece) == CONNECT_N:
                return True

    # 4. قطريًا (نزولاً لليمين \)
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r + i][c + i] for i in range(CONNECT_N)]
            if window.count(piece) == CONNECT_N:
                return True

    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    count_piece = window.count(piece)
    count_opp = window.count(opp_piece)
    count_empty = window.count(EMPTY)

    # التهديدات الفائزة
    if count_piece == 4:
        score += SCORE_FOUR
    elif count_piece == 3 and count_empty == 1:
        score += SCORE_THREE
    elif count_piece == 2 and count_empty == 2:
        score += SCORE_TWO

    # منع الخصم
    if count_opp == 3 and count_empty == 1:
        score -= SCORE_BLOCKED_THREE

    return score

# Heuristic evaluation functions for AI (position scoring)
def get_position_score(board_instance, piece):
    board_data = board_instance.board
    score = 0
    center_col = COLUMNS // 2
    
    # 1. Center column bonus
    center_count = sum(1 for r in range(ROWS) if board_data[r][center_col] == piece)
    score += center_count * CENTER_WEIGHT

    # 2. Evaluate all windows (horizontal, vertical, diagonal)
    
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = board_data[r][c:c + CONNECT_N]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - CONNECT_N + 1):
            window = [board_data[r + i][c] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)
            
    # Diagonal ascending (/)
    for r in range(CONNECT_N - 1, ROWS):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r - i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)

    # Diagonal descending (\)
    for r in range(ROWS - CONNECT_N + 1):
        for c in range(COLUMNS - CONNECT_N + 1):
            window = [board_data[r + i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return (
        check_win(board, PLAYER_PIECE)
        or check_win(board, AI_PIECE)
        or board.is_full()
    )
