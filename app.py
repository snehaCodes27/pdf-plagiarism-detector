from flask import Flask, render_template, request
import fitz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def extract_text(filename):
    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        f1 = request.files["f1"]
        f2 = request.files["f2"]

        if not f1.filename.lower().endswith(".pdf"):
            return render_template("home.html", msg="First file should be PDF")

        if not f2.filename.lower().endswith(".pdf"):
            return render_template("home.html", msg="Second file should be PDF")

        f1.save("a.pdf")
        f2.save("b.pdf")

        s1 = extract_text("a.pdf")
        s2 = extract_text("b.pdf")

        texts = [s1, s2]
        cv = CountVectorizer()
        vector = cv.fit_transform(texts)

        cs = cosine_similarity(vector)
        score = round(cs[0][1] * 100, 2)

        if score > 70:
            msg = f"High Plagiarism ({score}%)"
        elif score > 40:
            msg = f"Medium Plagiarism ({score}%)"
        else:
            msg = f"Unique ({score}%)"

        return render_template("home.html", msg=msg)

    return render_template("home.html")


# Run server (keep commented for deployment / GitHub)
# app.run(debug=True)
