def load_queries(path):
    queries = {}
    query_name = None
    parameters = []

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('--[') and line.endswith(']'):
                if query_name and parameters:
                    queries[query_name] = ' '.join(parameters)
                query_name = line[4:-1]
                parameters = []
            elif query_name:
                parameters.append(line)

        if query_name and parameters:
            queries[query_name] = ' '.join(parameters)

    return queries