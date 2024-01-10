# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-09 21:47:02
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Schedule methods.
"""


from typing import Any, Dict, Literal, Callable, Union
from reytool.rschedule import RSchedule as RRSchedule

from .rwechat import RWeChat


class RSchedule(object):
    """
    Rey's `schedule` type.
    """

    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `schedule` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.rrschedule = RRSchedule(1)

        # Start.
        self.rrschedule.start()


    def send(
        self,
        trigger: Literal['date', 'interval', 'cron'],
        trigger_kwargs: Dict,
        send_type: Literal[
            "text",
            "at",
            "file",
            "image",
            "emotion",
            "pat",
            "public",
            "forward"
        ],
        receive_id: str,
        **params: Dict[str, Union[Callable[[], Any], Any]]
    ) -> None:
        """
        Schedule send message.

        Parameters
        ----------
        trigger : Trigger type.
        trigger_kwargs : Trigger keyword arguments.
        send_type : Send type.
            - `Literal['text']` : Send text message, use `RClient.send_text` method.
            - `Literal['at']` : Send text message with `@`, use `RClient.send_text_at` method.
            - `Literal['file']` : Send file message, use `RClient.send_file` method.
            - `Literal['image']` : Send image message, use `RClient.send_image` method.
            - `Literal['emotion']` : Send emotion message, use `RClient.send_emotion` method.
            - `Literal['pat']` : Send pat message, use `RClient.send_pat` method.
            - `Literal['public']` : Send public account message, use `RClient.send_public` method.
            - `Literal['forward']` : Forward message, use `RClient.send_forward` method.

        receive_id : User ID or chat room ID of receive message.
        params : Send parameters.
            - `Callable` : Use execute return value.
            - `Any` : Use this value.
        """


        # Define.
        def task() -> None:
            """
            Task of schedule send message.
            """

            # Handle parameter.
            params_execute = {
                key: (
                    value()
                    if callable(value)
                    else value
                )
                for key, value in params.items()
            }

            # Send.
            self.rwechat.rsend.send(
                send_type,
                receive_id,
                **params_execute
            )


        # Add.
        self.rrschedule.add_task(
            task,
            trigger,
            **trigger_kwargs
        )


    def pause(self) -> None:
        """
        Pause scheduler.
        """

        # Pause.
        self.rrschedule.pause()


    def resume(self) -> None:
        """
        Resume scheduler.
        """

        # Pause.
        self.rrschedule.resume()