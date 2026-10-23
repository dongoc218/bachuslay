import streamlit as st
import time

st.set_page_config(page_title="🏠 Bà Chủ Slay: Siêu Trộm", layout="centered", page_icon="🕵️")

# === KHỞI TẠO TRẠNG THÁI ===
if 'game_state' not in st.session_state:
    st.session_state.game_state = "menu"
if 'tx' not in st.session_state: st.session_state.tx = 1
if 'ty' not in st.session_state: st.session_state.ty = 5
if 'collected' not in st.session_state: st.session_state.collected = []
if 'hiding' not in st.session_state: st.session_state.hiding = False
if 'lady_x' not in st.session_state: st.session_state.lady_x = 8
if 'lady_y' not in st.session_state: st.session_state.lady_y = 2
if 'lady_dir' not in st.session_state: st.session_state.lady_dir = -1

GRID_W, GRID_H = 10, 7

# VỊ TRÍ ĐỒ QUÝ
treasures = {
    (2, 1): "💎",
    (5, 0): "👑",
    (7, 3): "💰"
}

# VỊ TRÍ NƠI TRỐN
hides = {
    (3, 3): "🪑",
    (6, 5): "🗄️"
}

def reset_game():
    st.session_state.game_state = "playing"
    st.session_state.tx, st.session_state.ty = 1, 5
    st.session_state.collected = []
    st.session_state.hiding = False
    st.session_state.lady_x, st.session_state.lady_y = 8, 2
    st.session_state.lady_dir = -1

# === GIAO DIỆN ===
st.markdown("""
<style>
    * {font-family: sans-serif;}
    .title-box {
        background: linear-gradient(90deg, #1a1a2e, #16213e);
        border: 3px solid #ffd700;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .title-text {
        color: #ffd700;
        font-size: 26px;
        font-weight: bold;
    }
    .desc-text {
        color: #ccc;
        font-size: 15px;
        margin-top: 5px;
    }
    /* === KHUNG PHÒNG === */
    .room-container {
        background: #16213e;
        border: 4px solid #ffd700;
        border-radius: 12px;
        padding: 15px;
        display: inline-block;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.15);
    }
    .grid-row {
        display: flex;
    }
    .cell {
        width: 58px;
        height: 58px;
        background: #233458;
        border: 1px solid #2a3a5a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        position: relative;
    }
    .cell-wall {
        background: #4a3f35;
        border: 2px solid #2f2720;
    }
    .cell-floor {
        background: #2d4263;
    }
    .cell-exit {
        background: #00b894;
        border: 2px solid #00a085;
    }
    .cell-hide {
        background: #444444;
        border: 2px solid #666666;
    }
    .cell-item {
        background: #3d4f6f;
    }
    /* === THANH TRẠNG THÁI === */
    .status-bar {
        display: flex;
        gap: 12px;
        margin: 15px 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    .status-box {
        background: #16213e;
        border: 2px solid #ffd700;
        border-radius: 8px;
        padding: 8px 15px;
        color: white;
        font-size: 15px;
    }
    /* === NÚT === */
    .btn-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        max-width: 400px;
        margin: 20px auto;
    }
    .stButton>button {
        background: #2d4263;
        color: white;
        border: 2px solid #ffd700;
        border-radius: 8px;
        font-size: 20px;
        padding: 12px;
        width: 100%;
    }
    .stButton>button:hover {
        background: #ffd700;
        color: #1a1a2e;
        font-weight: bold;
    }
    .btn-action>button {
        background: #16213e;
        font-size: 17px;
    }
    .btn-restart>button {
        background: #ffd700;
        color: #1a1a2e;
        font-weight: bold;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# === TIÊU ĐỀ ===
st.markdown("""
<div class='title-box'>
    <div class='title-text'>🕵️ BÀ CHỦ SLAY: SIÊU TRỘM</div>
    <div class='desc-text'>Đột nhập bí thự • Lấy 3 món đồ quý • Trốn bà chủ • Thoát ra ngoài</div>
</div>
""", unsafe_allow_html=True)

# === MENU CHÍNH ===
if st.session_state.game_state == "menu":
    st.info("### 📜 Cách chơi:")
    st.write("🔹 Dùng các nút mũi tên để di chuyển kẻ trộm")
    st.write("🔹 Đi đến 💎 👑 💰 để nhặt đồ quý giá")
    st.write("🔹 Đứng cạnh 🪑 Bàn hoặc 🗄️ Tủ → nhấn *TRỐN* để bà chủ không thấy bạn")
    st.write("🔹 Lấy đủ 3 đồ → chạy ra 🚪 CỬA RA ở góc dưới trái để thắng!")
    st.write("🔹 ⚠️ Gặp bà chủ 👩‍🦱 mà không trốn = BỊ BẮT!")
    
    if st.button("🎮 BẮT ĐẦU CHƠI!", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

# === BỊ BẮT ===
elif st.session_state.game_state == "caught":
    st.markdown("<h2 style='text-align:center;color:#ff6b6b;'>🚨 BỊ PHÁT HIỆN RỒI!</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Bà chủ bắt được bạn rồi! 😱</h3>", unsafe_allow_html=True)
    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset_game()
        st.rerun()

# === THẮNG ===
elif st.session_state.game_state == "won":
    st.markdown("<h2 style='text-align:center;color:#00b894;'>🎉 THÀNH CÔNG!</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Lấy đủ đồ & trốn thoát! 💰</h3>", unsafe_allow_html=True)
    st.balloons()
    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset_game()
        st.rerun()

# === ĐANG CHƠI ===
elif st.session_state.game_state == "playing":
    # === THANH TRẠNG THÁI ===
    items_count = len(st.session_state.collected)
    hiding_status = "🙈 Đang trốn" if st.session_state.hiding else "🕵️ Đang lén lút"
    
    st.markdown(f"""
    <div class='status-bar'>
        <div class='status-box'>💎 Đồ quý: {items_count}/3</div>
        <div class='status-box'>🚨 Báo động: thấp</div>
        <div class='status-box'>{hiding_status}</div>
    </div>
    """, unsafe_allow_html=True)

    # === VẼ PHÒNG ===
    room_html = "<div class='room-container'><div style='display:flex;flex-direction:column;'>"
    
    for y in range(GRID_H):
        room_html += "<div class='grid-row'>"
        for x in range(GRID_W):
            cell_class = "cell cell-floor"
            content = ""
            
            # CỬA RA
            if x == 0 and y == 6:
                cell_class = "cell cell-exit"
                content = "🚪"
            # BÀN & TỦ
            elif (x, y) in hides:
                cell_class = "cell cell-hide"
                content = hides[(x, y)]
            # ĐỒ QUÝ
            elif (x, y) in treasures and (x, y) not in st.session_state.collected:
                cell_class = "cell cell-item"
                content = treasures[(x, y)]
            
            # BÀ CHỦ
            if x == st.session_state.lady_x and y == st.session_state.lady_y:
                content = "👩‍🦱"
            
            # KẺ TRỘM
            if x == st.session_state.tx and y == st.session_state.ty:
                if st.session_state.hiding:
                    content = "🙈"
                else:
                    content = "🥷"
            
            room_html += f"<div class='{cell_class}'>{content}</div>"
        room_html += "</div>"
    room_html += "</div></div>"
    
    st.markdown(room_html, unsafe_allow_html=True)
    
    st.caption("🥷=Bạn | 👩‍🦱=Bà chủ | 💎👑💰=Đồ quý | 🪑=Bàn | 🗄️=Tủ | 🚪=Cửa ra")
    st.divider()

    # === NÚT ĐIỀU KHIỂN ===
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2: up = st.button("⬆️ LÊN")
    with c1: left = st.button("⬅️ TRÁI")
    with c2: hide_btn = st.button("🙈 TRỐN / RA")
    with c3: right = st.button("➡️ PHẢI")
    with c2: down = st.button("⬇️ XUỐNG")

    # === XỬ LÝ DI CHUYỂN ===
    tx, ty = st.session_state.tx, st.session_state.ty
    moved = False

    if up and ty > 0:
        st.session_state.ty -= 1
        st.session_state.hiding = False
        moved = True
    if down and ty < GRID_H - 1:
        st.session_state.ty += 1
        st.session_state.hiding = False
        moved = True
    if left and tx > 0:
        st.session_state.tx -= 1
        st.session_state.hiding = False
        moved = True
    if right and tx < GRID_W - 1:
        st.session_state.tx += 1
        st.session_state.hiding = False
        moved = True

    # Nút trốn
    if hide_btn:
        if (tx, ty) in hides:
            st.session_state.hiding = not st.session_state.hiding
            moved = True

    # Nhặt đồ
    if (tx, ty) in treasures and (tx, ty) not in st.session_state.collected:
        st.session_state.collected.append((tx, ty))
        st.toast(f"✨ Nhặt được {treasures[(tx, ty)]}!")
        moved = True

    # Bà chủ di chuyển
    if moved:
        lx, ly = st.session_state.lady_x, st.session_state.lady_y
        new_lx = lx + st.session_state.lady_dir
        if new_lx <= 0 or new_lx >= GRID_W - 1:
            st.session_state.lady_dir *= -1
        st.session_state.lady_x = lx + st.session_state.lady_dir

    # Kiểm tra thắng/thua
    lx, ly = st.session_state.lady_x, st.session_state.lady_y
    
    # Bị bắt
    if not st.session_state.hiding and abs(tx - lx) <= 1 and abs(ty - ly) <= 1:
        st.session_state.game_state = "caught"
        st.rerun()
    
    # Thắng
    if len(st.session_state.collected) == 3 and tx == 0 and ty == 6:
        st.session_state.game_state = "won"
        st.rerun()

    if moved:
        st.rerun()

