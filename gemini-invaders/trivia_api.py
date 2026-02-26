import requests

class TriviaAPI:
    def __init__(self):
        self.api_url = "https://opentdb.com/api.php?amount=1&type=boolean"

    def get_trivia_question(self):
        response = requests.get(self.api_url)
        try:
            data = response.json()
            if data["results"]:
                question_data = data["results"][0]
                question = question_data["question"]
                correct_answer = question_data["correct_answer"]
                return question, correct_answer
            else:
                return None, None
        except KeyError:
            print("Error: 'results' key not found in API response.")
            return None, None
