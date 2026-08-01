def evaluate_shadow(production_log, shadow_log, criteria):
    """
    Evaluate whether a shadow model is ready for promotion.
    """
    # Write code here
    min_accuracy_gain = criteria.get('min_accuracy_gain',0.0)
    max_latency_p95 = criteria.get('max_latency_p95',0.0)
    min_aggreement_rate = criteria.get('min_agreement_rate',0.0)
    
    n = len(production_log)
    prod_matched, shadow_matched, both_matched = 0,0,0
    for i in range(n):
        
        if production_log[i]['prediction'] == production_log[i]['actual']:
            prod_matched+=1
        
        if shadow_log[i]['prediction'] == shadow_log[i]['actual']:
            shadow_matched+=1

        if shadow_log[i]['prediction'] == production_log[i]['prediction']:
            both_matched+=1
    
    
    prod_accuracy = prod_matched/n
    shadow_accuracy = shadow_matched/n
    accuracy_gain = shadow_accuracy - prod_accuracy
    aggreement_rate = both_matched/n
    shadow_p95_latency = shadow_log[int(0.95*n)]['latency_ms']
    output_log = {'promote': False,
                  'metrics': {
                 'shadow_accuracy': shadow_accuracy,
                 'production_accuracy': prod_accuracy,
                 'accuracy_gain': accuracy_gain,
                 'shadow_latency_p95': shadow_p95_latency,
                 'agreement_rate': aggreement_rate}}
    

    if accuracy_gain >= min_accuracy_gain and shadow_p95_latency <= max_latency_p95 and aggreement_rate >= min_aggreement_rate:
        output_log['promote'] = True

    return output_log