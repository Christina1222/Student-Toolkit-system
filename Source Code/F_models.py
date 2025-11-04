
# Inheritance type of flashcard

class Flashcard:
    
    def __init__(self, id=None, formatted_id=None, question="", answer="", card_type="base"):
        self.id = id
        self.formatted_id = formatted_id
        self.question = question
        self.answer = answer
        self.type = card_type
    # Convert flashcard to dictionary format for database storage
    def to_dict(self):
        return {
            "id": self.id,
            "formatted_id": self.formatted_id,
            "type": self.type,
            "question": self.question,
            "answer": self.answer
        }
    
    def __str__(self):
        return f"{self.formatted_id}: {self.question} -> {self.answer}"
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}, formatted_id={self.formatted_id}>"

class OpenQuestionFlashcard(Flashcard):
    # Flashcard for open-ended questions
    def __init__(self, id=None, formatted_id=None, question="", answer=""):
        super().__init__(id, formatted_id, question, answer, "open")
    
    def to_dict(self):
        """Convert to dictionary format"""
        data = super().to_dict()
        return data

class MultipleChoiceFlashcard(Flashcard):
    # Flashcard for multiple choice questions
    def __init__(self, id=None, formatted_id=None, question="", answer="", options=None, correct_answer_index=0):
        super().__init__(id, formatted_id, question, answer, "multiple")
        self.options = options or []
        self.correct_answer_index = correct_answer_index
    
    def to_dict(self):
        """Convert to dictionary format"""
        data = super().to_dict()
        data.update({
            "options": self.options,
            "correct_answer": self.correct_answer_index
        })
        return data
    
    def get_correct_option(self):
        """Get the correct option text"""
        if self.options and 0 <= self.correct_answer_index < len(self.options):
            return self.options[self.correct_answer_index]
        return ""
    
    def __str__(self):
        options_str = "\n".join([f"  {i+1}. {opt}" for i, opt in enumerate(self.options)])
        return f"{self.formatted_id}: {self.question}\n{options_str}\nCorrect: {self.get_correct_option()}"

def flashcard_from_dict(data):
    # Factory function to create appropriate flashcard object from dictionary
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")
    
    card_type = data.get("type", "open")
    
    if card_type == "open":
        return OpenQuestionFlashcard(
            id=data.get("id"),
            formatted_id=data.get("formatted_id"),
            question=data.get("question", ""),
            answer=data.get("answer", "")
        )
    elif card_type == "multiple":
        return MultipleChoiceFlashcard(
            id=data.get("id"),
            formatted_id=data.get("formatted_id"),
            question=data.get("question", ""),
            answer=data.get("answer", ""),
            options=data.get("options", []),
            correct_answer_index=data.get("correct_answer", 0)
        )
    else:
        raise ValueError(f"Unknown flashcard type: {card_type}")
