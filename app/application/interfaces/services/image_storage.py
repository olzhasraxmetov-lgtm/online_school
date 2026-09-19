from abc import abstractmethod, ABC


class ImageStorage(ABC):
    @abstractmethod
    async def save(self, file_name: str, content: bytes) -> str:
        raise NotImplementedError