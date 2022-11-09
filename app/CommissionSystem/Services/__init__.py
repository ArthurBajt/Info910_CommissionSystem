from fastapi import APIRouter

from .HomeService import app as home

services: list[APIRouter] = [
    home
]
