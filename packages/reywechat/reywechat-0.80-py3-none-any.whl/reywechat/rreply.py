# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-10 16:24:10
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Reply methods.
"""


from typing import Any, List, Dict, Literal, Callable, Union

from .rreceive import RMessage
from .rwechat import RWeChat


__all__ = (
    "RReply",
)


class RReply(object):
    """
    Rey's `reply` type.
    """


    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `reply` instance.

        Parameters
        ----------
        rwechat : `RWeChat` instance.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.rules: List[Dict[Literal["judge", "sends", "level"], Any]] = []

        # Add handler.
        self._reply_by_rule()


    def _reply_by_rule(self) -> None:
        """
        Add handler, reply message by rules.
        """


        # Define.
        def handler_reply_by_rule(message: RMessage) -> None:
            """
            Reply message by rules.

            Parameters
            ----------
            message : `RMessage` instance.
            """

            # Loop.
            for rule in self.rules:
                judge: Callable[[RMessage], bool] = rule["judge"]
                sends: List[Callable[[RMessage], Dict]] = rule["sends"]

                # Judge.
                result = judge(message)
                if result:

                    # Send.
                    for send in sends:
                        params = send(message)
                        self.rwechat.rsend.send(**params)

                    break


        # Add handler.
        self.rwechat.rreceive.add_handler(handler_reply_by_rule)


    def add_rule(
        self,
        judge: Callable[[RMessage], bool],
        sends: Union[Callable[[RMessage], Dict], List[Callable[[RMessage], Dict]]],
        level: float = 1
    ) -> None:
        """
        Add reply rule.

        Parameters
        ----------
        judge : Function to judge whether to reply.
        sends : Functions to generate send parameters.
        level : Priority level, sort from large to small.
        """

        # Get parameter.
        if callable(sends):
            sends = [sends]
        rule = {
            "judge": judge,
            "sends": sends,
            "level": level
        }

        # Add.
        self.rules.append(rule)

        # Sort.
        fund_sort = lambda rule: rule["level"]
        self.rules.sort(
            key=fund_sort,
            reverse=True
        )