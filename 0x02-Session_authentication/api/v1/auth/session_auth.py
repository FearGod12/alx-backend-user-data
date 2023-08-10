#!/usr/bin/env python3
"""the Authentication module"""
from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    pass
