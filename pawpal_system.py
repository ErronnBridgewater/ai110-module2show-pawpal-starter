from __future__ import annotations
"""Core data models and scheduling interfaces for PawPal+.

This module defines the domain classes used by the app:
- Owner: manages one or more pets.
- Pet: stores pet profile data and care requirements.
- Task: represents a single care activity.
- Scheduler: coordinates and optimizes task selection.
"""

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timedelta


@dataclass
class Owner:
	"""Represents a pet owner and high-level scheduling constraints."""

	name: str
	available_hours: list[Any] = field(default_factory=list)
	energy_level: int = 0
	owned_pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet_details: Pet) -> None:
		"""Attach a Pet to this owner and establish the relationship."""
		pass

	def update_availability(self, times: Any) -> None:
		"""Update the owner's available time blocks used by scheduling logic."""
		pass

	def get_preferences(self) -> str:
		"""Return a human-readable summary of owner preferences."""
		pass


@dataclass
class Pet:
	"""Represents a pet profile, including health and care requirements."""

	name: str
	species: str
	age: int
	health_status: str
	owner: Owner | None = None
	requirements: dict[str, Any] = field(default_factory=dict)

	def get_needs(self) -> dict[str, Any]:
		"""Return normalized care needs that can be consumed by a scheduler."""
		pass

	def update_health_record(self, note: str) -> None:
		"""Record a new health-related note for the pet."""
		pass


@dataclass
class Task:
	"""A single pet-care activity with time and completion metadata."""

	task_id: str
	category: str
	priority: int
	estimated_duration: int
	pet: Pet | None = None
	owner: Owner | None = None
	is_completed: bool = False
	completed_date: datetime | None = None
	skip_count: int = 0
	scheduled_start: datetime | None = None
	scheduled_end: datetime | None = None
	dependency: Task | None = None

	def mark_complete(self) -> Task | None:
		"""Mark the task complete and optionally generate its next recurrence.

		Returns:
			A new Task instance when this task is recurring (daily/weekly),
			otherwise None.
		"""
		if self.is_completed:
			return None

		self.is_completed = True
		self.completed_date = datetime.now()

		return self._build_next_occurrence()

	def _build_next_occurrence(self) -> Task | None:
		"""Create the next recurring task instance for daily/weekly categories."""
		recurrence_days = {"daily": 1, "weekly": 7}
		days = recurrence_days.get(self.category.lower())
		if days is None:
			return None

		delta = timedelta(days=days)
		next_start = self.scheduled_start + delta if self.scheduled_start else None
		next_end = self.scheduled_end + delta if self.scheduled_end else None

		return Task(
			task_id=f"{self.task_id}-next",
			category=self.category,
			priority=self.priority,
			estimated_duration=self.estimated_duration,
			pet=self.pet,
			owner=self.owner,
			skip_count=0,
			scheduled_start=next_start,
			scheduled_end=next_end,
			dependency=self.dependency,
		)

	def get_priority_score(self) -> int:
		"""Calculate a scheduling score based on urgency and history."""
		pass


@dataclass
class ScheduleResult:
	"""Container for scheduler outputs, conflicts, and status messaging."""

	success: bool
	scheduled_tasks: list[Task] = field(default_factory=list)
	conflicts: list[str] = field(default_factory=list)
	message: str = ""


@dataclass
class Scheduler:
	"""Scheduling engine that organizes tasks across an owner's pets."""

	owner: Owner
	daily_queue: list[Task] = field(default_factory=list)
	total_time_budget: int = 0
	generated_plan: dict[str, Any] = field(default_factory=dict)

	def complete_task(self, task: Task) -> Task | None:
		"""Complete a task and enqueue the next occurrence when recurring."""
		next_task = task.mark_complete()
		if next_task is not None:
			self.daily_queue.append(next_task)
		return next_task

	def optimize_schedule(self, pet_list: list[Pet]) -> ScheduleResult:
		"""Build an optimized daily task plan given pet inputs and constraints."""
		pass

	def explain_logic(self) -> str:
		"""Explain the rules or heuristics used to generate the current plan."""
		pass

	def export_to_streamlit(self) -> dict[str, Any]:
		"""Return the generated plan in a UI-friendly dictionary structure."""
		pass

	def detect_time_conflicts(self) -> list[str]:
		"""Detect overlapping task windows in the current daily queue.

		The algorithm builds effective time windows for schedulable tasks,
		then compares each pair of windows to find interval overlaps.

		Returns:
			A list of human-readable conflict messages. Each message identifies
			the two task IDs involved and labels the overlap as either
			"same pet" or "different pets".
		"""
		conflicts: list[str] = []
		tasks_with_windows = []

		for task in self.daily_queue:
			window = self._get_task_window(task)
			if window is not None:
				tasks_with_windows.append((task, window[0], window[1]))

		for i, (left_task, left_start, left_end) in enumerate(tasks_with_windows):
			for right_task, right_start, right_end in tasks_with_windows[i + 1:]:
				if left_start < right_end and right_start < left_end:
					left_pet = left_task.pet.name if left_task.pet else "Unknown"
					right_pet = right_task.pet.name if right_task.pet else "Unknown"
					relation = "same pet" if left_pet == right_pet else "different pets"
					conflicts.append(
						f"Time conflict ({relation}): "
						f"{left_task.task_id} ({left_pet}) overlaps with "
						f"{right_task.task_id} ({right_pet})"
					)

		return conflicts

	def detect_time_conflicts_lightweight(self) -> list[str]:
		"""Run conflict detection defensively for UI-safe behavior.

		This wrapper calls detect_time_conflicts() and suppresses unexpected
		exceptions so app flows can continue without crashing.

		Returns:
			The same conflict message list returned by detect_time_conflicts()
			when successful. If an exception occurs, returns a single warning
			message instructing the user to verify task times.
		"""
		try:
			return self.detect_time_conflicts()
		except Exception:
			return [
				"Warning: Conflict detection could not be completed. "
				"Please verify scheduled task times."
			]

	def _get_task_window(self, task: Task) -> tuple[datetime, datetime] | None:
		"""Build a normalized half-open time window for one task.

		Args:
			task: The task to normalize into a [start, end) interval.

		Returns:
			A tuple of (start, end) datetimes when the task has a valid window.
			If scheduled_start is missing or end is not after start, returns None.
			When scheduled_end is missing, end is inferred from estimated_duration.
		"""
		if task.scheduled_start is None:
			return None

		end_time = task.scheduled_end
		if end_time is None:
			end_time = task.scheduled_start + timedelta(minutes=task.estimated_duration)

		if end_time <= task.scheduled_start:
			return None

		return task.scheduled_start, end_time

	def filter_tasks(
		self,
		is_completed: bool | None = None,
		pet_name: str | None = None,
	) -> list[Task]:
		"""Return tasks from the daily queue matching the given filters.

		Args:
			is_completed: If provided, keep only tasks whose completion status
				matches this value.
			pet_name: If provided, keep only tasks assigned to the pet with
				this name (case-insensitive).

		Returns:
			A list of Task objects that satisfy all supplied filters.
		"""
		results = self.daily_queue

		if is_completed is not None:
			results = [t for t in results if t.is_completed == is_completed]

		if pet_name is not None:
			results = [
				t for t in results
				if t.pet is not None and t.pet.name.lower() == pet_name.lower()
			]

		return results

	def sort_by_time(self) -> list[Task]:
		"""Return tasks from the daily queue sorted by scheduled_start.

		Tasks with no scheduled_start are placed at the end.
		"""
		return sorted(
			self.daily_queue,
			key=lambda t: (t.scheduled_start is None, t.scheduled_start),
		)


