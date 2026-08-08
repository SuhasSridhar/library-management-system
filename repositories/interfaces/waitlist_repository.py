from abc import ABC, abstractmethod

class WaitlistRepository(ABC):

    @abstractmethod
    def waitlist_member(self) -> None:
        ...