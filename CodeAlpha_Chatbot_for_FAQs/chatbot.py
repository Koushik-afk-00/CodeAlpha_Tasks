# Import Libraries
import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# File Settings
BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faqs.json"

SIMILARITY_THRESHOLD = 0.20


# FAQ Chatbot Class
class FAQChatbot:

    # Initialize Chatbot
    def __init__(self, faq_file):

        # Load FAQ data
        with faq_file.open("r", encoding="utf-8") as file:
            self.faqs = json.load(file)

        if not self.faqs:
            raise ValueError("faqs.json does not contain any FAQs.")

        # Get FAQ questions
        self.questions = [
            faq["question"]
            for faq in self.faqs
        ]

        # Create TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )

        # Convert questions into TF-IDF vectors
        self.question_matrix = self.vectorizer.fit_transform(
            self.questions
        )

    # Find Best Answer
    def get_answer(self, user_question):

        # Convert user's question into TF-IDF vector
        user_vector = self.vectorizer.transform(
            [user_question]
        )

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(
            user_vector,
            self.question_matrix
        )[0]

        # Find highest similarity
        best_index = similarity_scores.argmax()
        best_score = float(similarity_scores[best_index])

        # Check similarity threshold
        if best_score < SIMILARITY_THRESHOLD:
            return (
                "Sorry, I couldn't find a confident answer "
                "to that question. Please try asking about "
                "AI, Python, Data Science, Machine Learning, "
                "or another FAQ topic.",
                best_score
            )

        # Return matching answer
        return (
            self.faqs[best_index]["answer"],
            best_score
        )


# Chatbot Application Class
class ChatbotApp:

    # Initialize Application
    def __init__(self, root):

        self.root = root

        # Window Settings
        self.root.title("🤖 FAQ Chatbot")
        self.root.geometry("720x560")
        self.root.minsize(560, 440)

        # Load Chatbot
        try:
            self.bot = FAQChatbot(FAQ_FILE)

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            ValueError
        ) as error:

            messagebox.showerror(
                "Startup Error",
                f"Could not load FAQs:\n\n{error}"
            )

            root.destroy()
            return

        # Create User Interface
        self.create_ui()

        # Welcome Message
        self.add_message(
            "Bot",
            "Hi! 👋 Welcome to the FAQ Chatbot!\n"
            "Ask me something about AI, Python, "
            "Data Science, Machine Learning, etc."
        )

    # Create User Interface
    def create_ui(self):

        # Header
        header = tk.Label(
            self.root,
            text="🤖 FAQ Chatbot",
            font=("Segoe UI", 20, "bold"),
            pady=15
        )

        header.pack(fill="x")

        # Chat Area
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state="disabled",
            font=("Segoe UI", 11),
            padx=12,
            pady=12
        )

        self.chat_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        # Bottom Input Area
        bottom_frame = tk.Frame(
            self.root,
            padx=10,
            pady=10
        )

        bottom_frame.pack(
            fill="x",
            side="bottom"
        )

        # Ask Label
        input_label = tk.Label(
            bottom_frame,
            text="Ask:",
            font=("Segoe UI", 11, "bold")
        )

        input_label.pack(
            side="left",
            padx=(0, 8)
        )

        # Input Box
        self.input_box = tk.Entry(
            bottom_frame,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )

        self.input_box.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        # Enter Key
        self.input_box.bind(
            "<Return>",
            self.send_message
        )

        # Send Button
        send_button = tk.Button(
            bottom_frame,
            text="Send",
            command=self.send_message,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        )

        send_button.pack(
            side="left",
            padx=(8, 0)
        )

        # Clear Button
        clear_button = tk.Button(
            bottom_frame,
            text="Clear",
            command=self.clear_chat,
            font=("Segoe UI", 10),
            padx=15,
            pady=8
        )

        clear_button.pack(
            side="left",
            padx=(8, 0)
        )

        # Focus Input Box
        self.input_box.focus_force()

    # Add Message to Chat
    def add_message(self, sender, message):

        self.chat_area.configure(
            state="normal"
        )

        self.chat_area.insert(
            tk.END,
            f"{sender}: {message}\n\n"
        )

        self.chat_area.configure(
            state="disabled"
        )

        self.chat_area.see(tk.END)

    # Send Message
    def send_message(self, event=None):

        # Get User Question
        user_text = self.input_box.get().strip()

        # Ignore Empty Input
        if not user_text:
            return "break"

        # Display User Message
        self.add_message(
            "You",
            user_text
        )

        # Clear Input Box
        self.input_box.delete(
            0,
            tk.END
        )

        # Exit Commands
        if user_text.lower() in {
            "quit",
            "exit",
            "bye"
        }:

            self.add_message(
                "Bot",
                "Goodbye! 👋"
            )

            self.root.after(
                700,
                self.root.destroy
            )

            return "break"

        # Get Chatbot Answer
        answer, score = self.bot.get_answer(
            user_text
        )

        # Display Bot Answer
        self.add_message(
            "Bot",
            answer
        )

        return "break"

    # Clear Chat
    def clear_chat(self):

        self.chat_area.configure(
            state="normal"
        )

        self.chat_area.delete(
            "1.0",
            tk.END
        )

        self.chat_area.configure(
            state="disabled"
        )

        self.add_message(
            "Bot",
            "Chat cleared! Ask me another question. 😊"
        )


# Run Application
if __name__ == "__main__":

    root = tk.Tk()

    app = ChatbotApp(root)

    root.mainloop()