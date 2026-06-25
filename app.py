from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import pickle

app = Flask(__name__)
app.secret_key = "admission_secret_key"

# Load model
model = pickle.load(open("admission_model.pkl", "rb"))

@app.route("/")
def home():

    prediction_text = session.pop("prediction_text", None)
    student_data = session.pop("student_data", None)

    return render_template(
        "index.html",
        prediction_text=prediction_text,
        student_data=student_data
    )


@app.route("/predict", methods=["POST"])
def predict():

    gpa = float(request.form["gpa"])
    entrance_score = int(request.form["entrance_score"])
    activities = int(request.form["activities"])
    recommendation = int(request.form["recommendation"])

    student = pd.DataFrame(
        [[gpa, entrance_score, activities, recommendation]],
        columns=[
            "GPA",
            "Entrance_Score",
            "Extracurricular_Activities",
            "Recommendation_Score"
        ]
    )

    prediction = model.predict(student)[0]

    if prediction == 1:
        result = "ADMITTED"
    else:
        result = "REJECTED"

    session["prediction_text"] = result

    session["student_data"] = {
        "gpa": gpa,
        "entrance_score": entrance_score,
        "activities": activities,
        "recommendation": recommendation
    }

    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():

    total_students = 1000
    admitted_students = 126
    rejected_students = 874
    accuracy = 100

    return render_template(
        "dashboard.html",
        total_students=total_students,
        admitted_students=admitted_students,
        rejected_students=rejected_students,
        accuracy=accuracy
    )


if __name__ == "__main__":
    app.run(debug=True)