from typing import Awaitable, Callable, TypeVar, ParamSpec
from result import Result, Ok

P = ParamSpec("P")
E = TypeVar("E", covariant=True)



from typing import Callable, TypeVar, Any

R = TypeVar('R')  # Declare TypeVar for any return type
F = TypeVar('F', bound=Callable[..., Any])  # Declare TypeVar for any callable


def parametrized(decorator: Callable[[F, Callable[..., R]], F]) -> Callable[[Callable[..., R]], Callable[[F], F]]:
    def layer(exception_handler: Callable[..., R]) -> Callable[[F], F]:
        def wrapper(func: F) -> F:
            return decorator(func, exception_handler)
        return wrapper
    return layer

# def parametrized(
#     decorator: Callable[
#         [Callable[P, R], Callable[..., Result[R, E]]],
#         Callable[P, Result[R, E]],
#     ]
# ) -> Callable[
#     [Callable[..., Result[R, E]]],
#     Callable[[Callable[P, R]], Callable[P, Result[R, E]]],
# ]:
#     def layer(
#         exception_handler: Callable[..., Result[R, E]]
#     ) -> Callable[[Callable[P, R]], Callable[P, Result[R, E]]]:
#         def wrapper(func: Callable[P, R]) -> Callable[P, Result[R, E]]:
#             return decorator(func, exception_handler)

#         return wrapper

#     return layer


@parametrized
def exception_handled(
    func: Callable[P, R], exception_handler: Callable[[Exception], Result[R, E]]
) -> Callable[P, Result[R, E]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, E]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:  # catch all exceptions and delegate to handler
            return exception_handler(e)

    return wrapper


@parametrized
def exception_handled_async(
    func: Callable[P, Awaitable[R]],
    exception_handler: Callable[..., Result[R, E]],
) -> Callable[P, Awaitable[Result[R, E]]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, E]:
        try:
            return Ok(await func(*args, **kwargs))
        except Exception as e:  # catch all exceptions and delegate to handler
            return exception_handler(e)

    return wrapper
