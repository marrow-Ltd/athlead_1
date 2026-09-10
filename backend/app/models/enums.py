from enum import Enum


class UserRole(str, Enum):
    student = "student"
    coach = "coach"
