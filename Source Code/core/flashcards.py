from dataclasses import dataclass
from typing import List, Dict, Optional
import random
from core.storage import JSONStorage


@dataclass
class Flashcard:
    q: str
    a: str
    
    def to_dict(self):
        return {"q": self.q, "a": self.a}
    
    @classmethod
    def from_dict(cls, data):
        return cls(q=data["q"], a=data["a"])


class Flashcards:
    def __init__(self, storage: JSONStorage):
        self.storage = storage
        self.decks: Dict[str, List[Flashcard]] = {}
        self._load_flashcards()
    
    def _load_flashcards(self):
        """Load flashcards from storage"""
        try:
            data = self.storage.load("flashcards")
            if data:
                self.decks = {}
                for deck_name, cards_data in data.items():
                    self.decks[deck_name] = [Flashcard.from_dict(card) for card in cards_data]
        except Exception:
            self.decks = {}
    
    def _save_flashcards(self):
        """Save flashcards to storage"""
        try:
            data = {}
            for deck_name, cards in self.decks.items():
                data[deck_name] = [card.to_dict() for card in cards]
            self.storage.save("flashcards", data)
        except Exception as e:
            raise RuntimeError(f"Failed to save flashcards: {e}")
    
    def create_deck(self, name: str):
        """Create a new flashcard deck"""
        if name in self.decks:
            raise ValueError(f"Deck '{name}' already exists")
        self.decks[name] = []
        self._save_flashcards()
    
    def delete_deck(self, name: str):
        """Delete a flashcard deck"""
        if name not in self.decks:
            raise ValueError(f"Deck '{name}' does not exist")
        del self.decks[name]
        self._save_flashcards()
    
    def add_card(self, deck_name: str, question: str, answer: str):
        """Add a card to a deck"""
        if deck_name not in self.decks:
            raise ValueError(f"Deck '{deck_name}' does not exist")
        if not question.strip() or not answer.strip():
            raise ValueError("Question and answer cannot be empty")
        
        card = Flashcard(q=question.strip(), a=answer.strip())
        self.decks[deck_name].append(card)
        self._save_flashcards()
    
    def list_cards(self, deck_name: str) -> List[Flashcard]:
        """List all cards in a deck"""
        if deck_name not in self.decks:
            raise ValueError(f"Deck '{deck_name}' does not exist")
        return self.decks[deck_name].copy()
    
    def start_quiz(self, deck_name: str) -> List[Flashcard]:
        """Start a quiz with cards from a deck"""
        if deck_name not in self.decks:
            raise ValueError(f"Deck '{deck_name}' does not exist")
        if not self.decks[deck_name]:
            return []
        
        cards = self.decks[deck_name].copy()
        random.shuffle(cards)
        return cards
    
    def multiple_choice_options(self, deck_name: str, correct_answer: str) -> List[str]:
        """Generate multiple choice options for a quiz"""
        if deck_name not in self.decks:
            raise ValueError(f"Deck '{deck_name}' does not exist")
        
        # Get all unique answers from the deck
        all_answers = list(set(card.a for card in self.decks[deck_name]))
        
        # Remove the correct answer and shuffle
        wrong_answers = [ans for ans in all_answers if ans != correct_answer]
        random.shuffle(wrong_answers)
        
        # Take up to 3 wrong answers
        options = wrong_answers[:3]
        options.append(correct_answer)
        random.shuffle(options)
        
        return options
