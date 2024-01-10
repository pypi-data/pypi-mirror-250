from abc import ABC, abstractmethod


class BaseCRUD(ABC):
    """Data Access Layer for operating user info"""

    @abstractmethod
    async def create(self, **kwargs):
        """Create a new record."""
        pass

    @abstractmethod
    async def read(self, **kwargs):
        """Read a record by ID."""
        pass

    @abstractmethod
    async def read_all(self, **kwargs):
        """Read all records."""
        pass

    @abstractmethod
    async def update(self, **kwargs):
        """Update a record by ID."""
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        """Delete a record by ID."""
        pass
