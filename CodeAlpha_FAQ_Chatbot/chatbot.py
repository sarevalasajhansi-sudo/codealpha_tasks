import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text


class FAQChatbot:

    def __init__(self, faq_file="faq_data.json"):
        self.faq_file = Path(faq_file)

        self.faqs = self.load_faqs()

        self.questions = []
        self.answers = []
        self.original_questions = []

        self.last_question = None
        self.last_answer = None
        self.last_topic = None

        self.greetings = {
            "hi",
            "hello",
            "hey",
            "hii",
            "hiii",
            "good morning",
            "good afternoon",
            "good evening"
        }

        self.goodbyes = {
            "bye",
            "goodbye",
            "see you",
            "see you later"
        }

        for faq in self.faqs:

            variations = [
                faq["question"]
            ] + faq.get("variations", [])

            for variation in variations:
                processed = preprocess_text(variation)

                self.questions.append(processed)
                self.answers.append(faq["answer"])
                self.original_questions.append(variation)

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )

        if self.questions:
            self.question_vectors = self.vectorizer.fit_transform(
                self.questions
            )
        else:
            self.question_vectors = None

    def load_faqs(self):

        try:
            with open(
                self.faq_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except FileNotFoundError:
            print("FAQ file not found.")
            return []

        except json.JSONDecodeError:
            print("Invalid JSON format in FAQ file.")
            return []

        except Exception as e:
            print("Error loading FAQ data:", e)
            return []

    def clean_input(self, text):

        text = text.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    def is_greeting(self, text):

        cleaned = self.clean_input(text)

        return cleaned in self.greetings

    def is_goodbye(self, text):

        cleaned = self.clean_input(text)

        return cleaned in self.goodbyes

    def keyword_bonus(
        self,
        user_question,
        faq_question
    ):

        user_words = set(
            preprocess_text(user_question).split()
        )

        faq_words = set(
            preprocess_text(faq_question).split()
        )

        if not user_words or not faq_words:
            return 0.0

        common_words = user_words.intersection(
            faq_words
        )

        return len(common_words) / len(user_words)

    def find_best_match(self, user_question):

        if self.question_vectors is None:
            return None, 0.0

        processed_question = preprocess_text(
            user_question
        )

        if not processed_question.strip():
            return None, 0.0

        user_vector = self.vectorizer.transform(
            [processed_question]
        )

        similarities = cosine_similarity(
            user_vector,
            self.question_vectors
        )[0]

        best_index = similarities.argmax()

        best_score = float(
            similarities[best_index]
        )

        bonus = self.keyword_bonus(
            user_question,
            self.original_questions[best_index]
        )

        final_score = min(
            best_score + (bonus * 0.15),
            1.0
        )

        return best_index, final_score

    def build_context_question(self, user_question):

        if not self.last_question:
            return user_question

        follow_up_phrases = [
            "what is it",
            "what is that",
            "what does it do",
            "what are its uses",
            "what is it used for",
            "how does it work",
            "why is it important",
            "why is it useful",
            "tell me more",
            "explain more",
            "more about it"
        ]

        cleaned = self.clean_input(
            user_question
        )

        for phrase in follow_up_phrases:

            if phrase in cleaned:

                return (
                    user_question
                    + " "
                    + self.last_question
                )

        return user_question

    def get_response(self, user_question):

        if not user_question.strip():

            return {
                "answer": "Please enter a question.",
                "confidence": 0,
                "matched_question": None
            }

        cleaned = self.clean_input(
            user_question
        )

        if self.is_greeting(cleaned):

            return {
                "answer": (
                    "Hello! 👋\n\n"
                    "I'm your AI & Technology Assistant. "
                    "You can ask me about Artificial Intelligence, "
                    "Machine Learning, Deep Learning, NLP, "
                    "Computer Vision, Data Science, Python, "
                    "and other technology topics."
                ),
                "confidence": 100.0,
                "matched_question": "Greeting"
            }

        if self.is_goodbye(cleaned):

            return {
                "answer": (
                    "Goodbye! 👋\n"
                    "Keep learning and building amazing things!"
                ),
                "confidence": 100.0,
                "matched_question": "Goodbye"
            }

        search_question = self.build_context_question(
            user_question
        )

        best_index, best_score = self.find_best_match(
            search_question
        )

        similarity_threshold = 0.25

        if (
            best_index is not None
            and best_score >= similarity_threshold
        ):

            answer = self.answers[best_index]

            matched_question = self.original_questions[
                best_index
            ]

            self.last_question = matched_question
            self.last_answer = answer
            self.last_topic = matched_question

            return {
                "answer": answer,
                "confidence": round(
                    best_score * 100,
                    1
                ),
                "matched_question": matched_question
            }

        return {
            "answer": (
                "I'm not quite sure about that yet. 🤔\n\n"
                "I currently specialize in AI and technology "
                "topics such as:\n\n"
                "• Artificial Intelligence\n"
                "• Machine Learning\n"
                "• Deep Learning\n"
                "• Natural Language Processing\n"
                "• Computer Vision\n"
                "• Data Science\n"
                "• Python\n"
                "• Neural Networks\n\n"
                "Try asking me a question about one of these topics."
            ),
            "confidence": round(
                best_score * 100,
                1
            ),
            "matched_question": None
        }


if __name__ == "__main__":

    chatbot = FAQChatbot()

    print()
    print("=" * 55)
    print("       AI & TECHNOLOGY FAQ CHATBOT")
    print("=" * 55)
    print("Type 'exit' to quit.")
    print()

    while True:

        user_question = input("You: ").strip()

        if user_question.lower() == "exit":

            print(
                "Bot: Goodbye! 👋"
            )

            break

        result = chatbot.get_response(
            user_question
        )

        print()
        print(
            "Bot:",
            result["answer"]
        )

        print(
            "Confidence:",
            result["confidence"],
            "%"
        )

        print()