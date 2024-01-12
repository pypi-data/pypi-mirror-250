from typing import Any

from awslambdaric.lambda_context import LambdaContext

from pydantic_lambda_handler.models import BaseOutput


class BaseHook:
    @staticmethod
    def method_init(**kwargs) -> None:
        """1st"""
        return

    @staticmethod
    def post_create_response(**kwargs) -> None:
        """
        2nd: This is called after the hook is created.
        """
        return

    @staticmethod
    def pre_path(**kwargs) -> None:
        """3rd"""
        return

    @staticmethod
    def pre_func(event, context) -> tuple[dict, LambdaContext]:
        """4th"""
        return event, context

    @staticmethod
    def post_func(body) -> Any:
        """5th"""
        return body

    @staticmethod
    def pre_return(output: BaseOutput) -> BaseOutput:
        """6th"""
        return output
