from flask import Blueprint, render_template, request, flash
from app.services.transcript import TranscriptService
from app.services.summarizer import SummarizerService

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        print(f"\n--- Processing URL: {url} ---")

        if not url:
            flash("Please enter a YouTube URL", "danger")
            return render_template("index.html")

        try:
            video_id = TranscriptService.extract_video_id(url)
            print("Video ID:", video_id)
            if not video_id:
                flash("Invalid YouTube URL format", "danger")
                return render_template("index.html")

            transcript = TranscriptService.get_transcript(video_id)
            print("Transcript length:", len(transcript))
            summary = SummarizerService().summarize(transcript, language=request.form.get("language", "en"), length_mode=request.form.get("length_mode", "medium"))
            print("Summary generated:", bool(summary))

            return render_template("index.html", transcript=transcript, summary="\n" + summary)

        except Exception as e:
            print("Error:", str(e))
            flash(str(e), "danger")

    return render_template("index.html")