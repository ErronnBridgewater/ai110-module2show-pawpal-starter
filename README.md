# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

The current implementation includes these scheduling and task-management algorithms:

- Time-based sorting with `Scheduler.sort_by_time()`, which returns the daily queue ordered by `scheduled_start` and places unscheduled tasks at the end.
- Conflict detection with `Scheduler.detect_time_conflicts()`, which compares task time windows and reports overlaps, including whether the conflict is for the same pet or different pets.
- Safe conflict reporting with `Scheduler.detect_time_conflicts_lightweight()`, which wraps conflict detection and returns a warning instead of crashing if task data is invalid.
- Task filtering with `Scheduler.filter_tasks()`, which narrows the queue by completion status or pet name.
- Recurring task rollover with `Task.mark_complete()` and `Task._build_next_occurrence()`, which mark a task complete and create the next daily or weekly occurrence when appropriate.
- Queue completion handling with `Scheduler.complete_task()`, which marks a task complete and appends the generated follow-up task back into the scheduler queue.
- Task window normalization with `Scheduler._get_task_window()`, which infers an end time from `estimated_duration` when `scheduled_end` is missing.

The project also includes tests that verify chronological sorting, daily task rollover, and duplicate-time conflict detection.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### UML Diagram

classDiagram
	class Owner {
		+String name
		+List~Any~ available_hours
		+Integer energy_level
		+List~Pet~ owned_pets
		+add_pet(pet_details) None
		+update_availability(times) None
		+get_preferences() String
	}

	class Pet {
		+String name
		+String species
		+Integer age
		+String health_status
		+Owner owner
		+Dictionary requirements
		+get_needs() Dictionary
		+update_health_record(note) None
	}

	class Task {
		+String task_id
		+String category
		+Integer priority
		+Integer estimated_duration
		+Pet pet
		+Owner owner
		+Boolean is_completed
		+DateTime completed_date
		+Integer skip_count
		+DateTime scheduled_start
		+DateTime scheduled_end
		+Task dependency
		+mark_complete() Task
		-_build_next_occurrence() Task
		+get_priority_score() Integer
	}

	class ScheduleResult {
		+Boolean success
		+List~Task~ scheduled_tasks
		+List~String~ conflicts
		+String message
	}

	class Scheduler {
		+Owner owner
		+List~Task~ daily_queue
		+Integer total_time_budget
		+Dictionary generated_plan
		+complete_task(task) Task
		+optimize_schedule(pet_list) ScheduleResult
		+explain_logic() String
		+export_to_streamlit() Dictionary
		+detect_time_conflicts() List~String~
		+detect_time_conflicts_lightweight() List~String~
		+filter_tasks(is_completed, pet_name) List~Task~
		+sort_by_time() List~Task~
		-_get_task_window(task) Tuple~DateTime,DateTime~
	}

	Owner "1" o-- "0..*" Pet : owns
	Pet "0..1" --> "1" Owner : belongs to
	Scheduler "1" --> "1" Owner : uses
	Scheduler "1" o-- "0..*" Task : schedules
	Scheduler ..> ScheduleResult : returns
	Task "0..1" --> "0..1" Task : depends on
	Task "0..1" --> "0..1" Pet : assigned to
	Task "0..1" --> "0..1" Owner : assigned to
```

### Smarter Scheduling 

The _build_next_occurrence method handles the lifecycle of recurring tasks. It automatically calculates new start and end times for "daily" or "weekly" categories and generates a new Task instance to keep the pet care routine consistent.

The detect_time_conflicts engine identifies overlapping schedules. It compares task time windows to find conflicts and categorizes them based on whether they involve the same pet or different pets.

The detect_time_conflicts_lightweight method prevents the entire application from crashing if a task has missing or corrupted data, returning a helpful warning message instead.

The filter_tasks method isolates tasks based on their completion status or specific pet names.

The sort_by_time feature organizes the daily queue by their scheduled start times and handles unscheduled tasks by placing them at the end of the list, so the owner sees immediate priorities first.

The _get_task_window helper logic determines the effective duration of a task. It can derive an end time using the estimated_duration if a specific scheduled_end isn't provided. 

#### Testing PawPal+ 

python -m pytest
Confidence Level: 4 
The tests cover the following: 
- Ensures that tasks are correctly sorted by their scheduled_start time in ascending order.
- Confirms that when a daily task is marked complete, a new task is automatically created for the next day with appropriately shifted start and end times, and added back into the scheduler queue.
- Verifies that tasks scheduled at the same time are identified as conflicts, and that the system returns a clear message including the conflicting task IDs.

### 📸 Demo
<a href="/course_images/ai110/fianl_screenshot.png" target="_blank"><img src='/course_images/ai110 </a>
# I added the png file into the folder in case the embedded syntax does not work 