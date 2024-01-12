def _object_to_dict(obj):
    """
    Recursively converts an object's attributes to a dictionary.
    """
    if isinstance(obj, (int, float, str, bool, type(None))):
        # Base case for simple types
        return obj

    if isinstance(obj, (list, tuple)):
        # Process each item in list or tuple recursively
        return [_object_to_dict(item) for item in obj]

    if hasattr(obj, "__dict__"):
        # Process each attribute of the object recursively
        return {attr: _object_to_dict(getattr(obj, attr)) for attr in dir(obj) if not attr.startswith('__') and not callable(getattr(obj, attr))}

    return str(obj)  # Fallback for unhandled types


def get_subscriptable_obj(obj):
    # Check if the object is already subscriptable (like dict, list, tuple)
    if isinstance(obj, (dict, list, tuple)):
        return obj
    else:
        return _object_to_dict(obj)