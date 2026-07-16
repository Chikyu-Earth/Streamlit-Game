import streamlit as st
import time
import random

# ==========================================
# 1. PAGE CONFIGURATION & CSS
# ==========================================
st.set_page_config(
    page_title="Number Ascend",
    page_icon="🔢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly tiles and text
st.markdown("""
    <style>
    /* Style the Streamlit buttons to look like large square tiles */
    div.stButton > button {
        height: 100px;
        font-size: 32px !important;
        font-weight: bold;
        width: 100%;
        border-radius: 10px;
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #888888;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:active {
        transform: scale(0.95);
    }
    .main-title { text-align: center; margin-bottom: 5px; }
    .message-text { text-align: center; font-size: 18px; font-weight: bold; height: 30px; }
    .timer-text { text-align: center; color: #ff5555; font-size: 24px; font-weight: bold; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE INITIALIZATION (GAME ENGINE)
# ==========================================
def init_level(level):
    """Sets up a new level, shuffles the board, and resets the timer."""
    st.session_state.current_level = level
    st.session_state.expected_num = 1
    
    # Generate and shuffle tiles
    num_tiles = level + 2
    board = list(range(1, num_tiles + 1))
    random.shuffle(board)
    st.session_state.board = board
    
    # Record the exact moment the level started
    st.session_state.start_time = time.time()
    st.session_state.status_msg = f"Level {level}: Tap numbers in order"

# Run this only once when the app first loads
if 'current_level' not in st.session_state:
    st.session_state.max_level = 10
    st.session_state.game_over = False
    init_level(1)

# ==========================================
# 3. GAME LOGIC CALLBACKS
# ==========================================
def handle_click(clicked_num):
    """Processes the user's tap, checking the time and the number."""
    if st.session_state.game_over:
        return
        
    # Check if 5 seconds have passed since the level started
    elapsed_time = time.time() - st.session_state.start_time
    if elapsed_time > 5.0:
        st.session_state.status_msg = f"⏰ Time's up! Restarting Level {st.session_state.current_level}..."
        init_level(st.session_state.current_level)
        return

    # Check if they tapped the correct number
    if clicked_num == st.session_state.expected_num:
        st.session_state.expected_num += 1
        
        # Check if the level is complete
        if st.session_state.expected_num > st.session_state.current_level + 2:
            if st.session_state.current_level == st.session_state.max_level:
                st.session_state.status_msg = "🏆 Game Over - You Win!"
                st.session_state.game_over = True
            else:
                # Setup the next level
                init_level(st.session_state.current_level + 1)
    else:
        # Wrong tap!
        st.session_state.status_msg = f"❌ Wrong! Tap {st.session_state.expected_num} first."
        init_level(st.session_state.current_level)

def restart_game():
    st.session_state.game_over = False
    init_level(1)

# ==========================================
# 4. USER INTERFACE (FRONTEND)
# ==========================================
st.markdown("<h1 class='main-title'>Number Ascend</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='message-text'>{st.session_state.status_msg}</div>", unsafe_allow_html=True)

if not st.session_state.game_over:
    # Calculate time left for the UI (this shows the time at the exact moment of the last tap)
    elapsed = time.time() - st.session_state.start_time
    time_left = max(0, 5 - int(elapsed))
    st.markdown(f"<div class='timer-text'>⏳ ~{time_left}s</div>", unsafe_allow_html=True)
    
    # Render the 3-column grid
    cols = st.columns(3)
    
    for i, num in enumerate(st.session_state.board):
        # Determine which column this tile belongs in
        col_idx = i % 3 
        
        with cols[col_idx]:
            if num < st.session_state.expected_num:
                # The user already clicked this correctly. 
                # We inject an empty space of the exact same height so the grid doesn't collapse.
                st.markdown("<div style='height:100px; margin-bottom:15px;'></div>", unsafe_allow_html=True)
            else:
                # We pass the 'num' into the callback function using 'args'
                st.button(
                    str(num), 
                    key=f"btn_{num}_{st.session_state.current_level}", 
                    on_click=handle_click, 
                    args=(num,), 
                    use_container_width=True
                )
else:
    st.button("Play Again", on_click=restart_game, use_container_width=True)
