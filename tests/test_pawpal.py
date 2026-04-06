from datetime import datetime, timedelta
from pathlib import Path
import sys


# Ensure tests can import project modules regardless of pytest import mode.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pawpal_system import Task, Pet, Owner, Scheduler


def _build_owner_and_pet() -> tuple[Owner, Pet]:
    owner = Owner(name="Jordan", available_hours=[4.0], energy_level=2)
    pet = Pet(name="Mochi", species="dog", age=3, health_status="healthy", owner=owner)
    return owner, pet


class TestSchedulerBehavior:
    def test_tasks_returned_in_chronological_order(self):
        """Verify Scheduler.sort_by_time() orders tasks by scheduled_start ascending."""
        owner, pet = _build_owner_and_pet()

        t1 = Task(
            task_id="late",
            category="exercise",
            priority=2,
            estimated_duration=30,
            pet=pet,
            owner=owner,
            scheduled_start=datetime(2026, 4, 5, 10, 0),
        )
        t2 = Task(
            task_id="early",
            category="feeding",
            priority=3,
            estimated_duration=15,
            pet=pet,
            owner=owner,
            scheduled_start=datetime(2026, 4, 5, 8, 30),
        )
        t3 = Task(
            task_id="middle",
            category="grooming",
            priority=1,
            estimated_duration=20,
            pet=pet,
            owner=owner,
            scheduled_start=datetime(2026, 4, 5, 9, 0),
        )

        scheduler = Scheduler(owner=owner, daily_queue=[t1, t2, t3])

        ordered = scheduler.sort_by_time()

        assert [task.task_id for task in ordered] == ["early", "middle", "late"]

    def test_marking_daily_task_complete_creates_next_day_task(self):
        """Verify completing a daily task enqueues a new task one day later."""
        owner, pet = _build_owner_and_pet()
        start = datetime(2026, 4, 5, 7, 0)
        end = datetime(2026, 4, 5, 7, 30)

        daily_task = Task(
            task_id="walk-daily",
            category="daily",
            priority=3,
            estimated_duration=30,
            pet=pet,
            owner=owner,
            scheduled_start=start,
            scheduled_end=end,
        )

        scheduler = Scheduler(owner=owner, daily_queue=[daily_task])

        next_task = scheduler.complete_task(daily_task)

        assert daily_task.is_completed is True
        assert next_task is not None
        assert next_task.task_id == "walk-daily-next"
        assert next_task.scheduled_start == start + timedelta(days=1)
        assert next_task.scheduled_end == end + timedelta(days=1)
        assert next_task in scheduler.daily_queue

    def test_scheduler_flags_duplicate_times_as_conflict(self):
        """Verify overlapping tasks at the same time are flagged as conflicts."""
        owner, pet = _build_owner_and_pet()
        shared_start = datetime(2026, 4, 5, 9, 0)

        task_a = Task(
            task_id="meds",
            category="health",
            priority=3,
            estimated_duration=20,
            pet=pet,
            owner=owner,
            scheduled_start=shared_start,
        )
        task_b = Task(
            task_id="walk",
            category="exercise",
            priority=2,
            estimated_duration=30,
            pet=pet,
            owner=owner,
            scheduled_start=shared_start,
        )

        scheduler = Scheduler(owner=owner, daily_queue=[task_a, task_b])

        conflicts = scheduler.detect_time_conflicts()

        assert len(conflicts) == 1
        assert "Time conflict" in conflicts[0]
        assert "meds" in conflicts[0]
        assert "walk" in conflicts[0]
