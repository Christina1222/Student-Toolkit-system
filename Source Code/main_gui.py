from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Canvas
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False
import time
import datetime
import threading

from utils import COLORS
from core.storage import JSONStorage
from core.gpa import GPACalculator, GRADE_POINTS
from core.homework import HomeworkPlanner
from core.pomodoro import PomodoroEngine
from F_app import FlashcardApp
from F_ui_components import UIComponents

def open_flashcards(root):
    try:
        # Create a new Toplevel window for flashcards instead of destroying main window
        flashcard_window = tk.Toplevel(root)
        flashcard_window.title("🎯 Flashcards Master")
        flashcard_window.geometry("1000x800")
        flashcard_window.configure(bg=COLORS["background"])
        flashcard_window.resizable(True, True)
        
        # Add back to home button
        def back_to_home():
            flashcard_window.destroy()
        
        # Create header with back button
        header_frame = tk.Frame(flashcard_window, bg=COLORS["accent"], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(header_frame, text="🏠 Back to Home", 
                           font=("Arial", 12, "bold"), fg="white", 
                           bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                           command=back_to_home, cursor="hand2", height=1, width=15)
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Initialize FlashcardApp in the new window
        FlashcardApp(flashcard_window)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Flashcards: {e}")


def open_gpa_gui(root):
    storage = JSONStorage(os.path.join(os.path.dirname(__file__), "data"))
    calc = GPACalculator(storage)

    w = tk.Toplevel(root)
    w.title("📊 GPA Calculator")
    w.configure(bg=COLORS["background"]) 
    w.resizable(True, True)
    w.attributes('-topmost', False)  # Ensure window can be resized
    # w.transient(root)  # Commented out to allow proper resizing
    # Don't make it modal - allow users to switch between windows
    
    # Make the main GPA Calculator full screen - try multiple methods
    try:
        w.wm_state('zoomed')  # Alternative method for Windows
    except:
        try:
            w.state('zoomed')  # Fallback method
        except:
            # Fallback: set to screen dimensions
            w.geometry(f"{w.winfo_screenwidth()}x{w.winfo_screenheight()}+0+0")
    w.update()  # Force update to apply the state

    # Semester setup variables
    semester_setup = {"total_credits": 0, "is_setup": False}

    # Enhanced semester setup dialog - popup style
    def semester_setup_dialog():
        dlg = tk.Toplevel(w)
        dlg.title("📚 Semester Setup")
        dlg.configure(bg="#F5F5F5") 
        dlg.transient(w)
        dlg.grab_set()
        dlg.geometry("700x600")
        dlg.resizable(False, False)
        
        # Center the dialog
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() // 2) - (700 // 2)
        y = (dlg.winfo_screenheight() // 2) - (600 // 2)
        dlg.geometry(f"700x600+{x}+{y}")

        # Enhanced header with gradient effect
        header_frame = tk.Frame(dlg, bg="#2E7D32", height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg="#2E7D32")
        header_content.pack(expand=True)
        
        # Icon and title
        title_frame = tk.Frame(header_content, bg="#2E7D32")
        title_frame.pack(expand=True)
        
        title = tk.Label(title_frame, text="📚 Semester Setup", 
                        font=("Arial", 24, "bold"), fg="white", bg="#2E7D32")
        title.pack(pady=(10, 5))
        
        subtitle = tk.Label(title_frame, text="Configure your academic semester", 
                           font=("Arial", 14), fg="#E8F5E8", bg="#2E7D32")
        subtitle.pack(pady=(0, 15))

        # Main content area with better styling - popup style
        main_frame = tk.Frame(dlg, bg="#F5F5F5", padx=40, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input section with card-like design
        input_card = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        # Card header
        card_header = tk.Frame(input_card, bg="#E8F5E8", height=50)
        card_header.pack(fill=tk.X)
        card_header.pack_propagate(False)
        
        card_title = tk.Label(card_header, text="🎯 Total Credit Hours", 
                             font=("Arial", 16, "bold"), fg="#2E7D32", bg="#E8F5E8")
        card_title.pack(expand=True)
        
        # Input area
        input_area = tk.Frame(input_card, bg="white", padx=25, pady=20)
        input_area.pack(fill=tk.X)
        
        # Input field with better styling
        credits_e = tk.Entry(input_area, width=15, bg="white", fg="#333333", 
                            insertbackground="#2E7D32", font=("Arial", 16, "bold"),
                            relief=tk.SOLID, bd=2, justify=tk.CENTER) 
        credits_e.pack(pady=(0, 15))
        
        # Placeholder text effect
        def on_entry_click(event):
            if credits_e.get() == "Enter credit hours":
                credits_e.delete(0, tk.END)
                credits_e.config(fg="#333333")
        
        def on_focus_out(event):
            if not credits_e.get():
                credits_e.insert(0, "Enter credit hours")
                credits_e.config(fg="#999999")
        
        credits_e.insert(0, "Enter credit hours")
        credits_e.config(fg="#999999")
        credits_e.bind('<FocusIn>', on_entry_click)
        credits_e.bind('<FocusOut>', on_focus_out)
        
        # Helpful information section
        info_frame = tk.Frame(main_frame, bg="#F5F5F5")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_title = tk.Label(info_frame, text="💡 Important Information", 
                             font=("Arial", 14, "bold"), fg="#2E7D32", bg="#F5F5F5")
        info_title.pack(anchor=tk.W, pady=(0, 10))
        
        info_text = tk.Label(info_frame, 
                            text="• Enter the total number of credit hours you're taking this semester\n"
                                 "• This will limit the number of courses you can add to prevent exceeding your load\n"
                                 "• Typical semester loads range from 10-23 credit hours\n"
                                 "• You can modify the total credit hours later if needed",
                            font=("Arial", 11), fg="#666666", bg="#F5F5F5",
                            justify=tk.LEFT, anchor=tk.W)
        info_text.pack(anchor=tk.W)

        result = {"ok": False, "total_credits": 0}

        def ok():
            try:
                input_value = credits_e.get().strip()
                if input_value == "Enter credit hours" or not input_value:
                    messagebox.showerror("Input Required", "Please enter the total number of credit hours for this semester.")
                    return
                    
                total_credits = int(input_value)
                if total_credits < 10:
                    messagebox.showerror("Invalid Input", "Total credit hours must be at least 10.\n\nPlease enter a value between 10 and 23.")
                    return
                if total_credits > 23:  # Reasonable upper limit
                    messagebox.showerror("Invalid Input", "Total credit hours cannot exceed 23.\n\nPlease enter a value between 10 and 23.")
                    return
                    
                result["total_credits"] = total_credits
                result["ok"] = True
                dlg.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for total credit hours.")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

        # Enhanced button section - popup layout
        button_frame = tk.Frame(main_frame, bg="#F5F5F5")
        button_frame.pack(fill=tk.X, pady=(20, 0))

        # Continue button - appropriately sized for popup
        ok_btn = tk.Button(button_frame, text="✅ Continue to GPA Calculator", 
                          font=("Arial", 14, "bold"), fg="white", 
                          bg="#4CAF50", relief=tk.RAISED, bd=2,
                          command=ok, cursor="hand2", height=2, width=30)
        ok_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Cancel button
        cancel_btn = tk.Button(button_frame, text="❌ Cancel", 
                              font=("Arial", 14, "bold"), fg="white", 
                              bg="#F44336", relief=tk.RAISED, bd=2,
                              command=dlg.destroy, cursor="hand2", height=2, width=15)
        cancel_btn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Add hover effects
        def on_enter_ok(event):
            ok_btn.config(bg="#45A049")
        
        def on_leave_ok(event):
            ok_btn.config(bg="#4CAF50")
            
        def on_enter_cancel(event):
            cancel_btn.config(bg="#DA190B")
        
        def on_leave_cancel(event):
            cancel_btn.config(bg="#F44336")
        
        ok_btn.bind("<Enter>", on_enter_ok)
        ok_btn.bind("<Leave>", on_leave_ok)
        cancel_btn.bind("<Enter>", on_enter_cancel)
        cancel_btn.bind("<Leave>", on_leave_cancel)
        
        # Focus on input field
        credits_e.focus_set()
        credits_e.select_range(0, tk.END)

        dlg.wait_window()
        return result

    def modify_credits_dialog():
        """Dialog to modify total credit hours"""
        dlg = tk.Toplevel(w)
        dlg.title("✏️ Modify Credit Hours")
        dlg.configure(bg="#F5F5F5") 
        dlg.transient(w)
        dlg.grab_set()
        dlg.geometry("550x450")
        dlg.resizable(True, True)
        
        # Center the dialog
        dlg.update_idletasks()
        x = (dlg.winfo_screenwidth() // 2) - (550 // 2)
        y = (dlg.winfo_screenheight() // 2) - (450 // 2)
        dlg.geometry(f"550x450+{x}+{y}")

        # Header
        header_frame = tk.Frame(dlg, bg="#FF9800", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="✏️ Modify Credit Hours", 
                        font=("Arial", 20, "bold"), fg="white", bg="#FF9800")
        title.pack(expand=True)

        # Main content
        main_frame = tk.Frame(dlg, bg="#F5F5F5", padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Current info
        current_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        current_frame.pack(fill=tk.X, pady=(0, 20))
        
        current_label = tk.Label(current_frame, text="📊 Current Settings", 
                               font=("Arial", 14, "bold"), fg="#FF9800", bg="white")
        current_label.pack(pady=(15, 5))
        
        current_info = tk.Label(current_frame, 
                              text=f"Total Credit Hours: {semester_setup['total_credits']}\n"
                                   f"Current Courses: {len(calc.courses)} courses\n"
                                   f"Current Credits: {sum(c.credits for c in calc.courses)}",
                              font=("Arial", 12), fg="#333333", bg="white")
        current_info.pack(pady=(0, 15))

        # New input
        input_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        input_label = tk.Label(input_frame, text="🎯 New Total Credit Hours", 
                             font=("Arial", 14, "bold"), fg="#FF9800", bg="white")
        input_label.pack(pady=(15, 10))
        
        credits_e = tk.Entry(input_frame, font=("Arial", 16, "bold"), 
                           relief=tk.SOLID, bd=2, justify=tk.CENTER, width=10)
        credits_e.pack(pady=(0, 15))
        credits_e.insert(0, str(semester_setup['total_credits']))

        # Warning if current credits exceed new total
        warning_label = tk.Label(main_frame, text="", 
                               font=("Arial", 10), fg="#F44336", bg="#F5F5F5")
        warning_label.pack(pady=(0, 10))

        def update_warning():
            try:
                new_total = int(credits_e.get())
                current_credits = sum(c.credits for c in calc.courses)
                if current_credits > new_total:
                    warning_label.config(text=f"⚠️ Warning: You have {current_credits} credits but setting total to {new_total}")
                else:
                    warning_label.config(text="")
            except:
                warning_label.config(text="")

        credits_e.bind('<KeyRelease>', lambda e: update_warning())

        result = {"ok": False, "new_total": semester_setup['total_credits']}

        def ok():
            try:
                new_total = int(credits_e.get())
                if new_total < 10:
                    messagebox.showerror("Error", "Credit hours must be at least 10")
                    return
                if new_total > 23:
                    messagebox.showerror("Error", "Credit hours cannot exceed 23")
                    return
                
                current_credits = sum(c.credits for c in calc.courses)
                if current_credits > new_total:
                    messagebox.showerror("Cannot Reduce Credits", 
                        f"❌ Cannot set total to {new_total} credits.\n\n"
                        f"Current courses already total {current_credits} credits.\n\n"
                        f"You must either:\n"
                        f"• Remove some courses first, or\n"
                        f"• Set a total of at least {current_credits} credits")
                return
                
                result["ok"] = True
                result["new_total"] = new_total
                dlg.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        # Buttons - docked at bottom to always be visible
        button_frame = tk.Frame(dlg, bg="#F5F5F5")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        ok_btn = tk.Button(button_frame, text="✅ UPDATE CREDITS", 
                          font=("Arial", 16, "bold"), fg="white", 
                          bg="#4CAF50", relief=tk.RAISED, bd=4,
                          command=ok, cursor="hand2", height=4, width=25)
        ok_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 10), pady=(10, 10))

        cancel_btn = tk.Button(button_frame, text="❌ CANCEL", 
                              font=("Arial", 16, "bold"), fg="white", 
                              bg="#F44336", relief=tk.RAISED, bd=4,
                              command=dlg.destroy, cursor="hand2", height=4, width=25)
        cancel_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=(10, 10))

        # Keyboard shortcuts
        dlg.bind('<Return>', lambda e: ok())
        dlg.bind('<Escape>', lambda e: dlg.destroy())

        # Focus and select
        credits_e.focus_set()
        credits_e.select_range(0, tk.END)
        update_warning()

        dlg.wait_window()
        return result

    # Show semester setup dialog first
    setup_result = semester_setup_dialog()
    if not setup_result["ok"]:
        w.destroy()
        return
    
    semester_setup["total_credits"] = setup_result["total_credits"]
    semester_setup["is_setup"] = True

    # Beautiful header with better visibility
    header_frame = tk.Frame(w, bg=COLORS["primary"], height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_frame = tk.Frame(header_frame, bg=COLORS["primary"])
    title_frame.pack(expand=True)
    
    title = tk.Label(title_frame, text="📊 GPA Calculator", 
                    font=("Arial", 26, "bold"), fg="white", bg=COLORS["primary"])
    title.pack(pady=10)
    
    subtitle = tk.Label(title_frame, text="Track your academic performance", 
                       font=("Arial", 16, "bold"), fg="white", bg=COLORS["primary"])
    subtitle.pack(pady=(0, 8))

    frm = tk.Frame(w, bg=COLORS["background"], padx=25, pady=15)
    frm.pack(fill=tk.BOTH, expand=True)

    # Semester info display with modify button
    semester_info_frame = tk.Frame(frm, bg=COLORS["accent"], relief=tk.RAISED, bd=2)
    semester_info_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Top row: Info label and modify button
    semester_top_frame = tk.Frame(semester_info_frame, bg=COLORS["accent"])
    semester_top_frame.pack(fill=tk.X, padx=10, pady=5)
    
    semester_info_label = tk.Label(semester_top_frame, 
                                  text=f"📚 Semester Total: {semester_setup['total_credits']} credit hours | Current: 0 credit hours", 
                                  font=("Arial", 14, "bold"), fg="white", bg=COLORS["accent"])
    semester_info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Modify credits button
    def modify_credits():
        result = modify_credits_dialog()
        if result["ok"]:
            # Update semester setup
            semester_setup['total_credits'] = result["new_total"]
            # Update the display
            current_credits = sum(c.credits for c in calc.courses)
            semester_info_label.config(
                text=f"📚 Semester Total: {semester_setup['total_credits']} credit hours | Current: {current_credits} credit hours"
            )
            messagebox.showinfo("Success", f"Total credit hours updated to {result['new_total']}")
    
    modify_btn = tk.Button(semester_top_frame, text="✏️ Modify Credits", 
                          font=("Arial", 12, "bold"), fg="white", 
                          bg="#FF9800", relief=tk.RAISED, bd=3,
                          command=modify_credits, cursor="hand2", width=15, height=2)
    modify_btn.pack(side=tk.RIGHT, padx=(10, 0))

    # Courses table with beautiful styling - flexible height
    table_frame = tk.Frame(frm, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    table_title = tk.Label(table_frame, text="📚 Your Courses", 
                          font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                          bg=COLORS["border"])
    table_title.pack(pady=(10, 5))
    
    columns = ("order", "name", "credits", "grade")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    table.heading("order", text="No")
    table.heading("name", text="Course Name")
    table.heading("credits", text="Credits")
    table.heading("grade", text="Grade")
    table.column("order", width=60, anchor=tk.CENTER)
    table.column("name", width=600, minwidth=400)
    table.column("credits", width=100, anchor=tk.CENTER)
    table.column("grade", width=100, anchor=tk.CENTER)
    table.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def refresh():
        for iid in table.get_children():
            table.delete(iid)
        for idx, c in enumerate(calc.courses):
            table.insert("", tk.END, iid=str(idx), values=(idx+1, c.name, c.credits, c.grade))
        
        # Update semester info
        current_credits = sum(course.credits for course in calc.courses)
        semester_info_label.config(text=f"📚 Semester Total: {semester_setup['total_credits']} credit hours | Current: {current_credits} credit hours")

    # Dialog for add/edit
    def course_dialog(initial=None):
        dlg = tk.Toplevel(w)
        dlg.title("Add/Edit Course" if initial is None else "Edit Course")
        dlg.configure(bg=COLORS["background"]) 
        dlg.transient(w)
        dlg.grab_set()
        dlg.geometry("500x450")
        dlg.resizable(True, True)
        dlg.minsize(450, 400)  # Set minimum size
        dlg.maxsize(800, 700)  # Set maximum size

        # Header
        header_frame = tk.Frame(dlg, bg=COLORS["primary"], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="📚 Course Information", 
                        font=("Arial", 18, "bold"), fg="white", bg=COLORS["primary"])
        title.pack(expand=True)

        f = tk.Frame(dlg, bg=COLORS["background"], padx=30, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        # Course name
        name_label = tk.Label(f, text="📖 Course Name", bg=COLORS["background"], 
                             fg=COLORS["text_primary"], font=("Arial", 14, "bold"))
        name_label.pack(anchor=tk.W, pady=(0, 5))
        name_e = tk.Entry(f, width=50, bg=COLORS["border"], fg=COLORS["text_primary"], 
                         insertbackground=COLORS["text_primary"], font=("Arial", 11)) 
        name_e.pack(fill=tk.X, pady=(0, 15))

        # Credits restricted to 2.0, 3.0, 4.0
        credits_label = tk.Label(f, text="🎯 Credits", bg=COLORS["background"], 
                                fg=COLORS["text_primary"], font=("Arial", 14, "bold"))
        credits_label.pack(anchor=tk.W, pady=(0, 5))
        credits_var = tk.StringVar(value="3.0")
        credits_cb = ttk.Combobox(f, textvariable=credits_var, values=["2.0", "3.0", "4.0"],
                                 state="readonly", font=("Arial", 11), width=8)
        credits_cb.pack(anchor=tk.W, pady=(0, 15))
        
        # Helpful hint
        credits_hint = tk.Label(f, text="Allowed credit hours: 2.0, 3.0, 4.0", 
                               bg=COLORS["background"], fg=COLORS["text_secondary"], font=("Arial", 9))
        credits_hint.pack(anchor=tk.W, pady=(0, 15))

        # Grade
        grade_label = tk.Label(f, text="⭐ Grade", bg=COLORS["background"], 
                              fg=COLORS["text_primary"], font=("Arial", 14, "bold"))
        grade_label.pack(anchor=tk.W, pady=(0, 5))
        grade_var = tk.StringVar(value="A")
        grade_cb = ttk.Combobox(f, textvariable=grade_var, values=list(GRADE_POINTS.keys()), 
                               state="readonly", font=("Arial", 11))
        grade_cb.pack(anchor=tk.W, pady=(0, 15))
        
        # Add grade points display
        def update_grade_points(*args):
            selected_grade = grade_var.get()
            points = GRADE_POINTS.get(selected_grade, 0.0)
            grade_points_label.config(text=f"Grade Points: {points:.2f}")
        
        grade_var.trace('w', update_grade_points)
        grade_points_label = tk.Label(f, text="Grade Points: 4.00", bg=COLORS["background"], 
                                     fg=COLORS["text_secondary"], font=("Arial", 10))
        grade_points_label.pack(anchor=tk.W, pady=(0, 15))

        if initial is not None:
            name_e.insert(0, initial["name"]) 
            credits_var.set(f"{float(initial["credits"]):.1f}")
            grade_var.set(initial["grade"])

        # Button frame with VERY STRONG contrast
        btn_frame = tk.Frame(f, bg="#E8F5E8", relief=tk.RAISED, bd=3)
        btn_frame.pack(pady=(20, 0), padx=15)

        result = {"ok": False, "name": "", "credits": 0.0, "grade": "A"}

        def ok():
            try:
                result["name"] = name_e.get().strip()
                if not result["name"]:
                    messagebox.showerror("Error", "Course name cannot be empty")
                    return
                
                # Course name validation - cannot be just numbers and must be at least 2 characters
                if result["name"].isdigit():
                    messagebox.showerror("Error", "Course name cannot be just numbers")
                    return
                if len(result["name"]) < 2:
                    messagebox.showerror("Error", "Course name must be at least 2 characters long")
                    return
                
                credits_str = credits_var.get().strip()
                if not credits_str:
                    messagebox.showerror("Error", "Credits cannot be empty")
                    return
                    
                result["credits"] = float(credits_str)
                if result["credits"] not in (2.0, 3.0, 4.0):
                    messagebox.showerror("Error", "Credits must be one of: 2.0, 3.0, 4.0")
                    return
                
                # Check if adding this course would exceed semester total
                current_credits = sum(course.credits for course in calc.courses)
                if initial is None:  # Only check for new courses, not edits
                    if current_credits + result["credits"] > semester_setup["total_credits"]:
                        messagebox.showerror("Error", f"Adding this course would exceed your semester total of {semester_setup['total_credits']} credit hours.\nCurrent: {current_credits} + New: {result['credits']} = {current_credits + result['credits']}")
                        return
                    
                result["grade"] = grade_var.get().strip().upper()
                if result["grade"] not in GRADE_POINTS:
                    messagebox.showerror("Error", f"Invalid grade. Valid grades are: {', '.join(GRADE_POINTS.keys())}")
                    return
                    
                result["ok"] = True
                dlg.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid credits selection. Choose 2.0, 3.0, or 4.0")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        # Reasonable size buttons - visible but not too large
        ok_btn = tk.Button(btn_frame, text="✅ Save Course", 
                          font=("Arial", 12, "bold"), fg="white", 
                          bg="#4CAF50", relief=tk.RAISED, bd=2,
                          command=ok, cursor="hand2", height=2, width=15)
        ok_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = tk.Button(btn_frame, text="❌ Cancel", 
                              font=("Arial", 12, "bold"), fg="white", 
                              bg="#F44336", relief=tk.RAISED, bd=2,
                              command=dlg.destroy, cursor="hand2", height=2, width=15)
        cancel_btn.pack(side=tk.LEFT)

        dlg.wait_window()
        return result

    # Beautiful control buttons with better spacing
    control_frame = tk.Frame(frm, bg=COLORS["background"])
    control_frame.pack(fill=tk.X, pady=(10, 15))

    def add_course():
        # Check if we've reached the semester credit limit
        current_credits = sum(course.credits for course in calc.courses)
        if current_credits >= semester_setup["total_credits"]:
            messagebox.showwarning("Credit Limit Reached", 
                                 f"You have reached your semester total of {semester_setup['total_credits']} credit hours.\n"
                                 f"Current courses: {current_credits} credit hours")
            return
            
        data = course_dialog()
        if not data["ok"]:
            return
        try:
            calc.add_course(data["name"], data["credits"], data["grade"])
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=w)

    def edit_course():
        sel = table.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a course to edit", parent=w)
            return
        idx = int(sel[0])
        c = calc.courses[idx]
        data = course_dialog({"name": c.name, "credits": c.credits, "grade": c.grade})
        if not data["ok"]:
            return
        try:
            # Use the new update_course method to edit in place
            calc.update_course(idx, data["name"], data["credits"], data["grade"])
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=w)

    def remove_course():
        sel = table.selection()
        if not sel:
            return
        idx = int(sel[0])
        
        # Get course details for confirmation message
        course = calc.courses[idx]
        course_info = f"{course.name} ({course.credits} credits, Grade: {course.grade})"
        
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Removal", 
            f"Are you sure you want to remove this course?\n\n{course_info}\n\nThis action cannot be undone.",
            icon='warning',
            parent=w
        )
        
        if result:
            try:
                calc.remove_course(idx)
                refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_all():
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Confirm Clear All", 
            f"Are you sure you want to remove ALL courses?\n\nThis will delete {len(calc.courses)} course(s) and cannot be undone.",
            icon='warning',
            parent=w
        )
        
        if result:
            try:
                calc.clear_courses()
                refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # Create beautiful buttons with icons - better spacing
    add_btn = tk.Button(control_frame, text="➕ Add Course", 
                       font=("Arial", 12, "bold"), fg="white", 
                       bg=COLORS["accent"], relief=tk.RAISED, bd=2,
                       command=add_course, cursor="hand2", height=2, width=14)
    add_btn.pack(side=tk.LEFT, padx=(0, 8))

    edit_btn = tk.Button(control_frame, text="✏️ Edit", 
                        font=("Arial", 12, "bold"), fg="white", 
                        bg=COLORS["primary"], relief=tk.RAISED, bd=2,
                        command=edit_course, cursor="hand2", height=2, width=12)
    edit_btn.pack(side=tk.LEFT, padx=(0, 8))

    remove_btn = tk.Button(control_frame, text="🗑️ Remove", 
                          font=("Arial", 12, "bold"), fg="white", 
                          bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                          command=remove_course, cursor="hand2", height=2, width=14)
    remove_btn.pack(side=tk.LEFT, padx=(0, 8))

    clear_btn = tk.Button(control_frame, text="🧹 Clear All", 
                         font=("Arial", 12, "bold"), fg="white", 
                         bg=COLORS["border"], relief=tk.RAISED, bd=2,
                         command=clear_all, cursor="hand2", height=2, width=14)
    clear_btn.pack(side=tk.LEFT, padx=(0, 8))
    
    # Global list to track open statistics windows
    open_stats_windows = []
    
    def refresh_stats_windows():
        """Refresh all open statistics windows"""
        for window_info in open_stats_windows:
            if window_info['window'].winfo_exists():
                window_info['refresh_func']()
    
    def show_gpa_stats():
        # Create a new window for statistics and history
        stats_window = tk.Toplevel(w)
        stats_window.title("📊 GPA Statistics & History")
        stats_window.configure(bg=COLORS["background"])
        stats_window.geometry("1400x1000")
        stats_window.resizable(True, True)
        stats_window.minsize(1200, 900)
        stats_window.maxsize(1800, 1200)
        
        # Register this window for refresh capability
        def on_window_close():
            # Remove from tracking list when window is closed
            nonlocal open_stats_windows
            open_stats_windows = [w for w in open_stats_windows if w['window'] != stats_window]
            stats_window.destroy()
        
        stats_window.protocol("WM_DELETE_WINDOW", on_window_close)
        
        # Enhanced header with gradient effect
        header_frame = tk.Frame(stats_window, bg=COLORS["primary"], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg=COLORS["primary"])
        title_frame.pack(expand=True)
        
        title = tk.Label(title_frame, text="📊 GPA Statistics & History", 
                        font=("Arial", 24, "bold"), fg="white", bg=COLORS["primary"])
        title.pack(pady=10)
        
        subtitle = tk.Label(title_frame, text="Comprehensive Academic Performance Analysis", 
                           font=("Arial", 14), fg="white", bg=COLORS["primary"])
        subtitle.pack(pady=(0, 15))
        
        # Main content frame with better spacing
        main_frame = tk.Frame(stats_window, bg=COLORS["background"], padx=25, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # GPA History Section
        history_frame = tk.Frame(main_frame, bg=COLORS["border"], relief=tk.RAISED, bd=3)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        history_title = tk.Label(history_frame, text="📈 GPA History & Trends", 
                                font=("Arial", 18, "bold"), fg=COLORS["text_primary"], 
                                bg=COLORS["border"])
        history_title.pack(pady=(15, 10))
        
        # History + Chart container with better layout
        history_content = tk.Frame(history_frame, bg=COLORS["border"])
        history_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Left panel for history data
        left_panel = tk.Frame(history_content, bg=COLORS["background"], relief=tk.RAISED, bd=2) 
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel for chart
        right_panel = tk.Frame(history_content, bg=COLORS["background"], relief=tk.RAISED, bd=2) 
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # History display with better formatting
        history_text = tk.Text(left_panel, height=15, bg=COLORS["background"], 
                              fg=COLORS["text_primary"], font=("Arial", 11),
                              relief=tk.FLAT, bd=0, wrap=tk.WORD)
        history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def update_history_display():
            history_text.config(state=tk.NORMAL)
            history_text.delete(1.0, tk.END)
            
            if not calc.history:
                history_text.insert(tk.END, "📊 No GPA history available yet.\n\n")
                history_text.insert(tk.END, "Add courses and calculate GPA to build your academic history!\n\n")
                history_text.insert(tk.END, "💡 Tip: Save your GPA calculations to track your progress over time.")
            else:
                # Calculate and display statistics
                    avg_gpa = calc.get_average_gpa()
                    highest = calc.get_highest_gpa()
                    lowest = calc.get_lowest_gpa()
                    
                    history_text.insert(tk.END, "📈 Historical Statistics:\n")
                    history_text.insert(tk.END, "=" * 50 + "\n")
                    history_text.insert(tk.END, f"🎯 Average GPA: {avg_gpa:.2f}\n")
                    history_text.insert(tk.END, f"📈 Highest GPA: {highest:.2f}\n")
                    history_text.insert(tk.END, f"📉 Lowest GPA: {lowest:.2f}\n")
                    history_text.insert(tk.END, f"📊 Total Calculations: {len(calc.history)}\n")
                    
                    # Show individual GPA entries
                    history_text.insert(tk.END, "\n" + "=" * 50 + "\n")
                    history_text.insert(tk.END, "📋 GPA History:\n")
                    history_text.insert(tk.END, "-" * 25 + "\n")
                    for i, entry in enumerate(calc.history, 1):
                        gpa_value = entry.get("gpa", 0.0)
                        history_text.insert(tk.END, f"{i}. GPA: {gpa_value:.2f}\n")
                
                    # Show appropriate message based on number of entries
                    if len(calc.history) == 1:
                        history_text.insert(tk.END, "\n" + "=" * 50 + "\n")
                        history_text.insert(tk.END, "💡 Getting Started:\n")
                        history_text.insert(tk.END, "-" * 20 + "\n")
                        history_text.insert(tk.END, "🎉 Great! You've saved your first GPA calculation.\n")
                        history_text.insert(tk.END, "📈 Save more GPA calculations to see trends and analysis!\n")
                    else:
                        # Add improvement analysis for multiple entries
                            recent_gpa = calc.get_gpa_trend()[-1] if calc.get_gpa_trend() else 0.0
                            history_text.insert(tk.END, "\n" + "=" * 50 + "\n")
                            history_text.insert(tk.END, "💡 Performance Analysis:\n")
                            history_text.insert(tk.END, "-" * 25 + "\n")
                            
                            if recent_gpa > avg_gpa:
                                improvement = recent_gpa - avg_gpa
                                history_text.insert(tk.END, f"🚀 Excellent progress! Your recent GPA ({recent_gpa:.2f}) is {improvement:.2f} points above your average ({avg_gpa:.2f})\n")
                            elif recent_gpa < avg_gpa:
                                decline = avg_gpa - recent_gpa
                                history_text.insert(tk.END, f"📚 Consider reviewing your study strategies. Recent GPA ({recent_gpa:.2f}) is {decline:.2f} points below your average ({avg_gpa:.2f})\n")
                            else:
                                history_text.insert(tk.END, f"⚖️ Consistent performance! Your recent GPA ({recent_gpa:.2f}) matches your average ({avg_gpa:.2f})\n")
                            
                    # Add trend analysis
                    if len(calc.history) >= 3:
                        recent_trend = calc.get_gpa_trend()[-3:]
                        if recent_trend[-1] > recent_trend[0]:
                            history_text.insert(tk.END, "📈 Upward trend detected in recent calculations!\n")
                        elif recent_trend[-1] < recent_trend[0]:
                            history_text.insert(tk.END, "📉 Downward trend in recent calculations.\n")
                        else:
                            history_text.insert(tk.END, "➡️ Stable performance in recent calculations.\n")
        
            history_text.config(state=tk.DISABLED)

            # Draw/refresh academic progress chart with enhanced styling
            for child in right_panel.winfo_children():
                child.destroy()
            
            if _HAS_MPL and calc.history:
                try:
                    fig = Figure(figsize=(5.5, 4.0), dpi=100, facecolor='white')
                    ax = fig.add_subplot(111, facecolor='white')
                    trend = list(calc.get_gpa_trend())
                    xs = list(range(1, len(trend)+1))
                    
                    # Enhanced chart styling
                    ax.plot(xs, trend, marker='o', color='#1976D2', linewidth=3, markersize=8, markerfacecolor='#1976D2', markeredgecolor='white', markeredgewidth=2)
                    ax.fill_between(xs, trend, alpha=0.3, color='#1976D2')
                    
                    ax.set_title('Academic Progress Trend', fontsize=14, fontweight='bold', color='#333333', pad=20)
                    ax.set_xlabel('Calculation Number', fontsize=12, color='#666666')
                    ax.set_ylabel('GPA', fontsize=12, color='#666666')
                    ax.set_ylim(0.0, 4.0)
                    ax.set_xlim(0.5, len(trend) + 0.5)
                    
                    # Enhanced grid and styling
                    ax.grid(True, linestyle='--', alpha=0.3, color='#CCCCCC')
                    ax.set_facecolor('#FAFAFA')
                    
                    # Add horizontal lines for GPA benchmarks
                    ax.axhline(y=3.7, color='#4CAF50', linestyle=':', alpha=0.7, label='Excellent (3.7+)')
                    ax.axhline(y=3.0, color='#FFC107', linestyle=':', alpha=0.7, label='Good (3.0+)')
                    ax.axhline(y=2.0, color='#FF9800', linestyle=':', alpha=0.7, label='Passing (2.0+)')
                    
                    # Add trend line if there are enough points
                    if len(trend) >= 2:
                        import numpy as np
                        z = np.polyfit(xs, trend, 1)
                        p = np.poly1d(z)
                        ax.plot(xs, p(xs), "r--", alpha=0.8, linewidth=2, label='Trend')
                    
                    ax.legend(loc='upper right', fontsize=9)
                    
                    # Adjust layout
                    fig.tight_layout(pad=2.0)
                    
                    canvas = FigureCanvasTkAgg(fig, master=right_panel)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                    
                except Exception as e:
                    fallback = tk.Label(right_panel, text=f"📊 Chart unavailable\nError: {str(e)[:50]}...", 
                                       bg=COLORS["background"], fg=COLORS["text_secondary"], 
                                       font=("Arial", 12), justify=tk.CENTER) 
                    fallback.pack(fill=tk.BOTH, expand=True)
            else:
                if not _HAS_MPL:
                    info = tk.Label(right_panel, text="📊 Chart Feature\n\nInstall matplotlib to see\nyour academic progress chart:\n\npip install matplotlib", 
                                   bg=COLORS["background"], fg=COLORS["text_secondary"], 
                                   font=("Arial", 12), justify=tk.CENTER) 
                else:
                    info = tk.Label(right_panel, text="📊 No History Data\n\nCalculate and save your GPA\nto see progress charts!", 
                                   bg=COLORS["background"], fg=COLORS["text_secondary"], 
                                   font=("Arial", 12), justify=tk.CENTER)
                info.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced history control buttons
        history_control_frame = tk.Frame(history_frame, bg=COLORS["border"])
        history_control_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        def clear_history():
            if messagebox.askyesno("Confirm Clear History", 
                                 "⚠️ Are you sure you want to clear all GPA history?\n\nThis action cannot be undone!",
                                 parent=stats_window):
                calc.clear_history()
                update_history_display()
                # Refresh any other open statistics windows
                refresh_stats_windows()
                messagebox.showinfo("Success", "✅ GPA history cleared successfully!", parent=stats_window)
        
        def export_history():
            if not calc.history:
                messagebox.showwarning("No Data", "No GPA history available to export.", parent=stats_window)
                return
            
            try:
                import tkinter.filedialog as fd
                filename = fd.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Export GPA History"
                )
                if filename:
                    with open(filename, 'w') as f:
                        f.write("GPA History Export\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(f"Total Calculations: {len(calc.history)}\n")
                        f.write(f"Average GPA: {calc.get_average_gpa():.2f}\n")
                        f.write(f"Highest GPA: {calc.get_highest_gpa():.2f}\n")
                        f.write(f"Lowest GPA: {calc.get_lowest_gpa():.2f}\n")
                    messagebox.showinfo("Success", f"✅ GPA history exported to:\n{filename}", parent=stats_window)
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export history:\n{str(e)}", parent=stats_window)
        
        # Control buttons with better styling
        clear_history_btn = tk.Button(history_control_frame, text="🗑️ Clear History", 
                                     font=("Arial", 11, "bold"), fg="white", 
                                     bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                                     command=clear_history, cursor="hand2", height=1, width=15)
        clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_history_btn = tk.Button(history_control_frame, text="🔄 Refresh Data", 
                                       font=("Arial", 11, "bold"), fg="white", 
                                       bg=COLORS["primary"], relief=tk.RAISED, bd=2,
                                       command=update_history_display, cursor="hand2", height=1, width=15)
        refresh_history_btn.pack(side=tk.LEFT, padx=5)
        
        export_history_btn = tk.Button(history_control_frame, text="📤 Export History", 
                                      font=("Arial", 11, "bold"), fg="white", 
                                      bg=COLORS["accent"], relief=tk.RAISED, bd=2,
                                      command=export_history, cursor="hand2", height=1, width=15)
        export_history_btn.pack(side=tk.LEFT, padx=5)
        
        # Initial update
        update_history_display()
        
        # Register this window for refresh capability
        open_stats_windows.append({
            'window': stats_window,
            'refresh_func': update_history_display
        })

    # Stats button for viewing detailed statistics
    stats_btn = tk.Button(control_frame, text="📊 View Stats", 
                         font=("Arial", 12, "bold"), fg="white", 
                         bg="#9C27B0", relief=tk.RAISED, bd=2,
                         command=show_gpa_stats, cursor="hand2", height=2, width=14)
    stats_btn.pack(side=tk.LEFT, padx=(0, 8))

    # Calculate button and result display side by side
    def calc_now():
        res = calc.calculate()
        result_lbl.config(text=f"🎯 GPA: {res['gpa']}  |  📚 Credits: {res['total_credits']}")
        if messagebox.askyesno("Save", "Save GPA to history?", parent=w):
            calc.save_result(res["gpa"])
            # Refresh any open statistics windows
            refresh_stats_windows()
            # Show success message
            messagebox.showinfo("Success", f"✅ GPA {res['gpa']:.2f} saved to history successfully!", parent=w)

    # Calculate button and result container side by side
    calc_result_container = tk.Frame(frm, bg=COLORS["background"])
    calc_result_container.pack(fill=tk.X, pady=(15, 10))
    
    # Calculate button on the left
    calc_btn = tk.Button(calc_result_container, text="🧮 Calculate GPA", 
                        font=("Arial", 16, "bold"), fg="white", 
                        bg="#FF5722", relief=tk.RAISED, bd=3,
                        command=calc_now, cursor="hand2", height=2, width=20)
    calc_btn.pack(side=tk.LEFT, padx=(0, 15))

    # Result display on the right
    result_frame = tk.Frame(calc_result_container, bg=COLORS["primary"], relief=tk.RAISED, bd=3)
    result_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    result_lbl = tk.Label(result_frame, text="🎯 GPA: -", fg="white", bg=COLORS["primary"], 
                         font=("Arial", 18, "bold"))
    result_lbl.pack(pady=15)


    refresh()


def open_homework_gui(root):
    storage = JSONStorage(os.path.join(os.path.dirname(__file__), "data"))
    planner = HomeworkPlanner(storage)

    # Subject categories database
    SUBJECTS_DATABASE = {
        "Programming Subjects": [
            "AMCS1013 - PROGRAMMING FUNDAMENTALS (3 credits)",
            "AMCS1034 - SOFTWARE DEVELOPMENT FUNDAMENTALS (4 credits)",
            "AMCS1043 - DATA STRUCTURES AND ALGORITHMS (3 credits)",
            "AMCS1054 - OBJECT-ORIENTED PROGRAMMING (4 credits)",
            "AMCS1084 - SOFTWARE ENGINEERING (4 credits)",
            "AMCS1093 - ARTIFICIAL INTELLIGENCE (3 credits)",
            "AMCS1103 - MACHINE LEARNING (3 credits)",
            "AMCS1114 - MOBILE APPLICATION DEVELOPMENT (4 credits)",
            "AMCS1123 - WEB DEVELOPMENT (3 credits)",
            "AMCS1133 - CLOUD COMPUTING (3 credits)",
            "AMCS1143 - CYBERSECURITY FUNDAMENTALS (3 credits)",
            "AMCS1153 - HUMAN-COMPUTER INTERACTION (3 credits)",
            "AMCS1163 - SOFTWARE TESTING (3 credits)",
            "AMIT2014 - WEB AND MOBILE SYSTEMS (4 credits)"
        ],
        "Mathematics Subjects": [
            "AMAT1013 - CALCULUS I (3 credits)",
            "AMAT1023 - CALCULUS II (3 credits)",
            "AMAT1033 - LINEAR ALGEBRA (3 credits)",
            "AMAT1043 - PROBABILITY AND STATISTICS (3 credits)",
            "AMAT1053 - DIFFERENTIAL EQUATIONS (3 credits)",
            "AMCS1073 - DISCRETE MATHEMATICS (3 credits)"
        ],
        "Theory Subjects": [
            "AMCS1023 - DATABASE SYSTEMS (3 credits)",
            "AMCS1063 - COMPUTER ARCHITECTURE (3 credits)",
            "AMCS2093 - OPERATING SYSTEMS (3 credits)",
            "AMIT2033 - NETWORKING ESSENTIALS (3 credits)",
            "AMIS1012 - ETHICS IN COMPUTING (2 credits)"
        ],
        "General Subjects": [
            "ECOQ - CO-CURRICULAR (2 credits)",
            "EGU2 - ELECTIVE COURSE (2 credits)",
            "MPU-2202 - CIVIC CONSCIOUSNESS AND VOLUNTEERISM",
            "MPU-2212 - BAHASA KEBANGSAAN A"
        ]
    }

    w = tk.Toplevel(root)
    w.title("📝 Homework Planner - Year 2 Semester 1")
    w.configure(bg=COLORS["background"]) 
    w.resizable(True, True)  # Allow resizing
    w.minsize(800, 500)  # Set minimum size
    w.maxsize(1400, 1000)  # Set maximum size
    w.attributes('-topmost', False)  # Ensure window can be resized
    # w.transient(root)  # Commented out to allow proper resizing
    # Don't make it modal - allow users to switch between windows
    
    # Set full screen after window is created - try multiple methods
    try:
        w.wm_state('zoomed')  # Alternative method for Windows
    except:
        try:
            w.state('zoomed')  # Fallback method
        except:
            # Fallback: set to screen dimensions
            w.geometry(f"{w.winfo_screenwidth()}x{w.winfo_screenheight()}+0+0")
    w.update()  # Force update to apply the state

    frm = ttk.Frame(w, padding=20)
    frm.pack(fill=tk.BOTH, expand=True)

    title = tk.Label(frm, text="📝 Homework Planner - Year 2 Semester 1", font=("Arial", 22, "bold"), fg=COLORS["primary"], bg=COLORS["background"])
    title.pack(pady=(0, 10))

    # Simple stats bar
    stats_frame = tk.Frame(frm, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    stats_frame.pack(fill=tk.X, pady=(0, 15))
    
    pending_count = sum(1 for item in planner.items if item.status == "Pending")
    completed_count = sum(1 for item in planner.items if item.status == "Completed")
    total_count = len(planner.items)
    
    # Calculate overdue items
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    overdue_count = sum(1 for item in planner.items if item.status == "Pending" and item.due < today)
    
    stats_text = f"📊 Quick Stats: {total_count} total | {pending_count} pending | {completed_count} completed | {overdue_count} overdue"
    stats_label = tk.Label(stats_frame, text=stats_text, 
                          fg=COLORS["text_primary"], bg=COLORS["border"], 
                          font=("Arial", 14, "bold"))
    stats_label.pack(pady=10)

    # Simple filter buttons with better spacing
    filter_frame = tk.Frame(frm, bg=COLORS["background"])
    filter_frame.pack(fill=tk.X, pady=(0, 8))

    current_filter = {"value": "all"}

    def apply_filter(filter_type):
        current_filter["value"] = filter_type
        refresh()

    # Create simple filter buttons with better spacing
    all_btn = tk.Button(filter_frame, text="📋 All", 
                       font=("Arial", 11, "bold"), fg="white", 
                       bg=COLORS["primary"], relief=tk.RAISED, bd=2,
                       command=lambda: apply_filter("all"), cursor="hand2", height=1, width=8)
    all_btn.pack(side=tk.LEFT, padx=(0, 5))

    pending_btn = tk.Button(filter_frame, text="⏳ Pending", 
                           font=("Arial", 11, "bold"), fg="white", 
                           bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                           command=lambda: apply_filter("pending"), cursor="hand2", height=1, width=10)
    pending_btn.pack(side=tk.LEFT, padx=(0, 5))

    completed_btn = tk.Button(filter_frame, text="✅ Completed", 
                             font=("Arial", 11, "bold"), fg="white", 
                             bg=COLORS["accent"], relief=tk.RAISED, bd=2,
                             command=lambda: apply_filter("completed"), cursor="hand2", height=1, width=12)
    completed_btn.pack(side=tk.LEFT, padx=(0, 5))

    overdue_btn = tk.Button(filter_frame, text="🚨 Overdue", 
                           font=("Arial", 11, "bold"), fg="white", 
                           bg="#FF5722", relief=tk.RAISED, bd=2,
                           command=lambda: apply_filter("overdue"), cursor="hand2", height=1, width=10)
    overdue_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Status color guide
    guide_frame = tk.Frame(frm, bg=COLORS["background"])
    guide_frame.pack(fill=tk.X, pady=(5, 10))
    
    guide_label = tk.Label(guide_frame, text="📊 Color Guide: ✅ Completed (Green) | ⚠️ Overdue (Red) | ⏳ Pending (Orange) ", 
                          font=("Arial", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["background"])
    guide_label.pack()

    # Simple homework table
    columns = ("id", "subject", "title", "deadline", "priority", "status")
    tree = ttk.Treeview(frm, columns=columns, show="headings", height=10)
    tree.heading("id", text="ID")
    tree.heading("subject", text="Subject")
    tree.heading("title", text="Title")
    tree.heading("deadline", text="Deadline")
    tree.heading("priority", text="Priority")
    tree.heading("status", text="Status")
    tree.column("id", width=50, anchor=tk.CENTER, minwidth=40)
    tree.column("subject", width=500, minwidth=300)
    tree.column("title", width=400, minwidth=200)
    tree.column("deadline", width=120, anchor=tk.CENTER, minwidth=100)
    tree.column("priority", width=100, anchor=tk.CENTER, minwidth=80)
    tree.column("status", width=120, anchor=tk.CENTER, minwidth=100)
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Add tooltip functionality for truncated text
    def show_tooltip(event):
        item = tree.identify_row(event.y)
        if item:
            values = tree.item(item, "values")
            if values:
                subject = values[1]
                title = values[2]
                # Show tooltip if text is truncated
                if "..." in subject or "..." in title:
                    tooltip_text = f"Subject: {subject}\nTitle: {title}"
                    # Create tooltip window
                    tooltip = tk.Toplevel()
                    tooltip.wm_overrideredirect(True)
                    tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                    label = tk.Label(tooltip, text=tooltip_text, 
                                   bg="lightyellow", fg="black", 
                                   font=("Arial", 10), relief="solid", borderwidth=1)
                    label.pack()
                    # Store tooltip reference for cleanup
                    tree.tooltip = tooltip
                    # Auto-hide after 3 seconds
                    tree.after(3000, lambda: tooltip.destroy() if tooltip.winfo_exists() else None)
    
    def hide_tooltip(event):
        if hasattr(tree, 'tooltip') and tree.tooltip.winfo_exists():
            tree.tooltip.destroy()
    
    tree.bind("<Motion>", show_tooltip)
    tree.bind("<Leave>", hide_tooltip)

    def refresh():
        for iid in tree.get_children():
            tree.delete(iid)
        
        # Filter items
        filtered_items = planner.items
        if current_filter["value"] == "pending":
            filtered_items = [item for item in planner.items if item.status == "Pending"]
        elif current_filter["value"] == "completed":
            filtered_items = [item for item in planner.items if item.status == "Completed"]
        elif current_filter["value"] == "overdue":
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            filtered_items = [item for item in planner.items if item.status == "Pending" and item.due < today]

        # Sort by priority (High -> Medium -> Low) then by due date
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        filtered_items = list(filtered_items)
        filtered_items.sort(key=lambda x: (priority_order.get(getattr(x, 'priority', 'Medium'), 1), getattr(x, 'due', None) or "9999-12-31"))

        for idx, item in enumerate(filtered_items):
            # Use colored text for priority display
            if item.priority == "High":
                priority_display = "● HIGH"
            elif item.priority == "Medium":
                priority_display = "● MED"
            else:  # Low
                priority_display = "● LOW"
            
            status_icon = "✅" if item.status == "Completed" else "⏳"
            tree.insert("", tk.END, iid=str(idx), values=(
                idx + 1,
                item.subject[:80] + "..." if len(item.subject) > 80 else item.subject,
                item.title[:60] + "..." if len(item.title) > 60 else item.title,
                item.due,
                priority_display,
                f"{status_icon} {item.status}"
            ))
            
            # Apply color styling based on status
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")
            
            if item.status == "Completed":
                tree.tag_configure("completed", foreground="green", background="#f0f8f0")
                tree.item(str(idx), tags=("completed",))
            elif item.status == "Pending" and item.due and item.due < today:
                tree.tag_configure("overdue", foreground="red", background="#fff0f0")
                tree.item(str(idx), tags=("overdue",))
            elif item.status == "Pending":
                tree.tag_configure("pending", foreground="orange", background="#fff8f0")
                tree.item(str(idx), tags=("pending",))
            else:  # In Progress or other status
                tree.tag_configure("in_progress", foreground="blue", background="#f0f0ff")
                tree.item(str(idx), tags=("in_progress",))

    # Add homework dialog - improved version
    def homework_dialog(initial=None):
        dlg = tk.Toplevel(w)
        dlg.title("Add/Edit Homework" if initial is None else "Edit Homework")
        dlg.configure(bg=COLORS["background"]) 
        dlg.transient(w)
        dlg.grab_set()
        dlg.geometry("700x600")
        dlg.resizable(True, True)
        dlg.minsize(600, 500)  # Set minimum size
        dlg.maxsize(1000, 800)  # Set maximum size

        # Header
        header_frame = tk.Frame(dlg, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="📝 Homework Details", 
                        font=("Arial", 18, "bold"), fg="white", bg=COLORS["primary"])
        title.pack(expand=True)

        f = tk.Frame(dlg, bg=COLORS["background"], padx=30, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        # Subject category selection
        category_label = tk.Label(f, text="📚 Subject Category", bg=COLORS["background"], 
                                 fg=COLORS["text_primary"], font=("Arial", 12, "bold"))
        category_label.pack(anchor=tk.W, pady=(0, 5))
        category_var = tk.StringVar(value="Programming Subjects")
        category_cb = ttk.Combobox(f, textvariable=category_var, values=list(SUBJECTS_DATABASE.keys()), 
                                  state="readonly", font=("Arial", 11))
        category_cb.pack(fill=tk.X, pady=(0, 15))

        # Subject selection with custom course option
        subject_label = tk.Label(f, text="📖 Subject", bg=COLORS["background"], 
                                fg=COLORS["text_primary"], font=("Arial", 12, "bold"))
        subject_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Subject selection frame
        subject_frame = tk.Frame(f, bg=COLORS["background"])
        subject_frame.pack(fill=tk.X, pady=(0, 15))
        
        subject_var = tk.StringVar()
        subject_cb = ttk.Combobox(subject_frame, textvariable=subject_var, state="readonly", font=("Arial", 11))
        subject_cb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Add custom course button
        add_course_btn = tk.Button(subject_frame, text="➕ Add Custom", 
                                  font=("Arial", 10, "bold"), fg="white", 
                                  bg="#FF9800", relief=tk.RAISED, bd=2,
                                  cursor="hand2", height=1, width=12)
        add_course_btn.pack(side=tk.RIGHT)

        def add_custom_course():
            """Dialog to add a custom course to the current category"""
            custom_dlg = tk.Toplevel(dlg)
            custom_dlg.title("Add Custom Course")
            custom_dlg.configure(bg=COLORS["background"])
            custom_dlg.transient(dlg)
            custom_dlg.grab_set()
            custom_dlg.geometry("400x200")
            custom_dlg.resizable(False, False)
            
            # Center the dialog
            custom_dlg.update_idletasks()
            x = (custom_dlg.winfo_screenwidth() // 2) - (400 // 2)
            y = (custom_dlg.winfo_screenheight() // 2) - (200 // 2)
            custom_dlg.geometry(f"400x200+{x}+{y}")
            
            # Header
            header_frame = tk.Frame(custom_dlg, bg=COLORS["primary"], height=50)
            header_frame.pack(fill=tk.X)
            header_frame.pack_propagate(False)
            
            title = tk.Label(header_frame, text="➕ Add Custom Course", 
                            font=("Arial", 14, "bold"), fg="white", bg=COLORS["primary"])
            title.pack(expand=True)
            
            # Content
            content_frame = tk.Frame(custom_dlg, bg=COLORS["background"], padx=20, pady=15)
            content_frame.pack(fill=tk.BOTH, expand=True)
            
            # Course name input
            course_label = tk.Label(content_frame, text="Course Name:", bg=COLORS["background"], 
                                   fg=COLORS["text_primary"], font=("Arial", 11, "bold"))
            course_label.pack(anchor=tk.W, pady=(0, 5))
            
            course_var = tk.StringVar()
            course_entry = tk.Entry(content_frame, textvariable=course_var, width=40, 
                                   bg=COLORS["border"], fg=COLORS["text_primary"], 
                                   insertbackground=COLORS["text_primary"], font=("Arial", 11))
            course_entry.pack(fill=tk.X, pady=(0, 10))
            
            # Category info
            category_info = tk.Label(content_frame, 
                                    text=f"Adding to category: {category_var.get()}", 
                                    bg=COLORS["background"], fg=COLORS["text_secondary"], 
                                    font=("Arial", 10))
            category_info.pack(anchor=tk.W, pady=(0, 15))
            
            # Buttons
            btn_frame = tk.Frame(content_frame, bg=COLORS["background"])
            btn_frame.pack(fill=tk.X)
            
            def save_custom_course():
                course_name = course_var.get().strip()
                if not course_name:
                    messagebox.showerror("Error", "Course name cannot be empty", parent=custom_dlg)
                    return
                
                # Add to the current category
                current_category = category_var.get()
                if current_category in SUBJECTS_DATABASE:
                    # Check if course already exists in this category
                    if course_name in SUBJECTS_DATABASE[current_category]:
                        messagebox.showwarning("Duplicate Course", 
                            f"Course '{course_name}' already exists in {current_category}.\n\n"
                            f"Please choose a different name or select the existing course from the dropdown.",
                            parent=custom_dlg)
                        return
                    
                    SUBJECTS_DATABASE[current_category].append(course_name)
                    # Update the combobox
                    update_subjects()
                    # Set the new course as selected
                    subject_var.set(course_name)
                    messagebox.showinfo("Success", f"Course '{course_name}' added to {current_category}", parent=custom_dlg)
                    custom_dlg.destroy()
                else:
                    messagebox.showerror("Error", "Invalid category selected", parent=custom_dlg)
            
            save_btn = tk.Button(btn_frame, text="✅ Add Course", 
                                font=("Arial", 10, "bold"), fg="white", 
                                bg="#4CAF50", relief=tk.RAISED, bd=2,
                                command=save_custom_course, cursor="hand2", height=1, width=12)
            save_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            cancel_btn = tk.Button(btn_frame, text="❌ Cancel", 
                                  font=("Arial", 10, "bold"), fg="white", 
                                  bg="#F44336", relief=tk.RAISED, bd=2,
                                  command=custom_dlg.destroy, cursor="hand2", height=1, width=12)
            cancel_btn.pack(side=tk.LEFT)
            
            # Focus on entry
            course_entry.focus()
            
            # Bind Enter key to save
            course_entry.bind('<Return>', lambda e: save_custom_course())

        add_course_btn.config(command=add_custom_course)

        def update_subjects():
            subjects = SUBJECTS_DATABASE.get(category_var.get(), [])
            subject_cb['values'] = subjects
            if subjects:
                subject_var.set(subjects[0])

        category_cb.bind('<<ComboboxSelected>>', lambda e: update_subjects())
        update_subjects()

        # Title
        title_label = tk.Label(f, text="📝 Title", bg=COLORS["background"], 
                              fg=COLORS["text_primary"], font=("Arial", 12, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 5))
        title_e = tk.Entry(f, width=50, bg=COLORS["border"], fg=COLORS["text_primary"], 
                          insertbackground=COLORS["text_primary"], font=("Arial", 11)) 
        title_e.pack(fill=tk.X, pady=(0, 15))

        # Description
        desc_label = tk.Label(f, text="📄 Description (optional)", bg=COLORS["background"], 
                             fg=COLORS["text_primary"], font=("Arial", 12, "bold"))
        desc_label.pack(anchor=tk.W, pady=(0, 5))
        desc_e = tk.Text(f, height=4, bg=COLORS["border"], fg=COLORS["text_primary"], 
                        insertbackground=COLORS["text_primary"], font=("Arial", 11)) 
        desc_e.pack(fill=tk.X, pady=(0, 15))

        # Deadline
        deadline_label = tk.Label(f, text="📅 Deadline (YYYY-MM-DD)", bg=COLORS["background"], 
                                 fg=COLORS["text_primary"], font=("Arial", 12, "bold"))
        deadline_label.pack(anchor=tk.W, pady=(0, 5))
        deadline_e = tk.Entry(f, width=20, bg=COLORS["border"], fg=COLORS["text_primary"], 
                             insertbackground=COLORS["text_primary"], font=("Arial", 11)) 
        deadline_e.pack(fill=tk.X, pady=(0, 8))
        
        # Set default value to today's date
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        deadline_e.insert(0, today_str)
        
        # Add helpful hint
        hint_label = tk.Label(f, text=f"💡 Tip: Deadline must be today or in the future (Today: {today_str})", 
                             bg=COLORS["background"], fg=COLORS["text_secondary"], font=("Arial", 10))
        hint_label.pack(anchor=tk.W, pady=(0, 15))

        # Priority
        priority_label = tk.Label(f, text="⚡ Priority", bg=COLORS["background"], 
                                 fg=COLORS["text_primary"], font=("Arial", 12, "bold"))
        priority_label.pack(anchor=tk.W, pady=(0, 5))
        priority_var = tk.StringVar(value="Medium")
        priority_cb = ttk.Combobox(f, textvariable=priority_var, values=["High", "Medium", "Low"], 
                                  state="readonly", font=("Arial", 11))
        priority_cb.pack(fill=tk.X, pady=(0, 15))

        if initial:
            title_e.insert(0, initial.get("title", ""))
            desc_e.insert("1.0", initial.get("description", ""))
            deadline_e.insert(0, initial.get("due", ""))
            priority_var.set(initial.get("priority", "Medium"))
            # Find and set subject
            for category, subjects in SUBJECTS_DATABASE.items():
                if initial.get("subject") in subjects:
                    category_var.set(category)
                    subject_var.set(initial.get("subject"))
                    break

        # Button frame with better styling
        btn_frame = tk.Frame(f, bg=COLORS["background"], relief=tk.RAISED, bd=2)
        btn_frame.pack(pady=(20, 0), padx=10)

        result = {"ok": False, "subject": "", "title": "", "description": "", "deadline": "", "priority": "Medium"}

        def ok():
            try:
                result["subject"] = subject_var.get().strip()
                result["title"] = title_e.get().strip()
                result["description"] = desc_e.get("1.0", tk.END).strip()
                result["deadline"] = deadline_e.get().strip()
                result["priority"] = priority_var.get().strip()
                
                # Validate required fields
                if not result["subject"] or not result["subject"].strip():
                    messagebox.showerror("Error", "Subject is required and cannot be empty", parent=dlg)
                    return
                if not result["title"] or not result["title"].strip():
                    messagebox.showerror("Error", "Title is required and cannot be empty", parent=dlg)
                    return
                
                # Validate title is not numeric only
                if result["title"].strip().isdigit():
                    messagebox.showerror("Error", "Title must contain text, not just numbers", parent=dlg)
                    return
                
                # Validate due date is required
                if not result["deadline"] or not result["deadline"].strip():
                    messagebox.showerror("Error", "Due date is required and cannot be empty", parent=dlg)
                    return
                
                # Validate deadline format and date
                if result["deadline"]:
                    try:
                        from datetime import datetime
                        deadline_date = datetime.strptime(result["deadline"], "%Y-%m-%d").date()
                        today = datetime.now().date()
                        
                        if deadline_date < today:
                            messagebox.showerror("Error", f"Deadline must be today or in the future.\n"
                                                         f"Today: {today.strftime('%Y-%m-%d')}\n"
                                                         f"Your deadline: {deadline_date.strftime('%Y-%m-%d')}", parent=dlg)
                            return
                            
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD (e.g., 2024-01-15)", parent=dlg)
                        return
                
                result["ok"] = True
                dlg.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}", parent=dlg)

        # Beautiful buttons
        save_btn = tk.Button(btn_frame, text="✅ Save Homework", 
                            font=("Arial", 12, "bold"), fg="white", 
                            bg="#4CAF50", relief=tk.RAISED, bd=2,
                            command=ok, cursor="hand2", height=2, width=18)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = tk.Button(btn_frame, text="❌ Cancel", 
                              font=("Arial", 12, "bold"), fg="white", 
                              bg="#F44336", relief=tk.RAISED, bd=2,
                              command=dlg.destroy, cursor="hand2", height=2, width=15)
        cancel_btn.pack(side=tk.LEFT)

        dlg.wait_window()
        return result

    # Enhanced control buttons
    controls = tk.Frame(frm, bg=COLORS["background"])
    controls.pack(fill=tk.X, pady=15)

    def add_homework():
        data = homework_dialog()
        if not data["ok"]:
            return
        try:
            planner.add(data["subject"], data["title"], data["deadline"], data["description"], data["priority"])
            refresh()
            # Update stats
            pending_count = sum(1 for item in planner.items if item.status == "Pending")
            completed_count = sum(1 for item in planner.items if item.status == "Completed")
            stats_label.config(text=f"📊 Quick Stats: {pending_count} pending, {completed_count} completed")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=w)

    # Simple control buttons
    add_btn = tk.Button(controls, text="📝 Add Homework", 
                       font=("Arial", 12, "bold"), fg="white", 
                       bg=COLORS["accent"], relief=tk.RAISED, bd=2,
                       command=add_homework, cursor="hand2", height=2, width=15)
    add_btn.pack(side=tk.LEFT, padx=5)

    def edit_homework():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a homework item to edit", parent=w)
            return
        idx = int(sel[0])
        filtered_items = [item for item in planner.items if current_filter["value"] == "all" or 
                         (current_filter["value"] == "pending" and item.status == "Pending") or
                         (current_filter["value"] == "completed" and item.status == "Completed") or
                         (current_filter["value"] == "overdue" and item.status == "Pending" and item.due < datetime.now().strftime("%Y-%m-%d"))]
        if idx >= len(filtered_items):
            return
        item = filtered_items[idx]
        data = homework_dialog({"subject": item.subject, "title": item.title, "due": item.due, 
                               "description": getattr(item, 'details', ''), "priority": getattr(item, 'priority', 'Medium')})
        if not data["ok"]:
            return
        try:
            # Find original index
            orig_idx = planner.items.index(item)
            planner.update(orig_idx, subject=data["subject"], title=data["title"], due=data["deadline"], details=data["description"], priority=data["priority"])
            refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=w)

    edit_btn = tk.Button(controls, text="✏️ Edit", 
                        font=("Arial", 12, "bold"), fg="white", 
                        bg=COLORS["primary"], relief=tk.RAISED, bd=2,
                        command=edit_homework, cursor="hand2", height=2, width=10)
    edit_btn.pack(side=tk.LEFT, padx=5)

    def mark_complete():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a homework item", parent=w)
            return
        idx = int(sel[0])
        filtered_items = [item for item in planner.items if current_filter["value"] == "all" or 
                         (current_filter["value"] == "pending" and item.status == "Pending") or
                         (current_filter["value"] == "completed" and item.status == "Completed") or
                         (current_filter["value"] == "overdue" and item.status == "Pending" and item.due < datetime.now().strftime("%Y-%m-%d"))]
        if idx >= len(filtered_items):
            return
        item = filtered_items[idx]
        try:
            orig_idx = planner.items.index(item)
            if item.status == "Pending":
                planner.mark_complete(orig_idx)
            else:
                planner.update(orig_idx, status="Pending")
            refresh()
            # Update stats
            pending_count = sum(1 for item in planner.items if item.status == "Pending")
            completed_count = sum(1 for item in planner.items if item.status == "Completed")
            stats_label.config(text=f"📊 Quick Stats: {pending_count} pending, {completed_count} completed")
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=w)

    toggle_btn = tk.Button(controls, text="✅ Toggle Status", 
                          font=("Arial", 12, "bold"), fg="white", 
                          bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                          command=mark_complete, cursor="hand2", height=2, width=15)
    toggle_btn.pack(side=tk.LEFT, padx=5)

    def delete_homework():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a homework item to delete", parent=w)
            return
        idx = int(sel[0])
        filtered_items = [item for item in planner.items if current_filter["value"] == "all" or 
                         (current_filter["value"] == "pending" and item.status == "Pending") or
                         (current_filter["value"] == "completed" and item.status == "Completed") or
                         (current_filter["value"] == "overdue" and item.status == "Pending" and item.due < datetime.now().strftime("%Y-%m-%d"))]
        if idx >= len(filtered_items):
            return
        item = filtered_items[idx]
        if messagebox.askyesno("Confirm", f"Delete '{item.title}'?"):
            try:
                orig_idx = planner.items.index(item)
                planner.remove(orig_idx)
                refresh()
                # Update stats
                pending_count = sum(1 for item in planner.items if item.status == "Pending")
                completed_count = sum(1 for item in planner.items if item.status == "Completed")
                stats_label.config(text=f"📊 Quick Stats: {pending_count} pending, {completed_count} completed")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=w)

    delete_btn = tk.Button(controls, text="🗑️ Delete", 
                          font=("Arial", 12, "bold"), fg="white", 
                          bg="red", relief=tk.RAISED, bd=2,
                          command=delete_homework, cursor="hand2", height=2, width=10)
    delete_btn.pack(side=tk.LEFT, padx=5)

    # Back to Home button
    def back_to_home():
        w.destroy()
    
    back_home_btn = tk.Button(controls, text="🏠 Back to Home", 
                             font=("Arial", 12, "bold"), fg="white", 
                             bg="#9C27B0", relief=tk.RAISED, bd=2,
                             command=back_to_home, cursor="hand2", height=2, width=15)
    back_home_btn.pack(side=tk.LEFT, padx=5)

    refresh()


def open_pomodoro_gui(root):
    w = tk.Toplevel(root)
    w.title("⏱ Pomodoro Timer")
    w.configure(bg=COLORS["background"]) 
    w.resizable(True, True)
    w.minsize(600, 500)
    w.maxsize(900, 700)  # Set maximum size
    w.attributes('-topmost', False)  # Ensure window can be resized
    # w.transient(root)  # Commented out to allow proper resizing
    # Don't make it modal - users should be able to use other features while timer runs
    
    # Set a reasonable window size to show all buttons
    w.geometry("800x600+200+150")  # Width x Height + X offset + Y offset
    w.update()  # Force update to apply the state

    # Beautiful header
    header_frame = tk.Frame(w, bg=COLORS["accent"], height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_frame = tk.Frame(header_frame, bg=COLORS["accent"])
    title_frame.pack(expand=True)
    
    title = tk.Label(title_frame, text="⏱ Study Pomodoro Timer", 
                    font=("Arial", 26, "bold"), fg="white", bg=COLORS["accent"])
    title.pack(pady=10)
    
    subtitle = tk.Label(title_frame, text="Focus • Break • Repeat", 
                       font=("Arial", 12), fg="white", bg=COLORS["accent"])
    subtitle.pack(pady=(0, 5))

    frm = tk.Frame(w, bg=COLORS["background"], padx=25, pady=20)
    frm.pack(fill=tk.BOTH, expand=True)

    # Session details storage
    session_details = {
        'start_time': '',
        'work_time': (0, 0),
        'break_time': (0, 0),
        'rounds': 0,
        'completed_work_sessions': 0,
        'status': 'Incomplete',
        'work_title': '',
        'date': ''
    }
    
    # Session history storage
    session_history = []

    # Timer variables
    timer_running = False
    current_round = 0
    current_mode = "Work"  # "Work" or "Break"
    time_left = 0

    # Beautiful timer display frame
    display_frame = tk.Frame(frm, bg=COLORS["border"], relief=tk.RAISED, bd=3)
    display_frame.pack(fill=tk.X, pady=(10, 15))

    # Timer display with circular effect
    timer_frame = tk.Frame(display_frame, bg=COLORS["primary"], relief=tk.RAISED, bd=2)
    timer_frame.pack(pady=15, padx=15, fill=tk.X)
    
    timer_label = tk.Label(timer_frame, text="00:00", font=("Arial", 56, "bold"), 
                          fg="white", bg=COLORS["primary"])
    timer_label.pack(pady=15)

    # Status display
    status_label = tk.Label(display_frame, text="🎯 Ready to start your focus session", 
                           font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                           bg=COLORS["border"])
    status_label.pack(pady=(0, 10))

    # Round display
    round_label = tk.Label(display_frame, text="", font=("Arial", 14), 
                          fg=COLORS["text_secondary"], bg=COLORS["border"])
    round_label.pack(pady=(0, 15))

    # Beautiful settings frame
    settings_frame = tk.Frame(frm, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    settings_frame.pack(fill=tk.X, pady=(5, 10))
    
    settings_title = tk.Label(settings_frame, text="⚙️ Timer Settings", 
                             font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                             bg=COLORS["border"])
    settings_title.pack(pady=(12, 8))

    # Work title setting (moved to top)
    title_frame = tk.Frame(settings_frame, bg=COLORS["border"])
    title_frame.pack(fill=tk.X, pady=8, padx=15)

    tk.Label(title_frame, text="📝 Work Title:", font=("Arial", 14, "bold"), 
            fg=COLORS["text_primary"], bg=COLORS["border"]).pack(side=tk.LEFT)

    work_title_var = tk.StringVar(value="")
    work_title_entry = tk.Entry(title_frame, textvariable=work_title_var, width=40, font=("Arial", 12),
                               bg=COLORS["background"], fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"])
    work_title_entry.pack(side=tk.LEFT, padx=(20, 5), fill=tk.X, expand=True)

    # Work time settings
    work_frame = tk.Frame(settings_frame, bg=COLORS["border"])
    work_frame.pack(fill=tk.X, pady=8, padx=15)

    tk.Label(work_frame, text="💼 Work Time:", font=("Arial", 14, "bold"), 
            fg=COLORS["text_primary"], bg=COLORS["border"]).pack(side=tk.LEFT)

    work_min_var = tk.StringVar(value="25")
    work_sec_var = tk.StringVar(value="0")
    
    tk.Label(work_frame, text="Minutes:", bg=COLORS["border"], fg=COLORS["text_primary"], font=("Arial", 12)).pack(side=tk.LEFT, padx=(20, 5))
    work_min_entry = tk.Entry(work_frame, textvariable=work_min_var, width=5, font=("Arial", 12),
                             bg=COLORS["background"], fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"])
    work_min_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(work_frame, text="Seconds:", bg=COLORS["border"], fg=COLORS["text_primary"], font=("Arial", 12)).pack(side=tk.LEFT, padx=(10, 5))
    work_sec_entry = tk.Entry(work_frame, textvariable=work_sec_var, width=5, font=("Arial", 12),
                             bg=COLORS["background"], fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"])
    work_sec_entry.pack(side=tk.LEFT, padx=5)

    # Break time settings
    break_frame = tk.Frame(settings_frame, bg=COLORS["border"])
    break_frame.pack(fill=tk.X, pady=8, padx=15)

    tk.Label(break_frame, text="☕ Break Time:", font=("Arial", 14, "bold"), 
            fg=COLORS["text_primary"], bg=COLORS["border"]).pack(side=tk.LEFT)

    break_min_var = tk.StringVar(value="5")
    break_sec_var = tk.StringVar(value="0")
    
    tk.Label(break_frame, text="Minutes:", bg=COLORS["border"], fg=COLORS["text_primary"], font=("Arial", 12)).pack(side=tk.LEFT, padx=(20, 5))
    break_min_entry = tk.Entry(break_frame, textvariable=break_min_var, width=5, font=("Arial", 12),
                              bg=COLORS["background"], fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"])
    break_min_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(break_frame, text="Seconds:", bg=COLORS["border"], fg=COLORS["text_primary"], font=("Arial", 12)).pack(side=tk.LEFT, padx=(10, 5))
    break_sec_entry = tk.Entry(break_frame, textvariable=break_sec_var, width=5, font=("Arial", 12),
                              bg=COLORS["background"], fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"])
    break_sec_entry.pack(side=tk.LEFT, padx=5)

    # Rounds setting
    rounds_frame = tk.Frame(settings_frame, bg=COLORS["border"])
    rounds_frame.pack(fill=tk.X, pady=8, padx=15)

    tk.Label(rounds_frame, text="🔄 Rounds:", font=("Arial", 14, "bold"), 
            fg=COLORS["text_primary"], bg=COLORS["border"]).pack(side=tk.LEFT)

    rounds_var = tk.StringVar(value="4")
    rounds_entry = tk.Entry(rounds_frame, textvariable=rounds_var, width=5, font=("Arial", 12),
                           bg=COLORS["background"], fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"])
    rounds_entry.pack(side=tk.LEFT, padx=(20, 5))

    # Beautiful control buttons
    control_frame = tk.Frame(frm, bg=COLORS["background"])
    control_frame.pack(fill=tk.X, pady=(15, 10))

    def update_timer_display():
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def countdown_timer():
        nonlocal time_left, timer_running, current_round, current_mode
        
        if not timer_running:
            return
            
        # Update display every tick
        update_timer_display()

        if time_left > 0:
            time_left -= 1
            w.after(1000, countdown_timer)
            return

        # Timer finished (time_left == 0)
        # Provide an alert
        try:
            w.bell()
        except Exception:
            pass

        if current_mode == "Work":
            # Completed a work session
            session_details['completed_work_sessions'] += 1
            current_round += 1
            if current_round <= session_details['rounds']:
                current_mode = "Break"
                time_left = session_details['break_time'][0] * 60 + session_details['break_time'][1]
                work_title = session_details['work_title']
                status_label.config(text=f"☕ Break time! Round {current_round}/{session_details['rounds']}")
                round_label.config(text=f"Round {current_round}/{session_details['rounds']} - Break | 📝 {work_title}")
                # Immediately update display for new phase
                update_timer_display()
                w.after(1000, countdown_timer)
            else:
                # All rounds completed
                session_details['status'] = "Completed"
                session_details['end_time'] = datetime.datetime.now().strftime("%H:%M")
                # Save to history
                session_history.append(session_details.copy())
                status_label.config(text=f"🎉 All {session_details['rounds']} rounds completed! Good job!")
                round_label.config(text="")
                timer_running = False
        else:
            # Break finished, start next work session
            current_mode = "Work"
            time_left = session_details['work_time'][0] * 60 + session_details['work_time'][1]
            work_title = session_details['work_title']
            status_label.config(text=f"💼 Work time! Round {current_round}/{session_details['rounds']}")
            round_label.config(text=f"Round {current_round}/{session_details['rounds']} - Work | 📝 {work_title}")
            update_timer_display()
            w.after(1000, countdown_timer)

    def start_timer():
        nonlocal timer_running, time_left, current_round, current_mode
        
        if timer_running:
            return
        
        try:
            work_min = int(work_min_var.get())
            work_sec = int(work_sec_var.get())
            break_min = int(break_min_var.get())
            break_sec = int(break_sec_var.get())
            rounds = int(rounds_var.get())
            work_title = work_title_var.get().strip()
            
            # Work title validation
            if not work_title:
                messagebox.showerror("Error", "Work title cannot be empty. Please enter what you're working on.", parent=w)
                return
            if len(work_title) < 3:
                messagebox.showerror("Error", "Work title must be at least 3 characters long.", parent=w)
                return
            if len(work_title) > 100:
                messagebox.showerror("Error", "Work title cannot exceed 100 characters.", parent=w)
                return
            if work_title.isdigit():
                messagebox.showerror("Error", "Work title must contain text, not just numbers.", parent=w)
                return
            
            # Enhanced validation like console version
            if work_min < 0 or work_sec < 0:
                messagebox.showerror("Error", "Work time cannot be negative", parent=w)
                return
            if break_min < 0 or break_sec < 0:
                messagebox.showerror("Error", "Break time cannot be negative", parent=w)
                return
            if work_min == 0 and work_sec == 0:
                messagebox.showerror("Error", "Work time cannot be zero", parent=w)
                return
            if rounds <= 0:
                messagebox.showerror("Error", "Rounds must be a positive integer", parent=w)
                return
            if work_sec >= 60:
                messagebox.showerror("Error", "Work seconds must be less than 60", parent=w)
                return
            if break_sec >= 60:
                messagebox.showerror("Error", "Break seconds must be less than 60", parent=w)
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer numbers for all fields", parent=w)
            return
        
        # Update session details
        session_details.update({
            'start_time': datetime.datetime.now().strftime("%H:%M"),
            'work_time': (work_min, work_sec),
            'break_time': (break_min, break_sec),
            'rounds': rounds,
            'completed_work_sessions': 0,
            'status': 'In Progress',
            'work_title': work_title,
            'date': datetime.datetime.now().strftime("%Y-%m-%d")
        })
        
        # Start timer
        current_round = 1
        current_mode = "Work"
        time_left = work_min * 60 + work_sec
        timer_running = True
        
        work_title = session_details['work_title']
        status_label.config(text=f"💼 Work time! Round {current_round}/{rounds}")
        round_label.config(text=f"Round {current_round}/{rounds} - Work | 📝 {work_title}")
        
        # Update initial display
        update_timer_display()
        
        # Start the countdown using tkinter's after method
        w.after(1000, countdown_timer)

    def pause_timer():
        nonlocal timer_running
        if timer_running:
            timer_running = False
            status_label.config(text="⏸️ Paused")
        else:
            # Resume timer
            timer_running = True
            work_title = session_details['work_title']
            status_label.config(text=f"▶️ Resumed - {current_mode} time! Round {current_round}/{session_details['rounds']}")
            round_label.config(text=f"Round {current_round}/{session_details['rounds']} - {current_mode} | 📝 {work_title}")
            w.after(1000, countdown_timer)

    def stop_timer():
        nonlocal timer_running, time_left, current_round, current_mode
        if timer_running:
            timer_running = False
            # Update session status with interrupt information
            session_details['status'] = f"User Interrupt at round {current_round} ({datetime.datetime.now().strftime('%H:%M')})"
            session_details['end_time'] = datetime.datetime.now().strftime("%H:%M")
            # Save to history
            session_history.append(session_details.copy())
            status_label.config(text="⏹️ Timer stopped by user")
            round_label.config(text=f"Interrupted at Round {current_round}/{session_details['rounds']}")
            w.bell()  # Beep sound

    def reset_timer():
        nonlocal timer_running, time_left, current_round, current_mode
        timer_running = False
        time_left = 0
        current_round = 0
        current_mode = "Work"
        timer_label.config(text="00:00")
        status_label.config(text="🎯 Ready to start your focus session")
        round_label.config(text="")
        session_details['status'] = 'Incomplete'
        session_details['completed_work_sessions'] = 0

    def show_session_details():
        if not session_history and not session_details['start_time']:
            messagebox.showinfo("Session History", "⚠ No session data available yet.\n\nStart a Pomodoro session to begin tracking your productivity!", parent=w)
            return
        
        # Create history window
        history_window = tk.Toplevel(w)
        history_window.title("📊 Pomodoro Session History")
        history_window.configure(bg=COLORS["background"])
        history_window.geometry("800x600")
        history_window.resizable(True, True)
        
        # Header
        header_frame = tk.Frame(history_window, bg=COLORS["accent"], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📊 Pomodoro Session History", 
                              font=("Arial", 20, "bold"), fg="white", bg=COLORS["accent"])
        title_label.pack(expand=True)
        
        # Content frame with scrollbar
        content_frame = tk.Frame(history_window, bg=COLORS["background"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create scrollable text widget
        text_frame = tk.Frame(content_frame, bg=COLORS["background"])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        history_text = tk.Text(text_frame, font=("Consolas", 11), bg=COLORS["background"], 
                              fg=COLORS["text_primary"], wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=history_text.yview)
        history_text.configure(yscrollcommand=scrollbar.set)
        
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate history
        history_text.config(state=tk.NORMAL)
        history_text.delete(1.0, tk.END)
        
        if session_history:
            history_text.insert(tk.END, "📈 Session History:\n")
            history_text.insert(tk.END, "=" * 60 + "\n\n")
            
            for i, session in enumerate(reversed(session_history), 1):
                history_text.insert(tk.END, f"Session #{len(session_history) - i + 1}:\n")
                history_text.insert(tk.END, "-" * 30 + "\n")
                history_text.insert(tk.END, f"📝 Work Title: {session.get('work_title', 'N/A')}\n")
                history_text.insert(tk.END, f"📅 Date: {session.get('date', 'N/A')}\n")
                history_text.insert(tk.END, f"⏰ Start Time: {session['start_time']}\n")
                history_text.insert(tk.END, f"⏰ End Time: {session.get('end_time', 'N/A')}\n")
                history_text.insert(tk.END, f"💼 Work Time: {session['work_time'][0]} min {session['work_time'][1]} sec\n")
                history_text.insert(tk.END, f"☕ Break Time: {session['break_time'][0]} min {session['break_time'][1]} sec\n")
                history_text.insert(tk.END, f"🔄 Rounds: {session['rounds']}\n")
                history_text.insert(tk.END, f"✅ Completed Sessions: {session['completed_work_sessions']}\n")
                history_text.insert(tk.END, f"📊 Status: {session['status']}\n")
                history_text.insert(tk.END, "\n")
        else:
            history_text.insert(tk.END, "📊 Current Session:\n")
            history_text.insert(tk.END, "=" * 30 + "\n\n")
            history_text.insert(tk.END, f"📝 Work Title: {session_details.get('work_title', 'N/A')}\n")
            history_text.insert(tk.END, f"📅 Date: {session_details.get('date', 'N/A')}\n")
            history_text.insert(tk.END, f"⏰ Start Time: {session_details['start_time']}\n")
            history_text.insert(tk.END, f"💼 Work Time: {session_details['work_time'][0]} min {session_details['work_time'][1]} sec\n")
            history_text.insert(tk.END, f"☕ Break Time: {session_details['break_time'][0]} min {session_details['break_time'][1]} sec\n")
            history_text.insert(tk.END, f"🔄 Rounds: {session_details['rounds']}\n")
            history_text.insert(tk.END, f"✅ Completed Sessions: {session_details['completed_work_sessions']}\n")
            history_text.insert(tk.END, f"📊 Status: {session_details['status']}\n")
        
        # Add statistics if we have history
        if session_history:
            total_sessions = len(session_history)
            completed_sessions = sum(1 for s in session_history if s['status'] == 'Completed')
            total_work_sessions = sum(s['completed_work_sessions'] for s in session_history)
            total_work_time = sum(s['work_time'][0] * 60 + s['work_time'][1] for s in session_history)
            total_break_time = sum(s['break_time'][0] * 60 + s['break_time'][1] for s in session_history)
            
            history_text.insert(tk.END, "\n" + "=" * 60 + "\n")
            history_text.insert(tk.END, "📈 Statistics:\n")
            history_text.insert(tk.END, "-" * 20 + "\n")
            history_text.insert(tk.END, f"🎯 Total Sessions: {total_sessions}\n")
            history_text.insert(tk.END, f"✅ Completed Sessions: {completed_sessions}\n")
            history_text.insert(tk.END, f"📊 Completion Rate: {(completed_sessions/total_sessions)*100:.1f}%\n")
            history_text.insert(tk.END, f"💼 Total Work Sessions: {total_work_sessions}\n")
            history_text.insert(tk.END, f"⏱️ Total Work Time: {total_work_time//60} hours {total_work_time%60} minutes\n")
            history_text.insert(tk.END, f"☕ Total Break Time: {total_break_time//60} hours {total_break_time%60} minutes\n")
        
        history_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(content_frame, text="❌ Close", 
                             font=("Arial", 12, "bold"), fg="white", 
                             bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                             command=history_window.destroy, cursor="hand2", height=2, width=15)
        close_btn.pack(pady=(20, 0))

    # Beautiful control buttons - COMPACT SIZE
    start_btn = tk.Button(control_frame, text="▶️ Start", 
                         font=("Arial", 12, "bold"), fg="white", 
                         bg=COLORS["accent"], relief=tk.RAISED, bd=2,
                         command=start_timer, cursor="hand2", height=2, width=12)
    start_btn.pack(side=tk.LEFT, padx=5)

    pause_btn = tk.Button(control_frame, text="⏸️ Pause", 
                         font=("Arial", 12, "bold"), fg="white", 
                         bg=COLORS["secondary"], relief=tk.RAISED, bd=2,
                         command=pause_timer, cursor="hand2", height=2, width=12)
    pause_btn.pack(side=tk.LEFT, padx=5)

    stop_btn = tk.Button(control_frame, text="⏹️ Stop", 
                        font=("Arial", 12, "bold"), fg="white", 
                        bg="#FF5722", relief=tk.RAISED, bd=2,
                        command=stop_timer, cursor="hand2", height=2, width=10)
    stop_btn.pack(side=tk.LEFT, padx=5)

    reset_btn = tk.Button(control_frame, text="🔄 Reset", 
                         font=("Arial", 12, "bold"), fg="white", 
                         bg=COLORS["primary"], relief=tk.RAISED, bd=2,
                         command=reset_timer, cursor="hand2", height=2, width=10)
    reset_btn.pack(side=tk.LEFT, padx=5)

    details_btn = tk.Button(control_frame, text="📊 Details", 
                           font=("Arial", 10, "bold"), fg="white", 
                           bg=COLORS["border"], relief=tk.RAISED, bd=2,
                           command=show_session_details, cursor="hand2", height=2, width=12)
    details_btn.pack(side=tk.LEFT, padx=5)

    # Back to Home button
    def back_to_home():
        w.destroy()
    
    back_home_btn = tk.Button(control_frame, text="🏠 Home", 
                             font=("Arial", 12, "bold"), fg="white", 
                             bg="#9C27B0", relief=tk.RAISED, bd=2,
                             command=back_to_home, cursor="hand2", height=2, width=12)
    back_home_btn.pack(side=tk.LEFT, padx=10)

    # Initial display
    update_timer_display()
    
    # Make sure timer display shows 00:00 initially
    timer_label.config(text="00:00")


def launch_main_gui():
    root = tk.Tk()
    root.title("🎓 TARUMT Student Toolkit")
    root.configure(bg=COLORS["background"]) 
    root.resizable(True, True)
    root.minsize(700, 600)
    root.maxsize(1200, 900)  # Set maximum size
    
    # Set full screen after window is created - try multiple methods
    try:
        root.wm_state('zoomed')  # Alternative method for Windows
    except:
        try:
            root.state('zoomed')  # Fallback method
        except:
            # Fallback: set to screen dimensions
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.update()  # Force update to apply the state

    # Create a beautiful header with gradient effect
    header_frame = tk.Frame(root, bg=COLORS["primary"], height=120)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    # Main title with shadow effect
    title_frame = tk.Frame(header_frame, bg=COLORS["primary"])
    title_frame.pack(expand=True)
    
    title = tk.Label(title_frame, text="🎓 TARUMT Student Toolkit", 
                    font=("Arial", 28, "bold"), fg="white", bg=COLORS["primary"]) 
    title.pack(pady=10)
    
    subtitle = tk.Label(title_frame, text="Your Complete Study Companion", 
                       font=("Arial", 14), fg="white", bg=COLORS["primary"]) 
    subtitle.pack()

    # Main container with beautiful styling
    container = tk.Frame(root, bg=COLORS["background"], padx=40, pady=30)
    container.pack(fill=tk.BOTH, expand=True)

    # Create modern card-style buttons
    style = ttk.Style()
    style.configure("Card.TButton", 
                   font=("Arial", 16, "bold"),
                   padding=(20, 15),
                   relief="flat",
                   borderwidth=0)
    
    # Button frame with better spacing
    button_frame = tk.Frame(container, bg=COLORS["background"])
    button_frame.pack(expand=True)
    
    # GPA Calculator Card
    gpa_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    gpa_frame.pack(fill=tk.X, pady=8, padx=10)
    gpa_btn = tk.Button(gpa_frame, text="📊 GPA Calculator", 
                       font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                       bg=COLORS["primary"], relief=tk.FLAT, bd=0,
                       command=lambda: open_gpa_gui(root), cursor="hand2")
    gpa_btn.pack(fill=tk.X, padx=2, pady=2)
    
    # Homework Planner Card
    hw_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    hw_frame.pack(fill=tk.X, pady=8, padx=10)
    hw_btn = tk.Button(hw_frame, text="📝 Homework Planner", 
                      font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                      bg=COLORS["secondary"], relief=tk.FLAT, bd=0,
                      command=lambda: open_homework_gui(root), cursor="hand2")
    hw_btn.pack(fill=tk.X, padx=2, pady=2)
    
    # Pomodoro Timer Card
    pomo_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    pomo_frame.pack(fill=tk.X, pady=8, padx=10)
    pomo_btn = tk.Button(pomo_frame, text="⏱ Pomodoro Timer", 
                        font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                        bg=COLORS["accent"], relief=tk.FLAT, bd=0,
                        command=lambda: open_pomodoro_gui(root), cursor="hand2")
    pomo_btn.pack(fill=tk.X, padx=2, pady=2)
    
    # Flashcards Card
    flash_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    flash_frame.pack(fill=tk.X, pady=8, padx=10)
    flash_btn = tk.Button(flash_frame, text="🎯 Flashcards Master", 
                         font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                         bg=COLORS["primary"], relief=tk.FLAT, bd=0,
                         command=lambda: open_flashcards(root), cursor="hand2")
    flash_btn.pack(fill=tk.X, padx=2, pady=2)

    # Footer with exit button
    footer_frame = tk.Frame(container, bg=COLORS["background"])
    footer_frame.pack(fill=tk.X, pady=(20, 0))
    
    exit_btn = tk.Button(footer_frame, text="🚪 Exit", 
                        font=("Arial", 14), fg=COLORS["text_primary"], 
                        bg=COLORS["border"], relief=tk.FLAT, bd=1,
                        command=root.destroy, cursor="hand2")
    exit_btn.pack(side=tk.RIGHT)

    # Add hover effects
    def on_enter(event):
        event.widget.config(bg=COLORS["text_secondary"])
    
    def on_leave(event):
        if event.widget == gpa_btn:
            event.widget.config(bg=COLORS["primary"])
        elif event.widget == hw_btn:
            event.widget.config(bg=COLORS["secondary"])
        elif event.widget == pomo_btn:
            event.widget.config(bg=COLORS["accent"])
        elif event.widget == flash_btn:
            event.widget.config(bg=COLORS["primary"])
        else:
            event.widget.config(bg=COLORS["border"])
    
    for btn in [gpa_btn, hw_btn, pomo_btn, flash_btn, exit_btn]:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    root.mainloop()

def launch_main_gui2(root):

    root.title("🎓 TARUMT Student Toolkit")
    root.configure(bg=COLORS["background"]) 
    root.resizable(True, True)
    root.minsize(700, 600)
    root.maxsize(1200, 900)  # Set maximum size
    
    # Set full screen after window is created - try multiple methods
    try:
        root.wm_state('zoomed')  # Alternative method for Windows
    except:
        try:
            root.state('zoomed')  # Fallback method
        except:
            # Fallback: set to screen dimensions
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.update()  # Force update to apply the state

    # Create a beautiful header with gradient effect
    header_frame = tk.Frame(root, bg=COLORS["primary"], height=120)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    # Main title with shadow effect
    title_frame = tk.Frame(header_frame, bg=COLORS["primary"])
    title_frame.pack(expand=True)
    
    title = tk.Label(title_frame, text="🎓 TARUMT Student Toolkit", 
                    font=("Arial", 28, "bold"), fg="white", bg=COLORS["primary"]) 
    title.pack(pady=10)
    
    subtitle = tk.Label(title_frame, text="Your Complete Study Companion", 
                       font=("Arial", 14), fg="white", bg=COLORS["primary"]) 
    subtitle.pack()

    # Main container with beautiful styling
    container = tk.Frame(root, bg=COLORS["background"], padx=40, pady=30)
    container.pack(fill=tk.BOTH, expand=True)

    # Create modern card-style buttons
    style = ttk.Style()
    style.configure("Card.TButton", 
                   font=("Arial", 16, "bold"),
                   padding=(20, 15),
                   relief="flat",
                   borderwidth=0)
    
    # Button frame with better spacing
    button_frame = tk.Frame(container, bg=COLORS["background"])
    button_frame.pack(expand=True)
    
    # GPA Calculator Card
    gpa_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    gpa_frame.pack(fill=tk.X, pady=8, padx=10)
    gpa_btn = tk.Button(gpa_frame, text="📊 GPA Calculator", 
                       font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                       bg=COLORS["primary"], relief=tk.FLAT, bd=0,
                       command=lambda: open_gpa_gui(root), cursor="hand2")
    gpa_btn.pack(fill=tk.X, padx=2, pady=2)
    
    # Homework Planner Card
    hw_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    hw_frame.pack(fill=tk.X, pady=8, padx=10)
    hw_btn = tk.Button(hw_frame, text="📝 Homework Planner", 
                      font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                      bg=COLORS["secondary"], relief=tk.FLAT, bd=0,
                      command=lambda: open_homework_gui(root), cursor="hand2")
    hw_btn.pack(fill=tk.X, padx=2, pady=2)
    
    # Pomodoro Timer Card
    pomo_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    pomo_frame.pack(fill=tk.X, pady=8, padx=10)
    pomo_btn = tk.Button(pomo_frame, text="⏱ Pomodoro Timer", 
                        font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                        bg=COLORS["accent"], relief=tk.FLAT, bd=0,
                        command=lambda: open_pomodoro_gui(root), cursor="hand2")
    pomo_btn.pack(fill=tk.X, padx=2, pady=2)
    
    # Flashcards Card
    flash_frame = tk.Frame(button_frame, bg=COLORS["border"], relief=tk.RAISED, bd=2)
    flash_frame.pack(fill=tk.X, pady=8, padx=10)
    flash_btn = tk.Button(flash_frame, text="🎯 Flashcards Master", 
                         font=("Arial", 16, "bold"), fg=COLORS["text_primary"], 
                         bg=COLORS["primary"], relief=tk.FLAT, bd=0,
                         command=lambda: open_flashcards(root), cursor="hand2")
    flash_btn.pack(fill=tk.X, padx=2, pady=2)

    # Footer with exit button
    footer_frame = tk.Frame(container, bg=COLORS["background"])
    footer_frame.pack(fill=tk.X, pady=(20, 0))
    
    exit_btn = tk.Button(footer_frame, text="🚪 Exit", 
                        font=("Arial", 14), fg=COLORS["text_primary"], 
                        bg=COLORS["border"], relief=tk.FLAT, bd=1,
                        command=root.destroy, cursor="hand2")
    exit_btn.pack(side=tk.RIGHT)

    # Add hover effects
    def on_enter(event):
        event.widget.config(bg=COLORS["text_secondary"])
    
    def on_leave(event):
        if event.widget == gpa_btn:
            event.widget.config(bg=COLORS["primary"])
        elif event.widget == hw_btn:
            event.widget.config(bg=COLORS["secondary"])
        elif event.widget == pomo_btn:
            event.widget.config(bg=COLORS["accent"])
        elif event.widget == flash_btn:
            event.widget.config(bg=COLORS["primary"])
        else:
            event.widget.config(bg=COLORS["border"])
    
    for btn in [gpa_btn, hw_btn, pomo_btn, flash_btn, exit_btn]:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    root.mainloop()
if __name__ == "__main__":
    launch_main_gui()


