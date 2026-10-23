import streamlit as st
import time

st.set_page_config(page_title="🕵️ Kẻ Trộm & Bà Chủ Mập", layout="wide", page_icon="🕵️")

# === KHỞI TẠO GAME ===
if 'game_state' not in st.session_state:
    st.session_state.game_state = "menu"
if 'tx' not in st.session_state: st.session_state.tx = 0
if 'ty' not in st.session_state: st.session_state.ty = 6
if 'collected' not in st.session_state: st.session_state.collected = []
if 'hiding' not in st.session_state: st.session_state.hiding = False
if 'lx' not in st.session_state: st.session_state.lx = 8
if 'ly' not in st.session_state: st.session_state.ly = 1
if 'ldir' not in st.session_state: st.session_state.ldir = -1

GRID_W, GRID_H = 10, 7

# VỊ TRÍ ĐỒ QUÝ
treasures = {
    (2, 1): ("💎", "Kim cương"),
    (5, 0): ("👑", "Vương miện"),
    (8, 3): ("💰", "Tiền vàng"),
    (3, 5): ("🏺", "Bình cổ")
}

# VỊ TRÍ NƠI TRỐN
hides = {
    (4, 3): ("🪑", "Bàn"),
    (7, 5): ("🗄️", "Tủ")
}

def reset():
    st.session_state.game_state = "playing"
    st.session_state.tx, st.session_state.ty = 0, 6
    st.session_state.collected = []
    st.session_state.hiding = False
    st.session_state.lx, st.session_state.ly = 8, 1
    st.session_state.ldir = -1

# === GIAO DIỆN ===
st.markdown("""
<style>
    .main-title { text-align: center; font-size: 36px; font-weight: bold; color: #8B4513; margin-bottom: 20px; }
    .game-cell { 
        width: 65px; height: 65px; 
        background: linear-gradient(145deg, #e8d4b9, #d4b996);
        border: 1px solid #b8966c;
        display: flex; align-items: center; justify-content: center;
        font-size: 28px;
        transition: all 0.15s;
    }
    .door-cell { background: linear-gradient(145deg, #90EE90, #7CCD7C); border: 2px solid #2E7D32; }
    .hide-cell { background: linear-gradient(145deg, #DEB887, #D2B48C); border: 2px solid #8B4513; }
    .item-cell { background: linear-gradient(145deg, #FFF8DC, #F5F5DC); }
    .row { display: flex; gap: 0; }
    .grid { display: flex; flex-direction: column; align-items: center; margin: 20px auto; }
    .stButton>button { font-size: 22px; padding: 8px 16px; border-radius: 8px; background: #ff9800; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background: #e65100; }
    .status-box { padding: 10px; border-radius: 8px; font-size: 16px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🕵️ KẺ TRỘM & BÀ CHỦ MẬP 👩‍🦱</div>", unsafe_allow_html=True)

# === MENU CHÍNH ===
if st.session_state.game_state == "menu":
    st.info("### 📜 Hướng dẫn chơi")
    st.markdown("""
    - 🕵️ *Bạn là kẻ trộm* — di chuyển khắp nhà để lấy 4 vật phẩm quý giá
    - 👩‍🦱 *Bà chủ tóc xoăn mập mạp* đang đi tuần tra trong nhà
    - 🪑*Bàn** và 🗄️ *Tủ* = nơi trốn! Đứng ở đó rồi nhấn nút*🙈 ẨN** để bà chủ không thấy
    - 🚪 Lấy đủ tất cả đồ rồi chạy ra *Cửa ra* ở góc dưới bên trái để thắng!
    - ⚠️ *Cảnh báo:* Gặp bà chủ mà không ẩn = *BỊ BẮT! Kết thúc game!*
    """)
    if st.button("🎮 BẮT ĐẦU CHƠI!", type="primary", use_container_width=True):
        reset()
        st.rerun()

# === BỊ BẮT ===
elif st.session_state.game_state == "caught":
    st.markdown("<h2 style='text-align:center;color:red;'>🚨 BỊ PHÁT HIỆN RỒI!</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Bà chủ bắt được bạn rồi! 😱</h3>", unsafe_allow_html=True)
    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset()
        st.rerun()

# === THẮNG ===
elif st.session_state.game_state == "won":
    st.markdown("<h2 style='text-align:center;color:green;'>🎉 CHIẾN THẮNG!</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Bạn đã lấy hết đồ và trốn thoát an toàn! 💰</h3>", unsafe_allow_html=True)
    st.balloons()
    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset()
        st.rerun()

# === ĐANG CHƠI ===
elif st.session_state.game_state == "playing":
    # Thanh trạng thái
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.info(f"📦 Đã lấy: *{len(st.session_state.collected)}/4* vật phẩm")
    with col2:
        if st.session_state.hiding:
            st.success("🙈 *Đang ẩn* — An toàn!")
        else:
            st.warning("🕵️ *Đang di chuyển* — Cẩn thận!")
    with col3:
        st.info("👩‍🦱 Bà chủ đang tuần tra...")

    st.divider()

    # === VẼ BẢN ĐỒ ===
    grid_html = "<div class='grid'>"
    for y in range(GRID_H):
        grid_html += "<div class='row'>"
        for x in range(GRID_W):
            cls = "game-cell"
            content = ""
            
            # CỬA RA
            if x == 0 and y == 6:
                cls += " door-cell"
                content = "🚪"
            
            # NƠI TRỐN
            elif (x, y) in hides:
                cls += " hide-cell"
                content = hides[(x, y)][0]
            
            # ĐỒ QUÝ
            elif (x, y) in treasures and (x, y) not in st.session_state.collected:
                cls += " item-cell"
                content = treasures[(x, y)][0]
            
            # BÀ CHỦ
            if x == st.session_state.lx and y == st.session_state.ly:
                content = "👩‍🦱"
            
            # KẺ TRỘM
            if x == st.session_state.tx and y == st.session_state.ty:
                if st.session_state.hiding:
                    content = "🙈"
                else:
                    content = "🕵️"
            
            grid_html += f"<div class='{cls}'>{content}</div>"
        grid_html += "</div>"
    grid_html += "</div>"
    
    st.markdown(grid_html, unsafe_allow_html=True)
    st.caption("🕵️=Bạn | 👩‍🦱=Bà chủ | 💎👑💰🏺=Đồ quý | 🪑=Bàn | 🗄️=Tủ | 🚪=Cửa ra")
    st.divider()

    # === NÚT ĐIỀU KHIỂN ===
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2: up = st.button("⬆️ LÊN")
    with c1: left = st.button("⬅️ TRÁI")
    with c2: hide_btn = st.button("🙈 ẨN / HIỆN")
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

    # Nút ẩn/hiện
    if hide_btn:
        if (tx, ty) in hides:
            st.session_state.hiding = not st.session_state.hiding
            moved = True

    # Nhặt đồ
    if (tx, ty) in treasures and (tx, ty) not in st.session_state.collected:
        st.session_state.collected.append((tx, ty))
        st.toast(f"✨ Nhặt được: {treasures[(tx, ty)][1]}!")
        moved = True

    # Bà chủ di chuyển
    if moved:
        lx, ly = st.session_state.lx, st.session_state.ly
        new_lx = lx + st.session_state.ldir
        if new_lx <= 0 or new_lx >= GRID_W - 1:
            st.session_state.ldir *= -1
        st.session_state.lx = lx + st.session_state.ldir

    # Kiểm tra thắng/thua
    lx, ly = st.session_state.lx, st.session_state.ly
    
    # Bị bắt
    if not st.session_state.hiding and abs(tx - lx) <= 1 and abs(ty - ly) <= 1:
        st.session_state.game_state = "caught"
        st.rerun()
    
    # Thắng
    if len(st.session_state.collected) == 4 and tx == 0 and ty == 6:
        st.session_state.game_state = "won"
        st.rerun()

    if moved:
        st.rerun()
