import json
import os
from typing import Any


class JSONStorage:
	"""Tiny JSON-backed storage helper.

	- Uses a base directory
	- Provides load/save with defaults
	"""

	def __init__(self, base_dir: str):
		self.base_dir = base_dir
		os.makedirs(self.base_dir, exist_ok=True)

	def _path(self, name: str) -> str:
		return os.path.join(self.base_dir, name)

	def load(self, name: str, default: Any):
		path = self._path(name)
		if not os.path.exists(path):
			return default
		try:
			with open(path, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception:
			return default

	def save(self, name: str, data: Any) -> None:
		path = self._path(name)
		with open(path, "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=2)


