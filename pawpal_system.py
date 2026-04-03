from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


@dataclass
class Owner:
	name: str
	available_hours: list[Any] = field(default_factory=list)
	energy_level: int = 0
	owned_pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet_details: Pet) -> None:
		pass

	def update_availability(self, times: Any) -> None:
		pass

	def get_preferences(self) -> str:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age: int
	health_status: str
	owner: Owner | None = None
	requirements: dict[str, Any] = field(default_factory=dict)

	def get_needs(self) -> dict[str, Any]:
		pass

	def update_health_record(self, note: str) -> None:
		pass


@dataclass
class Task:
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

	def mark_complete(self) -> None:
		pass

	def get_priority_score(self) -> int:
		pass


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

	def optimize_schedule(self, pet_list: list[Pet]) -> ScheduleResult:
		pass

	def explain_logic(self) -> str:
		pass

	def export_to_streamlit(self) -> dict[str, Any]:
		pass
