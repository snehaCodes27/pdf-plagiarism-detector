from flask import Flask, render_template, request
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Extract text from PDF
def extract_text(filepath):
    text = ""
    try:
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
        doc.close()
    except:
        return ""
    return text.strip()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        f1 = request.files.get("f1")
        f2 = request.files.get("f2")

        if not f1 or not f1.filename.lower().endswith(".pdf"):
            return render_template("home.html", msg="First file must be PDF")

        if not f2 or not f2.filename.lower().endswith(".pdf"):
            return render_template("home.html", msg="Second file must be PDF")

        path1 = "a.pdf"
        path2 = "b.pdf"

        f1.save(path1)
        f2.save(path2)

        s1 = extract_text(path1)
        s2 = extract_text(path2)

        # If PDFs contain no readable text
        if not s1 or not s2:
            os.remove(path1)
            os.remove(path2)
            return render_template("home.html", msg="Unable to extract text from PDF")

        texts = [s1, s2]

        try:
            cv = CountVectorizer()
            vector = cv.fit_transform(texts)
            similarity_matrix = cosine_similarity(vector)
            score = round(similarity_matrix[0][1] * 100, 2)
        except:
            os.remove(path1)
            os.remove(path2)
            return render_template("home.html", msg="Error while processing documents")

        if score > 70:
            msg = f"High Plagiarism ({score}%)"
        elif score > 40:
            msg = f"Medium Plagiarism ({score}%)"
        else:
            msg = f"Unique ({score}%)"

        os.remove(path1)
        os.remove(path2)

        return render_template("home.html", msg=msg)

    return render_template("home.html")


# Keep this commented for deployment
# if __name__ == "__main__":
#     app.run(debug=True)
