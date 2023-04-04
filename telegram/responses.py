from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello","hi","sup"):
        return "Hey ! How its going?"
    if user_message in ("who are you","who are you?"):
        return "Hey ! PMDL , abbrevated as Parkinsons Disease prediction using ML Algorithms"
    return "I don't understand you"