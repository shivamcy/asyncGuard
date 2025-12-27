from abc import ABC, abstractmethod

class BaseCheck(ABC):
    name: str
    severity: str

    @abstractmethod
    async def execute(self, api):
        """
        api: ApiEndpoint SQLAlchemy model
        returns: dict { passed: bool, details: dict }
        """
        pass
