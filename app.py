from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# MongoDB connection — we will update this later
MONGO_URI = "mongodb+srv://shabzkp:shabu123@cluster0.cctut1w.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["student_db"]
collection = db["students"]

# Home route — shows the form
@app.route("/", methods=["GET"])
def index():
    return render_template("form.html", error=None)

# Submit route — saves data to MongoDB
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name  = request.form.get("name")
        email = request.form.get("email")
        grade = request.form.get("grade")

        if not name or not email or not grade:
            return render_template("form.html",
                   error="All fields are required!")

        student = {"name": name, "email": email, "grade": grade}
        collection.insert_one(student)
        return redirect(url_for("success"))

    except PyMongoError as e:
        return render_template("form.html",
               error=f"Database error: {str(e)}")

# Success route
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)