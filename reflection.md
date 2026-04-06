# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design consists of Owner, Pet, Scheduler, and Task. The Owner class is responsible for defining the boundaries of the schedule. The Pet Class is responsible for setting the current state of the animal (age, weight, energy levels), converting needs into data and logging what has been done for specific pets in the past. The Task class is responsible for making sure a task has a duration and a category and Tracking whether it is "Pending," "InProgress," or "Completed." It also identifies how it essential it is in relation to other tasks. The Scheduler class sorts through tasks in a timeline and manages the risk of scheduling conflicts. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

My design did change during implementation. One change I made was concrete time slots and adding tracking for completions and skips. The reason why I had made this change was to provide the user the necessary data for the sorting of tasks. Another change I made was introducing a ScheduleResult dataclass to report conflicts and localizing the Scheduler logic to specific owners. This was to increase the risk of a poorly made feedback loop. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff that the Scheduler class makes is instead of exploring all possible task orderings (which would be computationally expensive), it sorts by time or urgeny to produce a schedule quickly.

This tardeoff is reasonable for this scenario because pet care tasks don’t need a perfect schedule, just one that is understandable. A faster system is also better for users, since they get results right away. Any small issues can still be caught later by the conflict detection feature.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
