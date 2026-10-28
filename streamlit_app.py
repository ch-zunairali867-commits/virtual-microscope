import streamlit as st
st.set_page_config(page_title="Virtual Microscope", layout="wide")
st.title("🔬 Virtual Microscope - By Zunair Ahmad")
st.write("10th Class Science Project")
zoom = st.slider("Zoom Level", 1, 20, 10)
focus = st.slider("Focus", 1, 10, 5)
st.info(f"Viewing at {zoom}X Zoom - Focus {focus}/10")
st.image("https://upload.wikimedia.org/wikipedia/commons/5/5c/Onion_epidermal_cells.jpg", caption="Onion Cell Under Microscope")
if st.button("Light ON/OFF"):
    st.balloons()
    st.success("Light Changed!")
