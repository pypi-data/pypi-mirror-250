import wrapt


def required_params(*keys):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        invalid_params = keys - \
            kwargs.keys() if not set(keys).issubset(set(kwargs.keys())) else []
        # raise exception when seeing invalid parameters
        if invalid_params:
            raise KeyError(
                f'The required keys (parameters) were missing: {list(invalid_params)}')
        return wrapped(*args, **kwargs)
    return wrapper
