import streamlit as st
import random

st.set_page_config(page_title="BÀ CHỦ SLAY 👑", page_icon="👠")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#ffe0ef,#fff5fb);
}
h1,h2,h3,p {color:#a31565}
.stButton button {
    border-radius:15px;
    min-height:45px;
    font-weight:bold;
    border:2px solid #ff9acb;
}
</style>
""", unsafe_allow_html=True)

N = 5
ITEMS = {(0, 1): "💎", (3, 3): "👜"}
HIDES = {(2, 1): "🪑", (1, 3): "🚪"}
EXIT = (4, 4)

def reset():
    st.session_state.player = (4, 0)
    st.session_state.boss = (0, 4)
    st.session_state.items = set()
    st.session_state.hidden = False
    st.session_state.over = False
    st.session_state.win = False
    st.session_state.msg = "🥷 Hãy lấy 2 món đồ rồi trốn thoát!"

if "player" not in st.session_state:
    reset()

def caught():
    if not st.session_state.hidden and \
       st.session_state.player == st.session_state.boss:
        st.session_state.over = True
        st.session_state.win = False
        st.session_state.msg = "🚨 Bà chủ bắt được tên trộm!"
        return True
    return False

def move(dr, dc):
    if st.session_state.over:
        return

    r, c = st.session_state.player
    p = (r + dr, c + dc)

    if not (0 <= p[0] < N and 0 <= p[1] < N):
        st.session_state.msg = "⛔ Không đi ra ngoài phòng được!"
        return

    st.session_state.player = p
    st.session_state.hidden = False

    if caught():
        return

    if p in ITEMS and p not in st.session_state.items:
        st.session_state.items.add(p)
        st.session_state.msg = "✨ Bạn lấy được " + ITEMS[p] + "!"
    else:
        st.session_state.msg = "🤫 Đi nhẹ thôi, bà chủ đang tuần tra!"

    # Bà chủ đuổi theo tên trộm
    b = st.session_state.boss
    options = [(b[0]+1,b[1]),(b[0]-1,b[1]),
               (b[0],b[1]+1),(b[0],b[1]-1)]
    options = [x for x in options
               if 0 <= x[0] < N and 0 <= x[1] < N]

    if options:
        if random.random() < 0.8:
            options.sort(key=lambda x:
                abs(x[0]-p[0])+abs(x[1]-p[1]))
            st.session_state.boss = options[0]
        else:
            st.session_state.boss = random.choice(options)

    if caught():
        return

    if p == EXIT and len(st.session_state.items) == 2:
        st.session_state.over = True
        st.session_state.win = True
        st.session_state.msg = "🎉 THẮNG RỒI! Bạn đã trốn thoát!"

def hide():
    if st.session_state.over:
        return
    if st.session_state.player in HIDES:
        st.session_state.hidden = True
        st.session_state.msg = "🙈 Bạn đã trốn thành công!"
    else:
        st.session_state.msg = "Hãy đến 🪑 hoặc 🚪 để trốn!"

st.title("👠 BÀ CHỦ SLAY 👑")
st.write("🥷 Trộm 2 món đồ, trốn bà chủ và chạy đến cửa thoát!")

st.info(st.session_state.msg)

a, b = st.columns(2)
a.metric("💎 Đã lấy", f"{len(st.session_state.items)}/2")
b.metric("🫣", "Đang trốn" if st.session_state.hidden else "Đang đi")

st.subheader("🏠 Căn nhà của bà chủ")

for r in range(N):
    cols = st.columns(N)
    for c in range(N):
        p = (r, c)
        if st.session_state.hidden and p == st.session_state.player:
            icon = "🙈"
        elif p == st.session_state.player and p == st.session_state.boss:
            icon = "🚨"
        elif p == st.session_state.player:
            icon = "🥷"
        elif p == st.session_state.boss:
            icon = "👑"
        elif p in ITEMS and p not in st.session_state.items:
            icon = ITEMS[p]
        elif p in HIDES:
            icon = HIDES[p]
        elif p == EXIT:
            icon = "🏃"
        else:
            icon = "⬜"

        cols[c].markdown(
            f"<div style='background:white;border:2px solid #ffadd4;"
            f"border-radius:12px;text-align:center;padding:12px 0;"
            f"font-size:26px'>{icon}</div>",
            unsafe_allow_html=True
        )

st.caption("🥷 Bạn | 👑 Bà chủ | 💎👜 Đồ cần trộm | 🪑🚪 Chỗ trốn | 🏃 Cửa")

st.subheader("🎮 Điều khiển")

_, up, _ = st.columns(3)
if up.button("⬆️ LÊN", use_container_width=True,
             disabled=st.session_state.over):
    move(-1, 0)
    st.rerun()

left, down, right = st.columns(3)

if left.button("⬅️ TRÁI", use_container_width=True,
               disabled=st.session_state.over):
    move(0, -1)
    st.rerun()

if down.button("⬇️ XUỐNG", use_container_width=True,
               disabled=st.session_state.over):
    move(1, 0)
    st.rerun()

if right.button("➡️ PHẢI", use_container_width=True,
                disabled=st.session_state.over):
    move(0, 1)
    st.rerun()

c1, c2 = st.columns(2)

if c1.button("🙈 TRỐN", use_container_width=True,
             disabled=st.session_state.over):
    hide()
    st.rerun()

if c2.button("👀 RA NGOÀI", use_container_width=True,
             disabled=st.session_state.over):
    st.session_state.hidden = False
    st.session_state.msg = "👀 Bạn đã ra khỏi chỗ trốn!"
    caught()
    st.rerun()

if st.session_state.over:
    if st.session_state.win:
        st.balloons()
        st.success(st.session_state.msg)
    else:
        st.error(st.session_state.msg)

    if st.button("🔄 CHƠI LẠI", use_container_width=True):
        reset()
        st.rerun()

