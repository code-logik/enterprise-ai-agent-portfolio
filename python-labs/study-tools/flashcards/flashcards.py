"""
AI Certification Visual Flashcard Study Tool

A reusable desktop flashcard application built with Python's standard
Tkinter library.

Add weekly decks to the decks folder using this naming convention:

    week_02.json
    week_03.json
    week_04.json

The application discovers valid weekly decks automatically.
"""

import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


BASE_DIR = Path(__file__).resolve().parent
DECKS_DIR = BASE_DIR / "decks"
DECK_PATTERN = "week_[0-9][0-9].json"


class FlashcardApp:
    """Visual flashcard study application."""

    def __init__(self, root):
        self.root = root
        self.root.title("AI Certification Flashcards")
        self.root.geometry("960x700")
        self.root.minsize(800, 600)

        self.decks = []
        self.study_cards = []
        self.review_cards = []
        self.current_index = 0
        self.showing_answer = False
        self.known_count = 0

        self.deck_var = tk.StringVar()
        self.shuffle_var = tk.BooleanVar(value=True)
        self.progress_var = tk.DoubleVar(value=0)

        self._configure_styles()
        self._build_ui()
        self._load_decks()
        self._bind_keys()

    def _configure_styles(self):
        """Configure ttk widget styles."""
        style = ttk.Style()

        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
        )
        style.configure(
            "CardHeader.TLabel",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "CardText.TLabel",
            font=("Segoe UI", 18),
            justify="center",
        )
        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(14, 10),
        )

    def _build_ui(self):
        """Create the visual interface."""
        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer,
            text="AI Certification Flashcards",
            style="Title.TLabel",
        ).pack(anchor="center")

        ttk.Label(
            outer,
            text="Reusable weekly review for your AI certification curriculum",
            style="Subtitle.TLabel",
        ).pack(anchor="center", pady=(4, 18))

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(0, 14))

        ttk.Label(
            controls,
            text="Deck:",
            style="CardHeader.TLabel",
        ).pack(side="left")

        self.deck_combo = ttk.Combobox(
            controls,
            textvariable=self.deck_var,
            state="readonly",
            width=58,
        )
        self.deck_combo.pack(side="left", padx=(8, 12), fill="x", expand=True)

        ttk.Checkbutton(
            controls,
            text="Shuffle",
            variable=self.shuffle_var,
        ).pack(side="left", padx=(0, 12))

        ttk.Button(
            controls,
            text="Start",
            command=self.start_session,
            style="Action.TButton",
        ).pack(side="left")

        self.progress = ttk.Progressbar(
            outer,
            variable=self.progress_var,
            maximum=100,
        )
        self.progress.pack(fill="x", pady=(0, 8))

        self.status_label = ttk.Label(
            outer,
            text="Select a deck and click Start.",
            style="Status.TLabel",
        )
        self.status_label.pack(anchor="center", pady=(0, 14))

        self.card = tk.Frame(
            outer,
            bg="#ffffff",
            highlightbackground="#c7c7c7",
            highlightthickness=1,
            bd=0,
        )
        self.card.pack(fill="both", expand=True, padx=22, pady=(0, 18))

        self.card_category = tk.Label(
            self.card,
            text="READY",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#666666",
        )
        self.card_category.pack(pady=(34, 12))

        self.card_side = tk.Label(
            self.card,
            text="QUESTION",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#555555",
        )
        self.card_side.pack()

        self.card_text = tk.Label(
            self.card,
            text="Choose a weekly deck to begin.",
            font=("Segoe UI", 20),
            bg="#ffffff",
            fg="#111111",
            justify="center",
            wraplength=720,
        )
        self.card_text.pack(fill="both", expand=True, padx=60, pady=35)

        self.flip_button = ttk.Button(
            outer,
            text="Reveal Answer",
            command=self.flip_card,
            style="Action.TButton",
            state="disabled",
        )
        self.flip_button.pack(pady=(0, 12))

        rating_row = ttk.Frame(outer)
        rating_row.pack(fill="x")

        self.review_button = ttk.Button(
            rating_row,
            text="Needs Review",
            command=lambda: self.rate_card(False),
            style="Action.TButton",
            state="disabled",
        )
        self.review_button.pack(side="left", expand=True, padx=(0, 6))

        self.known_button = ttk.Button(
            rating_row,
            text="Known",
            command=lambda: self.rate_card(True),
            style="Action.TButton",
            state="disabled",
        )
        self.known_button.pack(side="left", expand=True, padx=(6, 0))

        ttk.Label(
            outer,
            text=(
                "Keyboard: Space/Enter = flip   "
                "Left = needs review   Right = known"
            ),
            style="Status.TLabel",
        ).pack(anchor="center", pady=(14, 0))

    def _bind_keys(self):
        """Bind convenient keyboard shortcuts."""
        self.root.bind("<space>", self._keyboard_flip)
        self.root.bind("<Return>", self._keyboard_flip)
        self.root.bind("<Left>", self._keyboard_review)
        self.root.bind("<Right>", self._keyboard_known)

    def _keyboard_flip(self, _event):
        if str(self.flip_button["state"]) != "disabled":
            self.flip_card()

    def _keyboard_review(self, _event):
        if str(self.review_button["state"]) != "disabled":
            self.rate_card(False)

    def _keyboard_known(self, _event):
        if str(self.known_button["state"]) != "disabled":
            self.rate_card(True)

    def _load_decks(self):
        """Discover and load all valid weekly deck files."""
        self.decks = []

        if not DECKS_DIR.exists():
            messagebox.showwarning(
                "Deck folder missing",
                f"Deck folder not found:\n{DECKS_DIR}",
            )
            return

        for deck_path in sorted(DECKS_DIR.glob(DECK_PATTERN)):
            deck = self._read_deck(deck_path)

            if deck is not None:
                self.decks.append(deck)

        if not self.decks:
            messagebox.showwarning(
                "No decks found",
                "Add a file such as decks/week_02.json.",
            )
            return

        labels = [
            f"Week {deck['week']}: {deck['title']}"
            for deck in self.decks
        ]
        labels.append("All Weeks")

        self.deck_combo["values"] = labels
        self.deck_combo.current(0)

    def _read_deck(self, deck_path):
        """Read and validate one JSON flashcard deck."""
        try:
            with deck_path.open("r", encoding="utf-8") as file:
                raw = json.load(file)
        except (OSError, json.JSONDecodeError):
            return None

        if not all(key in raw for key in ("week", "title", "cards")):
            return None

        cards = []

        for card in raw["cards"]:
            if not isinstance(card, dict):
                continue

            question = card.get("question")
            answer = card.get("answer")

            if not question or not answer:
                continue

            cards.append(
                {
                    "week": raw["week"],
                    "deck_title": raw["title"],
                    "category": card.get("category", "General"),
                    "question": question,
                    "answer": answer,
                }
            )

        if not cards:
            return None

        return {
            "week": raw["week"],
            "title": raw["title"],
            "cards": cards,
        }

    def start_session(self):
        """Start a study session using the selected deck."""
        if not self.decks:
            return

        selected_index = self.deck_combo.current()

        if selected_index == len(self.decks):
            cards = []

            for deck in self.decks:
                cards.extend(deck["cards"])
        else:
            cards = self.decks[selected_index]["cards"].copy()

        if self.shuffle_var.get():
            random.shuffle(cards)

        self.study_cards = cards
        self.review_cards = []
        self.current_index = 0
        self.known_count = 0

        self._show_current_card()

    def _show_current_card(self):
        """Display the front of the current flashcard."""
        if not self.study_cards:
            return

        if self.current_index >= len(self.study_cards):
            self._finish_session()
            return

        card = self.study_cards[self.current_index]
        self.showing_answer = False

        self.card_category.config(
            text=f"WEEK {card['week']}  •  {card['category'].upper()}"
        )
        self.card_side.config(text="QUESTION")
        self.card_text.config(text=card["question"])

        self.flip_button.config(text="Reveal Answer", state="normal")
        self.review_button.config(state="disabled")
        self.known_button.config(state="disabled")

        position = self.current_index + 1
        total = len(self.study_cards)
        self.progress_var.set(((position - 1) / total) * 100)

        self.status_label.config(
            text=(
                f"Card {position} of {total}   •   "
                f"Known: {self.known_count}   •   "
                f"Needs review: {len(self.review_cards)}"
            )
        )

    def flip_card(self):
        """Flip between the question and answer sides."""
        if not self.study_cards:
            return

        card = self.study_cards[self.current_index]

        if not self.showing_answer:
            self.card_side.config(text="ANSWER")
            self.card_text.config(text=card["answer"])
            self.flip_button.config(text="Show Question")
            self.review_button.config(state="normal")
            self.known_button.config(state="normal")
            self.showing_answer = True
        else:
            self.card_side.config(text="QUESTION")
            self.card_text.config(text=card["question"])
            self.flip_button.config(text="Reveal Answer")
            self.showing_answer = False

    def rate_card(self, known):
        """Record the user's self-rating and advance."""
        if not self.showing_answer:
            return

        card = self.study_cards[self.current_index]

        if known:
            self.known_count += 1
        else:
            self.review_cards.append(card)

        self.current_index += 1
        self._show_current_card()

    def _finish_session(self):
        """Show results and optionally repeat missed cards."""
        total = len(self.study_cards)
        missed = len(self.review_cards)
        score = round((self.known_count / total) * 100) if total else 0

        self.progress_var.set(100)
        self.flip_button.config(state="disabled")
        self.review_button.config(state="disabled")
        self.known_button.config(state="disabled")

        self.card_category.config(text="SESSION COMPLETE")
        self.card_side.config(text="RESULTS")
        self.card_text.config(
            text=(
                f"Known: {self.known_count}\n\n"
                f"Needs review: {missed}\n\n"
                f"Score: {score}%"
            )
        )

        self.status_label.config(
            text=f"Completed {total} flashcards."
        )

        if missed:
            review_again = messagebox.askyesno(
                "Review missed cards?",
                (
                    f"You marked {missed} card(s) for review.\n\n"
                    "Would you like to study only those cards now?"
                ),
            )

            if review_again:
                self.study_cards = self.review_cards.copy()
                random.shuffle(self.study_cards)
                self.review_cards = []
                self.current_index = 0
                self.known_count = 0
                self._show_current_card()
                return

        messagebox.showinfo(
            "Study session complete",
            "Your flashcard study session is complete.",
        )


def main():
    """Start the visual flashcard application."""
    root = tk.Tk()
    FlashcardApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
