import streamlit as st

st.set_page_config(page_title="🕵️ Kẻ Trộm & Bà Chủ Mập", layout="wide")

# === KHỞI TẠO ===
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

# === LINK ẢNH ONLINE (KHÔNG CẦN TẢI GÌ HẾT!) ===
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

def img(url, size=45):
    return f"<img src='{url}' width='{size}' height='{size}'>"

treasures = {(2,1):"diamond", (5,0):"crown", (8,3):"coin", (3,5):"vase"}
hides = {(4,3):"table", (7,5):"cabinet"}

def reset():
    st.session_state.game_state = "playing"
    st.session_state.tx, st.session_state.ty = 0, 6
    st.session_state.collected = []
    st.session_state.hiding = False
    st.session_state.lx, st.session_state.ly = 8,...


