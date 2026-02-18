from flask import render_template, request, redirect, url_for, session, current_app
from . import mental_health
from .services.stress_engine import predict_stress
from .services.chatbot_engine import generate_response


# -----------------------------
# Home
# -----------------------------
@mental_health.route("/")
def home():
    return render_template("home.html")


# -----------------------------
# Analyze Stress
# -----------------------------
@mental_health.route("/analyze", methods=["GET", "POST"])
def analyze():

    if request.method == "POST":

        user_text = request.form.get("text")
        age_group = request.form.get("age_group")

        if not user_text:
            return redirect(url_for("mental_health.analyze"))

        # Predict stress level
        stress_level, confidence = predict_stress(user_text)

        # Store in session
        session["stress_level"] = stress_level
        session["confidence"] = confidence
        session["age_group"] = age_group

        # Initialize chat history with first user message
        session["chat_history"] = [
            {
                "role": "user",
                "message": user_text
            }
        ]

        # Generate first assistant reply
        first_reply = generate_response(
            user_message=user_text,
            stress_level=stress_level,
            chat_history=session["chat_history"],
            age_group=age_group
        )

        session["chat_history"].append({
            "role": "assistant",
            "message": first_reply
        })

        session.modified = True

        current_app.logger.info(
            f"Stress detected: {stress_level} | Confidence: {confidence}"
        )

        return redirect(url_for("mental_health.chat"))

    return render_template("analyze.html")


# -----------------------------
# Chat (Conversational Mode)
# -----------------------------
@mental_health.route("/chat", methods=["GET", "POST"])
def chat():

    if "chat_history" not in session:
        return redirect(url_for("mental_health.home"))

    if request.method == "POST":

        user_message = request.form.get("message")

        if user_message:

            # Append user message
            session["chat_history"].append({
                "role": "user",
                "message": user_message
            })

            stress_level = session.get("stress_level")
            age_group = session.get("age_group")

            # Generate contextual AI response (FIXED)
            ai_reply = generate_response(
                user_message=user_message,
                stress_level=stress_level,
                chat_history=session.get("chat_history", []),
                age_group=age_group
            )

            # Append assistant reply
            session["chat_history"].append({
                "role": "assistant",
                "message": ai_reply
            })

            session.modified = True

    return render_template(
        "chat.html",
        chat_history=session.get("chat_history", []),
        stress_level=session.get("stress_level"),
        confidence=session.get("confidence")
    )
