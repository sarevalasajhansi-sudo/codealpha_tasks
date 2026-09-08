import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import random
import os
from PIL import Image, ImageTk

from chatbot import FAQChatbot
from themes import get_theme
from export_chat import export_as_txt, export_as_pdf


class FAQChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI & Technology FAQ Chatbot")
        self.root.geometry("950x750")
        self.root.minsize(800, 650)

        self.chatbot = FAQChatbot()
        self.chat_history = []
        self.theme_mode = "light"
        self.theme = get_theme(self.theme_mode)

        self.typing = False
        self.typing_label = None

        self.bg = self.theme["bg"]
        self.chat_bg = self.theme["chat_bg"]
        self.input_bg = self.theme["input_bg"]
        self.text_color = self.theme["text"]
        self.secondary_text = self.theme["secondary_text"]
        self.dark_pink = self.theme["primary"]
        self.light_pink = self.theme["primary_light"]
        self.user_color = self.theme["user"]
        self.border = self.theme["border"]
        self.button_text = self.theme["button_text"]

        self.root.configure(bg=self.bg)

        self.build_ui()
        self.show_welcome_message()

    def build_ui(self):
        self.header = tk.Frame(
            self.root,
            bg=self.bg,
            height=78
        )
        self.header.pack(fill="x", padx=18, pady=(12, 0))
        self.header.pack_propagate(False)

        self.title_label = tk.Label(
            self.header,
            text="AI & Technology FAQ Chatbot",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg,
            fg=self.dark_pink
        )
        self.title_label.pack(pady=(5, 0))

        self.subtitle_label = tk.Label(
            self.header,
            text="Ask questions about Artificial Intelligence and Technology",
            font=("Segoe UI", 10),
            bg=self.bg,
            fg=self.secondary_text
        )
        self.subtitle_label.pack()

        self.status_label = tk.Label(
            self.header,
            text="● Online",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg,
            fg=self.dark_pink
        )
        self.status_label.pack(pady=(2, 0))

        self.chat_container = tk.Frame(
            self.root,
            bg=self.chat_bg,
            highlightthickness=1,
            highlightbackground=self.border
        )
        self.chat_container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(5, 8)
        )

        self.chat_canvas = tk.Canvas(
            self.chat_container,
            bg=self.chat_bg,
            highlightthickness=0,
            bd=0
        )
        self.chat_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar = tk.Scrollbar(
            self.chat_container,
            orient="vertical",
            command=self.chat_canvas.yview
        )
        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.chat_frame = tk.Frame(
            self.chat_canvas,
            bg=self.chat_bg
        )

        self.chat_window = self.chat_canvas.create_window(
            (0, 0),
            window=self.chat_frame,
            anchor="nw"
        )

        self.chat_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.chat_canvas.bind(
            "<Configure>",
            self.resize_chat_frame
        )

        self.chat_canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

        self.suggestion_title = tk.Label(
            self.root,
            text="Suggested Questions",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg,
            fg=self.text_color,
            anchor="w"
        )
        self.suggestion_title.pack(
            fill="x",
            padx=20,
            pady=(0, 5)
        )

        self.suggestions_frame = tk.Frame(
            self.root,
            bg=self.bg
        )
        self.suggestions_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        self.suggestions = [
            "What is AI?",
            "What is machine learning?",
            "What is NLP?",
            "What is deep learning?"
        ]

        self.suggestion_buttons = []

        for question in self.suggestions:
            button = tk.Button(
                self.suggestions_frame,
                text=question,
                font=("Segoe UI", 9),
                bg=self.light_pink,
                fg=self.dark_pink,
                activebackground=self.dark_pink,
                activeforeground="white",
                relief="flat",
                bd=0,
                padx=12,
                pady=7,
                cursor="hand2",
                command=lambda q=question: self.use_suggestion(q)
            )
            button.pack(
                side="left",
                padx=(0, 7)
            )
            self.suggestion_buttons.append(button)

        self.input_frame = tk.Frame(
            self.root,
            bg=self.bg
        )
        self.input_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        self.message_entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            bd=0
        )
        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=11,
            padx=(0, 8)
        )

        self.message_entry.bind(
            "<Return>",
            self.handle_enter
        )

        self.send_button = tk.Button(
            self.input_frame,
            text="Send  ➤",
            font=("Segoe UI", 10, "bold"),
            bg=self.dark_pink,
            fg="white",
            activebackground=self.dark_pink,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=22,
            pady=9,
            cursor="hand2",
            command=self.send_message
        )
        self.send_button.pack(
            side="right"
        )

        self.actions_frame = tk.Frame(
            self.root,
            bg=self.bg
        )
        self.actions_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 12)
        )

        self.clear_button = tk.Button(
            self.actions_frame,
            text="Clear Chat",
            font=("Segoe UI", 9),
            bg=self.light_pink,
            fg=self.button_text,
            activebackground=self.dark_pink,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.clear_chat
        )
        self.clear_button.pack(side="left", padx=(0, 7))

        self.history_button = tk.Button(
            self.actions_frame,
            text="Chat History",
            font=("Segoe UI", 9),
            bg=self.light_pink,
            fg=self.button_text,
            activebackground=self.dark_pink,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.show_history
        )
        self.history_button.pack(side="left", padx=(0, 7))

        self.save_button = tk.Button(
            self.actions_frame,
            text="Save Chat",
            font=("Segoe UI", 9),
            bg=self.light_pink,
            fg=self.button_text,
            activebackground=self.dark_pink,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.save_chat
        )
        self.save_button.pack(side="left", padx=(0, 7))

        self.clear_history_button = tk.Button(
            self.actions_frame,
            text="Clear History",
            font=("Segoe UI", 9),
            bg=self.light_pink,
            fg=self.button_text,
            activebackground=self.dark_pink,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.clear_history
        )
        self.clear_history_button.pack(side="left", padx=(0, 7))

        self.theme_button = tk.Button(
            self.actions_frame,
            text="☾ Dark Mode",
            font=("Segoe UI", 9),
            bg=self.light_pink,
            fg=self.button_text,
            activebackground=self.dark_pink,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right")

    def update_scroll_region(self, event=None):
        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )
        self.root.after(
            50,
            lambda: self.chat_canvas.yview_moveto(1.0)
        )

    def resize_chat_frame(self, event):
        self.chat_canvas.itemconfig(
            self.chat_window,
            width=event.width
        )

    def mouse_scroll(self, event):
        self.chat_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def show_welcome_message(self):
        self.add_bot_message(
            "Hello! 👋\n\n"
            "I can answer questions about Artificial Intelligence "
            "and Technology.\n\n"
            "Choose a suggested question or type your own question below."
        )

    def add_user_message(self, message):
        outer = tk.Frame(
            self.chat_frame,
            bg=self.chat_bg
        )
        outer.pack(
            fill="x",
            padx=12,
            pady=(8, 4)
        )

        bubble_area = tk.Frame(
            outer,
            bg=self.chat_bg
        )
        bubble_area.pack(
            anchor="e"
        )

        name_label = tk.Label(
            bubble_area,
            text="👤 You",
            font=("Segoe UI", 9, "bold"),
            bg=self.chat_bg,
            fg=self.user_color,
            anchor="e"
        )
        name_label.pack(
            anchor="e",
            padx=10,
            pady=(0, 3)
        )

        bubble = tk.Label(
            bubble_area,
            text=message,
            font=("Segoe UI", 10),
            bg=self.user_color,
            fg="white",
            justify="left",
            anchor="w",
            wraplength=600,
            padx=16,
            pady=10
        )
        bubble.pack(
            anchor="e"
        )

        timestamp = tk.Label(
            bubble_area,
            text=datetime.now().strftime("%I:%M %p"),
            font=("Segoe UI", 8),
            bg=self.chat_bg,
            fg=self.secondary_text,
            anchor="e"
        )
        timestamp.pack(
            anchor="e",
            padx=10,
            pady=(3, 0)
        )

    def add_bot_message(self, message, confidence=None):
        outer = tk.Frame(
            self.chat_frame,
            bg=self.chat_bg
        )
        outer.pack(
            fill="x",
            padx=12,
            pady=(8, 4)
        )

        bubble_area = tk.Frame(
            outer,
            bg=self.chat_bg
        )
        bubble_area.pack(
            anchor="w"
        )

        name_label = tk.Label(
            bubble_area,
            text="🤖 Bot",
            font=("Segoe UI", 9, "bold"),
            bg=self.chat_bg,
            fg=self.dark_pink,
            anchor="w"
        )
        name_label.pack(
            anchor="w",
            padx=10,
            pady=(0, 3)
        )

        bubble = tk.Label(
            bubble_area,
            text=message,
            font=("Segoe UI", 10),
            bg=self.light_pink,
            fg=self.text_color,
            justify="left",
            anchor="w",
            wraplength=650,
            padx=16,
            pady=10
        )
        bubble.pack(
            anchor="w"
        )

        info_frame = tk.Frame(
            bubble_area,
            bg=self.chat_bg
        )
        info_frame.pack(
            anchor="w",
            padx=10,
            pady=(3, 0)
        )

        if confidence is not None:
            confidence_label = tk.Label(
                info_frame,
                text=f"Similarity: {confidence:.1%}",
                font=("Segoe UI", 8),
                bg=self.chat_bg,
                fg=self.secondary_text
            )
            confidence_label.pack(
                side="left"
            )

        timestamp = tk.Label(
            info_frame,
            text=datetime.now().strftime("  •  %I:%M %p"),
            font=("Segoe UI", 8),
            bg=self.chat_bg,
            fg=self.secondary_text
        )
        timestamp.pack(
            side="left"
        )

    def show_typing_indicator(self):
        if self.typing_label is not None:
            return

        outer = tk.Frame(
            self.chat_frame,
            bg=self.chat_bg
        )
        outer.pack(
            fill="x",
            padx=12,
            pady=(8, 4)
        )

        self.typing_outer = outer

        bubble_area = tk.Frame(
            outer,
            bg=self.chat_bg
        )
        bubble_area.pack(
            anchor="w"
        )

        name_label = tk.Label(
            bubble_area,
            text="🤖 Bot",
            font=("Segoe UI", 9, "bold"),
            bg=self.chat_bg,
            fg=self.dark_pink
        )
        name_label.pack(
            anchor="w",
            padx=10,
            pady=(0, 3)
        )

        self.typing_label = tk.Label(
            bubble_area,
            text="Bot is typing...",
            font=("Segoe UI", 10, "italic"),
            bg=self.light_pink,
            fg=self.secondary_text,
            padx=16,
            pady=10
        )
        self.typing_label.pack(
            anchor="w"
        )

        self.typing_dots = 0
        self.animate_typing()

        self.root.after(
            50,
            lambda: self.chat_canvas.yview_moveto(1.0)
        )

    def animate_typing(self):
        if not self.typing or self.typing_label is None:
            return

        self.typing_dots = (self.typing_dots + 1) % 4

        dots = "." * self.typing_dots

        self.typing_label.config(
            text=f"Bot is typing{dots}"
        )

        self.root.after(
            400,
            self.animate_typing
        )

    def remove_typing_indicator(self):
        if self.typing_outer is not None:
            self.typing_outer.destroy()

        self.typing_outer = None
        self.typing_label = None

    def handle_enter(self, event):
        self.send_message()
        return "break"

    def send_message(self):
        if self.typing:
            return

        question = self.message_entry.get().strip()

        if not question:
            return

        self.message_entry.delete(0, tk.END)

        self.add_user_message(question)

        self.chat_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": question,
            "bot": None,
            "confidence": None
        })

        self.typing = True
        self.send_button.config(
            state="disabled",
            text="Typing..."
        )
        self.message_entry.config(
            state="disabled"
        )

        self.show_typing_indicator()

        self.root.after(
            900,
            lambda q=question: self.generate_response(q)
        )

    def generate_response(self, question):
        try:
            result = self.chatbot.get_response(question)

            answer = result["answer"]
            confidence = result.get("confidence", 0)

        except Exception:
            answer = (
                "Sorry, I couldn't process that question right now. "
                "Please try asking it in another way."
            )
            confidence = 0

        self.remove_typing_indicator()

        self.add_bot_message(
            answer,
            confidence
        )

        if self.chat_history:
            self.chat_history[-1]["bot"] = answer
            self.chat_history[-1]["confidence"] = confidence

        self.typing = False

        self.send_button.config(
            state="normal",
            text="Send  ➤"
        )

        self.message_entry.config(
            state="normal"
        )

        self.message_entry.focus_set()

        self.root.after(
            250,
            self.show_heart_animation
        )

    def use_suggestion(self, question):
        if self.typing:
            return

        self.message_entry.delete(
            0,
            tk.END
        )

        self.message_entry.insert(
            0,
            question
        )

        self.send_message()

    def clear_chat(self):
        if self.typing:
            return

        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        self.show_welcome_message()

    def show_history(self):
        if not self.chat_history:
            messagebox.showinfo(
                "Chat History",
                "No chat history available yet."
            )
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Chat History")
        history_window.geometry("750x600")
        history_window.configure(
            bg=self.bg
        )

        title = tk.Label(
            history_window,
            text="Chat History",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg,
            fg=self.dark_pink
        )
        title.pack(
            pady=(15, 10)
        )

        text_frame = tk.Frame(
            history_window,
            bg=self.bg
        )
        text_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 15)
        )

        history_text = tk.Text(
            text_frame,
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            relief="flat",
            wrap="word",
            padx=15,
            pady=15
        )
        history_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        history_scroll = tk.Scrollbar(
            text_frame,
            command=history_text.yview
        )
        history_scroll.pack(
            side="right",
            fill="y"
        )

        history_text.configure(
            yscrollcommand=history_scroll.set
        )

        for item in self.chat_history:
            history_text.insert(
                tk.END,
                f"{item['timestamp']}\n",
            )

            history_text.insert(
                tk.END,
                f"You: {item['user']}\n"
            )

            history_text.insert(
                tk.END,
                f"Bot: {item['bot']}\n"
            )

            confidence = item.get("confidence")

            if confidence is not None:
                history_text.insert(
                    tk.END,
                    f"Similarity: {confidence:.1%}\n"
                )

            history_text.insert(
                tk.END,
                "\n" + "─" * 70 + "\n\n"
            )

        history_text.config(
            state="disabled"
        )

        close_button = tk.Button(
            history_window,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg=self.dark_pink,
            fg="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=8,
            command=history_window.destroy
        )
        close_button.pack(
            pady=(0, 15)
        )

    def save_chat(self):
        if not self.chat_history:
            messagebox.showinfo(
                "Save Chat",
                "There is no chat to save yet."
            )
            return

        save_window = tk.Toplevel(self.root)
        save_window.title("Save Chat")
        save_window.geometry("360x220")
        save_window.resizable(False, False)
        save_window.configure(
            bg=self.bg
        )

        title = tk.Label(
            save_window,
            text="Save Chat",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg,
            fg=self.dark_pink
        )
        title.pack(
            pady=(20, 15)
        )

        text_button = tk.Button(
            save_window,
            text="Save as TXT",
            font=("Segoe UI", 10, "bold"),
            bg=self.light_pink,
            fg=self.button_text,
            relief="flat",
            bd=0,
            padx=20,
            pady=9,
            cursor="hand2",
            command=lambda: self.save_as_txt(save_window)
        )
        text_button.pack(
            pady=5
        )

        pdf_button = tk.Button(
            save_window,
            text="Save as PDF",
            font=("Segoe UI", 10, "bold"),
            bg=self.dark_pink,
            fg="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=9,
            cursor="hand2",
            command=lambda: self.save_as_pdf(save_window)
        )
        pdf_button.pack(
            pady=5
        )

    def save_as_txt(self, window):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt")
            ],
            initialfile="chat_history.txt"
        )

        if not filename:
            return

        try:
            export_as_txt(
                self.chat_history,
                filename
            )

            window.destroy()

            messagebox.showinfo(
                "Saved",
                "Chat saved successfully as TXT."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save chat:\n{error}"
            )

    def save_as_pdf(self, window):
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf")
            ],
            initialfile="chat_history.pdf"
        )

        if not filename:
            return

        try:
            export_as_pdf(
                self.chat_history,
                filename
            )

            window.destroy()

            messagebox.showinfo(
                "Saved",
                "Chat saved successfully as PDF."
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save PDF:\n{error}"
            )

    def clear_history(self):
        if not self.chat_history:
            messagebox.showinfo(
                "Clear History",
                "There is no history to clear."
            )
            return

        answer = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all chat history?"
        )

        if answer:
            self.chat_history.clear()

            messagebox.showinfo(
                "Clear History",
                "Chat history cleared successfully."
            )

    def toggle_theme(self):
        if self.theme_mode == "light":
            self.theme_mode = "dark"
        else:
            self.theme_mode = "light"

        self.theme = get_theme(
            self.theme_mode
        )

        self.bg = self.theme["bg"]
        self.chat_bg = self.theme["chat_bg"]
        self.input_bg = self.theme["input_bg"]
        self.text_color = self.theme["text"]
        self.secondary_text = self.theme["secondary_text"]
        self.dark_pink = self.theme["primary"]
        self.light_pink = self.theme["primary_light"]
        self.user_color = self.theme["user"]
        self.border = self.theme["border"]
        self.button_text = self.theme["button_text"]

        self.apply_theme()

    def apply_theme(self):
        self.root.configure(
            bg=self.bg
        )

        self.update_widget_colors(
            self.root
        )

        if self.theme_mode == "dark":
            self.theme_button.config(
                text="☀ Light Mode"
            )
        else:
            self.theme_button.config(
                text="☾ Dark Mode"
            )

        self.refresh_chat()

    def update_widget_colors(self, widget):
        try:
            if widget == self.root:
                widget.configure(
                    bg=self.bg
                )

            elif isinstance(widget, tk.Frame):
                widget.configure(
                    bg=self.bg
                )

            elif isinstance(widget, tk.Label):
                current_bg = widget.cget("bg")

                if current_bg in [
                    "#FFF0F5",
                    "#241B20",
                    self.bg
                ]:
                    widget.configure(
                        bg=self.bg
                    )

            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=self.input_bg,
                    fg=self.text_color,
                    insertbackground=self.text_color
                )

            elif isinstance(widget, tk.Button):
                if widget == self.send_button:
                    widget.configure(
                        bg=self.dark_pink,
                        fg="white",
                        activebackground=self.dark_pink,
                        activeforeground="white"
                    )
                else:
                    widget.configure(
                        bg=self.light_pink,
                        fg=self.button_text,
                        activebackground=self.dark_pink,
                        activeforeground="white"
                    )

            elif isinstance(widget, tk.Canvas):
                widget.configure(
                    bg=self.chat_bg
                )

        except tk.TclError:
            pass

        for child in widget.winfo_children():
            self.update_widget_colors(
                child
            )

    def refresh_chat(self):
        messages = []

        for item in self.chat_history:
            if item.get("user"):
                messages.append(
                    ("user", item["user"])
                )

            if item.get("bot"):
                messages.append(
                    (
                        "bot",
                        item["bot"],
                        item.get("confidence")
                    )
                )

        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        if not messages:
            self.show_welcome_message()
            return

        for message in messages:
            if message[0] == "user":
                self.add_user_message(
                    message[1]
                )
            else:
                self.add_bot_message(
                    message[1],
                    message[2]
                )

    def show_heart_animation(self):
        animation = tk.Toplevel(self.root)
        animation.overrideredirect(True)
        animation.attributes(
            "-topmost",
            True
        )
        animation.configure(
            bg=self.bg
        )

        width = 300
        height = 230

        screen_width = animation.winfo_screenwidth()
        screen_height = animation.winfo_screenheight()

        x = int(
            (screen_width - width) / 2
        )
        y = int(
            (screen_height - height) / 2
        )

        animation.geometry(
            f"{width}x{height}+{x}+{y}"
        )

        canvas = tk.Canvas(
            animation,
            width=width,
            height=height,
            bg=self.bg,
            highlightthickness=0
        )
        canvas.pack(
            fill="both",
            expand=True
        )

        heart = canvas.create_text(
            150,
            70,
            text="♥",
            font=("Arial", 65, "bold"),
            fill=self.dark_pink
        )

        message = canvas.create_text(
            150,
            145,
            text="Answer ready!",
            font=("Segoe UI", 15, "bold"),
            fill=self.text_color
        )

        subtitle = canvas.create_text(
            150,
            175,
            text="Here is what I found for you ✨",
            font=("Segoe UI", 9),
            fill=self.secondary_text
        )

        shinchan_image = self.load_shinchan()

        if shinchan_image:
            canvas.create_image(
                150,
                215,
                image=shinchan_image
            )
            animation.shinchan_image = shinchan_image

        self.animate_heart(
            animation,
            canvas,
            heart,
            0
        )

    def animate_heart(
        self,
        window,
        canvas,
        heart,
        step
    ):
        if not window.winfo_exists():
            return

        if step >= 12:
            window.after(
                700,
                window.destroy
            )
            return

        size = 65 + (
            8 * abs(
                6 - step
            )
        )

        canvas.itemconfig(
            heart,
            font=("Arial", size, "bold")
        )

        window.after(
            70,
            lambda: self.animate_heart(
                window,
                canvas,
                heart,
                step + 1
            )
        )

    def load_shinchan(self):
        possible_paths = [
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                ),
                "shinchan.png"
            ),
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)
                ),
                "assets",
                "shinchan.png"
            )
        ]

        for path in possible_paths:
            if os.path.exists(path):
                try:
                    image = Image.open(
                        path
                    )

                    image.thumbnail(
                        (75, 75)
                    )

                    return ImageTk.PhotoImage(
                        image
                    )

                except Exception:
                    return None

        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = FAQChatbotGUI(root)
    root.mainloop()