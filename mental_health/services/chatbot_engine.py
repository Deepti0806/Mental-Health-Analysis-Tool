import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# =====================================================
# Emotion Keyword Intensity
# =====================================================

HIGH_INTENSITY_WORDS = [
    "hopeless", "worthless", "suicidal", "can't go on",
    "panic attack", "extremely anxious", "give up",
    "overwhelmed", "broken", "no point", "depressed",
    "crying all the time", "nothing matters"
]

MODERATE_INTENSITY_WORDS = [
    "stressed", "tired", "worried", "pressure",
    "sad", "anxious", "frustrated", "confused",
    "burnout", "exhausted", "overthinking"
]


# =====================================================
# Emotion Detection
# =====================================================

def detect_emotion_intensity(message: str) -> str:
    if not isinstance(message, str):
        return "Low"

    message = message.lower()

    for word in HIGH_INTENSITY_WORDS:
        if word in message:
            return "High"

    for word in MODERATE_INTENSITY_WORDS:
        if word in message:
            return "Moderate"

    return "Low"


# =====================================================
# Escalation Logic
# =====================================================

def count_recent_negative_messages(chat_history: List[Dict]) -> int:

    user_messages = [
        msg["message"]
        for msg in chat_history
        if msg.get("role") == "user"
    ][-6:]

    count = 0

    for msg in user_messages:
        if detect_emotion_intensity(msg) in ["High", "Moderate"]:
            count += 1

    return count


def professional_support_message(age_group: Optional[str]):

    if age_group == "Teen":
        return (
            "It might really help to talk to a trusted adult, school counselor, "
            "or a licensed mental health professional."
        )

    elif age_group == "Senior":
        return (
            "Reaching out to a healthcare provider or a support group "
            "could provide structured and meaningful support."
        )

    return (
        "Speaking with a licensed therapist or counselor "
        "could provide additional support and clarity."
    )


# =====================================================
# Smart Topic Extraction
# =====================================================

def detect_topic(message: str) -> str:

    message = message.lower()

    if any(word in message for word in ["sleep", "insomnia", "not sleeping"]):
        return "sleep"

    if any(word in message for word in ["work", "office", "deadline", "boss", "workload"]):
        return "work"

    if any(word in message for word in ["exam", "college", "study", "marks"]):
        return "academics"

    if any(word in message for word in ["relationship", "partner", "breakup", "family"]):
        return "relationships"

    if any(word in message for word in ["tired", "exhausted", "burnout"]):
        return "fatigue"

    return "general"


# =====================================================
# Main Generator
# =====================================================

def generate_response(
    user_message: str,
    stress_level: str,
    chat_history: List[Dict],
    age_group: str = None
):

    logger.info("Generating advanced contextual response")

    if not isinstance(user_message, str):
        return "Can you tell me more about that?"

    topic = detect_topic(user_message)
    emotion = detect_emotion_intensity(user_message)
    negative_count = count_recent_negative_messages(chat_history)

    user_turns = len([m for m in chat_history if m["role"] == "user"])

    # Last assistant message (for repetition prevention)
    last_assistant_message = None
    for msg in reversed(chat_history):
        if msg["role"] == "assistant":
            last_assistant_message = msg["message"]
            break

    # =====================================================
    # 🚨 Escalation (if emotional intensity stays high)
    # =====================================================

    if negative_count >= 3 or emotion == "High":

        support = professional_support_message(age_group)

        reply = (
            "I’m really concerned about how intense this feels for you. "
            f"{support} "
            "Would you like to tell me what feels most overwhelming right now?"
        )

        return reply

    # =====================================================
    # Topic Based Dynamic Responses
    # =====================================================

    if topic == "sleep":
        reply = (
            "Sleep issues can deeply affect both mood and energy levels. "
            "Do you find it hard to fall asleep, or do you wake up frequently?"
        )

    elif topic == "work":
        reply = (
            "Work pressure can slowly build up and feel exhausting. "
            "Is it workload, expectations, or lack of balance that's affecting you most?"
        )

    elif topic == "academics":
        reply = (
            "Academic stress can feel overwhelming, especially with expectations. "
            "Are upcoming exams or performance pressure contributing to this?"
        )

    elif topic == "relationships":
        reply = (
            "Relationships can strongly impact emotional well-being. "
            "Would you like to share what’s been happening in that area?"
        )

    elif topic == "fatigue":
        reply = (
            "Constant fatigue can sometimes be linked to stress or emotional strain. "
            "Do you feel mentally drained as well?"
        )

    # =====================================================
    # Progressive Flow (conversation maturity)
    # =====================================================

    elif user_turns == 1:
        reply = (
            "Thank you for sharing that with me. "
            "Can you tell me a little more about what has been happening recently?"
        )

    elif user_turns == 2:
        reply = (
            "That gives me more context. "
            "How long have you been feeling this way?"
        )

    elif user_turns == 3:
        reply = (
            "It sounds like this has been ongoing. "
            "What do you think has contributed most to this situation?"
        )

    elif user_turns == 4:
        reply = (
            "What do you feel would help you most right now — rest, structure, or someone to talk to?"
        )

    elif user_turns >= 5:
        reply = (
            "It might help to take a small practical step today. "
            "What is one small action you feel comfortable taking right now?"
        )

    else:
        reply = "I'm here to listen. Tell me more."

    # =====================================================
    # Prevent Repetition
    # =====================================================

    if reply == last_assistant_message:
        reply += " I want to understand this better."

    return reply
