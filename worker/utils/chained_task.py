from abc import ABC
from typing import Tuple, Any

from celery import Task


class ChainedTask(Task, ABC):
    abstract = True

    @staticmethod
    def _merge_args(*args: list, **kwargs: dict) -> Tuple[list, dict]:
        remaining_args = []
        if len(args) == 1:
            if isinstance(args[0], dict):
                kwargs.update(args[0])
            elif isinstance(args[0], list):
                for arg in args[0]:
                    if isinstance(arg, dict):
                        kwargs.update(arg)
                    else:
                        remaining_args.append(arg)
        else:
            remaining_args.extend(args)
        return remaining_args, kwargs

    def __call__(
        self,
        *args: list,
        carry_args: bool = False,
        return_kwargs: bool = False,
        result_name: str = None,
        **kwargs: dict,
    ) -> Any:
        if carry_args:
            args, kwargs = self._merge_args(*args, **kwargs)

        result = super(ChainedTask, self).__call__(*args, **kwargs)

        if result_name:
            result = {result_name: result}

        if return_kwargs and isinstance(result, dict):
            result.update(kwargs)

        return result
