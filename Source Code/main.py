from __future__ import annotations

import os
import sys
import time

from core.storage import JSONStorage
from core.gpa import GPACalculator, GRADE_POINTS
from core.homework import HomeworkPlanner
from core.pomodoro import PomodoroEngine
from core.flashcards import Flashcards

try:
	import tkinter as tk
	from tkinter import ttk, messagebox
except Exception:
	# Tkinter may not be available in some environments; GUI functions will error if called
	pass


# ---- Utilities ----
def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")

def pause(msg: str = "Press Enter to continue..."):
	try:
		input(msg)
	except EOFError:
		pass

# ---- Storage ----
def get_storage() -> JSONStorage:
	base_dir = os.path.join(os.path.dirname(__file__), "data")
	return JSONStorage(base_dir)


# ---- GPA Calculator UI ----
def run_gpa_calculator():
	storage = get_storage()
	calc = GPACalculator(storage)
	while True:
		clear_screen()
		print("=== GPA Calculator ===")
		print("Courses:")
		for idx, c in enumerate(calc.courses):
			print(f" {idx+1}. {c.name} - {c.credits} credits - {c.grade}")
		print("\nMenu:")
		print(" 1) Add Course")
		print(" 2) Remove Course")
		print(" 3) Calculate GPA")
		print(" 4) Clear Courses")
		print(" 5) Back to Home")
		choice = input("Select: ").strip()
		if choice == "1":
			try:
				name = input("Course name: ").strip()
				credits = float(input("Credits (e.g., 3): ").strip())
				print("Valid grades:", ", ".join(GRADE_POINTS.keys()))
				grade = input("Grade (e.g., A-, B+): ").strip().upper()
				calc.add_course(name, credits, grade)
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "2":
			try:
				idx = int(input("Index to remove: ").strip()) - 1
				if 0 <= idx < len(calc.courses):
					course = calc.courses[idx]
					print(f"\nCourse to remove: {course.name} ({course.credits} credits, Grade: {course.grade})")
					confirm = input("Are you sure you want to remove this course? (y/N): ").strip().lower()
					if confirm == 'y':
						calc.remove_course(idx)
						print("Course removed successfully.")
					else:
						print("Removal cancelled.")
				else:
					print("Invalid course index.")
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "3":
			res = calc.calculate()
			print(f"\nGPA: {res['gpa']}  |  Total Credits: {res['total_credits']}  |  Weighted Points: {res['weighted_points']}")
			try:
				save = input("Save GPA to history? (y/N): ").strip().lower() == "y"
				if save:
					calc.save_result(res["gpa"])
			except Exception:
				pass
			pause()
		elif choice == "4":
			if len(calc.courses) > 0:
				print(f"\nThis will remove ALL {len(calc.courses)} course(s) from your GPA calculation.")
				confirm = input("Are you sure you want to clear all courses? (y/N): ").strip().lower()
				if confirm == 'y':
					calc.clear_courses()
					print("All courses cleared successfully.")
				else:
					print("Clear all cancelled.")
			else:
				print("No courses to clear.")
			pause()
		elif choice == "5":
			break
		else:
			print("Invalid option.")
			pause()


# ---- Homework Planner UI ----
def run_homework_planner():
	storage = get_storage()
	planner = HomeworkPlanner(storage)
	while True:
		clear_screen()
		print("=== Homework Planner ===")
		if not planner.items:
			print("(No items)")
		else:
			for i, item in enumerate(planner.items):
				print(f" {i+1}. [{item.status}] {item.subject} - {item.title} (Due: {item.due or '-'} )")
		print("\nMenu:")
		print(" 1) Add Item")
		print(" 2) Update Item")
		print(" 3) Remove Item")
		print(" 4) Mark Completed")
		print(" 5) Back to Home")
		choice = input("Select: ").strip()
		if choice == "1":
			try:
				subject = input("Subject: ").strip()
				title = input("Title: ").strip()
				due = input("Due (YYYY-MM-DD or empty): ").strip()
				details = input("Details (optional): ").strip()
				planner.add(subject, title, due, details)
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "2":
			try:
				idx = int(input("Index to update: ").strip()) - 1
				field = input("Field (subject/title/due/status/details): ").strip()
				value = input("New value: ").strip()
				planner.update(idx, **{field: value})
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "3":
			try:
				idx = int(input("Index to remove: ").strip()) - 1
				planner.remove(idx)
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "4":
			try:
				idx = int(input("Index to mark complete: ").strip()) - 1
				planner.mark_complete(idx)
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "5":
			break
		else:
			print("Invalid option.")
			pause()


# ---- Pomodoro UI ----
def run_pomodoro_timer():
	storage = get_storage()
	engine = PomodoroEngine(storage)
	while True:
		clear_screen()
		print("=== Pomodoro Timer ===")
		print(f"Mode: {engine.state.mode} | Seconds Left: {engine.state.seconds_left} | Sessions: {engine.state.completed_sessions}")
		print("\nMenu:")
		print(" 1) Start/Resume Work")
		print(" 2) Tick 10 seconds (fast-forward)")
		print(" 3) Reset")
		print(" 4) Live run (1 minute demo)")
		print(" 5) Back to Home")
		choice = input("Select: ").strip()
		if choice == "1":
			engine.start()
		elif choice == "2":
			for _ in range(10):
				engine.tick()
		elif choice == "3":
			engine.reset()
		elif choice == "4":
			# Run ticking loop for up to 60 seconds for demo
			print("Running... Ctrl+C to stop early.")
			try:
				for _ in range(60):
					engine.tick()
					time.sleep(1)
					print(f"Mode: {engine.state.mode} | Left: {engine.state.seconds_left}", end="\r")
			except KeyboardInterrupt:
				pass
			print()
			pause()
		elif choice == "5":
			break
		else:
			print("Invalid option.")
			pause()


# ---- Flashcards UI ----
def run_flashcards_quizzer():
	storage = get_storage()
	fc = Flashcards(storage)
	while True:
		clear_screen()
		print("=== Flashcard Quizzer ===")
		print("Decks:")
		for name, cards in fc.decks.items():
			print(f" - {name} ({len(cards)} cards)")
		print("\nMenu:")
		print(" 1) Create Deck")
		print(" 2) Delete Deck")
		print(" 3) Add Card to Deck")
		print(" 4) List Cards in Deck")
		print(" 5) Quiz (Multiple Choice)")
		print(" 6) Launch GUI (Tkinter)")
		print(" 7) Back to Home")
		choice = input("Select: ").strip()
		if choice == "1":
			try:
				name = input("New deck name: ").strip()
				fc.create_deck(name)
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "2":
			name = input("Deck to delete: ").strip()
			fc.delete_deck(name)
		elif choice == "3":
			try:
				deck = input("Deck: ").strip()
				q = input("Question: ").strip()
				a = input("Answer: ").strip()
				fc.add_card(deck, q, a)
			except Exception as e:
				print(f"Error: {e}")
			pause()
		elif choice == "4":
			deck = input("Deck: ").strip()
			cards = fc.list_cards(deck)
			for i, c in enumerate(cards):
				print(f" {i+1}. Q: {c.q} | A: {c.a}")
			pause()
		elif choice == "5":
			deck = input("Deck: ").strip()
			cards = fc.start_quiz(deck)
			if not cards:
				print("No cards in deck.")
				pause()
				continue
			score = 0
			for c in cards:
				options = fc.multiple_choice_options(deck, c.a)
				print(f"\nQ: {c.q}")
				for i, opt in enumerate(options):
					print(f"  {i+1}) {opt}")
				try:
					ans = int(input("Your answer (1-4): ").strip()) - 1
					if 0 <= ans < len(options) and options[ans] == c.a:
						score += 1
				except Exception:
					pass
			print(f"\nScore: {score}/{len(cards)}")
			pause()
		elif choice == "6":
			try:
				from F_app import FlashcardApp
				FlashcardApp()
			except Exception as e:
				print(f"Failed to launch GUI: {e}")
			pause()
		elif choice == "7":
			break
		else:
			print("Invalid option.")
			pause()


# ---- Homepage / Welcome ----
def welcome_message():
	print("=" * 45)
	print("  🎓 Welcome to TARUMT Student Toolkit 🎓")
	print("=" * 45)
	print("This toolkit includes:")
	print(" - GPA Calculator")
	print(" - Homework Planner")
	print(" - Pomodoro Timer")
	print(" - Flashcard Quizzer")
	print("\nSelect a tool from the homepage menu below.\n")


def main_menu():
	while True:
		welcome_message()
		print("=================== HOMEPAGE ===================")
		print("1. GPA Calculator")
		print("2. Homework Planner")
		print("3. Pomodoro Timer")
		print("4. Flashcard Quizzer")
		print("5. Exit")
		choice = input("Select an option (1-5): ").strip()
		if choice == "1":
			run_gpa_calculator()
		elif choice == "2":
			run_homework_planner()
		elif choice == "3":
			run_pomodoro_timer()
		elif choice == "4":
			run_flashcards_quizzer()
		elif choice == "5":
			print("Goodbye. Wish you have a nice day 😀")
			break
		else:
			print("❌ Invalid selection. Please choose 1-5.")
			pause()
			clear_screen()


if __name__ == "__main__":
	# Try GUI home first, then fallback to CLI
	try:
		from main_gui import launch_main_gui
		launch_main_gui()
	except Exception:
		try:
			main_menu()
		except KeyboardInterrupt:
			print("\nExiting...")
			sys.exit(0)

