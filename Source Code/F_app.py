import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random 

from F_database import Database
from F_ui_components import UIComponents
from utils import COLORS
from F_models import OpenQuestionFlashcard, MultipleChoiceFlashcard

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Master")
        self.root.geometry("1000x800")
        self.root.configure(bg=COLORS["background"])
        root.resizable(True, True)
        
        # Set application icon
        try:
            self.root.iconbitmap("flashcard_icon.ico")
        except:
            pass
        
        # Initialize database
        self.database = Database()
        
        # Initialize UI components
        self.ui = UIComponents(self.root, self.database)
        
        # Create main container
        self.F_frame = ttk.Frame(root, padding=20)
        self.F_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI components
        self.create_ui_components()
        
        # Load flashcards and initialize
        self.flashcards = []
        self.load_flashcards_from_db()
        self.update_stats()
        self.update_progress_display()
        
        # Initialize with welcome screen
        self.show_welcome_screen()

    def create_ui_components(self):
        """Create all UI components"""
        # Header
        self.header_frame, self.total_label, self.progress_frame, self.stats_label = self.ui.create_header(self.F_frame)
        
        # Content area
        self.content_frame = ttk.Frame(self.F_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Footer
        self.footer_frame, self.create_btn, self.quiz_btn, self.view_btn, self.clear_btn = self.ui.create_footer(
            self.F_frame,
            self.create_flashcard_dialog,
            self.start_quiz,
            self.view_all_flashcards,
            self.clear_all_flashcards
        )

    def show_welcome_screen(self):
        """Show welcome screenmm"""
        self.ui.show_welcome_screen(self.content_frame, self.create_flashcard_dialog)
    
    def create_flashcard_dialog(self):
        """Create flashcard type selection dialog"""
        self.ui.create_flashcard_dialog(
            self.root,
            self.create_open_question,
            self.create_multiple_choice
        )

    def create_open_question(self, parent_dialog):
        """Handle open question creation"""
        parent_dialog.destroy()
        self.show_open_question_form()

    def show_open_question_form(self):
        """Show open question form"""
        form_frame, question_entry, answer_entry = self.ui.create_open_question_form(
            self.content_frame,
            self.submit_open_question,
            self.show_welcome_screen
        )
        
        self.current_question_entry = question_entry
        self.current_answer_entry = answer_entry

    def submit_open_question(self, question, answer):
        """Submit open question form"""
        if not question or not answer:
            messagebox.showerror("Error", "Both question and answer are required!")
            return
        
        # Validate length limits
        if len(question) > 250:
            messagebox.showerror("Error", "Question cannot exceed 250 characters!")
            return
        
        if len(answer) > 250:
            messagebox.showerror("Error", "Answer cannot exceed 250 characters!")
            return
        
        # Store flashcard using database
        self.database.add_flashcard("open", question, answer)
        
        # Reload flashcards and update UI
        self.load_flashcards_from_db()
        messagebox.showinfo("Success", "Open question added successfully!")
        self.update_stats()
        self.show_welcome_screen()

    def create_multiple_choice(self, parent_dialog):
        """Handle multiple choice creation"""
        parent_dialog.destroy()
        self.show_multiple_choice_form()

    def show_multiple_choice_form(self):
        """Show multiple choice form"""
        form_frame, question_entry, option_entries, correct_var = self.ui.create_multiple_choice_form(
            self.content_frame,
            self.submit_multiple_choice,
            self.show_welcome_screen
        )
        
        self.current_question_entry = question_entry
        self.current_option_entries = option_entries
        self.current_correct_var = correct_var

    def submit_multiple_choice(self, question, options, selected, answer_selected):
        """Submit multiple choice form"""
        if not question:
            messagebox.showerror("Error", "Question is required!")
            return
        
        # Validate question length
        if len(question) > 250:
            messagebox.showerror("Error", "Question cannot exceed 250 characters!")
            return
        
        if len(options) < 2:
            messagebox.showerror("Error", "At least 2 options are required!")
            return

        # Validate answer length
        if len(answer_selected) > 250:
            messagebox.showerror("Error", "Answer cannot exceed 250 characters!")
            return

        if answer_selected == "":
            messagebox.showerror("Error", "Selected answer option is empty! Please select again!")
            return

        # Store flashcard using database
        self.database.add_flashcard("multiple", question, answer_selected, options, selected)
        
        # Reload flashcards and update UI
        self.load_flashcards_from_db()
        messagebox.showinfo("Success", "Multiple choice question added successfully!")
        self.update_stats()
        self.show_welcome_screen()

    def start_quiz(self):
        """Start quiz mode"""
        if not self.flashcards:
            messagebox.showinfo("Info", "No flashcards available. Please create some first!")
            return
        
        self.clear_content()
        
        quiz_frame = ttk.Frame(self.content_frame, padding=20)
        quiz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.current_quiz_index = 0
        self.quiz_score = 0
        self.quiz_flashcards = random.sample(self.flashcards, min(10, len(self.flashcards)))
        
        self.show_quiz_question()

    def show_quiz_question(self):
        """Show current quiz question"""
        if self.current_quiz_index >= len(self.quiz_flashcards):
            self.show_quiz_results()
            return
        
        card = self.quiz_flashcards[self.current_quiz_index]
        
        # Clear previous question
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        quiz_frame = ttk.Frame(self.content_frame, padding=20)
        quiz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress
        progress_label = tk.Label(
            quiz_frame,
            text=f"Question {self.current_quiz_index + 1} of {len(self.quiz_flashcards)}",
            font=("Arial", 12),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )
        progress_label.pack(pady=(0, 20))
        
        # Question
        question_label = tk.Label(
            quiz_frame,
            text=card.question,
            font=("Arial", 16, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["background"],
            wraplength=600,
            justify=tk.CENTER
        )
        question_label.pack(pady=(0, 30))
        
        if card.type == "open":
            self.show_open_quiz(quiz_frame, card)
        else:
            self.show_multiple_quiz(quiz_frame, card)

    def show_open_quiz(self, parent_frame, card):
        """Show open question quiz interface"""
        answer_frame = ttk.Frame(parent_frame)
        answer_frame.pack(pady=20)
        
        tk.Label(
            answer_frame,
            text="Your Answer:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(0, 10))
        
        answer_entry = tk.Entry(
            answer_frame,
            font=("Arial", 12),
            width=50,
            bg="white",
            fg=COLORS["text_primary"]
        )
        answer_entry.pack(pady=(0, 20), fill=tk.X)
        answer_entry.focus()
        
        def check_answer():
            user_answer = answer_entry.get().strip().lower()
            correct_answer = card.answer.strip().lower()
            is_correct = user_answer == correct_answer
            
            if is_correct:
                self.quiz_score += 1
                messagebox.showinfo("Correct!", "✅ Great job! That's correct!")
            else:
                messagebox.showinfo("Incorrect", f"❌ The correct answer was: {card.answer}")
            
            # Record progress using database
            self.database.record_flashcard_response(card.id, user_answer, is_correct)
            self.database.update_spaced_repetition(card.id, is_correct)
            
            self.current_quiz_index += 1
            self.update_progress_display()
            self.show_quiz_question()
        
        check_btn = ttk.Button(
            answer_frame,
            text="✅ Check Answer",
            style="Success.TButton",
            command=check_answer
        )
        check_btn.pack(pady=10)

    def show_multiple_quiz(self, parent_frame, card):
        """Show multiple choice quiz interface"""
        options_frame = ttk.Frame(parent_frame)
        options_frame.pack(pady=20)
        
        selected_option = tk.IntVar(value=-1)
        
        for i, option in enumerate(card.options):
            rb = tk.Radiobutton(
                options_frame,
                text=option,
                variable=selected_option,
                value=i,
                bg=COLORS["background"],
                fg=COLORS["text_primary"],
                selectcolor=COLORS["primary"],
                font=("Arial", 12),
                wraplength=500,
                justify=tk.LEFT
            )
            rb.pack(anchor=tk.W, pady=5)
        
        def check_answer():
            if selected_option.get() == -1:
                messagebox.showwarning("Warning", "Please select an answer!")
                return
            
            is_correct = selected_option.get() == card.correct_answer_index
            user_answer = card.options[selected_option.get()] if selected_option.get() < len(card.options) else "Unknown"
            
            if is_correct:
                self.quiz_score += 1
                messagebox.showinfo("Correct!", "✅ Great job! That's correct!")
            else:
                correct_option = card.options[card.correct_answer_index]
                messagebox.showinfo("Incorrect", f"❌ The correct answer was: {correct_option}")
            
            # Record progress using database
            self.database.record_flashcard_response(card.id, user_answer, is_correct)
            self.database.update_spaced_repetition(card.id, is_correct)
            
            self.current_quiz_index += 1
            self.update_progress_display()
            self.show_quiz_question()
        
        check_btn = ttk.Button(
            parent_frame,
            text="✅ Check Answer",
            style="Success.TButton",
            command=check_answer
        )
        check_btn.pack(pady=20)

    def show_quiz_results(self):
        """Show quiz results"""
        self.clear_content()
        
        results_frame = ttk.Frame(self.content_frame, padding=20)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        score_percentage = (self.quiz_score / len(self.quiz_flashcards)) * 100
        
        # Result emoji based on score
        if score_percentage >= 80:
            emoji = "🎉"
            color = COLORS["success"]
        elif score_percentage >= 60:
            emoji = "👍"
            color = COLORS["warning"]
        else:
            emoji = "😢"
            color = COLORS["error"]
        
        tk.Label(
            results_frame,
            text=f"{emoji} Quiz Results {emoji}",
            font=("Arial", 24, "bold"),
            fg=color,
            bg=COLORS["background"]
        ).pack(pady=(0, 20))
        
        tk.Label(
            results_frame,
            text=f"Score: {self.quiz_score}/{len(self.quiz_flashcards)} ({score_percentage:.1f}%)",
            font=("Arial", 18),
            fg=COLORS["text_primary"],
            bg=COLORS["background"]
        ).pack(pady=(0, 30))
        
        # Performance message
        if score_percentage >= 80:
            message = "Excellent work! You're a flashcard master! 🏆"
        elif score_percentage >= 60:
            message = "Good job! Keep practicing to improve! 💪"
        else:
            message = "Don't worry! Practice makes perfect. Try again! 📚"
        
        tk.Label(
            results_frame,
            text=message,
            font=("Arial", 14),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"],
            wraplength=500
        ).pack(pady=(0, 30))
        
        # Action buttons
        btn_frame = ttk.Frame(results_frame)
        btn_frame.pack()
        
        retry_btn = ttk.Button(
            btn_frame,
            text="🔄 Try Again",
            style="Primary.TButton",
            command=self.start_quiz
        )
        retry_btn.pack(side=tk.LEFT, padx=10)
        
        home_btn = ttk.Button(
            btn_frame,
            text="🏠 Back to Home",
            command=self.show_welcome_screen
        )
        home_btn.pack(side=tk.LEFT, padx=10)

    def view_all_flashcards(self):
        """View all flashcards in table format"""
        self.clear_content()
        
        if not self.flashcards:
            # Show empty state instead of table
            empty_frame = ttk.Frame(self.content_frame, padding=20)
            empty_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                empty_frame,
                text="📭 No Flashcards Available",
                font=("Arial", 18, "bold"),
                fg=COLORS["text_secondary"],
                bg=COLORS["background"]
            ).pack(pady=(50, 20))
            
            tk.Label(
                empty_frame,
                text="You don't have any flashcards yet.\nCreate your first flashcard to get started!",
                font=("Arial", 12),
                fg=COLORS["text_secondary"],
                bg=COLORS["background"],
                justify=tk.CENTER
            ).pack(pady=(0, 30))
            
            create_btn = ttk.Button(
                empty_frame,
                text="➕ Create First Flashcard",
                style="Primary.TButton",
                command=self.create_flashcard_dialog
            )
            create_btn.pack(pady=10)
            
            back_btn = ttk.Button(
                empty_frame,
                text="⬅️ Back to Main",
                command=self.show_welcome_screen
            )
            back_btn.pack(pady=10)
            return
        
        view_frame = ttk.Frame(self.content_frame, padding=20)
        view_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            view_frame,
            text="📋 Manage Flashcards",
            font=("Arial", 18, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["background"]
        ).pack(pady=(0, 20))
        
        # Create a table frame
        table_frame = ttk.Frame(view_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create a scrollable frame
        canvas = tk.Canvas(table_frame, bg=COLORS["background"])
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create table headers
        headers = ["ID", "Type", "Question", "Answer/Options", "Actions"]
        for col, header in enumerate(headers):
            tk.Label(
                scrollable_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg=COLORS["primary"],
                bg=COLORS["background"],
                relief=tk.RAISED,
                borderwidth=1,
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="ew", padx=2, pady=2)
        
        # Display each flashcard in table format
        for row, card in enumerate(self.flashcards, 1):
            # Formatted ID
            tk.Label(
                scrollable_frame,
                text=card.formatted_id,
                font=("Arial", 10),
                bg=COLORS["card_bg"],
                relief=tk.RIDGE,
                borderwidth=1,
                padx=10,
                pady=5
            ).grid(row=row, column=0, sticky="ew", padx=2, pady=2)
            
            # Type
            tk.Label(
                scrollable_frame,
                text=card.type.title(),
                font=("Arial", 10),
                bg=COLORS["card_bg"],
                relief=tk.RIDGE,
                borderwidth=1,
                padx=10,
                pady=5
            ).grid(row=row, column=1, sticky="ew", padx=2, pady=2)
            
            # Question
            tk.Label(
                scrollable_frame,
                text=card.question,
                font=("Arial", 10),
                bg=COLORS["card_bg"],
                relief=tk.RIDGE,
                borderwidth=1,
                padx=10,
                pady=5,
                wraplength=300,
                justify=tk.LEFT
            ).grid(row=row, column=2, sticky="ew", padx=2, pady=2)
            
            # Answer/Options
            if card.type == "open":
                answer_text = card.answer
            else:
                options_text = ""
                for j, option in enumerate(card.options):
                    marker = " ✓" if j == card.correct_answer_index else ""
                    options_text += f"{j+1}. {option}{marker}\n"
                answer_text = options_text
            
            tk.Label(
                scrollable_frame,
                text=answer_text,
                font=("Arial", 10),
                bg=COLORS["card_bg"],
                relief=tk.RIDGE,
                borderwidth=1,
                padx=10,
                pady=5,
                wraplength=300,
                justify=tk.LEFT
            ).grid(row=row, column=3, sticky="ew", padx=2, pady=2)
            
            # Actions
            action_frame = ttk.Frame(scrollable_frame)
            action_frame.grid(row=row, column=4, sticky="ew", padx=2, pady=2)
            
            # Delete button
            delete_btn = ttk.Button(
                action_frame,
                text="🗑️ Delete",
                command=lambda cid=card.id: self.delete_single_flashcard(cid)
            )
            delete_btn.pack(side=tk.LEFT, padx=2)
            
            # Modify button
            modify_btn = ttk.Button(
                action_frame,
                text="✏️ Modify",
                command=lambda cid=card.id: self.modify_flashcard(cid)
            )
            modify_btn.pack(side=tk.LEFT, padx=2)
        
        # Configure column weights for proper resizing
        for col in range(5):
            scrollable_frame.columnconfigure(col, weight=1)
        
        # Back button (aligned to right)
        button_frame = ttk.Frame(view_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        back_btn = ttk.Button(
            button_frame,
            text="⬅️ Back to Main",
            command=self.show_welcome_screen
        )
        back_btn.pack(side=tk.RIGHT, pady=10)

    def clear_all_flashcards(self):
        """Clear all flashcards"""
        if not self.flashcards:
            messagebox.showinfo("Info", "No flashcards to clear!")
            return
        
        result = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to delete ALL flashcards? This action cannot be undone."
        )
        
        if result:
            # Clear database using database module
            self.database.delete_all_flashcards()
            
            # Clear local list
            self.flashcards.clear()
            messagebox.showinfo("Success", "All flashcards have been cleared!")
            self.update_stats()
            self.update_progress_display()
            self.show_welcome_screen()

    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_stats(self):
        """Update flashcard count statistics"""
        self.total_label.config(text=f"Total: {len(self.flashcards)} flashcards")
    
    def load_flashcards_from_db(self):
        """Load flashcards from database"""
        self.flashcards = self.database.get_all_flashcards()
    
    def update_progress_display(self):
        """Update progress statistics display"""
        stats = self.database.get_progress_stats()
        progress_text = f"Already studied {stats['studied']}/{stats['total']} | Accuracy Rate: {stats['accuracy']}%"
        self.stats_label.config(text=progress_text)
    
    def get_due_flashcards(self):
        """Get flashcards due for review"""
        return self.database.get_due_flashcards()
    
    def get_review_level(self, flashcard_id):
        """Get review level for a flashcard"""
        return self.database.get_review_level(flashcard_id)
    
    def delete_single_flashcard(self, flashcard_id):
        """Delete a single flashcard"""
        result = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this flashcard? This action cannot be undone."
        )
        
        if result:
            # Delete flashcard using database
            self.database.delete_flashcard(flashcard_id)
            
            # Reload flashcards and update UI
            self.load_flashcards_from_db()
            messagebox.showinfo("Success", "Flashcard deleted successfully!")
            self.update_stats()
            self.update_progress_display()
            self.view_all_flashcards()  # Refresh the view
    
    def modify_flashcard(self, flashcard_id):
        """Modify a flashcard"""
        # Find the flashcard to modify
        flashcard = None
        for card in self.flashcards:
            if card.id == flashcard_id:
                flashcard = card
                break
        
        if not flashcard:
            messagebox.showerror("Error", "Flashcard not found!")
            return
        
        # Create modification dialog
        modify_dialog = tk.Toplevel(self.root)
        modify_dialog.title("Modify Flashcard")
        modify_dialog.geometry("500x400")
        modify_dialog.configure(bg=COLORS["background"])
        modify_dialog.resizable(True, True)
        modify_dialog.minsize(450, 350)  # Set minimum size
        modify_dialog.maxsize(800, 600)  # Set maximum size
        modify_dialog.transient(self.root)
        modify_dialog.grab_set()
        
        tk.Label(
            modify_dialog,
            text=f"Modify {flashcard.type.title()} Flashcard",
            font=("Arial", 16, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["background"]
        ).pack(pady=20)
        
        # Question field
        tk.Label(
            modify_dialog,
            text="Question:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        question_entry = tk.Entry(
            modify_dialog,
            font=("Arial", 12),
            width=50,
            bg="white",
            fg=COLORS["text_primary"]
        )
        question_entry.pack(padx=20, pady=(0, 15), fill=tk.X)
        question_entry.insert(0, flashcard.question)
        
        if flashcard.type == "open":
            # Answer field for open questions
            tk.Label(
                modify_dialog,
                text="Answer:",
                font=("Arial", 12, "bold"),
                bg=COLORS["background"],
                fg=COLORS["text_primary"]
            ).pack(anchor=tk.W, padx=20, pady=(0, 5))
            
            answer_entry = tk.Entry(
                modify_dialog,
                font=("Arial", 12),
                width=50,
                bg="white",
                fg=COLORS["text_primary"]
            )
            answer_entry.pack(padx=20, pady=(0, 15), fill=tk.X)
            answer_entry.insert(0, flashcard.answer)
            
            def submit_modification():
                new_question = question_entry.get().strip()
                new_answer = answer_entry.get().strip()
                
                if not new_question or not new_answer:
                    messagebox.showerror("Error", "Both question and answer are required!")
                    return
                
                # Validate length limits
                if len(new_question) > 250:
                    messagebox.showerror("Error", "Question cannot exceed 250 characters!")
                    return
                
                if len(new_answer) > 250:
                    messagebox.showerror("Error", "Answer cannot exceed 250 characters!")
                    return
                
                # Update flashcard in database
                self.database.update_flashcard(flashcard_id, new_question, new_answer)
                
                messagebox.showinfo("Success", "Flashcard updated successfully!")
                modify_dialog.destroy()
                self.load_flashcards_from_db()
                self.update_stats()
                self.view_all_flashcards()  # Refresh the view
            
            submit_btn = ttk.Button(
                modify_dialog,
                text="✅ Update Flashcard",
                style="Success.TButton",
                command=submit_modification
            )
            submit_btn.pack(pady=20)
            
        else:
            # Options fields for multiple choice
            option_entries = []
            correct_var = tk.IntVar(value=flashcard.correct_answer_index)
            
            tk.Label(
                modify_dialog,
                text="Options:",
                font=("Arial", 12, "bold"),
                bg=COLORS["background"],
                fg=COLORS["text_primary"]
            ).pack(anchor=tk.W, padx=20, pady=(0, 5))
            
            options_frame = ttk.Frame(modify_dialog)
            options_frame.pack(padx=20, pady=(0, 15), fill=tk.X)
            
            for i, option in enumerate(flashcard.options):
                option_frame = ttk.Frame(options_frame)
                option_frame.pack(fill=tk.X, pady=2)
                
                rb = tk.Radiobutton(
                    option_frame,
                    variable=correct_var,
                    value=i,
                    bg=COLORS["background"],
                    fg=COLORS["text_primary"],
                    selectcolor=COLORS["primary"]
                )
                rb.pack(side=tk.LEFT, padx=(0, 5))
                
                option_entry = tk.Entry(
                    option_frame,
                    font=("Arial", 10),
                    bg="white",
                    fg=COLORS["text_primary"]
                )
                option_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
                option_entry.insert(0, option)
                option_entries.append(option_entry)
            
            def submit_modification():
                new_question = question_entry.get().strip()
                new_options = [entry.get().strip() for entry in option_entries]
                selected_option = correct_var.get()
                
                if not new_question:
                    messagebox.showerror("Error", "Question is required!")
                    return
                
                # Validate question length
                if len(new_question) > 250:
                    messagebox.showerror("Error", "Question cannot exceed 250 characters!")
                    return
                
                if len([opt for opt in new_options if opt]) < 2:
                    messagebox.showerror("Error", "At least 2 options are required!")
                    return
                
                # Validate answer length
                if selected_option < len(new_options) and new_options[selected_option]:
                    if len(new_options[selected_option]) > 250:
                        messagebox.showerror("Error", "Answer cannot exceed 250 characters!")
                        return
                
                if selected_option >= len(new_options) or not new_options[selected_option]:
                    messagebox.showerror("Error", "Please select a valid correct answer!")
                    return
                
                # Update flashcard in database
                self.database.update_flashcard(
                    flashcard_id, 
                    new_question, 
                    new_options[selected_option],
                    new_options,
                    selected_option
                )
                
                messagebox.showinfo("Success", "Flashcard updated successfully!")
                modify_dialog.destroy()
                self.load_flashcards_from_db()
                self.update_stats()
                self.view_all_flashcards()  # Refresh the view
            
            submit_btn = ttk.Button(
                modify_dialog,
                text="✅ Update Flashcard",
                style="Success.TButton",
                command=submit_modification
            )
            submit_btn.pack(pady=20)
