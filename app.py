import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

BACKEND_URL = "https://3092-20-198-48-150.ngrok-free.app/upload"

def visualize_sentiment(data, transcript_content):
    """
    Display sentiment analysis results, including polarity and intensity visualization.
    """
    st.subheader("Sentence-level Sentiments")

    # Load sentence details
    sentiment_results = data["sentiment_results"]
    sentence_details = pd.DataFrame(sentiment_results["sentence_details"])

    # Handle timestamps or use sequential indices
    sentence_details["timestamp"] = pd.Series(range(len(sentence_details)))

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

    # Original graph: Sentiment comparison between speakers
    st.write("### Dual-Speaker Sentiment Comparison")
    speakers = sentence_details["speaker"].unique()
    if len(speakers) == 2:
        speaker1, speaker2 = speakers
        speaker1_data = sentence_details[sentence_details["speaker"] == speaker1]
        speaker2_data = sentence_details[sentence_details["speaker"] == speaker2]

        fig1 = go.Figure()

        # Plot Speaker 1 Sentiments
        fig1.add_trace(
            go.Scatter(
                x=speaker1_data["timestamp"],
                y=speaker1_data["positive_score"] - speaker1_data["negative_score"],
                mode="lines",
                name=f"{speaker1} (Sentiment)",
                hovertext=speaker1_data["sentence"],  # Display only Speaker 1's sentence
                line=dict(color="blue"),
            )
        )

        # Plot Speaker 2 Sentiments
        fig1.add_trace(
            go.Scatter(
                x=speaker2_data["timestamp"],
                y=speaker2_data["positive_score"] - speaker2_data["negative_score"],
                mode="lines",
                name=f"{speaker2} (Sentiment)",
                hovertext=speaker2_data["sentence"],  # Display only Speaker 2's sentence
                line=dict(color="red"),
            )
        )

        fig1.update_layout(
            title="Sentiment Comparison Between Speakers",
            xaxis=dict(title="Timestamp", rangeslider=dict(visible=True)),
            yaxis=dict(title="Sentiment Score", zeroline=True),
            hovermode="closest",  # Ensure only the nearest point's hover text is shown
        )
        st.plotly_chart(fig1)

    # New graph: Polarity and intensity visualization
    st.write("### Polarity and Intensity per Sentence")
    fig2 = go.Figure()

    for speaker in speakers:
        speaker_data = sentence_details[sentence_details["speaker"] == speaker]

        # Plot polarity
        fig2.add_trace(
            go.Bar(
                x=speaker_data["timestamp"],
                y=speaker_data["polarity"],
                name=f"{speaker} (Polarity)",
                marker=dict(color="green"),
                hovertext=speaker_data["sentence"],  # Display only Speaker's sentence
            )
        )

        # Plot intensity
        fig2.add_trace(
            go.Bar(
                x=speaker_data["timestamp"],
                y=speaker_data["intensity"],
                name=f"{speaker} (Intensity)",
                marker=dict(color="orange"),
                hovertext=speaker_data["sentence"],  # Display only Speaker's sentence
            )
        )

    fig2.update_layout(
        title="Polarity and Intensity for Each Sentence",
        xaxis=dict(title="Timestamp"),
        yaxis=dict(title="Scores"),
        barmode="group",
    )
    st.plotly_chart(fig2)

def main():
    st.title("Call Transcript Sentiment Analysis")
    st.write("Upload a call transcript file (text format) to analyze speaker-level sentiment.")

    uploaded_file = st.file_uploader("Choose a file", type=["txt"])

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.subheader("Uploaded Transcript")

        if st.button("Analyze Sentiment"):
            uploaded_file.seek(0)
            files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
            response = requests.post(BACKEND_URL, files=files)

            if response.status_code == 200:
                data = response.json()
                st.success("Analysis complete!")
                visualize_sentiment(data, content)
            else:
                st.error(f"Failed to analyze sentiment. Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    main()