import os

import aiofiles

from app.application.exceptions import UploadImageError
from app.application.interfaces.services.image_storage import ImageStorage
from app.infrastructure.config.settings import get_settings


class ImageStorageSaver(ImageStorage):
    def __init__(self) -> None:
        self.settings = get_settings()

    async def save(self, file_name: str, content: bytes) -> str:
        path_dir = self.settings.image.image_cover_dir
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        file_location = os.path.join(path_dir, file_name)

        try:
            async with aiofiles.open(file_location, "wb") as out_file:
                await out_file.write(content)

        except OSError as e:
            if os.path.exists(file_location):
                os.remove(file_location)
            raise UploadImageError('An error occurred while saving the image') from e

        return f'{self.settings.image.image_cover_prefix}/{file_name}'