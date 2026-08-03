## The Problem: Tasks Have Dependencies and Limited Resources

Real-world data pipelines consist of many tasks with complex interdependencies. A feature engineering task cannot start until the raw data is loaded. A model training task cannot start until features are computed. A reporting task cannot start until all upstream tables are populated.

These dependencies form a **Directed Acyclic Graph (DAG)** where:
- Nodes represent tasks
- Edges represent dependencies (A -> B means "B depends on A")
- Acyclic means there are no circular dependencies

Simply running tasks sequentially is wasteful. If tasks A and B have no dependencies on each other, they could run in parallel, finishing faster overall.

But parallelization is constrained by **resources**. Each task requires computational resources (CPU, memory, workers). The system has a limited resource budget. You cannot run more tasks concurrently than the budget allows.

An **orchestrator** must schedule tasks to:
1. Respect all dependency constraints (never start a task before its prerequisites complete)
2. Never exceed the resource budget at any point in time
3. Maximize parallelization to minimize total execution time

---

## DAG Representation

A task graph is typically represented as:

**Task Definition:**
- name: Unique identifier for the task
- duration: How long the task takes to run (in time units)
- resources: How many resource units the task requires while running
- dependencies: List of task names that must complete before this task can start

**Example DAG:**
- Task "load_data": duration=5, resources=2, depends on nothing
- Task "clean_data": duration=3, resources=1, depends on "load_data"
- Task "compute_features": duration=4, resources=2, depends on "load_data"
- Task "train_model": duration=6, resources=3, depends on "clean_data" and "compute_features"

This creates a diamond-shaped dependency structure where "train_model" cannot start until both "clean_data" AND "compute_features" finish.

---

## Task States

Throughout execution, each task is in one of four states:

**Waiting**: The task has at least one incomplete dependency. It cannot start yet.

**Ready**: All dependencies are complete, but the task has not started (possibly due to resource constraints or tie-breaking).

**Running**: The task is currently executing. It occupies resources and will complete after its duration.

**Completed**: The task has finished. Its resources are released, and dependent tasks can now potentially become ready.

---

## The Scheduling Algorithm

At each point in time, the orchestrator follows this process:

**Step 1: Complete Finished Tasks**

Check all running tasks. Any task whose end time has been reached is marked as completed, and its resources are released.

**Step 2: Identify Ready Tasks**

A task is ready if:
- It is not yet started (not running, not completed)
- ALL of its dependencies are completed

**Step 3: Sort Ready Tasks**

Sort the ready tasks alphabetically by name. This deterministic ordering ensures reproducible schedules and breaks ties consistently.

**Step 4: Greedily Assign Tasks**

Iterate through sorted ready tasks. For each task:
- Check if adding its resource requirement would exceed the budget
- If it fits, start the task (assign start time = current time, add to running tasks)
- If it does not fit, skip it (but continue checking later tasks in the list)

This is a **greedy** approach: tasks are assigned in alphabetical order as long as resources allow. A large task that does not fit does not block smaller tasks that might fit.

**Step 5: Advance Time**

If no tasks can be assigned and tasks are still running, advance time to the next task completion event (the earliest end time among running tasks). Then repeat from Step 1.

**Step 6: Termination**

When all tasks are completed, output the schedule.

---

## Resource Management

Resources are managed as a simple numeric budget:

$$
\text{current\_usage} = \sum_{t \in \text{running}} \text{resources}(t)
$$

A task $t$ can start if:

$$
\text{current\_usage} + \text{resources}(t) \leq \text{budget}
$$

When a task completes, its resources are returned to the pool:

$$
\text{current\_usage} \leftarrow \text{current\_usage} - \text{resources}(t)
$$

This is a simplified model. Real systems may have multiple resource dimensions (CPU, memory, network) and more complex constraints.

---

## Time Advancement

Time does not advance one unit at a time. Instead, the algorithm jumps directly to the next meaningful event: when a running task completes.

$$
\text{next\_time} = \min_{t \in \text{running}} (\text{start\_time}(t) + \text{duration}(t))
$$

This event-driven approach is efficient even for tasks with long durations.

If multiple tasks complete at the same time, process all completions before attempting to start new tasks.

---

## A Detailed Worked Example

**Task Definitions:**
- A: duration=2, resources=2, depends=[]
- B: duration=3, resources=1, depends=[]
- C: duration=2, resources=2, depends=[A]
- D: duration=1, resources=1, depends=[A, B]

**Resource Budget: 3**

**Time 0:**
- Completed: none
- Ready: A, B (no dependencies)
- Sorted ready: [A, B]
- Current usage: 0
- Try A: 0 + 2 = 2 <= 3, START A at time 0
- Try B: 2 + 1 = 3 <= 3, START B at time 0
- Running: A (ends at 2), B (ends at 3)
- Usage: 3

**Time 2** (A completes):
- Complete A, release 2 resources, usage = 1
- Completed: {A}
- Check ready: C depends on [A] which is done, C is ready. D depends on [A, B], B not done, D not ready.
- Sorted ready: [C]
- Try C: 1 + 2 = 3 <= 3, START C at time 2
- Running: B (ends at 3), C (ends at 4)
- Usage: 3

**Time 3** (B completes):
- Complete B, release 1 resource, usage = 2
- Completed: {A, B}
- Check ready: D depends on [A, B], both done, D is ready.
- Sorted ready: [D]
- Try D: 2 + 1 = 3 <= 3, START D at time 3
- Running: C (ends at 4), D (ends at 4)
- Usage: 3

**Time 4** (C and D complete):
- Complete C and D
- All tasks done

**Final Schedule (sorted by start_time, then name):**
- (A, 0)
- (B, 0)
- (C, 2)
- (D, 3)

**Total Makespan:** 4 time units

If we had run everything sequentially: 2+3+2+1 = 8 time units. Parallelization saved 50% of the time.

---

## Handling Resource Constraints

Consider a scenario where resources limit parallelism:

**Tasks:**
- X: duration=1, resources=3
- Y: duration=1, resources=3
- Z: duration=1, resources=1

**Budget: 4**

**Time 0:**
- Ready: X, Y, Z (all alphabetically sorted)
- Try X: 0 + 3 <= 4, START X
- Try Y: 3 + 3 = 6 > 4, SKIP Y
- Try Z: 3 + 1 = 4 <= 4, START Z
- Running: X, Z

Even though Y is alphabetically before Z in some sense, we process in order X, Y, Z. X fits, Y does not, but we continue and Z fits.

**Time 1:**
- Complete X and Z
- Ready: Y
- START Y

**Schedule:**
- (X, 0)
- (Z, 0)
- (Y, 1)

---

## Why Alphabetical Ordering?

Using alphabetical order to break ties ensures:

**Determinism**: The same input always produces the same schedule, which is essential for debugging and reproducibility.

**Simplicity**: No need for complex priority schemes or heuristics.

**Consistency**: Easy to predict and verify the behavior.

In practice, production schedulers may use more sophisticated priority schemes (shortest job first, critical path, etc.), but alphabetical ordering provides a clear baseline.

---

## Complexity Analysis

Let $n$ be the number of tasks and $m$ be the total number of dependency edges.

**Building the graph**: $O(n + m)$

**Processing events**: At most $n$ completion events, each involving sorting ready tasks ($O(n \log n)$) and checking resource constraints ($O(n)$).

**Overall**: $O(n^2 \log n)$ in the worst case, though typically much faster in practice with sparse dependencies.

---

## Output Format

The schedule is returned as a list of tuples:

$$
[(\text{task\_name}, \text{start\_time}), ...]
$$

Sorted first by start_time (ascending), then by task_name (alphabetically) for ties.

This format allows easy verification that:
- All tasks are scheduled exactly once
- Dependencies are respected (dependent tasks start later)
- The schedule is deterministic

---

## Where Task Orchestration Shows Up

**Apache Airflow**: The most popular open-source workflow orchestrator, using DAGs to define ETL pipelines.

**Prefect**: Modern Python-native workflow orchestration with dynamic task graphs.

**Luigi**: Spotify's pipeline framework with automatic dependency resolution.

**dbt**: Data transformation tool that builds DAGs from SQL dependencies.

**Kubernetes Jobs**: Container orchestration with dependency-based job scheduling.

**CI/CD Pipelines**: Build systems (Jenkins, GitHub Actions, GitLab CI) schedule jobs with dependencies.

**MapReduce/Spark**: Big data frameworks manage task dependencies within computation graphs.

Understanding task orchestration is fundamental to building reliable, efficient data pipelines at scale.