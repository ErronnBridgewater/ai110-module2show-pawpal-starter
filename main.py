from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime

def main():
    # Create Owner with name and availability
    barry = Owner(name="Barry", available_hours=[4.0])

    # 2. Create two Pets
    cat = Pet(name="Luna", species="Cat", age=3, health_status="Healthy")
    dog = Pet(name="Buster", species="Dog", age=5, health_status="Needs Medication")

    # 3. Add Pets to Owner
    barry.add_pet(cat)
    barry.add_pet(dog)

    # 4. Add tasks out of order (scheduled_start times are intentionally scrambled)
    # Added third — scheduled earliest at 8:00 AM
    task3 = Task(task_id="grooming-1", estimated_duration=30, priority=1, category="Grooming",
                 pet=cat, owner=barry, scheduled_start=datetime(2026, 4, 4, 8, 0))

    # Added first — scheduled last at 10:00 AM
    task1 = Task(task_id="medication-1", estimated_duration=30, priority=3, category="Health",
                 pet=dog, owner=barry, scheduled_start=datetime(2026, 4, 4, 9, 0))

    # Added second — scheduled in the middle at 9:00 AM
    task2 = Task(task_id="walk-1", estimated_duration=60, priority=2, category="Exercise",
                 pet=dog, owner=barry, scheduled_start=datetime(2026, 4, 4, 9, 0))

    # 5. Initialize the Scheduler and run optimization
    scheduler = Scheduler(owner=barry, daily_queue=[task3, task1, task2])
    result = scheduler.optimize_schedule(pet_list=[cat, dog])

    # 6. Print "Today's Schedule" to the terminal
    print("-" * 40)
    print(f"🐶 PAWPAL: TODAY'S SCHEDULE FOR {barry.name.upper()} 🐱")
    print("-" * 40)
    
    if result and result.success:
        for i, task in enumerate(result.scheduled_tasks, 1):
            pet_name = task.pet.name if task.pet else "Unknown"
            print(f"{i}. [{task.category.upper()}] {task.task_id}")
            print(f"   Pet: {pet_name} | Duration: {task.estimated_duration} mins | Score: {task.get_priority_score()}")
            print("-" * 20)
    elif result is None:
        print("Schedule optimization not implemented yet; running conflict detection on current queue.")
    else:
        print("No tasks could be scheduled today.")

    # Print any conflicts/skipped items
    if result and result.conflicts:
        print("\n LOGIC NOTES / SKIPPED ITEMS:")
        for conflict in result.conflicts:
            print(f"- {conflict}")

    logic = scheduler.explain_logic()
    print("\n" + (logic if logic else "Logic explanation not implemented yet."))
    print("-" * 40)

    # Lightweight conflict check: return warnings/messages instead of raising errors.
    print("\nCONFLICT CHECK:")
    print("-" * 40)
    for message in scheduler.detect_time_conflicts_lightweight():
        if "Time conflict" in message:
            print(f"WARNING: {message}")
        else:
            print(message)
    print("-" * 40)

    # Demonstrate sort_by_time: tasks were added out of order above
    print("\nTASKS SORTED BY SCHEDULED START TIME:")
    print("-" * 40)
    for task in scheduler.sort_by_time():
        start = task.scheduled_start.strftime("%I:%M %p") if task.scheduled_start else "No time set"
        pet_name = task.pet.name if task.pet else "Unknown"
        print(f"  {start} | {task.task_id} ({pet_name})")
    print("-" * 40)

if __name__ == "__main__":
    main()