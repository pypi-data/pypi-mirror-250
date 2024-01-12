# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-11 22:00:14
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Baidu API voice methods.
"""


from typing import Optional
from reytool.ros import RFile
from reytool.rsystem import warn

from .rbaidu_base import RBaiduBase, RBaiduAPIError


class RBaiduVoice(RBaiduBase):
    """
    Rey's `Baidu API voice` type.
    """


    # Request parameters.
    url = "https://tsn.baidu.com/text2audio"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }


    def from_text(
        self,
        text: str,
        path: Optional[str] = None
    ) -> bytes:
        """
        Generate voice from text.

        Parameters
        ----------
        path : File save path.
            - `None` : Not save.

        Returns
        -------
        Voice bytes data.
        """

        # Check.
        if len(text) > 60:
            text = text[:60]
            warn("parameter 'text' length cannot exceed 60")

        # Get parameter.
        body = {
            "cuid": self.cuid,
            "ctp": 1,
            "lan": "zh",
            "spd": 5,
            "pit": 5,
            "vol": 5,
            "aue": 3,
            "per": 4,
            "tex": text
        }

        # Request.
        response = self.request(**body)

        # Extract.
        file_bytes = response.content

        # Save.
        if path is not None:
            rfile = RFile(path)
            rfile.write(file_bytes)

        return file_bytes