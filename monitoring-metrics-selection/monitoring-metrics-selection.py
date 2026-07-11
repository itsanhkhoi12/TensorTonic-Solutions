import math

def compute_monitoring_metrics(system_type, y_true, y_pred):
    """
    Compute the appropriate monitoring metrics for the given system type.
    """
    # Write code here
    
    feat_counts = len(y_true)

    # Classification metric
    if system_type == 'classification':
        tp,fp,tn,fn = 0,0,0,0
        
        for i in range(feat_counts):
            if y_true[i] == 1:
                if y_pred[i]==1:
                    tp+=1
                else:
                    fn+=1
            else:
                if y_pred[i]==1:
                    fp+=1
                else:
                    tn+=1

        accuracy = (tp+tn)/feat_counts
        precision = tp/(tp+fp) if (tp+fp) > 0 else 0.0
        recall = tp/(tp+fn) if (tp+fn) > 0 else 0.0
        f1 = (2*precision*recall)/(precision+recall) if (precision+recall) > 0 else 0.0
        return [("accuracy",accuracy),
                ("f1",f1),
               ("precision",precision),
               ("recall",recall),
               ]

        # Regression metric
    elif system_type == 'regression':
        mae = sum([abs(y-y_hat) for y, y_hat in zip(y_true,y_pred)])/feat_counts
        rmse = math.sqrt(sum([(y-y_hat)**2 for y, y_hat in zip(y_true,y_pred)])/feat_counts)

        return [('mae',mae),
               ('rmse',rmse)]

    else:
        total_relevant = y_true.count(1)
        relevant_item_in_top_3 = y_true[:3].count(1)
        precision_at_3 = relevant_item_in_top_3/3
        recall_at_3 = relevant_item_in_top_3/total_relevant if total_relevant > 0 else 0.0
        return [('precision_at_3',precision_at_3),
               ('recall_at_3',recall_at_3)]