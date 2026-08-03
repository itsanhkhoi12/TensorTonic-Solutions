def schedule_pipeline(tasks, resource_budget):
    """
    Schedule ETL tasks respecting dependencies and resource limits.
    """
    task_map = {t["name"]: t for t in tasks}
    running = {}
    completed = set()
    schedule = []
    t = 0
    while len(completed) < len(tasks):
        for name in [n for n, end in running.items() if end <= t]:
            completed.add(name)
            del running[name]
        cur_res = sum(task_map[n]["resources"] for n in running)
        ready = sorted(
            [tk for tk in tasks if tk["name"] not in completed
             and tk["name"] not in running
             and all(d in completed for d in tk["depends_on"])],
            key=lambda x: x["name"]
        )
        for tk in ready:
            if cur_res + tk["resources"] <= resource_budget:
                running[tk["name"]] = t + tk["duration"]
                schedule.append((tk["name"], t))
                cur_res += tk["resources"]
        if running:
            t = min(running.values())
        else:
            break
    return sorted(schedule, key=lambda x: (x[1], x[0]))