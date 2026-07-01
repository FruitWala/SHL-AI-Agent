from app.retrieval.retriever import retrieve
from app.utils.gemini_client import ask_gemini
from app.utils.intent import is_off_topic


def extract_profile(messages):
    """
    Extract role, experience and additional requirements
    from the stateless conversation history.
    """

    user_messages = [
        m.content.strip()
        for m in messages
        if m.role.lower() == "user"
    ]

    profile = {}

    if len(user_messages) >= 1:
        profile["role"] = user_messages[0]

    if len(user_messages) >= 2:
        profile["experience"] = user_messages[1]

    if len(user_messages) >= 3:
        profile["extra"] = " ".join(user_messages[2:])

    return profile


def build_context(retrieved):

    context = ""
    recommendations = []

    for item in retrieved:

        context += f"""
Assessment Name:
{item['name']}

Description:
{item['description']}

Duration:
{item['duration']}

Job Levels:
{item['job_levels']}

Languages:
{item['languages']}

Remote:
{item['remote']}

Adaptive:
{item['adaptive']}

Categories:
{item['categories']}

URL:
{item['url']}

----------------------------------------
"""

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "duration": item["duration"],
            "job_levels": item["job_levels"],
            "languages": item["languages"],
            "remote": item["remote"],
            "adaptive": item["adaptive"],
            "categories": item["categories"]
        })

    return context, recommendations


def chat(messages):

    # -----------------------------
    # Conversation History
    # -----------------------------

    conversation = "\n".join(
        f"{m.role}: {m.content}"
        for m in messages
    )

    last_user_message = ""

    for m in reversed(messages):
        if m.role.lower() == "user":
            last_user_message = m.content.strip()
            break

# -----------------------------
# Off-topic Detection
# -----------------------------

    if is_off_topic(last_user_message):
        return {
        "reply": "I can only help with SHL assessment recommendations. Please ask about hiring roles, assessments, or comparing SHL assessments.",
        "recommendations": [],
        "end_of_conversation": True
    }
    # -----------------------------
    # Comparison Intent
    # -----------------------------

    comparison_keywords = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    if any(k in last_user_message.lower() for k in comparison_keywords):

        retrieved = retrieve(last_user_message, k=2)

        context, recommendations = build_context(retrieved)

        reply = ask_gemini(
            context=context,
            conversation=conversation
        )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    # -----------------------------
    # Build Profile
    # -----------------------------

    profile = extract_profile(messages)

    if "role" not in profile:

        return {
            "reply": "What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    if "experience" not in profile:

        return {
            "reply": "What experience level are you hiring for? (Entry-Level, Mid-Professional, Senior Leadership)",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Retrieval Query
    # -----------------------------

    query = f"""
Role:
{profile['role']}

Experience:
{profile['experience']}

Additional Requirements:
{profile.get("extra","")}
"""

    retrieved = retrieve(query, k=5)

    context, recommendations = build_context(retrieved)

    reply = ask_gemini(
        context=context,
        conversation=conversation
    )

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": True
    }