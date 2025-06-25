# backend/user_profile.py
def build_user_vector(user_id):
    from backend.embeddings import embed_text
    profiles = {
        "user_1": "I prefer personalized recommendations based on what I search.",
        "guest": "I want diverse and interesting suggestions related to my input."
    }
    return embed_text(profiles.get(user_id, "I want recommendations based on my prompt."))
