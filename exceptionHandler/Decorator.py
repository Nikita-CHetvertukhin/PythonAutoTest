def exception_handler(error_handler):
    """Декоратор для обработки исключений"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_exception(e)
                raise e
        return wrapper
    return decorator