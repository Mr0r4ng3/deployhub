from enum import Enum


class SessionCloseReason(Enum):
    UserRequest = "UserRequest"
    Inactivity = "Inactivity"
    Logout = "Logout"
    Expired = "Expired"

    def __str__(self):
        return self.value
