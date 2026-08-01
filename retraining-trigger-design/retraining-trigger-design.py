def retraining_policy(daily_stats, config):
    """
    Decide which days to trigger model retraining.
    """
    retrain_days = []
    budget_remaining = config["budget"]
    last_retrain_day = -config["cooldown"]
    days_since_retrain = 0
    for stat in daily_stats:
        day = stat["day"]
        days_since_retrain += 1
        drift_triggered = stat["drift_score"] > config["drift_threshold"]
        perf_triggered = stat["performance"] < config["performance_threshold"]
        stale_triggered = days_since_retrain >= config["max_staleness"]
        should_retrain = drift_triggered or perf_triggered or stale_triggered
        cooldown_ok = (day - last_retrain_day) >= config["cooldown"]
        budget_ok = budget_remaining >= config["retrain_cost"]
        if should_retrain and cooldown_ok and budget_ok:
            retrain_days.append(day)
            budget_remaining -= config["retrain_cost"]
            last_retrain_day = day
            days_since_retrain = 0
    return retrain_days
