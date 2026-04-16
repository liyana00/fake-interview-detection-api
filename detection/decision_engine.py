history = {
    "faces": [],
    "behavior": [],
    "lip": []
}


def update_history(face_count, behavior, lip):
    history["faces"].append(face_count)
    history["behavior"].append(behavior)
    history["lip"].append(lip)

    # Keep last 20 frames
    if len(history["faces"]) > 20:
        history["faces"].pop(0)
        history["behavior"].pop(0)
        history["lip"].pop(0)


def make_decision(score):
    # 🔴 Rule 1: Multiple faces continuously
    if history["faces"].count(2) > 5:
        return "Cheating (Multiple Persons)"

    # 🔴 Rule 2: Looking away continuously
    if history["behavior"].count("Looking Left") + history["behavior"].count("Looking Right") > 8:
        return "Suspicious (Looking Away)"

    # 🔴 Rule 3: Talking frequently
    if history["lip"].count("Talking") > 10:
        return "Suspicious (Talking Too Much)"

    # 🔴 Rule 4: Score-based fallback
    if score > 60:
        return "Cheating"
    elif score > 30:
        return "Suspicious"
    else:
        return "Normal"