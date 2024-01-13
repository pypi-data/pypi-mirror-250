from logging import basicConfig, WARNING, INFO, info
from sys import stdout
from threading import get_ident


def logs_config(
    file_path: str | None = None,
    verbose: bool = None
) -> None:
    basicConfig(
        stream=stdout,
        format='%(asctime)s %(message)s',
        datefmt='[%m/%d/%Y %I:%M:%S %p]',
        encoding='utf-8',
        level=INFO if verbose else WARNING,
        filename=file_path,
    )


def error_manager(max_tries: int = 1) -> object:
    def funcwrapper(func) -> object:
        def argswrapper(*args, **kwargs) -> object:
            x: object = None
            for i in range(max_tries):
                try:
                    x = func(*args, **kwargs)
                    break
                except Exception as e:
                    print(f"Error at try {i}/{max_tries}. {type(e)}:{e}")
            return x
        return argswrapper
    return funcwrapper


def logs_manager(message: str) -> object:
    def funcwrapper(func) -> object:
        def argswrapper(*args, **kwargs) -> object:
            info(f'Job {message} on thread {get_ident()} started.')
            return func(*args, **kwargs)
        info(f'Job {message} on thread {get_ident()} ended.')
        return argswrapper
    return funcwrapper
