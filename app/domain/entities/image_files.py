from dataclasses import dataclass, field

from app.domain.exceptions import InvalidCoverImageError


@dataclass(slots=True)
class ImageCover:
    content_type: str
    content: bytes = field(repr=False)

    MAX_COVER_IMAGE_SIZE = 5 * 1024 * 1024

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.content) <= 0:
            raise InvalidCoverImageError('Image content cannot be empty')
        if len(self.content) > self.MAX_COVER_IMAGE_SIZE:
            raise InvalidCoverImageError(
                f'Image size must be less than {self.MAX_COVER_IMAGE_SIZE // (1024 * 1024)} MB, '
                f'got {len(self.content) / (1024 * 1024):.1f} MB'
            )
        if self.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
            raise InvalidCoverImageError('Image extension must be PNG, JPG or WEBP')

    @property
    def extension(self) -> str:
        return {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/webp': '.webp',
        }[self.content_type]