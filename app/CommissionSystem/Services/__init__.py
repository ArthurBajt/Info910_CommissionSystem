from fastapi import APIRouter

from .HomeService import app as home
from .UserService import app as users
from .CommissionService import app as commissions

services: list[APIRouter] = [
    home,
    users,
    commissions
]
