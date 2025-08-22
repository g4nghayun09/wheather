# -------------------- 필요한 라이브러리 --------------------
import streamlit as st
import random
import time

# -------------------- 게임판 설정 --------------------
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

TETROMINOES = {
    'I': [[(0, 0), (1, 0), (2, 0), (3, 0)],
          [(1, 0), (1, 1), (1, 2), (1, 3)]],
    'J': [[(0, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (2, 0), (1, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (2, 2)],
          [(1, 0), (1, 1), (0, 2), (1, 2)]],
    'L': [[(0, 1), (1, 1), (2, 1), (2, 0)],
          [(1, 0), (1, 1), (1, 2), (0, 2)],
          [(0, 2), (0, 1), (1, 1), (2, 1)],
          [(2, 0), (1, 0), (1, 1), (1, 2)]],
    'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    'S': [[(1, 0), (2, 0), (0, 1), (1, 1)],
          [(0, 0), (0, 1), (1, 1), (1, 2)]],
    'T': [[(0, 1), (1, 1), (2, 1), (1, 0)],
          [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(1, 0), (0, 1), (1, 1), (2, 1)],
          [(0, 0), (1, 0), (1, 1), (1, 2)]],
    'Z': [[(0, 0), (1, 0), (1, 1), (2, 1)],
          [(2, 0), (1, 1), (2, 1), (1, 2)]],
}

BLOCK_COLORS = {
    'I': '🟦', 'J': '🟪', 'L': '🟧', 'O': '🟨',
    'S': '🟩', 'T': '🟥', 'Z': '⬜', 0: '⚫️'
}

# -------------------- 상태 초기화 --------------------
def initialize_game():
    st.session_state.board = [[0]*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    st.session_state.current_piece = None
    st.session_state.piece_type = None
    st.session_state.piece_rotation = 0
    st.session_state.piece_pos_x = 0
    st.session_state.piece_pos_y = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.last_drop_time = time.time()
    new_piece()

def new_piece():
    if st.session_state.game_over:
        return
    piece_type = random.choice(list(TETROMINOES.keys()))
    st.session_state.piece_type = piece_type
    st.session_state.current_piece = TETROMINOES[piece_type][0]
    st.session_state.piece_rotation = 0
    st.session_state.piece_pos_x = BOARD_WIDTH // 2 - 2
    st.session_state.piece_pos_y = 0
    if check_collision(st.session_state.current_piece, st.session_state.piece_pos_x, st.session_state.piece_pos_y):
        st.session_state.game_over = True

def check_collision(piece, x, y):
    for dx, dy in piece:
        px, py = x + dx, y + dy
        if px < 0 or px >= BOARD_WIDTH or py >= BOARD_HEIGHT:
            return True
        if py >= 0 and st.session_state.board[py][px] != 0:
            return True
    return False

def place_piece():
    for dx, dy in st.session_state.current_piece:
        px, py = st.session_state.piece_pos_x + dx, st.session_state.piece_pos_y + dy
        if 0 <= px < BOARD_WIDTH and 0 <= py < BOARD_HEIGHT:
            st.session_state.board[py][px] = st.session_state.piece_type
    clear_lines()

def clear_lines():
    lines_cleared = 0
    new_board = []
    for row in st.session_state.board:
        if 0 in row:
            new_board.append(row)
        else:
            lines_cleared += 1
    if lines_cleared == 1: st.session_state.score += 100
    elif lines_cleared == 2: st.session_state.score += 300
    elif lines_cleared == 3: st.session_state.score += 500
    elif lines_cleared == 4: st.session_state.score += 800
    for _ in range(lines_cleared):
        new_board.insert(0, [0]*BOARD_WIDTH)
    st.session_state.board = new_board

def move_down():
    next_y = st.session_state.piece_pos_y + 1
    if not check_collision(st.session_state.current_piece, st.session_state.piece_pos_x, next_y):
        st.session_state.piece_pos_y = next_y
    else:
        place_piece()
        new_piece()

def move_sideways(direction):
    next_x = st.session_state.piece_pos_x + direction
    if not check_collision(st.session_state.current_piece, next_x, st.session_state.piece_pos_y):
        st.session_state.piece_pos_x = next_x

def rotate_piece():
    next_rotation = (st.session_state.piece_rotation + 1) % len(TETROMINOES[st.session_state.piece_type])
    next_piece = TETROMINOES[st.session_state.piece_type][next_rotation]
    if not check_collision(next_piece, st.session_state.piece_pos_x, st.session_state.piece_pos_y):
        st.session_state.piece_rotation = next_rotation
        st.session_state.current_piece = next_piece

# -------------------- UI --------------------
st.title("🎮 Streamlit 테트리스")

if 'board' not in st.session_state:
    initialize_game()

st.header(f"점수: {st.session_state.score}")

def draw_board():
    temp_board = [row[:] for row in st.session_state.board]
    for dx, dy in st.session_state.current_piece:
        px, py = st.session_state.piece_pos_x + dx, st.session_state.piece_pos_y + dy
        if 0 <= px < BOARD_WIDTH and 0 <= py < BOARD_HEIGHT:
            temp_board[py][px] = st.session_state.piece_type
    board_str = ""
    for row in temp_board:
        board_str += "".join(BLOCK_COLORS.get(cell, '⚫️') for cell in row) + "\n"
    st.text(board_str)

board_placeholder = st.empty()
with board_placeholder:
    draw_board()

# -------------------- 버튼 조작 --------------------
col1, col2, col3, col4 = st.columns(4)
if col1.button("◀️"): move_sideways(-1)
if col2.button("▶️"): move_sideways(1)
if col3.button("🔽"): move_down()
if col4.button("⟳"): rotate_piece()

# 자동 하강
current_time = time.time()
if current_time - st.session_state.last_drop_time > 0.5:
    move_down()
    st.session_state.last_drop_time = current_time
    st.experimental_rerun()

# -------------------- 게임 오버 --------------------
if st.session_state.game_over:
    st.error("게임 오버! '새 게임' 버튼을 눌러 다시 시작하세요.")

if st.button("새 게임", on_click=initialize_game, use_container_width=True) or not st.session_state.game_started:
    st.session_state.game_started = True
    st.experimental_rerun()
