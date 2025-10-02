import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

# set page configuration 
st.set_page_config(
    page_title="Airline Analytics Dashboard",
    page_icon="✈️",
    layout="wide"
)

# minimal CSS for subtle card effect and spacing
st.markdown("""
    <style>
    .stMetric {
        background: #222831;
        border-radius: 8px;
        padding: 1.2em 0.5em;
        margin-bottom: 1em;
    }
    .stDataFrame, .stTable {
        background: #23272f !important;
    }
    </style>
""", unsafe_allow_html=True)

# load and preprocess data
@st.cache_data
def load_data():
    data_file = "data/Clean_Dataset.csv"
    if not os.path.exists(data_file):
        st.error("Dataset not found! Please ensure 'Clean_Dataset.csv' is placed in the 'data' directory.")
        st.stop()
    try:
        df = pd.read_csv(data_file)
        if "Unnamed: 0" in df.columns:
            df = df.drop("Unnamed: 0", axis=1)
        df = df.drop_duplicates()
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        st.stop()

df = load_data()

# sidebar nav
st.sidebar.title("✈️ Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Airline Analysis",
        "Price Analysis",
        "Duration Analysis",
        "Destination Analysis"
    ]
)

st.title("✈️ Airline Analytics Dashboard")
st.write("")

if page == "Overview":
    st.header("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Flights", f"{len(df):,}")
    col2.metric("Unique Airlines", df['airline'].nunique())
    col3.metric("Avg Price", f"₹{df['price'].mean():,.0f}")
    col4.metric("Avg Duration", f"{df['duration'].mean():.1f}h")
    st.subheader("Sample Data")
    st.dataframe(df.head(), use_container_width=True)

elif page == "Airline Analysis":
    st.header("Airline Frequency & Prices")
    st.subheader("Flight Frequency by Airline (Plotly)")
    airline_counts = df['airline'].value_counts()
    fig1 = px.bar(
        x=airline_counts.index,
        y=airline_counts.values,
        labels={'x': 'Airline', 'y': 'Number of Flights'},
        color=airline_counts.index,
        template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.subheader("Flight Frequency by Airline (Seaborn)")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=airline_counts.index, y=airline_counts.values, ax=ax, palette="crest")
    ax.set_xlabel("Airline", fontsize=11)
    ax.set_ylabel("Number of Flights", fontsize=11)
    ax.set_title("Frequency of Flights by Airline", fontsize=13, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(rotation=30)
    sns.despine()
    st.pyplot(fig)
    st.markdown("""
    - **Indigo** and **Air India** are the most frequent airlines in the dataset.
    - Some airlines have significantly fewer flights, indicating possible niche or premium services.
    """)
    st.subheader("Average Price by Airline (Plotly)")
    avg_prices = df.groupby('airline')['price'].mean().sort_values(ascending=False)
    fig2 = px.bar(
        x=avg_prices.index,
        y=avg_prices.values,
        labels={'x': 'Airline', 'y': 'Average Price (₹)'},
        color=avg_prices.index,
        template="plotly_dark"
    )
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Price Analysis":
    st.header("Price Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Price Distribution (Plotly)")
        fig = px.histogram(df, x='price', nbins=50, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Price by Class (Seaborn)")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x='class', y='price', data=df, ax=ax, palette="flare")
        ax.set_xlabel("Class", fontsize=11)
        ax.set_ylabel("Price", fontsize=11)
        ax.set_title("Price by Class", fontsize=13, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        sns.despine()
        st.pyplot(fig)
        st.markdown("""
        - **Business class** flights are, on average, much more expensive than **economy**.
        - There are some outliers in both classes, indicating premium or last-minute bookings.
        """)
    st.subheader("Price vs Days Before Departure (Plotly)")
    fig = px.scatter(df, x='days_left', y='price', color='class', trendline="lowess", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Duration Analysis":
    st.header("Duration Analysis")
    try:
        if df['duration'].isnull().any() or not pd.api.types.is_numeric_dtype(df['duration']):
            st.warning("Duration column contains missing or non-numeric values. Please check your data.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Duration Distribution (Seaborn)")
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.histplot(df['duration'], bins=30, kde=True, ax=ax, color="#4B79A1", edgecolor="#222831", linewidth=1.2)
                ax.set_xlabel("Duration (hours)", fontsize=11)
                ax.set_ylabel("Number of Flights", fontsize=11)
                ax.set_title("Distribution of Flight Durations", fontsize=13, fontweight='bold')
                ax.grid(axis='y', linestyle='--', alpha=0.6)
                sns.despine()
                st.pyplot(fig)
                st.markdown("""
                - Most flights have durations between **5 and 15 hours**.
                - There are a few long-haul flights with durations above 20 hours.
                """)
            with col2:
                st.subheader("Duration vs Price (Plotly)")
                fig = px.scatter(df, x='duration', y='price', color='class', trendline="lowess", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error in Duration Analysis: {e}")

elif page == "Destination Analysis":
    st.header("Destination Analysis")
    st.subheader("Average Duration by Destination (Plotly)")
    avg_duration = df.groupby('destination_city')['duration'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=avg_duration.index,
        y=avg_duration.values,
        labels={'x': 'Destination City', 'y': 'Avg Duration (h)'},
        color=avg_duration.index,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Price Distribution by Destination (Seaborn)")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(x='destination_city', y='price', data=df, ax=ax, palette="mako")
    ax.set_xlabel("Destination City", fontsize=11)
    ax.set_ylabel("Price", fontsize=11)
    ax.set_title("Price Distribution by Destination", fontsize=13, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(rotation=30)
    sns.despine()
    st.pyplot(fig)
    st.markdown("""
    - Some cities (e.g., **Delhi**, **Mumbai**) have a wider range of prices, likely due to higher demand and more flight options.
    - Outliers may represent premium or last-minute bookings.
    """)

st.markdown("""
---
<p style='text-align:center; color:gray;'>Airline Analytics Dashboard &copy; 2024</p>
""", unsafe_allow_html=True) 