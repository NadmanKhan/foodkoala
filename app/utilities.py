def overrides(interface_class: type):
    """Decorator to mark a method as overriding a method from an interface

    Args:
        interface_class (`type`): Interface class to check for method presence

    Returns:
        The decorator function
    """

    def overrider(method):
        assert method.__name__ in dir(
            interface_class
        ), f"Method {method.__name__} not found in {interface_class.__name__}"
        return method

    return overrider
