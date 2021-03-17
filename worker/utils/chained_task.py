"""
Chained task definition module
"""
from abc import ABC
from typing import Tuple, Any

from celery import Task


class ChainedTask(Task, ABC):
    """
    Chained task definition implementation
    """

    abstract = True

    @staticmethod
    def _merge_args(*args: list, **kwargs: dict) -> Tuple[list, dict]:
        """
        Merge the input args and kwargs

        Args:
            *args: positional arguments to merge
            **kwargs: keyword arguments to update with the args

        Returns: merged positional arguments, merged keyword arguments

        """
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

    def __call__(self, *args: list, carry_args: bool = False, return_kwargs: bool = False, result_name: str = None,
                 **kwargs: dict) -> Any:
        """
        Call the celery task implementation applying the modification to the arguments indicated by the flags

        Args:
            *args: positional arguments
            carry_args: True if the arguments should be merged with the keyword arguments, False otherwise
            return_kwargs: True if the result should be merged with the input kwargs
            result_name: Name for the result of the task in the merged result
            **kwargs: keyword arguments

        Returns: result of calling the task and applying the argument modifications

        """
        if carry_args:
            args, kwargs = self._merge_args(*args, **kwargs)

        result = super(ChainedTask, self).__call__(*args, **kwargs)

        if result_name:
            result = {result_name: result}

        if return_kwargs and isinstance(result, dict):
            result.update(kwargs)

        return result
