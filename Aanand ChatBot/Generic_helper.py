import re


def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""


def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])


if __name__ == "__main__":
    print(extract_session_id("projects/aanand-chatbot/agent/sessions/123456789/contexts/ongoing-order"))
    print(get_str_from_food_dict({"pizza": 2, "burger": 1, "coke": 3}))
    print(get_str_from_food_dict({"pizza": 0, "burger": 0, "coke": 0}))