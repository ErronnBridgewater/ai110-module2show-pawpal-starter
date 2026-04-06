# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design consists of Owner, Pet, Scheduler, and Task. The Owner class is responsible for defining the boundaries of the schedule. The Pet Class is responsible for setting the current state of the animal (age, weight, energy levels), converting needs into data and logging what has been done for specific pets in the past. The Task class is responsible for making sure a task has a duration and a category and racking whether it is "Pending," "InProgress," or "Completed." It also identifies how it essential it is in relation to other tasks. The Scheduler class sorts through tasks in a timeline and manages the risk of scheduling conflicts. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design did change during implementation. One change I made was concrete time slots and adding tracking for completions and skips. The reason why I had made this change was to provide the user the necessary data for the sorting of tasks. Another change I made was introducing a ScheduleResult dataclass to report conflicts and localizing the Scheduler logic to specific owners. This was to decrease the risk of a poorly made feedback loop. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The constraints the scheduler considers are both time and priority. It specifically evaluates time windows by calculating a task's start and end times based on scheduled_start and estimated_duration methods to identify possible overlaps.  I decided that the start and end times of the tasks were the most critical because many pet care tasks, such as administering medication or sticking to a feeding schedule, are time-sensitive and directly impact a pet's well-being. I used the I used estimated duration (int) as a fallback that prevents the owner from over-scheduling their time.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff that the Scheduler class makes is instead of exploring all possible task orderings (which would be computationally expensive), it sorts by time or urgeny to produce a schedule quickly.

This tradeoff is reasonable for this scenario because pet care tasks don’t need a perfect schedule, just one that is understandable. A faster system is also better for users, since they get results right away. Any small issues can still be caught later by the conflict detection feature.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I utitilzed AI as an assistant for designing the initial structures of the Scheduler and Task classes. It helped out the most when I was trying to generate edge-case scenarios, such as verifying how the system handles tasks with missing end times. I used refactoring to implement the "lightweight" conflict check method, which prevents the Streamlit UI from crashing during data entry. I belive the prompts that were most helpful were when I asked how certain classes interacted with each other and when I asked it to brainstorm possible alogorithms to reduce bottlenecks. 
When I made the tests for the apps, I use the Copilot Agent to debug any code that interrupted the app from running. 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment I did not accept an AI suggestion was when I was trying to detect task conflicts with the Scheduler class. I verified what the AI suggested by first analyzing what suggestions it was trying to make to pawpal_system.py. Then, I look at how much of the original code it was removing or changing. I realized that it was getting rid of lines that were essential to previous steps so I denied the suggestion. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested that tasks were correctly sorted by their scheduled_start time in ascending order. Also, I confirmed when a daily task is marked complete, a new task is automatically created for the next day with appropriately shifted start and end times, and added back into the scheduler queue. Finally, I verified that tasks scheduled at the same time are identified as conflicts, and that the system returns a clear message including the conflicting task IDs. These tests were important for verifying that tasks are being ordered correctly, daily tasks continue automatically, and any scheduling conflicts are detected and reported.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I have a 4-star confidence level in the current core behaviors. The implemented logic is backed by 100% passing automated tests but there were errors before I was abel to successfully run them. 

The system is reliable for standard daily scheduling. If I had more time, I would test dependecies between different tasks and how the scheduler would handle with invalid time formats or null values.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of this project that I am most satisfied with is how I was able to overcome the struggles I initially had to commiting and pushing my updates to Github like I did in the last assginment but more efficiently. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve on adding more filters for tasks and adding runtime checks in filter_tasks() to make sure that the function inputs are actually the types they should be. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
When designing a system, it is crucial to ensure that each part’s actions flow smoothly through each other and can be traced back to its source within the system. 
