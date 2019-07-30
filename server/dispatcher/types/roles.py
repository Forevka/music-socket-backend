from enum import Enum, auto

class AutoName(Enum):
     def _generate_next_value_(name, start, count, last_values):
          return name

class Roles(AutoName):
    Guest = auto()
    User = auto()
    Admin = auto()
