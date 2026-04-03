import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Test Task completion behavior."""

    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's is_completed status."""
        task = Task(
            description="Walk the dog",
            estimated_duration=30,
            category="exercise",
            priority=2,
        )

        # Initially, task should not be completed
        assert task.is_completed is False
        assert task.completed_date is None

        # Mark the task as complete
        task.mark_complete()

        # Verify status changed and timestamp was set
        assert task.is_completed is True
        assert task.completed_date is not None


class TestPetTaskManagement:
    """Test Pet task management behavior."""

    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(name="Mochi", species="dog", age=3, health_status="healthy")
        assert len(pet.tasks) == 0

        # Create and add a task
        task = Task(
            description="Morning walk",
            estimated_duration=20,
            category="exercise",
            priority=2,
        )
        pet.add_task(task)

        # Verify task count increased and task is assigned to pet
        assert len(pet.tasks) == 1
        assert task in pet.tasks
        assert task.pet == pet

        # Add another task and verify count
        task2 = Task(
            description="Feeding",
            estimated_duration=10,
            category="feeding",
            priority=3,
        )
        pet.add_task(task2)

        assert len(pet.tasks) == 2
        assert task2 in pet.tasks
