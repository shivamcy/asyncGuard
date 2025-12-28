from abc import ABC, abstractmethod

class BaseCheck(ABC):
    name: str
    severity: str

    @abstractmethod
    def execute(self, api):
        """
        returns:
        {
          "passed": bool,
          "details": dict
        }
        """
        pass
