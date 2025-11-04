from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal, Callable, Optional, Tuple, Dict
import json
import os


Mode = Literal["Work", "Short Break", "Long Break", "Idle"]


# Base class for timer configurations
class TimerConfig:
	"""Base class for timer configurations with common functionality"""
	
	def __init__(self, name: str):
		self._name = name  # Private attribute for encapsulation
	
	@property
	def name(self) -> str:
		"""Get the configuration name"""
		return self._name
	
	@name.setter
	def name(self, value: str):
		"""Set the configuration name with validation"""
		if not isinstance(value, str) or not value.strip():
			raise ValueError("Configuration name must be a non-empty string")
		self._name = value.strip()
	
	def to_dict(self) -> Dict:
		"""Convert to dictionary format"""
		return {"name": self._name}
	
	def __str__(self) -> str:
		return f"{self.__class__.__name__}: {self._name}"


class PomodoroSettings(TimerConfig):
	"""Pomodoro settings with inheritance from TimerConfig"""
	
	def __init__(self, work_minutes: int = 25, short_break: int = 5, long_break: int = 15, cycles_before_long: int = 4):
		"""Initialize pomodoro settings with validation"""
		super().__init__("Pomodoro Settings")
		self.work_minutes = work_minutes
		self.short_break = short_break
		self.long_break = long_break
		self.cycles_before_long = cycles_before_long
		self._validate_settings()
	
	def _validate_settings(self):
		"""Private method for settings validation - encapsulation"""
		if not isinstance(self.work_minutes, int) or self.work_minutes <= 0:
			raise ValueError("Work minutes must be a positive integer")
		if not isinstance(self.short_break, int) or self.short_break <= 0:
			raise ValueError("Short break must be a positive integer")
		if not isinstance(self.long_break, int) or self.long_break <= 0:
			raise ValueError("Long break must be a positive integer")
		if not isinstance(self.cycles_before_long, int) or self.cycles_before_long <= 0:
			raise ValueError("Cycles before long break must be a positive integer")
		if self.long_break <= self.short_break:
			raise ValueError("Long break must be longer than short break")
	
	def to_dict(self) -> Dict:
		"""Override parent method to include settings data"""
		base_dict = super().to_dict()
		base_dict.update({
			"work_minutes": self.work_minutes,
			"short_break": self.short_break,
			"long_break": self.long_break,
			"cycles_before_long": self.cycles_before_long
		})
		return base_dict
	
	def get_work_seconds(self) -> int:
		"""Get work time in seconds"""
		return self.work_minutes * 60
	
	def get_short_break_seconds(self) -> int:
		"""Get short break time in seconds"""
		return self.short_break * 60
	
	def get_long_break_seconds(self) -> int:
		"""Get long break time in seconds"""
		return self.long_break * 60


@dataclass
class PomodoroState:
	"""Pomodoro state with enhanced validation"""
	mode: Mode = "Idle"
	seconds_left: int = 0
	cycles_completed: int = 0
	completed_sessions: int = 0
	
	def __post_init__(self):
		"""Validate state data"""
		self._validate_state()
	
	def _validate_state(self):
		"""Private method for state validation - encapsulation"""
		if self.mode not in ["Work", "Short Break", "Long Break", "Idle"]:
			raise ValueError(f"Invalid mode. Valid modes: {['Work', 'Short Break', 'Long Break', 'Idle']}")
		if not isinstance(self.seconds_left, int) or self.seconds_left < 0:
			raise ValueError("Seconds left must be a non-negative integer")
		if not isinstance(self.cycles_completed, int) or self.cycles_completed < 0:
			raise ValueError("Cycles completed must be a non-negative integer")
		if not isinstance(self.completed_sessions, int) or self.completed_sessions < 0:
			raise ValueError("Completed sessions must be a non-negative integer")
	
	def is_active(self) -> bool:
		"""Check if timer is currently active"""
		return self.mode != "Idle" and self.seconds_left > 0
	
	def get_time_remaining(self) -> Tuple[int, int]:
		"""Get time remaining as (minutes, seconds) tuple"""
		minutes = self.seconds_left // 60
		seconds = self.seconds_left % 60
		return (minutes, seconds)


class PomodoroEngine:
	"""Enhanced tick-driven Pomodoro logic engine with inheritance, encapsulation, and comprehensive exception handling.

	External orchestrator calls tick() every second and can persist state.
	"""

	def __init__(self, storage, storage_name: str = "pomodoro.json"):
		"""Initialize Pomodoro Engine with proper validation"""
		try:
			if not storage:
				raise ValueError("Storage object is required")
			if not isinstance(storage_name, str) or not storage_name.strip():
				raise ValueError("Storage name must be a non-empty string")
			
			self._storage = storage  # Private attribute for encapsulation
			self._storage_name = storage_name.strip()  # Private attribute
			
			# Load data with error handling
			data = self._load_pomodoro_data()
			
			# Initialize settings and state with validation
			self._settings = self._create_settings(data.get("settings", {}))
			self._state = self._create_state(data.get("state", {}))
			
		except Exception as e:
			raise RuntimeError(f"Failed to initialize Pomodoro Engine: {e}")
	
	def _load_pomodoro_data(self) -> Dict:
		"""Private method to load pomodoro data with error handling"""
		try:
			return self._storage.load(self._storage_name, default={})
		except Exception as e:
			raise RuntimeError(f"Failed to load pomodoro data: {e}")
	
	def _create_settings(self, settings_data: Dict) -> PomodoroSettings:
		"""Private method to create settings with validation"""
		try:
			# Create default settings and convert to dict manually
			default_settings = PomodoroSettings()
			default_dict = {
				'work_minutes': default_settings.work_minutes,
				'short_break': default_settings.short_break,
				'long_break': default_settings.long_break,
				'cycles_before_long': default_settings.cycles_before_long
			}
			merged_settings = {**default_dict, **settings_data}
			return PomodoroSettings(**merged_settings)
		except Exception as e:
			raise RuntimeError(f"Failed to create pomodoro settings: {e}")
	
	def _create_state(self, state_data: Dict) -> PomodoroState:
		"""Private method to create state with validation"""
		try:
			default_state = asdict(PomodoroState())
			merged_state = {**default_state, **state_data}
			return PomodoroState(**merged_state)
		except Exception as e:
			raise RuntimeError(f"Failed to create pomodoro state: {e}")
	
	def _save_pomodoro_data(self):
		"""Private method to save pomodoro data with error handling"""
		try:
			# Convert settings to dict manually since it's not a dataclass
			settings_dict = {
				'work_minutes': self._settings.work_minutes,
				'short_break': self._settings.short_break,
				'long_break': self._settings.long_break,
				'cycles_before_long': self._settings.cycles_before_long
			}
			data = {
				"settings": settings_dict,
				"state": asdict(self._state)
			}
			self._storage.save(self._storage_name, data)
		except Exception as e:
			raise RuntimeError(f"Failed to save pomodoro data: {e}")
	
	@property
	def settings(self) -> PomodoroSettings:
		"""Get pomodoro settings"""
		return self._settings
	
	@property
	def state(self) -> PomodoroState:
		"""Get pomodoro state"""
		return self._state
	
	def save(self) -> bool:
		"""Save current state and settings"""
		try:
			self._save_pomodoro_data()
			return True
		except Exception as e:
			raise RuntimeError(f"Failed to save pomodoro data: {e}")

	def start(self) -> bool:
		"""Start the pomodoro timer with validation"""
		try:
			if self._state.mode in ("Idle", "Short Break", "Long Break") or self._state.seconds_left <= 0:
				self._state.mode = "Work"
				self._state.seconds_left = self._settings.get_work_seconds()
			self._save_pomodoro_data()
			return True
		except Exception as e:
			raise RuntimeError(f"Failed to start pomodoro timer: {e}")

	def pause(self) -> bool:
		"""Pause the pomodoro timer (no-op for core logic)"""
		try:
			# No-op for core logic; pausing managed by caller (stop calling tick)
			return True
		except Exception as e:
			raise RuntimeError(f"Failed to pause pomodoro timer: {e}")

	def reset(self) -> bool:
		"""Reset the pomodoro timer to initial state"""
		try:
			self._state = PomodoroState()
			self._save_pomodoro_data()
			return True
		except Exception as e:
			raise RuntimeError(f"Failed to reset pomodoro timer: {e}")

	def _transition(self):
		"""Private method to handle state transitions with validation"""
		try:
			if self._state.mode == "Work":
				self._state.completed_sessions += 1
				self._state.cycles_completed = (self._state.cycles_completed + 1) % self._settings.cycles_before_long
				if self._state.cycles_completed == 0:
					self._state.mode = "Long Break"
					self._state.seconds_left = self._settings.get_long_break_seconds()
				else:
					self._state.mode = "Short Break"
					self._state.seconds_left = self._settings.get_short_break_seconds()
			elif self._state.mode in ("Short Break", "Long Break", "Idle"):
				self._state.mode = "Work"
				self._state.seconds_left = self._settings.get_work_seconds()
		except Exception as e:
			raise RuntimeError(f"Failed to transition pomodoro state: {e}")

	def tick(self) -> bool:
		"""Process one second tick with comprehensive error handling"""
		try:
			if self._state.seconds_left <= 0:
				self._transition()
			self._state.seconds_left -= 1
			if self._state.seconds_left < 0:
				self._state.seconds_left = 0
			self._save_pomodoro_data()
			return True
		except Exception as e:
			raise RuntimeError(f"Failed to process pomodoro tick: {e}")
	
	def get_session_info(self) -> Tuple[str, int, int, int]:
		"""Get current session information as tuple"""
		try:
			minutes, seconds = self._state.get_time_remaining()
			return (self._state.mode, minutes, seconds, self._state.completed_sessions)
		except Exception as e:
			raise RuntimeError(f"Failed to get session info: {e}")
	
	def get_settings_summary(self) -> Tuple[int, int, int, int]:
		"""Get settings summary as tuple"""
		try:
			return (
				self._settings.work_minutes,
				self._settings.short_break,
				self._settings.long_break,
				self._settings.cycles_before_long
			)
		except Exception as e:
			raise RuntimeError(f"Failed to get settings summary: {e}")
	
	def is_timer_active(self) -> bool:
		"""Check if timer is currently active"""
		try:
			return self._state.is_active()
		except Exception as e:
			raise RuntimeError(f"Failed to check timer status: {e}")



