from datetime import datetime

def promote_model(models):
    """
    Decide which model version to promote to production.
    """
    # Write code here
    best_model = models[0]
    for model in models[1:]:
        # Accuracy comparison
        if model['accuracy'] > best_model['accuracy']:
            best_model = model
            continue
        elif model['accuracy'] == best_model['accuracy']:
            # Latency comparison
            if model['latency'] < best_model['latency']:
                best_model = model
                continue
            elif model['latency'] == best_model['latency']:
                # Timestamp comparison
                date_format = "%Y-%M-%d"

                if(datetime.strptime(model['timestamp'], date_format) >= datetime.strptime(best_model['timestamp'], date_format)):
                    best_model = model
                    continue

            else:
                continue
    return best_model['name']