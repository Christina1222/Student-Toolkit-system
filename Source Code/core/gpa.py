from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import json
import os


GRADE_POINTS = {
	"A": 4.00,
	"A-": 3.67,
	"B+": 3.33,
	"B": 3.00,
	"B-": 2.67,
	"C+": 2.33,
	"C": 2.00,
	"C-": 1.67,
	"D": 1.00,
	"F": 0.00,
}


# Base class for academic records
class AcademicRecord:
	"""Base class for academic records with common functionality"""
	
	def __init__(self, name: str):
		self._name = name  # Private attribute for encapsulation
	
	@property
	def name(self) -> str:
		"""Get the name of the academic record"""
		return self._name
	
	@name.setter
	def name(self, value: str):
		"""Set the name with validation"""
		if not isinstance(value, str) or not value.strip():
			raise ValueError("Name must be a non-empty string")
		self._name = value.strip()
	
	def to_dict(self) -> Dict:
		"""Convert to dictionary format"""
		return {"name": self._name}
	
	def __str__(self) -> str:
		return f"{self.__class__.__name__}: {self._name}"


class Course(AcademicRecord):
	"""Course class with inheritance from AcademicRecord"""
	
	def __init__(self, name: str, credits: float, grade: str):
		"""Initialize course with validation"""
		super().__init__(name)
		self.credits = credits
		self.grade = grade
		self._validate_course_data()
	
	def _validate_course_data(self):
		"""Private method for data validation - encapsulation"""
		ALLOWED_CREDIT_HOURS = {2.0, 3.0, 4.0}
		if not isinstance(self.credits, (int, float)):
			raise ValueError("Credits must be a number")
		if float(self.credits) not in ALLOWED_CREDIT_HOURS:
			raise ValueError("Credits must be one of: 2.0, 3.0, 4.0")
		if self.grade not in GRADE_POINTS:
			raise ValueError(f"Invalid grade. Valid grades: {list(GRADE_POINTS.keys())}")
	
	def to_dict(self) -> Dict:
		"""Override parent method to include course-specific data"""
		base_dict = super().to_dict()
		base_dict.update({
			"credits": self.credits,
			"grade": self.grade
		})
		return base_dict
	
	def get_grade_points(self) -> float:
		"""Get the grade points for this course"""
		return GRADE_POINTS.get(self.grade, 0.0)
	
	def get_weighted_points(self) -> float:
		"""Calculate weighted points for this course"""
		return self.credits * self.get_grade_points()


class GPACalculator:
	"""Enhanced GPA Calculator with inheritance, encapsulation, and comprehensive exception handling"""
	
	def __init__(self, storage, history_name: str = "gpa_history.json"):
		"""Initialize GPA Calculator with proper validation"""
		try:
			if not storage:
				raise ValueError("Storage object is required")
			if not isinstance(history_name, str) or not history_name.strip():
				raise ValueError("History name must be a non-empty string")
			
			self._storage = storage  # Private attribute for encapsulation
			self._history_name = history_name.strip()  # Private attribute
			self._courses: List[Course] = []  # Private attribute
			self._history: List[Dict] = self._load_history()  # Private attribute
		except Exception as e:
			raise RuntimeError(f"Failed to initialize GPA Calculator: {e}")
	
	def _load_history(self) -> List[Dict]:
		"""Private method to load history with error handling"""
		try:
			return self._storage.load(self._history_name, default=[])
		except Exception as e:
			raise RuntimeError(f"Failed to load GPA history: {e}")
	
	def _save_history(self):
		"""Private method to save history with error handling"""
		try:
			self._storage.save(self._history_name, self._history)
		except Exception as e:
			raise RuntimeError(f"Failed to save GPA history: {e}")
	
	@property
	def courses(self) -> Tuple[Course, ...]:
		"""Get courses as immutable tuple for encapsulation"""
		return tuple(self._courses)

	def clear_courses(self) -> None:
		"""Clear all courses from the current calculation"""
		try:
			self._courses.clear()
		except Exception as e:
			raise RuntimeError(f"Failed to clear courses: {e}")
	
	@property
	def history(self) -> Tuple[Dict, ...]:
		"""Get history as immutable tuple for encapsulation"""
		return tuple(self._history)
	
	def add_course(self, name: str, credits: float, grade: str) -> Course:
		"""Add a course with comprehensive validation"""
		try:
			# Input validation
			if not isinstance(name, str) or not name.strip():
				raise ValueError("Course name must be a non-empty string")
			if not isinstance(credits, (int, float)):
				raise ValueError("Credits must be a number")
			if not isinstance(grade, str) or not grade.strip():
				raise ValueError("Grade must be a non-empty string")
			
			credits_float = float(credits)
			grade_upper = grade.strip().upper()
			ALLOWED_CREDIT_HOURS = {2.0, 3.0, 4.0}
			if credits_float not in ALLOWED_CREDIT_HOURS:
				raise ValueError("Credits must be one of: 2.0, 3.0, 4.0")
			if grade_upper not in GRADE_POINTS:
				raise ValueError(f"Invalid grade '{grade}'. Valid grades: {list(GRADE_POINTS.keys())}")
			
			# Create and add course
			course = Course(name=name.strip(), credits=credits_float, grade=grade_upper)
			self._courses.append(course)
			return course
			
		except ValueError:
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error adding course: {e}")

	def remove_course(self, index: int) -> Course:
		"""Remove a course by index with validation"""
		try:
			if not isinstance(index, int):
				raise TypeError("Index must be an integer")
			if index < 0 or index >= len(self._courses):
				raise IndexError(f"Course index {index} out of range (0-{len(self._courses)-1})")
			
			return self._courses.pop(index)
			
		except (TypeError, IndexError):
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error removing course: {e}")

	def update_course(self, index: int, name: str, credits: float, grade: str) -> Course:
		"""Update a course by index with validation"""
		try:
			if not isinstance(index, int):
				raise TypeError("Index must be an integer")
			if index < 0 or index >= len(self._courses):
				raise IndexError(f"Course index {index} out of range (0-{len(self._courses)-1})")
			
			# Input validation
			if not isinstance(name, str) or not name.strip():
				raise ValueError("Course name must be a non-empty string")
			if not isinstance(credits, (int, float)):
				raise ValueError("Credits must be a number")
			if not isinstance(grade, str) or not grade.strip():
				raise ValueError("Grade must be a non-empty string")
			
			credits_float = float(credits)
			grade_upper = grade.strip().upper()
			ALLOWED_CREDIT_HOURS = {2.0, 3.0, 4.0}
			if credits_float not in ALLOWED_CREDIT_HOURS:
				raise ValueError("Credits must be one of: 2.0, 3.0, 4.0")
			if grade_upper not in GRADE_POINTS:
				raise ValueError(f"Invalid grade '{grade}'. Valid grades: {list(GRADE_POINTS.keys())}")
			
			# Update the course in place
			course = self._courses[index]
			course.name = name.strip()
			course.credits = credits_float
			course.grade = grade_upper
			course._validate_course_data()  # Re-validate
			
			return course
			
		except (TypeError, IndexError, ValueError):
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error updating course: {e}")

	def calculate(self) -> Dict[str, float]:
		"""Calculate GPA with comprehensive error handling"""
		try:
			if not self._courses:
				return {"gpa": 0.0, "total_credits": 0.0, "weighted_points": 0.0}
			
			total_credits = sum(course.credits for course in self._courses)
			weighted_points = sum(course.get_weighted_points() for course in self._courses)
			
			if total_credits <= 0:
				raise ValueError("Total credits must be greater than 0")
			
			gpa = weighted_points / total_credits
			
			return {
				"gpa": round(gpa, 2),
				"total_credits": round(total_credits, 2),
				"weighted_points": round(weighted_points, 2),
			}
		except Exception as e:
			raise RuntimeError(f"Error calculating GPA: {e}")

	def save_result(self, gpa_value: float) -> bool:
		"""Save GPA result to history with validation"""
		try:
			if not isinstance(gpa_value, (int, float)):
				raise TypeError("GPA value must be a number")
			if gpa_value < 0 or gpa_value > 4.0:
				raise ValueError("GPA value must be between 0.0 and 4.0")
			
			entry = {"gpa": float(round(gpa_value, 2))}
			self._history.append(entry)
			self._save_history()
			return True
		except (TypeError, ValueError):
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Failed to save GPA result: {e}")

	def clear_history(self) -> bool:
		"""Clear GPA history with error handling"""
		try:
			self._history.clear()
			self._save_history()
			return True
		except Exception as e:
			raise RuntimeError(f"Failed to clear GPA history: {e}")
	
	def get_course_count(self) -> int:
		"""Get the total number of courses"""
		try:
			return len(self._courses)
		except Exception as e:
			raise RuntimeError(f"Error getting course count: {e}")
	
	def get_grade_distribution(self) -> Dict[str, int]:
		"""Get the distribution of grades with error handling"""
		try:
			distribution = {}
			for course in self._courses:
				distribution[course.grade] = distribution.get(course.grade, 0) + 1
			return distribution
		except Exception as e:
			raise RuntimeError(f"Error getting grade distribution: {e}")
	
	def get_credit_distribution_by_grade(self) -> Dict[str, float]:
		"""Get the distribution of credits by grade with error handling"""
		try:
			distribution = {}
			for course in self._courses:
				if course.grade not in distribution:
					distribution[course.grade] = 0.0
				distribution[course.grade] += course.credits
			return distribution
		except Exception as e:
			raise RuntimeError(f"Error getting credit distribution: {e}")
	
	def get_gpa_trend(self) -> Tuple[float, ...]:
		"""Get historical GPA values as immutable tuple"""
		try:
			return tuple(entry.get("gpa", 0.0) for entry in self._history)
		except Exception as e:
			raise RuntimeError(f"Error getting GPA trend: {e}")
	
	def get_average_gpa(self) -> float:
		"""Get the average GPA from history with error handling"""
		try:
			gpa_trend = self.get_gpa_trend()
			if not gpa_trend:
				return 0.0
			return round(sum(gpa_trend) / len(gpa_trend), 2)
		except Exception as e:
			raise RuntimeError(f"Error calculating average GPA: {e}")
	
	def get_highest_gpa(self) -> float:
		"""Get the highest GPA from history with error handling"""
		try:
			gpa_trend = self.get_gpa_trend()
			if not gpa_trend:
				return 0.0
			return max(gpa_trend)
		except Exception as e:
			raise RuntimeError(f"Error getting highest GPA: {e}")
	
	def get_lowest_gpa(self) -> float:
		"""Get the lowest GPA from history with error handling"""
		try:
			gpa_trend = self.get_gpa_trend()
			if not gpa_trend:
				return 0.0
			return min(gpa_trend)
		except Exception as e:
			raise RuntimeError(f"Error getting lowest GPA: {e}")
	
	def get_course_summary(self) -> Tuple[Dict[str, any], ...]:
		"""Get course summary as tuple of dictionaries"""
		try:
			return tuple(course.to_dict() for course in self._courses)
		except Exception as e:
			raise RuntimeError(f"Error getting course summary: {e}")



