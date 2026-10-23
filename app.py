import streamlit as st
import random

st.set_page_config(page_title="BÀ CHỦ SLAY", page_icon="👠", layout="centered")

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#ffd6ec,#fff4fa)}
h1,h2,h3,p {color:#a31565}
div.stButton > button {
    border-radius:15px; min-height:45px;
    font-weight:bold; border:2px solid #f58cbe;
}
</style>
""", unsafe_allow_html=True)

N = 6
ITEMS = {
    (0, 1): ("💎", "Kim cương"),
    (2, 4): ("👜", "Túi hàng hiệu"),
    (4, 1): ("👑", "Trang sức"),
}
HIDES = {
    (1, 2): ("🪑", "Gầm bàn"),
    (3, 4): ("🚪", "Trong tủ"),
}
EXIT = (5, 5)


def reset():
    st.session_state.player = (5, 0)
    st.session_state.boss = (0, 5)
    st.session_state.stolen = set()
    st.session_state.hidden = False
    st.session_state.over = False
    st.session_state.win = False
    st.session_state.msg = "🥷 Lấy 3 món đồ, tránh bà chủ rồi chạy ra cửa!"
    st.session_state.turn = 0


if "player" not in st.session_state:
    reset()


def check_caught():
    if (not st.session_state.hidden and
            st.session_state.player == st.session_state.boss):
        st.session_state.over = True
        st.session_state.win = False
        st.session_state.msg = (
            "🚨 BÀ CHỦ SLAY BẮT ĐƯỢC BẠN!\n\n"
            "👠 Bà chủ phát hiện tên trộm!\n\n"
            "💥 POW! Cảnh phạt hoạt hình hài hước!"
        )
        return True
    return False


def move_boss():
    boss = st.session_state.boss
    player = st.session_state.player
    choices = [
        (boss[0] + 1, boss[1]),
        (boss[0] - 1, boss[1]),
        (boss[0], boss[1] + 1),
        (boss[0], boss[1] - 1),
    ]
    choices = [p for p in choices if 0 <= p[0] < N and 0 <= p[1] < N]
    if not choices:
        return

    if random.random() < 0.8:
        choices.sort(key=lambda p: abs(p[0] - player[0]) + abs(p[1] - player[1]))
        d = abs(choices[0][0] - player[0]) + abs(choices[0][1] - player[1])
        choices = [p for p in choices
                   if abs(p[0] - player[0]) + abs(p[1] - player[1]) == d]
    st.session_state.boss = random.choice(choices)


def move_player(dr, dc):
    if st.session_state.over:
        return

    r, c = st.session_state.player
    p = (r + dr, c + dc)

    if not (0 <= p[0] < N and 0 <= p[1] < N):
        st.session_state.msg = "⛔ Không thể đi xuyên tường!"
        return

    st.session_state.player = p
    st.session_state.hidden = False
    st.session_state.turn += 1

    if check_caught():
        return

    if p in ITEMS and p not in st.session_state.stolen:
        st.session_state.stolen.add(p)
        st.session_state.msg = f"✨ Đã lấy {ITEMS[p][1]}! Mau tìm món tiếp theo!"

    if p == EXIT:
        if len(st.session_state.stolen) == 3:
            st.session_state.over = True
            st.session_state.win = True
            st.session_state.msg = "🏆 THẮNG RỒI! Bạn lấy đủ 3 món và trốn thoát!"
            return
        else:
            st.session_state.msg = "🔒 Phải lấy đủ 3 món đồ mới thoát được!"

    move_boss()
    check_caught()


def hide():
    if st.session_state.over:
        return
    p = st.session_state.player
    if p in HIDES:
        st.session_state.hidden = True
        st.session_state.msg = f"🙈 Bạn đang trốn ở {HIDES[p][1]}!"
        st.session_state.turn += 1
        move_boss()
    else:
        st.session_state.msg = "Đi đến 🪑 gầm bàn hoặc 🚪 tủ rồi bấm TRỐN nhé!"


def show_board():
    player = st.session_state.player
    boss = st.session_state.boss

    for r in range(N):
        cols = st.columns(N)
        for c in range(N):
            p = (r, c)
            if p == player:
                symbol = "🙈" if st.session_state.hidden else "🥷"
            elif p == boss:
                symbol = "👠"
            elif p in ITEMS and p not in st.session_state.stolen:
                symbol = ITEMS[p][0]
            elif p in HIDES:
                symbol = HIDES[p][0]
            elif p == EXIT:
                symbol = "🏃"
            else:
                symbol = "⬜"

            cols[c].markdown(
                f"<div style='background:white;border:2px solid #f5a1cd;"
                f"border-radius:12px;text-align:center;padding:8px 0;"
                f"font-size:24px'>{symbol}</div>",
                unsafe_allow_html=True
            )


st.title("👠 BÀ CHỦ SLAY 👑")
st.write("🥷 Lấy 3 món đồ, trốn dưới bàn hoặc trong tủ, rồi tìm cửa thoát!")
st.info(st.session_state.msg)

a, b, c = st.columns(3)
a.metric("🎁 Đồ đã lấy", f"{len(st.session_state.stolen)}/3")
b.metric("👣 Lượt đi", st.session_state.turn)
c.metric("🙈 Trạng thái", "Đang trốn" if st.session_state.hidden else "Đang đi")

st.subheader("🏠 BẢN ĐỒ CĂN NHÀ")
show_board()
st.caption("🥷 Bạn | 👠 Bà chủ | 💎 Kim cương | 👜 Túi hiệu | 👑 Trang sức | 🪑 Gầm bàn | 🚪 Tủ | 🏃 Cửa")

st.subheader("🎮 Điều khiển")
st.caption("Mỗi lần bấm sẽ đi một ô.")

_, up, _ = st.columns(3)
if up.button("⬆️ LÊN", use_container_width=True, disabled=st.session_state.over):
    move_player(-1, 0)
    st.rerun()

left, down, right = st.columns(3)
if left.button("⬅️ TRÁI", use_container_width=True, disabled=st.session_state.over):
    move_player(0, -1)
    st.rerun()
if down.button("⬇️ XUỐNG", use_container_width=True, disabled=st.session_state.over):
    move_player(1, 0)
    st.rerun()
if right.button("➡️ PHẢI", use_container_width=True, disabled=st.session_state.over):
    move_player(0, 1)
    st.rerun()

h1, h2 = st.columns(2)
if h1.button("🙈 TRỐN", use_container_width=True, disabled=st.session_state.over):
    hide()
    st.rerun()
if h2.button("👀 RA NGOÀI", use_container_width=True, disabled=st.session_state.over):
    st.session_state.hidden = False
    st.session_state.msg = "👀 Bạn đã ra khỏi chỗ trốn!"
    check_caught()
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

st.markdown("---")
st.caption("💅 BÀ CHỦ SLAY — Liệu bạn có trốn thoát được không?")
