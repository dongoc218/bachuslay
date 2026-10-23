import streamlit as st

st.set_page_config(page_title="🕵️ Kẻ Trộm & Bà Chủ Mập", layout="wide")

# === KHỞI TẠO DỮ LIỆU ===
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

# === HÌNH ẢNH THẬT — KHÔNG CẦN TẢI GÌ HẾT ===
IMG = {
    "thief": "https://cdn-icons-png.flaticon.com/128/1004/1004267.png",
    "lady": "https://cdn-icons-png.flaticon.com/128/11402/11402706.png",
    "door": "https://cdn-icons-png.flaticon.com/128/612/612818.png",
    "table": "https://cdn-icons-png.flaticon.com/128/2976/2976516.png",
    "cabinet": "https://cdn-icons-png.flaticon.com/128/2759/2759796.png",
    "diamond": "https://cdn-icons-png.flaticon.com/128/1541/1541476.png",
    "crown": "https://cdn-icons-png.flaticon.com/128/1160/1160590.png",
    "coin": "https://cdn-icons-png.flaticon.com/128/1028/1028354.png",
    "vase": "https://cdn-icons-png.flaticon.com/128/2755/2755096.png",
}

def img(key, size=45):
    return f"<img src='{IMG[key]}' width='{size}' height='{size}'>"

treasures = {(2,1):"diamond", (5,0):"crown", (8,3):"coin", (3,5):"vase"}
hides = {(4,3):"table", (7,5):"cabinet"}

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
.cell{width:65px;height:65px;background:#e8d4b9;border:1px solid #b8966c;display:flex;align-items:center;justify-content:center;}
.door{background:#90EE90;border:2px solid #2E7D32;}
.hide{background:#DEB887;border:2px solid #8B4513;}
.item{background:#FFF8DC;}
.row{display:flex;gap:0;}
.grid{display:flex;flex-direction:column;align-items:center;margin:20px 0;}
button{font-size:24px !important;padding:10px !important;}
</style>
""", unsafe_allow_html=True)

st.title("🕵️ Kẻ Trộm & Bà Chủ Mập")

# === MENU ===
if st.session_state.game_state == "menu":
    st.subheader("📜 Cách chơi:")
    st.write("1. Di chuyển kẻ trộm để lấy 4 đồ vật quý giá 💎👑💰🏺")
    st.write("2. Đi đến Bàn 🪑 hoặc Tủ 🗄️ rồi nhấn Nút Ẩn để bà chủ không thấy")
    st.write("3. Lấy đủ 4 đồ → chạy ra Cửa 🚪 ở góc dưới bên trái để thắng")
    st.write("❌ Gặp bà chủ mà không ẩn = BỊ BẮT!")
    if st.button("🎮 BẮT ĐẦU CHƠI!", type="primary", use_container_width=True):
        reset()
        st.rerun()

# === BỊ BẮT ===
elif st.session_state.game_state == "caught":
    st.error("## 🚨 BỊ PHÁT HIỆN RỒI! BỊ BẮT! 😱")
    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset()
        st.rerun()

# === THẮNG ===
elif st.session_state.game_state == "won":
    st.success("## 🎉 CHIẾN THẮNG! Trốn thoát thành công! 🎉")
    st.balloons()
    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset()
        st.rerun()

# === ĐANG CHƠI ===
elif st.session_state.game_state == "playing":
    col1, col2, col3 = st.columns([2,2,2])
    with col1: st.info(f"📦 Đã lấy: {len(st.session_state.collected)}/4")
    with col2:
        if st.session_state.hiding: st.success("🙈 Đang ẩn — An toàn!")
        else: st.warning("🕵️ Đang di chuyển")
    with col3: st.write("👩‍🦱 Bà chủ đang đi...")

    # VẼ BẢN ĐỒ
    grid_html = "<div class='grid'>"
    for y in range(GRID_H):
        grid_html += "<div class='row'>"
        for x in range(GRID_W):
            cls = "cell"
            content = ""
            if x==0 and y==6:
                cls += " door"
                content = img("door")
            elif (x,y) in hides:
                cls += " hide"
                content = img(hides[(x,y)])
            elif (x,y) in treasures and (x,y) not in st.session_state.collected:
                cls += " item"
                content = img(treasures[(x,y)])
            if x==st.session_state.lx and y==st.session_state.ly:
                content = img("lady")
            if x==st.session_state.tx and y==st.session_state.ty:
                if st.session_state.hiding: content = "🙈"
                else: content = img("thief")
            grid_html += f"<div class='{cls}'>{content}</div>"
        grid_html += "</div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

    # NÚT ĐIỀU KHIỂN
    c1,c2,c3 = st.columns([1,1,1])
    with c2: up = st.button("⬆️ LÊN")
    with c1: left = st.button("⬅️ TRÁI")
    with c2: hide_btn = st.button("🙈 ẨN/HIỆN")
    with c3: right = st.button("➡️ PHẢI")
    with c2: down = st.button("⬇️ XUỐNG")

    # XỬ LÝ DI CHUYỂN
    tx, ty = st.session_state.tx, st.session_state.ty
    moved = False
    if up and ty>0: st.session_state.ty-=1; st.session_state.hiding=False; moved=True
    if down and ty<GRID_H-1: st.session_state.ty+=1; st.session_state.hiding=False; moved=True
    if left and tx>0: st.session_state.tx-=1; st.session_state.hiding=False; moved=True
    if right and tx<GRID_W-1: st.session_state.tx+=1; st.session_state.hiding=False; moved=True
    if hide_btn and (tx,ty) in hides: st.session_state.hiding=not st.session_state.hiding; moved=True

    # NHẬT ĐỒ
    if (tx,ty) in treasures and (tx,ty) not in st.session_state.collected:
        st.session_state.collected.append((tx,ty)); moved=True

    # BÀ CHỦ DI CHUYỂN
    if moved:
        lx, ly = st.session_state.lx, st.session_state.ly
        new_lx = lx + st.session_state.ldir
        if new_lx<=0 or new_lx>=GRID_W-1: st.session_state.ldir *= -1
        st.session_state.lx = lx + st.session_state.ldir

    # KIỂM TRA THẮNG/THUA
    lx, ly = st.session_state.lx, st.session_state.ly
    if not st.session_state.hiding and abs(tx-lx)<=1 and abs(ty-ly)<=1:
        st.session_state.game_state = "caught"; st.rerun()
    if len(st.session_state.collected)==4 and tx==0 and ty==6:
        st.session_state.game_state = "won"; st.rerun()
    if moved: st.rerun()

