from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from uuid import uuid4


@dataclass
class Owner:
	name: str
	available_hours: list[Any] = field(default_factory=list)
	energy_level: int = 0
	owned_pets: list[Pet] = field(default_factory=list)
	preferences: dict[str, Any] = field(default_factory=dict)

	def add_pet(self, pet_details: Pet) -> None:
		if pet_details not in self.owned_pets:
			self.owned_pets.append(pet_details)
		pet_details.owner = self
		for task in pet_details.tasks:
			task.owner = self

	def update_availability(self, times: Any) -> None:
		if isinstance(times, list):
			self.available_hours = times
			return

		raise TypeError("Availability must be provided as a list.")

	def get_preferences(self) -> str:
		if not self.preferences:
			return f"{self.name} has no saved preferences."

		items = ", ".join(f"{key}={value}" for key, value in sorted(self.preferences.items()))
		return f"{self.name} preferences: {items}"

	def get_all_tasks(self) -> list[Task]:
		all_tasks: list[Task] = []
		for pet in self.owned_pets:
			all_tasks.extend(pet.tasks)
		return all_tasks


@dataclass
class Pet:
	name: str
	species: str
	age: int
	health_status: str
	owner: Owner | None = None
	requirements: dict[str, Any] = field(default_factory=dict)
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		if task not in self.tasks:
			self.tasks.append(task)
		task.pet = self
		task.owner = self.owner

	def get_needs(self) -> dict[str, Any]:
		pending_tasks = [task for task in self.tasks if not task.is_completed]
		return {
			"health_status": self.health_status,
			"requirements": self.requirements,
			"pending_tasks": pending_tasks,
			"pending_count": len(pending_tasks),
		}

	def update_health_record(self, note: str) -> None:
		health_notes = self.requirements.setdefault("health_notes", [])
		health_notes.append({"timestamp": datetime.now(), "note": note})


@dataclass
class Task:
	task_id: str = field(default_factory=lambda: str(uuid4()))
	description: str = ""
	estimated_duration: int = 15
	frequency: str = "daily"
	category: str = "general"
	priority: int = 1
	pet: Pet | None = None
	owner: Owner | None = None
	is_completed: bool = False
	completed_date: datetime | None = None
	skip_count: int = 0
	scheduled_start: datetime | None = None
	scheduled_end: datetime | None = None
	dependency: Task | None = None

	def mark_complete(self) -> None:
		self.is_completed = True
		self.completed_date = datetime.now()

	def get_priority_score(self) -> int:
		if self.is_completed:
			return -1

		base_score = self.priority * 10
		skip_boost = self.skip_count * 2
		health_boost = 5 if self.pet and self.pet.health_status.lower() != "healthy" else 0
		return base_score + skip_boost + health_boost


@dataclass
class ScheduleResult:
	success: bool
	scheduled_tasks: list[Task] = field(default_factory=list)
	conflicts: list[str] = field(default_factory=list)
	message: str = ""


@dataclass
class Scheduler:
	owner: Owner
	daily_queue: list[Task] = field(default_factory=list)
	total_time_budget: int = 0
	generated_plan: dict[str, Any] = field(default_factory=dict)

	def _calculate_time_budget(self) -> int:
		total_minutes = 0
		for entry in self.owner.available_hours:
			if isinstance(entry, (int, float)):
				total_minutes += int(entry * 60)
			elif isinstance(entry, tuple) and len(entry) == 2:
				start, end = entry
				if isinstance(start, (int, float)) and isinstance(end, (int, float)) and end > start:
					total_minutes += int((end - start) * 60)
		return total_minutes

	def _retrieve_tasks(self, pet_list: list[Pet]) -> list[Task]:
		if pet_list:
			target_pets = pet_list
		else:
			target_pets = self.owner.owned_pets

		tasks: list[Task] = []
		for pet in target_pets:
			for task in pet.tasks:
				task.pet = pet
				task.owner = self.owner
				tasks.append(task)
		return tasks

	def _organize_tasks(self, tasks: list[Task]) -> list[Task]:
		pending_tasks = [task for task in tasks if not task.is_completed]
		return sorted(
			pending_tasks,
			key=lambda task: (task.get_priority_score(), -task.estimated_duration),
			reverse=True,
		)

	def optimize_schedule(self, pet_list: list[Pet]) -> ScheduleResult:
		self.total_time_budget = self._calculate_time_budget()
		all_tasks = self._retrieve_tasks(pet_list)
		ordered_tasks = self._organize_tasks(all_tasks)

		scheduled: list[Task] = []
		conflicts: list[str] = []
		remaining_time = self.total_time_budget

		for task in ordered_tasks:
			if task.dependency and not task.dependency.is_completed and task.dependency not in scheduled:
				task.skip_count += 1
				conflicts.append(
					f"Skipped '{task.description}' because dependency '{task.dependency.description}' is incomplete."
				)
				continue

			if task.estimated_duration > remaining_time:
				task.skip_count += 1
				conflicts.append(
					f"Skipped '{task.description}' due to time budget ({task.estimated_duration}m needed)."
				)
				continue

			scheduled.append(task)
			remaining_time -= task.estimated_duration

		self.daily_queue = scheduled
		self.generated_plan = {
			"owner": self.owner.name,
			"scheduled_count": len(scheduled),
			"remaining_time": remaining_time,
			"conflicts": conflicts,
		}

		message = (
			f"Scheduled {len(scheduled)} task(s) with {remaining_time} minute(s) left in the budget."
		)
		return ScheduleResult(success=len(scheduled) > 0, scheduled_tasks=scheduled, conflicts=conflicts, message=message)

	def explain_logic(self) -> str:
		if not self.generated_plan:
			return "No schedule generated yet."

		return (
			f"PawPal prioritized pending tasks by priority score, skip history, and pet health, "
			f"then filled a {self.total_time_budget}-minute time budget."
		)

	def export_to_streamlit(self) -> dict[str, Any]:
		schedule_rows: list[dict[str, Any]] = []
		for task in self.daily_queue:
			schedule_rows.append(
				{
					"task_id": task.task_id,
					"description": task.description,
					"pet": task.pet.name if task.pet else "unassigned",
					"duration_minutes": task.estimated_duration,
					"frequency": task.frequency,
					"priority": task.priority,
				}
			)

		return {
			"summary": self.generated_plan,
			"schedule": schedule_rows,
			"explanation": self.explain_logic(),
		}
