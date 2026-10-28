import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
from PIL import Image, ImageFilter, ImageEnhance

st.set_page_config(
    page_title="Virtual Microscope",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Virtual Microscope")
st.subheader("Basic Microscopy for Cell Observation")
st.write("Explore different cell types, adjust magnification, and record your observations.")

# Specimen selection
specimens = {
    "Plant Leaf (Elodea)": "Observe rectangular plant cells and green chloroplasts.",
    "Onion Epidermis": "Observe brick-like plant cells and stained nuclei.",
    "Cheek Cells": "Observe irregular animal cells and their nuclei.",
    "Yeast Cells": "Observe small rounded fungal cells and budding.",
    "Human Blood": "Observe red blood cells and occasional white blood cells."
}

# Microscope controls
st.sidebar.header("Microscope Controls")

specimen = st.sidebar.selectbox(
    "Choose your specimen",
    list(specimens.keys())
)

objective = st.sidebar.select_slider(
    "Objective lens",
    options=[4, 10, 40],
    value=10,
    format_func=lambda x: f"{x}×"
)

eyepiece = 10
total_magnification = objective * eyepiece

light = st.sidebar.slider(
    "Light intensity",
    min_value=10,
    max_value=100,
    value=60
)

focus = st.sidebar.slider(
    "Focus",
    min_value=0,
    max_value=100,
    value=85
)

st.sidebar.metric(
    "Total magnification",
    f"{total_magnification}×"
)

# Draw illustrative specimen
def draw_cells(name, magnification):
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#fafafa")
    ax.set_aspect("equal")
    ax.axis("off")

    rng = np.random.default_rng(42)

    if name in ["Plant Leaf (Elodea)", "Onion Epidermis"]:
        plant = name == "Plant Leaf (Elodea)"
        fill = "#d7edc4" if plant else "#f1dff5"
        edge = "#49804c" if plant else "#9b6bb0"

        for x in np.arange(-5, 5, 2):
            for y in np.arange(-5, 5, 1.4):
                ax.add_patch(Rectangle(
                    (x, y), 1.9, 1.3,
                    facecolor=fill,
                    edgecolor=edge,
                    linewidth=1.5
                ))

                if plant:
                    for _ in range(5):
                        cx = x + rng.uniform(0.2, 1.7)
                        cy = y + rng.uniform(0.15, 1.15)
                        ax.add_patch(Ellipse(
                            (cx, cy), 0.18, 0.28,
                            facecolor="#299447",
                            edgecolor="#1d7134"
                        ))
                else:
                    ax.add_patch(Circle(
                        (x + 0.95, y + 0.65), 0.14,
                        facecolor="#753c91",
                        edgecolor="#51286b"
                    ))

    elif name == "Cheek Cells":
        for _ in range(25):
            x, y = rng.uniform(-4.5, 4.5, 2)
            w, h = rng.uniform(0.7, 1.3), rng.uniform(0.6, 1.1)

            ax.add_patch(Ellipse(
                (x, y), w, h,
                facecolor="#f4c8d8",
                edgecolor="#b86b91",
                linewidth=1.5
            ))

            ax.add_patch(Circle(
                (x, y), 0.14,
                facecolor="#713d8c",
                edgecolor="#51276b"
            ))

    elif name == "Yeast Cells":
        for _ in range(45):
            x, y = rng.uniform(-4.5, 4.5, 2)
            r = rng.uniform(0.18, 0.35)

            ax.add_patch(Circle(
                (x, y), r,
                facecolor="#e1c8f3",
                edgecolor="#8259a0",
                linewidth=1.2
            ))

            if rng.random() > 0.65:
                ax.add_patch(Circle(
                    (x + r * 0.85, y + r * 0.7),
                    r * 0.4,
                    facecolor="#e1c8f3",
                    edgecolor="#8259a0"
                ))

    else:
        # Illustrative blood smear
        for _ in range(65):
            x, y = rng.uniform(-4.7, 4.7, 2)
            r = rng.uniform(0.25, 0.38)

            ax.add_patch(Circle(
                (x, y), r,
                facecolor="#e99a9a",
                edgecolor="#ae505b",
                linewidth=1
            ))

            ax.add_patch(Circle(
                (x, y), r * 0.45,
                facecolor="#f6c9c1",
                edgecolor="none"
            ))

        for x, y in [(-1.2, 1.3), (2.4, -2.1)]:
            ax.add_patch(Circle(
                (x, y), 0.45,
                facecolor="#eee2f7",
                edgecolor="#86629d",
                linewidth=1.5
            ))
            ax.add_patch(Circle(
                (x, y), 0.2,
                facecolor="#76508e",
                edgecolor="none"
            ))

    # Higher magnification shows a smaller field of view
    width = 10 * 40 / magnification
    ax.set_xlim(-width / 2, width / 2)
    ax.set_ylim(-width / 2, width / 2)

    fig.tight_layout(pad=0)
    fig.canvas.draw()

    pixels = np.asarray(fig.canvas.buffer_rgba())[..., :3]
    image = Image.fromarray(pixels)
    plt.close(fig)

    # Adjust brightness and focus
    image = ImageEnhance.Brightness(image).enhance(light / 60)

    if focus < 50:
        image = image.filter(
            ImageFilter.GaussianBlur(
                radius=(50 - focus) / 12
            )
        )

    return image


# Display microscope view
left, right = st.columns([2, 1])

with left:
    st.subheader("Microscope View")

    image = draw_cells(specimen, objective)
    st.image(image, use_container_width=True)

    st.caption(
        f"{specimen} | Objective: {objective}× | "
        f"Total magnification: {total_magnification}×"
    )

with right:
    st.subheader("Observation Guide")
    st.write(specimens[specimen])

    if specimen == "Plant Leaf (Elodea)":
        st.markdown("""
        **Identify:**
        - Cell wall
        - Green chloroplasts
        - Cytoplasm

        **Think:** What is the role of chloroplasts?
        """)

    elif specimen == "Onion Epidermis":
        st.markdown("""
        **Identify:**
        - Cell wall
        - Cytoplasm
        - Stained nucleus

        **Think:** Why is staining useful?
        """)

    elif specimen == "Cheek Cells":
        st.markdown("""
        **Identify:**
        - Cell membrane
        - Cytoplasm
        - Nucleus

        **Think:** How do animal cells differ from plant cells?
        """)

    elif specimen == "Yeast Cells":
        st.markdown("""
        **Identify:**
        - Rounded cells
        - Cell wall
        - Budding cells

        **Think:** How does yeast reproduce?
        """)

    else:
        st.markdown("""
        **Identify:**
        - Red blood cells
        - White blood cells

        **Think:** Which cells transport oxygen?
        """)

st.divider()

# Student observation record
st.header("Student Observation Record")

col1, col2 = st.columns(2)

with col1:
    structures = st.text_input(
        "Structures observed"
    )

    shape = st.selectbox(
        "Cell shape",
        [
            "Select cell shape",
            "Rectangular",
            "Irregular",
            "Round or oval",
            "Mixed shapes"
        ]
    )

with col2:
    clearest = st.selectbox(
        "Clearest objective",
        ["4×", "10×", "40×"]
    )

    notes = st.text_area(
        "Your observations"
    )

if st.button("Submit Observation"):
    if not structures.strip():
        st.warning("Please enter the structures you observed.")
    else:
        st.success("Observation recorded for this session.")

        st.write("**Specimen:**", specimen)
        st.write("**Structures:**", structures)
        st.write("**Cell shape:**", shape)
        st.write("**Clearest objective:**", clearest)
        st.write("**Notes:**", notes)

st.info(
    "Educational simulation: the cell images are computer-generated "
    "illustrations, not real microscope photographs. The controls "
    "demonstrate basic magnification, brightness, and focus concepts."
)
