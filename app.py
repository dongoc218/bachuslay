import streamlit as st
import time
import random
from PIL import Image
import io

st.set_page_config(page_title="Kẻ Trộm & Bà Chủ Mập", page_icon="🕵️")

# === Khởi tạo trạng thái game ===
if 'game_state' not in st.session_state:
    st.session_state.game_state = "menu"  # menu, playing, won, caught
if 'thief_x' not in st.session_state:
    st.session_state.thief_x = 1
if 'thief_y' not in st.session_state:
    st.session_state.thief_y = 5
if 'collected' not in st.session_state:
    st.session_state.collected = []
if 'hiding' not in st.session_state:
    st.session_state.hiding = False
if 'treasures' not in st.session_state:
    st.session_state.treasures = {
        (2, 2): "💎",
        (5, 1): "👑",
        (7, 4): "💰",
        (3, 6): "🏺",
    }
if 'hiding_spots' not in st.session_state:
    st.session_state.hiding_spots = [(4, 3), (6, 6)]  # Bàn và Tủ
if 'lady_pos' not in st.session_state:
    st.session_state.lady_pos = (8, 2)
if 'lady_dir' not in st.session_state:
    st.session_state.lady_dir = -1

# === Bảng vẽ game ===
GRID_W, GRID_H = 10, 8
CELL = 55

def reset_game():
    st.session_state.game_state = "playing"
    st.session_state.thief_x = 1
    st.session_state.thief_y = 5
    st.session_state.collected = []
    st.session_state.hiding = False
    st.session_state.treasures = {(2,2):"💎",(5,1):"👑",(7,4):"💰",(3,6):"🏺"}
    st.session_state.lady_pos = (8, 2)
    st.session_state.lady_dir = -1

def draw_map():
    grid = []
    for y in range(GRID_H):
        row = []
        for x in range(GRID_W):
            cell = "⬜"
            # Vị trí ẩn
            if (x, y) in st.session_state.hiding_spots:
                if (x, y) == (4, 3):
                    cell = "🪑"  # Bàn
                else:
                    cell = "🗄️"  # Tủ
            # Đồ quý
            if (x, y) in st.session_state.treasures:
                cell = st.session_state.treasures[(x, y)]
            # Bà chủ
            if (x, y) == st.session_state.lady_pos:
                cell = "👩‍🦱"
            # Kẻ trộm
            if x == st.session_state.thief_x and y == st.session_state.thief_y:
                if st.session_state.hiding:
                    cell = "🙈"
                else:
                    cell = "🕵️"
            row.append(cell)
        grid.append(" ".join(row))
    return "\n".join(grid)

def move_lady():
    if st.session_state.game_state != "playing":
        return
    lx, ly = st.session_state.lady_pos
    new_x = lx + st.session_state.lady_dir
    if new_x <= 0 or new_x >= GRID_W-1:
        st.session_state.lady_dir *= -1
    st.session_state.lady_pos = (lx + st.session_state.lady_dir, ly)

def check_game():
    tx, ty = st.session_state.thief_x, st.session_state.thief_y
    lx, ly = st.session_state.lady_pos
    
    # Bị phát hiện nếu không ẩn và ở gần bà chủ
    if not st.session_state.hiding and abs(tx - lx) <= 1 and abs(ty - ly) <= 1:
        st.session_state.game_state = "caught"
    
    # Thu thập đủ đồ và trốn thành công
    if len(st.session_state.collected) == 4 and tx == 1 and ty == 7:
        st.session_state.game_state = "won"

# === Giao diện chính ===
st.title("🕵️ Kẻ Trộm & Bà Chủ Mập")

if st.session_state.game_state == "menu":
    st.subheader("🎯 Mục tiêu:")
    st.write("- Thu thập tất cả đồ vật quý giá 💎👑💰🏺")
    st.write("- Ẩn mình tại 🪑 Bàn hoặc 🗄️ Tủ khi bà chủ đi qua")
    st.write("- Sau khi lấy hết đồ, chạy ra cửa ra vào ở góc dưới bên trái để thắng!")
    st.write("- ❌ Bị bà chủ 👩‍🦱 phát hiện = THUA")
    if st.button("🎮 Bắt đầu chơi!", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

elif st.session_state.game_state == "caught":
    st.error("🚨 BỊ PHÁT HIỆN RỒI! Bị bắt rồi 😱")
    if st.button("🔄 Chơi lại", use_container_width=True):
        reset_game()
        st.rerun()

elif st.session_state.game_state == "won":
    st.success("🎉 CHIẾN THẮNG! Bạn đã trốn thoát với tất cả đồ quý!")
    st.balloons()
    if st.button("🔄 Chơi lại", use_container_width=True):
        reset_game()
        st.rerun()

elif st.session_state.game_state == "playing":
    # Thông tin
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Đã lấy: {len(st.session_state.collected)}/4 vật phẩm")
    with col2:
        if st.session_state.hiding:
            st.success("🙈 Đang ẩn... an toàn!")
        else:
            st.warning("🕵️ Đang di chuyển - Cẩn thận!")
    
    # Bản đồ game
    st.text(draw_map())
    st.caption("🕵️=Bạn | 👩‍🦱=Bà chủ | 💎👑💰🏺=Đồ quý | 🪑=Bàn | 🗄️=Tủ | ⬅️ góc dưới trái = Cửa ra")
    
    # Nút điều khiển
    c1, c2, c3 = st.columns(3)
    with c2:
        up = st.button("⬆️", use_container_width=True)
    with c1:
        left = st.button("⬅️", use_container_width=True)
    with c2:
        hide = st.button("🙈 Ẩn/Hiện", use_container_width=True)
    with c3:
        right = st.button("➡️", use_container_width=True)
    with c2:
        down = st.button("⬇️", use_container_width=True)
    
    # Xử lý di chuyển
    tx, ty = st.session_state.thief_x, st.session_state.thief_y
    moved = False
    
    if up and ty > 0:
        st.session_state.thief_y -= 1
        st.session_state.hiding = False
        moved = True
    if down and ty < GRID_H-1:
        st.session_state.thief_y += 1
        st.session_state.hiding = False
        moved = True
    if left and tx > 0:
        st.session_state.thief_x -= 1
        st.session_state.hiding = False
        moved = True
    if right and tx < GRID_W-1:
        st.session_state.thief_x += 1
        st.session_state.hiding = False
        moved = True
    
    if hide:
        if (tx, ty) in st.session_state.hiding_spots:
            st.session_state.hiding = not st.session_state.hiding
    
    # Thu thập đồ
    if (tx, ty) in st.session_state.treasures and (tx, ty) not in st.session_state.collected:
        st.session_state.collected.append((tx, ty))
        st.rerun()
    
    # Di chuyển bà chủ
    if moved:
        move_lady()
    
    # Kiểm tra kết thúc
    check_game()
    
    if moved or hide:
        st.rerun()
