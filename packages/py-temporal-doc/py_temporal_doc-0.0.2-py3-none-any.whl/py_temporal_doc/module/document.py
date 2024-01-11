def doc_workflow_caller(func):
    def wrapper(*args, **kwargs):
        # Call the decorated function
        result = func(*args, **kwargs)
        return result

    return wrapper


def doc_workflow_sequence(func):
    def wrapper(*args, **kwargs):
        # Call the decorated function
        result = func(*args, **kwargs)
        return result

    return wrapper


# TODO: Decide the structure of this later
def doc_workflow_schedule(func):
    def wrapper(*args, **kwargs):
        # Call the decorated function
        result = func(*args, **kwargs)
        return result

    return wrapper
