import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

from inference.inference import FoodInference
from utils.visualisation import Visualizer

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Food Nutrition AI",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Metric Cards */
[data-testid="metric-container"]{
    background-color:#F8F9FA;
    border:1px solid #E6E6E6;
    padding:18px;
    border-radius:12px;
    text-align:center;
}

/* DataFrames */
[data-testid="stDataFrame"]{
    border-radius:10px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#F7F9FC;
}

/* Success box */
.stAlert{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🍽️ FoodAI")

    st.markdown("---")

    st.subheader("🤖 Model Information")

    st.info(
        """
**Model:** YOLOv8s

**Food Classes:** 80

**Nutrition Dataset:** USDA + Kaggle

**Serving Basis:** Per 100 g

**Confidence Threshold:** 0.70
"""
    )

    st.markdown("---")

    st.subheader("📌 Project Pipeline")

    st.markdown("""
1. Upload Image

2. Detect Food

3. Nutrition Lookup

4. Nutrition Summary
""")

    st.markdown("---")

    st.success(
        """
### 👨‍💻 Developed By

**Anand Yesu Kumar**
"""
    )

# =====================================================
# TITLE
# =====================================================

st.title("🍽️ Food Nutrition AI")

st.caption(
    "AI Powered Food Detection and Nutrition Estimation"
)

st.divider()

# =====================================================
# INITIALIZE
# =====================================================

inference = FoodInference()

visualizer = Visualizer()

# =====================================================
# IMAGE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "📤 Upload a food image",
    type=["jpg", "jpeg", "png"]
)

# =====================================================
# PROCESS IMAGE
# =====================================================

if uploaded_file is not None:

    # Read image
    image = Image.open(uploaded_file)

    # Convert RGBA/other modes to RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    temp_image = Path("temp_image.jpg")
    image.save(temp_image)

    with st.spinner("🔍 Detecting food items..."):

        result = inference.analyze_image(str(temp_image))

        # If no food detected
        if "message" in result:
            st.warning(result["message"])

            try:
                temp_image.unlink()
            except Exception:
                pass

            st.stop()

    # =====================================================
    # Prepare detections for visualization
    # =====================================================

    detections = []

    for item in result["foods"]:

        detections.append({

            "food": item["food"],

            "confidence": item["confidence"],

            "bbox": item["bbox"]

        })

    # =====================================================
    # Draw bounding boxes
    # =====================================================

    output_image = visualizer.draw_detections(
        str(temp_image),
        detections
    )

    # =====================================================
    # Display Images
    # =====================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📷 Original Image")

        st.image(
            image,
            use_container_width=True
        )

    with col2:

        st.subheader("🎯 Detection Result")

        st.image(
            output_image,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # DETECTED FOODS
    # =====================================================

    st.subheader("📋 Detected Foods")

    food_df = pd.DataFrame(
        [
            {
                "Food": food.title(),
                "Count": count
            }
            for food, count in result["food_counts"].items()
        ]
    )

    st.dataframe(
        food_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # NUTRITION TABLE
    # =====================================================

    st.subheader("🥗 Nutrition Information")

    nutrition_rows = []

    for food_name, count in result["food_counts"].items():

        # Find first occurrence of this food
        food_data = next(
            (
                item for item in result["foods"]
                if item["food"] == food_name
            ),
            None
        )

        if food_data is None:
            continue

        nutrition = food_data["nutrition"]

        if nutrition is None:
            continue

        nutrition_rows.append({

            "Food": food_name.title(),

            "Count": count,

            "Calories\n(kcal/100g)": nutrition["Calories (kcal/100g)"],

            "Protein\n(g/100g)": nutrition["Protein (g/100g)"],

            "Carbohydrates\n(g/100g)": nutrition["Carbohydrates (g/100g)"],

            "Fat\n(g/100g)": nutrition["Fat (g/100g)"]

        })

    nutrition_df = pd.DataFrame(nutrition_rows)

    st.dataframe(
        nutrition_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "ℹ️ Nutrition values are based on **100 g** of each detected food item."
    )

    st.divider()

    # =====================================================
    # NUTRITION SUMMARY
    # =====================================================

    st.subheader("📊 Nutrition Summary")

    summary = result["nutrition_summary"]

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "🔥 Calories",
            f"{summary['Calories']:.2f} kcal"
        )

    with m2:
        st.metric(
            "💪 Protein",
            f"{summary['Protein']:.2f} g"
        )

    with m3:
        st.metric(
            "🍞 Carbohydrates",
            f"{summary['Carbohydrates']:.2f} g"
        )

    with m4:
        st.metric(
            "🥑 Fat",
            f"{summary['Fat']:.2f} g"
        )

    st.success(
        f"Serving Basis: {summary['Serving Basis']}"
    )

    st.divider()

    # =====================================================
    # DETECTION STATISTICS
    # =====================================================

    st.subheader("📈 Detection Statistics")

    total_detections = len(result["foods"])
    unique_foods = len(result["food_counts"])

    avg_confidence = 0

    if total_detections > 0:

        avg_confidence = round(

            sum(
                item["confidence"]
                for item in result["foods"]
            ) / total_detections,

            2
        )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🍽️ Total Detections",
            total_detections
        )

    with c2:
        st.metric(
            "🥗 Unique Foods",
            unique_foods
        )

    with c3:
        st.metric(
            "🎯 Average Confidence",
            f"{avg_confidence * 100:.1f}%"
        )

    st.divider()

    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.markdown(
        """
        <div style="text-align:center; padding:20px;">

        <h3>🍽️ Food Nutrition AI</h3>

        <p>
        AI Powered Food Detection and Nutrition Estimation
        </p>

        <p>
        <b>Developed by Anand Yesu Kumar</b>
        </p>

        <p>
        Version 1.0 | 2026
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CLEANUP
    # =====================================================

    try:
        temp_image.unlink()
    except Exception:
        pass

    # =====================================================
    # NO IMAGE UPLOADED
    # =====================================================

    else:

        st.info(
            """
            👆 Upload a food image to begin analysis.

            Supported formats:

            • JPG

            • JPEG

            • PNG
            """
        )