def feature_store_lookup(feature_store, requests, defaults):
    """
    Join offline user features with online request-time features.
    """
    # Write code here
    lookup_lst = []
    for request in requests:
        if request['user_id'] in feature_store.keys():
            lookup_lst.append(feature_store[request['user_id']] | request['online_features'])
        else:
            lookup_lst.append(defaults | request['online_features'])

    return lookup_lst