import tkinter as tk
from tkinter import ttk, messagebox
from utils import COLORS
from main import main_menu, sys

class UIComponents:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TFrame", background=COLORS["background"])
        self.style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text_primary"])
        self.style.configure("TButton", padding=10, font=("Arial", 10, "bold"))
        self.style.configure("Primary.TButton", background=COLORS["primary"], foreground="black")
        self.style.configure("Secondary.TButton", background=COLORS["secondary"], foreground="blue")
        self.style.configure("Accent.TButton", background=COLORS["accent"], foreground="blue")
    
    def Backhome(self):
        from main_gui import launch_main_gui2
        for widget in self.root.winfo_children():
            widget.destroy()
        try:
            launch_main_gui2(self.root)
        except Exception:
            try:
                main_menu()
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)

    def create_header(self, parent_frame):
        """Create header with title and flashcard count"""
        header_frame = ttk.Frame(parent_frame) 
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Title
        title_label = tk.Label(
            header_frame,
            text="🎯 Flashcard Master",
            font=("Arial", 28, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["background"]
        )
        title_label.pack(side=tk.LEFT)

        # Count of flashcards
        total_label = tk.Label(
            header_frame,
            text="Total: 0 flashcards",
            font=("Arial", 14),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )
        total_label.pack(side=tk.RIGHT)

        # Progress display
        progress_frame = ttk.Frame(parent_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        stats_label = tk.Label(
            progress_frame,
            text="Already studied 0/0 | Accuracy Rate: 0%",
            font=("Arial", 12),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )
        stats_label.pack(side=tk.RIGHT)

        return header_frame, total_label, progress_frame, stats_label

    
    def create_footer(self, parent_frame, create_callback, quiz_callback, view_callback, clear_callback):
        """Create footer with action buttons"""
        footer_frame = ttk.Frame(parent_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Action buttons
        button_frame = ttk.Frame(footer_frame)
        button_frame.pack()
        
        create_btn = ttk.Button(
            button_frame,
            text="➕ Create Flashcard",
            style="Primary.TButton",
            command=create_callback
        )
        create_btn.pack(side=tk.LEFT, padx=5)
        
        quiz_btn = ttk.Button(
            button_frame,
            text="🎯 Start Quiz",
            style="Secondary.TButton",
            command=quiz_callback
        )
        quiz_btn.pack(side=tk.LEFT, padx=5)
        
        view_btn = ttk.Button(
            button_frame,
            text="📋 View All",
            style="Accent.TButton",
            command=view_callback
        )
        view_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="Clear All",
            command=clear_callback
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        return footer_frame, create_btn, quiz_btn, view_btn, clear_btn
    
    def show_welcome_screen(self, content_frame, create_callback):
        """Show welcome screen with introduction"""
        # Clear previous content
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        welcome_frame = ttk.Frame(content_frame)
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        # Welcome message
        welcome_text = """🎯 Welcome to Flashcard Master!

        Create interactive flashcards to enhance your learning 
        experience with our modern, intuitive platform.

        ✨ FEATURES ✨
        • 📝 Create open-ended questions
        • 🔘 Design multiple-choice quizzes  
        • 🎯 Interactive learning mode
        • 📊 Track your progress
        • 🎨 Beautiful modern interface

        🚀 Get started by creating your first flashcard!"""
        
        # Add some subtle shadow effect using multiple frames
        shadow_frame = tk.Frame(
            welcome_frame,
            bg=COLORS["border"],
            padx=2,
            pady=2
        )
        shadow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=550, height=280)

        content_frame_inner = tk.Frame(
            shadow_frame,
            bg=COLORS["background"],
            padx=30,
            pady=25
        )
        content_frame_inner.pack(fill=tk.BOTH, expand=True)

        # Actual text label inside the framed content
        welcome_label_content = tk.Label(
            content_frame_inner,
            text=welcome_text,
            font=("Segoe UI", 12),
            fg=COLORS["text_primary"],
            bg=COLORS["background"],
            justify=tk.CENTER,
            wraplength=450
        )
        welcome_label_content.pack(expand=True)

        # Quick start button
        quick_start_btn = ttk.Button(
            welcome_frame,
            text="🚀 Quick Start - Create First Flashcard",
            style="Primary.TButton",
            command=create_callback
        )
        quick_start_btn.pack(pady=20)
        
        return welcome_frame
    
    def create_flashcard_dialog(self, parent, open_callback, multiple_callback):
        """Create flashcard type selection dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title("Create Flashcard")
        dialog.geometry("500x200")
        dialog.configure(bg=COLORS["background"])
        dialog.resizable(True, True)
        dialog.minsize(450, 180)  # Set minimum size
        dialog.maxsize(800, 400)  # Set maximum size
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - dialog.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Type selection
        type_frame = ttk.Frame(dialog, padding=20)
        type_frame.pack(fill=tk.X)
        
        tk.Label(
            type_frame,
            text="Select Question Type:",
            font=("Arial", 14, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        btn_frame = ttk.Frame(type_frame)
        btn_frame.pack()
        
        open_btn = ttk.Button(
            btn_frame,
            text="📝 Open Question",
            style="Primary.TButton",
            command=lambda: open_callback(dialog)
        )
        open_btn.pack(side=tk.LEFT, padx=10)
        
        multiple_btn = ttk.Button(
            btn_frame,
            text="🔘 Multiple Choice",
            style="Secondary.TButton",
            command=lambda: multiple_callback(dialog)
        )
        multiple_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(
            btn_frame,
            text="❌ Cancel",
            command=dialog.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        return dialog
    
    def create_open_question_form(self, content_frame, submit_callback, back_callback):
        """Create open question form"""
        # Clear previous content
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        form_frame = ttk.Frame(content_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            form_frame,
            text="📝 Create Open Question",
            font=("Arial", 18, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["background"]
        ).pack(pady=(0, 30))
        
        # Question input
        tk.Label(
            form_frame,
            text="Question:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        question_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=50,
            bg="white",
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["primary"],
            highlightbackground=COLORS["border"]
        )
        question_entry.pack(pady=(0, 20), fill=tk.X)
        question_entry.focus()
        
        # Answer input
        tk.Label(
            form_frame,
            text="Answer:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        answer_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=50,
            bg="white",
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["primary"],
            highlightbackground=COLORS["border"]
        )
        answer_entry.pack(pady=(0, 30), fill=tk.X)
        
        # Submit button
        def submit():
            question = question_entry.get().strip()
            answer = answer_entry.get().strip()
            submit_callback(question, answer)
        
        submit_btn = ttk.Button(
            form_frame,
            text="✅ Save Flashcard",
            style="Success.TButton",
            command=submit
        )
        submit_btn.pack()
        
        # Back button
        back_btn = ttk.Button(
            form_frame,
            text="⬅️ Back to Main",
            command=back_callback
        )
        back_btn.pack(pady=(20, 0))
        
        return form_frame, question_entry, answer_entry
    
    def create_multiple_choice_form(self, content_frame, submit_callback, back_callback):
        # Create multiple choice form
        # Clear previous content
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        form_frame = ttk.Frame(content_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            form_frame,
            text="🔘 Create Multiple Choice Question",
            font=("Arial", 18, "bold"),
            fg=COLORS["primary"],
            bg=COLORS["background"]
        ).pack(pady=(0, 30))
        
        # Question input
        tk.Label(
            form_frame,
            text="Question:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        question_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=50,
            bg="white",
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["primary"],
            highlightbackground=COLORS["border"]
        )
        question_entry.pack(pady=(0, 20), fill=tk.X)
        question_entry.focus()
        
        # Options frame
        options_frame = ttk.Frame(form_frame)
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            options_frame,
            text="Options:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        option_entries = []
        for i in range(4):
            entry = tk.Entry(
                options_frame,
                font=("Arial", 12),
                width=50,
                bg="white",
                fg=COLORS["text_primary"],
                relief=tk.FLAT,
                highlightthickness=1,
                highlightcolor=COLORS["primary"],
                highlightbackground=COLORS["border"]
            )
            entry.pack(pady=(0, 10), fill=tk.X)
            option_entries.append(entry)
        
        # Correct answer selection
        tk.Label(
            form_frame,
            text="Correct Answer:",
            font=("Arial", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text_primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        correct_var = tk.IntVar(value=1)
        option_frame = ttk.Frame(form_frame)
        option_frame.pack(fill=tk.X, pady=(0, 40))
        
        for i in range(4):
            rb = tk.Radiobutton(
                option_frame,
                indicatoron=0,
                text=f"Option {i+1}",
                variable=correct_var,
                value=i,
                bg=COLORS["background"],
                fg=COLORS["text_primary"],
                selectcolor="lightblue",
                font=("Arial", 12)
            )
            rb.pack(side=tk.LEFT, padx=10)

        # Submit button
        def submit():
            question = question_entry.get().strip()
            options = [entry.get().strip() for entry in option_entries]
            options = [opt for opt in options if opt]  # Remove empty options
            selected = correct_var.get()
            answer_selected = option_entries[selected].get().strip()
            submit_callback(question, options, selected, answer_selected)
        
        submit_btn = ttk.Button(
            form_frame,
            text="✅ Save Flashcard",
            style="Success.TButton",
            command=submit
        )
        submit_btn.pack()
        
        # Back button
        back_btn = ttk.Button(
            form_frame,
            text="⬅️ Back to Main",
            command=back_callback
        )
        back_btn.pack(pady=(20, 0))
        
        return form_frame, question_entry, option_entries, correct_var
