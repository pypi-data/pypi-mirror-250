# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-11 21:56:56
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Baidu API base methods.
"""


from typing import Any, Dict
from requests import Response
from uuid import uuid1
from reytool.rcomm import request


class RAPIBaidu(object):
    """
    Rey's `Baidu API` type.
    """


    # Request parameters.
    url: str
    headers: Dict


    def __init__(
        self,
        key: str,
        secret: str
    ) -> None:
        """
        Build `Baidu API` instance.

        Parameters
        ----------
        key : API key.
        secret : API secret.
        """

        # Set attribute.
        self.key = key
        self.secret = secret
        self.token = self.get_token()
        self.cuid = uuid1()


    def get_token(self) -> str:
        """
        Get token.

        Returns
        -------
        Token.
        """

        # Get parameter.
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "key": self.key,
            "secret": self.secret
        }

        # Request.
        response = request(
            url,
            params,
            method="post"
        )

        # Extract.
        response_json = response.json()
        token = response_json["access_token"]

        return token


    def request(
        self,
        **body: Any
    ) -> Response:
        """
        Request API.

        Parameters
        ----------
        body : Request body.
        """

        # Handle parameter.
        body["tok"] = self.token

        # Reqeust.
        response = request(
            self.url,
            data=body,
            headers=self.headers,
            method="post"
        )

        return response