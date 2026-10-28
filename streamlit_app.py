import streamlit as st
st.set_page_config(page_title="Virtual Microscope")
st.title("Virtual Microscope")
zoom = st.slider("Zoom Level", 1, 20, 10)
focus = st.slider("Focus", 1, 10, 5)
st.info(f"Viewing at {zoom}X Zoom - Focus {focus}/10")
if st.button("Light ON/OFF"):
    st.balloons()
    st.success("Light Changed!")
