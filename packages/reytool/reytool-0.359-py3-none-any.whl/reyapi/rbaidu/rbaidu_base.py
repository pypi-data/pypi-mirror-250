# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-11 21:56:56
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Baidu API base methods.
"""


from uuid import uuid1
from reytool.rcomm import request


class RAPIBaidu(object):
    """
    Rey's `Baidu API` type.
    """


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
            "client_id": self.key,
            "client_secret": self.secret
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