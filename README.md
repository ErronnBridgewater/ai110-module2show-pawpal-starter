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

### Smarter Scheduling 

The _build_next_occurrence method handles the lifecycle of recurring tasks. It automatically calculates new start and end times for "daily" or "weekly" categories and genereates a new Task instance to keep the pet care routine consistent.

The detect_time_conflicts engine identifies overlapping schedules. It compares task time windows to find conflictsand categorizes them based on whether they involve the same pet or different pets.

The detect_time_conflicts_lightweight method prevents the entire application from crashing if a task has missing or corrupted data, returning a helpful warning message instead.

The filter_tasks method isolates tasks based on their completion status or specific pet names.

 The sort_by_time feature organizes the daily queue by their scheduled start times. handles unscheduled tasks by placing them at the end of the list, so the owner sees immediate priorities first.

he _get_task_window helper logic determines the effective duration of a task. It can derive an end time using the estimated_duration if a specific scheduled_end isn't provided. 