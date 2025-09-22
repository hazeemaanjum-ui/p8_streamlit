import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

# Set page config
st.set_page_config(page_title="Advanced Data Explorer", layout="wide")

# Title
st.title("📊 Advanced Data Explorer")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📁 Upload & View Data", "📈 Data Visualization", "📥 Download Data"])

# Load default dataset
@st.cache_data
def load_default_data():
    return sns.load_dataset("iris")

# Upload CSV
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File uploaded successfully!")
else:
    df = load_default_data()
    st.sidebar.info("Using default Iris dataset.")

# Page 1: Data view
if page == "📁 Upload & View Data":
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("Summary Statistics")
    st.write(df.describe())

    if st.checkbox("Show column data types"):
        st.write(df.dtypes)

# Page 2: Visualization
elif page == "📈 Data Visualization":
    st.subheader("🔍 Interactive Data Visualization")

    # Select numeric columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Scatter plot
    st.markdown("### 📌 Scatter Plot")
    col1 = st.selectbox("Select X-axis", numeric_cols, index=0)
    col2 = st.selectbox("Select Y-axis", numeric_cols, index=1)
    color_col = st.selectbox("Color by", df.columns, index=len(df.columns) - 1)

    fig1 = px.scatter(df, x=col1, y=col2, color=df[color_col])
    st.plotly_chart(fig1, use_container_width=True)

    # Histogram
    st.markdown("### 📊 Histogram")
    hist_col = st.selectbox("Select column for histogram", numeric_cols, index=0)
    bins = st.slider("Number of bins", 5, 50, 20)

    fig2 = px.histogram(df, x=hist_col, nbins=bins, color=color_col)
    st.plotly_chart(fig2, use_container_width=True)

# Page 3: Download Data
elif page == "📥 Download Data":
    st.subheader("📤 Download Processed Data")

    st.write("Preview of data:")
    st.dataframe(df.head())

    csv = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="data.csv", mime="text/csv")

    st.info("Tip: You can upload your own CSV file from the sidebar.")

# Footer
st.markdown("---")
st.caption("Created with ❤️ using Streamlit")
