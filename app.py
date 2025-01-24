import streamlit as st
import pandas as pd
import altair as alt
from model import find_sentiment

# Page Configuration
st.set_page_config(page_title="Sentiment Analysis App", layout="wide")
# Add a title
st.title("Sentiment Analysis App")

# Design CSS for box styling
BOX_STYLE = """
    <style>
        .box {
            border: 1px solid #ddd;
            border-radius: 8px;
        }
    </style>
"""
st.markdown(BOX_STYLE, unsafe_allow_html=True)

# Initialize session state for positive and negative count
if "positive_count" not in st.session_state:
    st.session_state["positive_count"] = 0
if "negative_count" not in st.session_state:
    st.session_state["negative_count"] = 0
if "neutral_count" not in st.session_state:
    st.session_state["neutral_count"] = 0

# User Input 
user_message = st.text_input("Type your message below:")


if user_message:

    sentiment_type, sentiment_score  = find_sentiment(user_message)

    # Update counts based on sentiment type
    if sentiment_type == "Positive":
        st.session_state["positive_count"] += 1
    elif sentiment_type == "Negative":
        st.session_state["negative_count"] += 1
    else:
        st.session_state["neutral_count"] += 1

    # showing sentiment and summary side by side in consistent boxes
    col1, col2 = st.columns(2)

    with col1:
        # Display Results with border
        st.markdown('<div class="box column-box">', unsafe_allow_html=True)
        st.subheader("Sentiment Analysis Result")
        st.write(f"**Sentiment Type:** {sentiment_type}")
        st.write(f"**Sentiment Score:** {sentiment_score:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Sentiment Analysis Summary
        st.markdown('<div class="box column-box">', unsafe_allow_html=True)
        st.subheader("Sentiment Analysis Summary")
        st.write(f"**Positive Messages Count:** {st.session_state['positive_count']}")
        st.write(f"**Negative Messages Count:** {st.session_state['negative_count']}")
        st.write(f"**Neutral Messages Count:** {st.session_state['neutral_count']}")
        st.markdown('</div>', unsafe_allow_html=True)

# Data for the charts if sentiment counts are available
if st.session_state["positive_count"] > 0 or st.session_state["negative_count"] > 0:
    data = pd.DataFrame({
        "sentiment": ["Positive", "Negative", "Neutral"],
        "count": [st.session_state["positive_count"], st.session_state["negative_count"], st.session_state["neutral_count"]],
        "count_percentage" : [round((st.session_state["positive_count"] / (st.session_state["positive_count"] + st.session_state["negative_count"] + st.session_state["neutral_count"])) * 100 , 2),
                              round((st.session_state["negative_count"] / (st.session_state["positive_count"] + st.session_state["negative_count"] + st.session_state["neutral_count"])) * 100, 2),
                              round((st.session_state["neutral_count"] / (st.session_state["positive_count"] + st.session_state["negative_count"] + st.session_state["neutral_count"])) * 100, 2)]
    })

    # Bar Chart
    bar_chart = alt.Chart(data).mark_bar().encode(
        x=alt.X("sentiment", sort=["Positive", "Negative", "Neutral"]),
        y="count",
        color=alt.Color(
        "sentiment",
        scale=alt.Scale(domain=["Positive", "Negative", "Neutral"],
                        range=["blue", "red", "lightblue"])
    ),
        tooltip=["sentiment", "count"]
    ).properties(
        width=600,
        height=400
    )

    # Pie Chart
    pie_chart = alt.Chart(data).mark_arc().encode(
        theta="count_percentage",
        color=alt.Color(
        "sentiment",
        scale=alt.Scale(domain=["Positive", "Negative", "Neutral"],
                        range=["blue", "red", "lightblue"])
    ),
        tooltip=["sentiment", "count_percentage"]
    ).properties(
        width=400,
        height=400
    )

    # Layout: Side-by-Side Charts with border
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Chart 1 inside a box
        st.markdown('<div class="box column-box">', unsafe_allow_html=True)
        st.subheader("Sentiment Distribution Bar Chart")
        st.altair_chart(bar_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="box column-box">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        # Chart 2 inside a box
        st.markdown('<div class="box column-box">', unsafe_allow_html=True)
        st.subheader("Sentiment Distribution Pie Chart")
        st.altair_chart(pie_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="box column-box">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

