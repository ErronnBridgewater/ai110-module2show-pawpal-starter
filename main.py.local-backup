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

    # 4. Add at least three Tasks with different times/priorities
    # Task 1: High Priority, Short duration
    task1 = Task(description="Morning Medication", estimated_duration=10, priority=3, category="Health")
    dog.add_task(task1)

    # Task 2: Medium Priority, Longer duration
    task2 = Task(description="Long Park Walk", estimated_duration=60, priority=2, category="Exercise")
    dog.add_task(task2)

    # Task 3: Low Priority, Medium duration
    task3 = Task(description="Brushing/Grooming", estimated_duration=30, priority=1, category="Grooming")
    cat.add_task(task3)

    # 5. Initialize the Scheduler and run optimization
    scheduler = Scheduler(owner=barry)
    result = scheduler.optimize_schedule(pet_list=[cat, dog])

    # 6. Print "Today's Schedule" to the terminal
    print("-" * 40)
    print(f"🐶 PAWPAL: TODAY'S SCHEDULE FOR {barry.name.upper()} 🐱")
    print("-" * 40)
    
    if result.success:
        for i, task in enumerate(result.scheduled_tasks, 1):
            pet_name = task.pet.name if task.pet else "Unknown"
            print(f"{i}. [{task.category.upper()}] {task.description}")
            print(f"   Pet: {pet_name} | Duration: {task.estimated_duration} mins | Score: {task.get_priority_score()}")
            print("-" * 20)
    else:
        print("No tasks could be scheduled today.")

    # Print any conflicts/skipped items
    if result.conflicts:
        print("\n LOGIC NOTES / SKIPPED ITEMS:")
        for conflict in result.conflicts:
            print(f"- {conflict}")

    print("\n" + scheduler.explain_logic())
    print("-" * 40)

if __name__ == "__main__":
    main()