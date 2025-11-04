from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Literal, Tuple
import json
import os


Status = Literal["Pending", "In Progress", "Completed"]
Priority = Literal["High", "Medium", "Low"]


# Base class for academic tasks
class AcademicTask:
	"""Base class for academic tasks with common functionality"""
	
	def __init__(self, title: str, subject: str):
		self._title = title  # Private attribute for encapsulation
		self._subject = subject  # Private attribute for encapsulation
	
	@property
	def title(self) -> str:
		"""Get the title of the task"""
		return self._title
	
	@title.setter
	def title(self, value: str):
		"""Set the title with validation"""
		if not isinstance(value, str) or not value.strip():
			raise ValueError("Title must be a non-empty string")
		self._title = value.strip()
	
	@property
	def subject(self) -> str:
		"""Get the subject of the task"""
		return self._subject
	
	@subject.setter
	def subject(self, value: str):
		"""Set the subject with validation"""
		if not isinstance(value, str) or not value.strip():
			raise ValueError("Subject must be a non-empty string")
		self._subject = value.strip()
	
	def to_dict(self) -> Dict:
		"""Convert to dictionary format"""
		return {"title": self._title, "subject": self._subject}
	
	def __str__(self) -> str:
		return f"{self.__class__.__name__}: {self._title} ({self._subject})"


class HomeworkItem(AcademicTask):
	"""Homework item class with inheritance from AcademicTask"""
	
	def __init__(self, subject: str, title: str, due: str = "", status: Status = "Pending", details: str = "", priority: Priority = "Medium"):
		"""Initialize homework item with validation"""
		super().__init__(title, subject)
		self.due = due
		self.status = status
		self.details = details
		self.priority = priority
		self._validate_homework_data()
	
	def _validate_homework_data(self):
		"""Private method for data validation - encapsulation"""
		if not self.title.strip():
			raise ValueError("Title is required")
		if self.title.strip().isdigit():
			raise ValueError("Title must contain text, not just numbers")
		if not self.subject.strip():
			raise ValueError("Subject is required")
		if not self.due.strip():
			raise ValueError("Due date is required")
		if self.status not in ["Pending", "In Progress", "Completed"]:
			raise ValueError(f"Invalid status. Valid statuses: {['Pending', 'In Progress', 'Completed']}")
		if self.priority not in ["High", "Medium", "Low"]:
			raise ValueError(f"Invalid priority. Valid priorities: {['High', 'Medium', 'Low']}")
		if not self._is_valid_date_format():
			raise ValueError("Due date must be in YYYY-MM-DD format")
	
	def _is_valid_date_format(self) -> bool:
		"""Private method to validate date format"""
		try:
			datetime.strptime(self.due, "%Y-%m-%d")
			return True
		except (ValueError, TypeError):
			return False
	
	def is_valid_date(self) -> bool:
		"""Public method to check if date is valid"""
		return self._is_valid_date_format()
	
	def is_overdue(self) -> bool:
		"""Check if the homework is overdue"""
		if not self.due or self.status == "Completed":
			return False
		try:
			due_date = datetime.strptime(self.due, "%Y-%m-%d").date()
			return due_date < datetime.now().date()
		except (ValueError, TypeError):
			return False
	
	def to_dict(self) -> Dict:
		"""Override parent method to include homework-specific data"""
		base_dict = super().to_dict()
		base_dict.update({
			"due": self.due,
			"status": self.status,
			"details": self.details,
			"priority": self.priority
		})
		return base_dict
	
	def get_priority_weight(self) -> int:
		"""Get priority as numeric weight for sorting"""
		priority_weights = {"High": 3, "Medium": 2, "Low": 1}
		return priority_weights.get(self.priority, 2)


class HomeworkPlanner:
	"""Enhanced Homework Planner with inheritance, encapsulation, and comprehensive exception handling"""
	
	def __init__(self, storage, storage_name: str = "homework.json"):
		"""Initialize Homework Planner with proper validation"""
		try:
			if not storage:
				raise ValueError("Storage object is required")
			if not isinstance(storage_name, str) or not storage_name.strip():
				raise ValueError("Storage name must be a non-empty string")
			
			self._storage = storage  # Private attribute for encapsulation
			self._storage_name = storage_name.strip()  # Private attribute
			self._items: List[HomeworkItem] = []  # Private attribute
			self._load_homework()  # Private method call
		except Exception as e:
			raise RuntimeError(f"Failed to initialize Homework Planner: {e}")
	
	def _load_homework(self):
		"""Private method to load homework with error handling"""
		try:
			data = self._storage.load(self._storage_name, default=[])
			if not isinstance(data, list):
				raise ValueError("Homework data must be a list")
			
			self._items = []
			for item_data in data:
				if isinstance(item_data, dict):
					try:
						item = HomeworkItem(**item_data)
						self._items.append(item)
					except Exception as e:
						# Skip invalid items but continue loading
						continue
		except Exception as e:
			raise RuntimeError(f"Failed to load homework data: {e}")
	
	def _save_homework(self):
		"""Private method to save homework with error handling"""
		try:
			data = [item.to_dict() for item in self._items]
			self._storage.save(self._storage_name, data)
		except Exception as e:
			raise RuntimeError(f"Failed to save homework data: {e}")
	
	@property
	def items(self) -> Tuple[HomeworkItem, ...]:
		"""Get homework items as immutable tuple for encapsulation"""
		return tuple(self._items)
	
	def add(self, subject: str, title: str, due: str = "", details: str = "", priority: str = "Medium") -> HomeworkItem:
		"""Add homework item with comprehensive validation"""
		try:
			# Input validation
			if not isinstance(subject, str) or not subject.strip():
				raise ValueError("Subject must be a non-empty string")
			if not isinstance(title, str) or not title.strip():
				raise ValueError("Title must be a non-empty string")
			if not isinstance(due, str):
				raise ValueError("Due date must be a string")
			if not isinstance(details, str):
				raise ValueError("Details must be a string")
			if not isinstance(priority, str) or not priority.strip():
				raise ValueError("Priority must be a non-empty string")
			
			# Create and validate homework item
			item = HomeworkItem(
				subject=subject.strip(),
				title=title.strip(),
				due=due.strip(),
				details=details.strip(),
				priority=priority.strip()
			)
			
			self._items.append(item)
			self._save_homework()
			return item
			
		except ValueError:
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error adding homework: {e}")

	def update(self, index: int, **fields) -> HomeworkItem:
		"""Update homework item with validation"""
		try:
			if not isinstance(index, int):
				raise TypeError("Index must be an integer")
			if index < 0 or index >= len(self._items):
				raise IndexError(f"Homework index {index} out of range (0-{len(self._items)-1})")
			
			item = self._items[index]
			
			# Update fields with validation
			for field, value in fields.items():
				if hasattr(item, field):
					setattr(item, field, value)
				else:
					raise ValueError(f"Invalid field: {field}")
			
			# Re-validate the item
			item._validate_homework_data()
			
			self._save_homework()
			return item
			
		except (TypeError, IndexError, ValueError):
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error updating homework: {e}")

	def remove(self, index: int) -> HomeworkItem:
		"""Remove homework item by index with validation"""
		try:
			if not isinstance(index, int):
				raise TypeError("Index must be an integer")
			if index < 0 or index >= len(self._items):
				raise IndexError(f"Homework index {index} out of range (0-{len(self._items)-1})")
			
			item = self._items.pop(index)
			self._save_homework()
			return item
			
		except (TypeError, IndexError):
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error removing homework: {e}")

	def mark_complete(self, index: int) -> HomeworkItem:
		"""Mark homework as complete with validation"""
		try:
			if not isinstance(index, int):
				raise TypeError("Index must be an integer")
			if index < 0 or index >= len(self._items):
				raise IndexError(f"Homework index {index} out of range (0-{len(self._items)-1})")
			
			self._items[index].status = "Completed"
			self._save_homework()
			return self._items[index]
			
		except (TypeError, IndexError):
			raise  # Re-raise validation errors
		except Exception as e:
			raise RuntimeError(f"Unexpected error marking homework complete: {e}")

	def filter_by_status(self, status: Status | None) -> Tuple[HomeworkItem, ...]:
		"""Filter homework by status, returning immutable tuple"""
		try:
			if status is None:
				return tuple(self._items)
			if status not in ["Pending", "In Progress", "Completed"]:
				raise ValueError(f"Invalid status. Valid statuses: {['Pending', 'In Progress', 'Completed']}")
			
			return tuple(item for item in self._items if item.status == status)
		except Exception as e:
			raise RuntimeError(f"Error filtering homework by status: {e}")
	
	def get_overdue_items(self) -> Tuple[HomeworkItem, ...]:
		"""Get overdue homework items as immutable tuple"""
		try:
			return tuple(item for item in self._items if item.is_overdue())
		except Exception as e:
			raise RuntimeError(f"Error getting overdue homework: {e}")
	
	def get_homework_summary(self) -> Tuple[Dict[str, any], ...]:
		"""Get homework summary as tuple of dictionaries"""
		try:
			return tuple(item.to_dict() for item in self._items)
		except Exception as e:
			raise RuntimeError(f"Error getting homework summary: {e}")
	
	def get_priority_distribution(self) -> Dict[str, int]:
		"""Get distribution of homework by priority"""
		try:
			distribution = {}
			for item in self._items:
				distribution[item.priority] = distribution.get(item.priority, 0) + 1
			return distribution
		except Exception as e:
			raise RuntimeError(f"Error getting priority distribution: {e}")



