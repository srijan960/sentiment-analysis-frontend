import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

BACKEND_URL = "http://localhost:8005/upload"  # Update with your backend URL


def visualize_sentiment(data, transcript_content):
    """
    Display sentiment analysis results, including comparison graphs and heatmaps.
    """
    st.subheader("Sentence-level Sentiments")

    # Load sentence details
    sentence_details = pd.DataFrame(data["sentiment_results"]["sentence_details"])

    # Handle timestamps or use sequential indices
    sentence_details["timestamp"] = sentence_details["sentence"].str.extract(r"\[(\d{2}:\d{2})\]")[0]
    sentence_details["timestamp"] = pd.to_datetime(sentence_details["timestamp"], format="%M:%S", errors="coerce")
    sentence_details["timestamp"] = sentence_details["timestamp"].fillna(
        pd.Series(range(len(sentence_details)))
    )

    # Display raw details
    st.dataframe(sentence_details)

    # Scrollable transcription viewer
    st.write("### Transcription")
    transcription_html = f"""
    <div style="overflow-y: scroll; height: 300px; border: 1px solid #ddd; padding: 10px;">
        {transcript_content.replace("\n", "<br>")}
    </div>
    """
    st.markdown(transcription_html, unsafe_allow_html=True)

    # Dual-speaker comparison
    st.write("### Dual-Speaker Sentiment Comparison")
    speakers = sentence_details["speaker"].unique()
    if len(speakers) == 2:
        speaker1, speaker2 = speakers
        speaker1_data = sentence_details[sentence_details["speaker"] == speaker1]
        speaker2_data = sentence_details[sentence_details["speaker"] == speaker2]

        fig = go.Figure()

        # Plot Speaker 1 Sentiments
        fig.add_trace(
            go.Scatter(
                x=speaker1_data["timestamp"],
                y=speaker1_data["positive_score"],
                mode="lines+markers",
                name=f"{speaker1} Positive",
                hovertext=speaker1_data["sentence"],
            )
        )
        fig.add_trace(
            go.Scatter(
                x=speaker1_data["timestamp"],
                y=speaker1_data["negative_score"],
                mode="lines+markers",
                name=f"{speaker1} Negative",
                hovertext=speaker1_data["sentence"],
            )
        )

        # Plot Speaker 2 Sentiments
        fig.add_trace(
            go.Scatter(
                x=speaker2_data["timestamp"],
                y=speaker2_data["positive_score"],
                mode="lines+markers",
                name=f"{speaker2} Positive",
                hovertext=speaker2_data["sentence"],
            )
        )
        fig.add_trace(
            go.Scatter(
                x=speaker2_data["timestamp"],
                y=speaker2_data["negative_score"],
                mode="lines+markers",
                name=f"{speaker2} Negative",
                hovertext=speaker2_data["sentence"],
            )
        )

        fig.update_layout(
            title="Sentiment Comparison Between Speakers",
            xaxis_title="Timestamp (or Sentence Index if Missing)",
            yaxis_title="Sentiment Score",
            hovermode="x unified",
        )

        st.plotly_chart(fig)

       # Heatmap of sentiment changes
    st.write("### Sentiment Heatmap")
    heatmap_data = sentence_details.copy()
    heatmap_data["sentence_index"] = range(len(heatmap_data))

    # Positive sentiment heatmap
    positive_heatmap = heatmap_data.pivot(
        index="speaker", columns="sentence_index", values="positive_score"
    )
    fig_positive = px.imshow(
        positive_heatmap,
        labels=dict(x="Sentence Index", y="Speaker", color="Positive Sentiment"),
        title="Positive Sentiment Heatmap",
    )
    st.plotly_chart(fig_positive)

    # Negative sentiment heatmap
    negative_heatmap = heatmap_data.pivot(
        index="speaker", columns="sentence_index", values="negative_score"
    )
    fig_negative = px.imshow(
        negative_heatmap,
        labels=dict(x="Sentence Index", y="Speaker", color="Negative Sentiment"),
        title="Negative Sentiment Heatmap",
    )
    st.plotly_chart(fig_negative)


def main():
    st.title("Call Transcript Sentiment Analysis")
    st.write("Upload a call transcript file (text format) to analyze speaker-level sentiment.")

    # File upload widget
    uploaded_file = st.file_uploader("Choose a file", type=["txt"])

    if uploaded_file is not None:
        # Display uploaded file content in a scrollable window
        content = uploaded_file.read().decode("utf-8")
        st.subheader("Uploaded Transcript")

        if st.button("Analyze Sentiment"):
            # Reset file pointer
            uploaded_file.seek(0)

            # Call backend for sentiment analysis
            with st.spinner("Analyzing sentiment..."):
                # Prepare file for the POST request
                files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
                response = requests.post(
                    BACKEND_URL,
                    files=files,
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis complete!")
                    visualize_sentiment(data, content)
                else:
                    st.error(
                        f"Failed to analyze sentiment. Error {response.status_code}: {response.text}"
                    )


if __name__ == "__main__":
    main()