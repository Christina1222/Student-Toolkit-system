import sqlite3
import json
import datetime
from F_models import Flashcard, OpenQuestionFlashcard, MultipleChoiceFlashcard, flashcard_from_dict

class Database:
    def __init__(self, db_path="flashcard.db"):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        """Initialize database tables if they don't exist"""
        # Check if Flashcards table has the new columns
        self.cur.execute("PRAGMA table_info(Flashcards)")
        columns = [column[1] for column in self.cur.fetchall()]
        
        # If table doesn't exist or doesn't have the new columns, recreate it
        if not columns or 'formatted_id' not in columns:
            # Drop the old table if it exists
            self.cur.execute("DROP TABLE IF EXISTS Flashcards")
            
            # Create new table with formatted_id column
            self.cur.execute("""CREATE TABLE Flashcards(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                formatted_id TEXT UNIQUE,
                type TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                options TEXT,
                correct_answer_index INTEGER
            )""")
            
            # Also drop and recreate the progress tables to ensure consistency
            self.cur.execute("DROP TABLE IF EXISTS flashcard_progress")
            self.cur.execute("DROP TABLE IF EXISTS spaced_repetition")
            
            self.cur.execute("""CREATE TABLE flashcard_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flashcard_id INTEGER NOT NULL,
                user_answer TEXT,
                is_correct BOOLEAN,
                difficulty_rating INTEGER,
                response_time REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flashcard_id) REFERENCES Flashcards(id)
            )""")
            
            self.cur.execute("""CREATE TABLE spaced_repetition (
                flashcard_id INTEGER PRIMARY KEY,
                next_review DATETIME,
                interval_days INTEGER DEFAULT 1,
                ease_factor REAL DEFAULT 2.5,
                review_count INTEGER DEFAULT 0,
                last_reviewed DATETIME,
                FOREIGN KEY (flashcard_id) REFERENCES Flashcards(id)
            )""")
            
            self.conn.commit()
    
    def _generate_formatted_id(self):
        """Generate a formatted ID like F001, F002, etc."""
        self.cur.execute("SELECT formatted_id FROM Flashcards ORDER BY formatted_id")
        existing_ids = [row[0] for row in self.cur.fetchall()]
        
        # Find the next available ID
        if not existing_ids:
            return "F001"
        
        # Extract numeric parts and find the maximum
        max_num = 0
        for fid in existing_ids:
            if fid and fid.startswith('F'):
                try:
                    num = int(fid[1:])
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        
        next_num = max_num + 1
        return f"F{next_num:03d}"
    
    def _renumber_formatted_ids(self):
        """Renumber all formatted IDs sequentially after deletion"""
        self.cur.execute("SELECT id FROM Flashcards ORDER BY id")
        rows = self.cur.fetchall()
        
        for index, (card_id,) in enumerate(rows, 1):
            formatted_id = f"F{index:03d}"
            self.cur.execute(
                "UPDATE Flashcards SET formatted_id = ? WHERE id = ?",
                (formatted_id, card_id)
            )
        
        self.conn.commit()
    
    def add_flashcard(self, card_type, question, answer, options=None, correct_answer_index=None):
        """Add a new flashcard to the database"""
        formatted_id = self._generate_formatted_id()
        
        if card_type == "multiple":
            options_json = json.dumps(options) if options else None
            self.cur.execute(
                "INSERT INTO Flashcards (formatted_id, type, question, answer, options, correct_answer_index) VALUES (?, ?, ?, ?, ?, ?)",
                (formatted_id, card_type, question, answer, options_json, correct_answer_index)
            )
        else:
            self.cur.execute(
                "INSERT INTO Flashcards (formatted_id, type, question, answer) VALUES (?, ?, ?, ?)",
                (formatted_id, card_type, question, answer)
            )
        self.conn.commit()
        return self.cur.lastrowid
    
    def get_all_flashcards(self):
        """Get all flashcards from database as flashcard objects"""
        self.cur.execute("SELECT id, formatted_id, type, question, answer, options, correct_answer_index FROM Flashcards ORDER BY formatted_id")
        rows = self.cur.fetchall()
        
        flashcards = []
        for row in rows:
            card_id, formatted_id, card_type, question, answer, options_json, correct_index = row
            
            # Create flashcard data dictionary
            flashcard_data = {
                "id": card_id,
                "formatted_id": formatted_id,
                "type": card_type,
                "question": question,
                "answer": answer
            }
            
            # For multiple choice questions, load options and correct answer index
            if card_type == "multiple" and options_json:
                try:
                    flashcard_data["options"] = json.loads(options_json)
                    flashcard_data["correct_answer"] = correct_index if correct_index is not None else 0
                except json.JSONDecodeError:
                    flashcard_data["options"] = []
                    flashcard_data["correct_answer"] = 0
            
            # Convert to flashcard object
            flashcard = flashcard_from_dict(flashcard_data)
            flashcards.append(flashcard)
        
        return flashcards
    
    def delete_flashcard(self, flashcard_id):
        """Delete a specific flashcard and its related data"""
        self.cur.execute("DELETE FROM Flashcards WHERE id = ?", (flashcard_id,))
        self.cur.execute("DELETE FROM flashcard_progress WHERE flashcard_id = ?", (flashcard_id,))
        self.cur.execute("DELETE FROM spaced_repetition WHERE flashcard_id = ?", (flashcard_id,))
        self.conn.commit()
        
        # Do NOT renumber formatted IDs - keep them unique and persistent
        # Deleted IDs will not be reused, maintaining ID uniqueness
    
    def delete_all_flashcards(self):
        """Delete all flashcards and related data"""
        self.cur.execute("DELETE FROM Flashcards")
        self.cur.execute("DELETE FROM flashcard_progress")
        self.cur.execute("DELETE FROM spaced_repetition")
        self.conn.commit()
    
    def record_flashcard_response(self, flashcard_id, user_answer, is_correct):
        """Record user response for progress tracking"""
        self.cur.execute(
            "INSERT INTO flashcard_progress (flashcard_id, user_answer, is_correct) VALUES (?, ?, ?)",
            (flashcard_id, user_answer, is_correct)
        )
        self.conn.commit()
    
    def get_progress_stats(self):
        """Get progress statistics"""
        # Get total flashcards
        self.cur.execute("SELECT COUNT(*) FROM Flashcards")
        total_flashcards = self.cur.fetchone()[0] or 0
        
        # Get studied flashcards
        self.cur.execute("SELECT COUNT(DISTINCT flashcard_id) FROM flashcard_progress")
        studied_flashcards = self.cur.fetchone()[0] or 0
        
        # Get accuracy stats
        self.cur.execute("""
            SELECT 
                COUNT(*) as total_attempts,
                SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct_attempts
            FROM flashcard_progress
        """)
        result = self.cur.fetchone()
        total_attempts = result[0] or 0 if result else 0
        correct_attempts = result[1] or 0 if result and result[0] else 0
        
        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            'total': total_flashcards,
            'studied': studied_flashcards,
            'accuracy': round(accuracy, 1),
            'correct': correct_attempts,
            'incorrect': total_attempts - correct_attempts
        }
    
    def update_spaced_repetition(self, flashcard_id, is_correct):
        """Update spaced repetition schedule"""
        # Get current spaced repetition data
        self.cur.execute("SELECT * FROM spaced_repetition WHERE flashcard_id = ?", (flashcard_id,))
        result = self.cur.fetchone()
        
        now = datetime.datetime.now()
        
        if result is None:
            # First review
            interval = 1
            ease_factor = 2.5
            review_count = 1
            
            if is_correct:
                interval = 1  # Review tomorrow
            else:
                interval = 1  # Review again today
            
            next_review = now + datetime.timedelta(days=interval)
            
            self.cur.execute("""
                INSERT INTO spaced_repetition 
                (flashcard_id, next_review, interval_days, ease_factor, review_count, last_reviewed)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (flashcard_id, next_review, interval, ease_factor, review_count, now))
            
        else:
            # Existing card - apply simple spaced repetition
            _, _, current_interval, current_ease, review_count, last_reviewed = result
            
            if is_correct:
                # Successful recall - increase interval
                if review_count == 0:
                    interval = 1
                elif review_count == 1:
                    interval = 2
                elif review_count == 2:
                    interval = 5
                else:
                    interval = 10
                
                review_count += 1
            else:
                # Failed recall - reset interval
                interval = 1
                review_count = max(0, review_count - 1)
            
            next_review = now + datetime.timedelta(days=interval)
            
            self.cur.execute("""
                UPDATE spaced_repetition 
                SET next_review = ?, interval_days = ?, review_count = ?, last_reviewed = ?
                WHERE flashcard_id = ?
            """, (next_review, interval, review_count, now, flashcard_id))
        
        self.conn.commit()
    
    def get_due_flashcards(self):
        """Get flashcards that are due for review"""
        self.cur.execute("SELECT flashcard_id FROM spaced_repetition WHERE next_review <= datetime('now')")
        return [row[0] for row in self.cur.fetchall()]
    
    def get_review_level(self, flashcard_id):
        """Get the review level for a flashcard"""
        self.cur.execute("SELECT review_count FROM spaced_repetition WHERE flashcard_id = ?", (flashcard_id,))
        result = self.cur.fetchone()
        return result[0] if result else 0
    
    def update_flashcard(self, flashcard_id, question, answer, options=None, correct_answer_index=None):
        """Update an existing flashcard"""
        # First get the current flashcard type
        self.cur.execute("SELECT type FROM Flashcards WHERE id = ?", (flashcard_id,))
        result = self.cur.fetchone()
        
        if not result:
            raise ValueError("Flashcard not found")
        
        card_type = result[0]
        
        if card_type == "multiple":
            options_json = json.dumps(options) if options else None
            self.cur.execute(
                "UPDATE Flashcards SET question = ?, answer = ?, options = ?, correct_answer_index = ? WHERE id = ?",
                (question, answer, options_json, correct_answer_index, flashcard_id)
            )
        else:
            self.cur.execute(
                "UPDATE Flashcards SET question = ?, answer = ? WHERE id = ?",
                (question, answer, flashcard_id)
            )
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close()
