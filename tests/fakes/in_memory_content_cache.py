import copy
from uuid import UUID

from app.application.dto.course_catalog import CourseCatalogCardDTO, CourseCatalogItemDTO
from app.application.dto.course_structure import CoursesStructureDTO
from app.application.interfaces.content_cache import ContentCache


class InMemoryContentCache(ContentCache):
    def __init__(self) -> None:
        self.catalogs: dict[str, list[CourseCatalogItemDTO]] = {}
        self.course_cards: dict[UUID, CourseCatalogCardDTO] = {}
        self.course_structures: dict[UUID, CoursesStructureDTO] = {}

    async def get_catalog(self, key: str) -> list[CourseCatalogItemDTO] | None:
        return copy.deepcopy(self.catalogs.get(key))

    async def set_catalog(self, key: str, value: list[CourseCatalogItemDTO]) -> None:
        self.catalogs[key] = copy.deepcopy(value)

    async def get_course_card(self, course_id: UUID) -> CourseCatalogCardDTO | None:
        return copy.deepcopy(self.course_cards.get(course_id))

    async def set_course_card(self, course_id: UUID, value: CourseCatalogCardDTO) -> None:
        self.course_cards[course_id] = copy.deepcopy(value)

    async def get_course_structure(self, course_id: UUID) -> CoursesStructureDTO | None:
        return copy.deepcopy(self.course_structures.get(course_id))

    async def set_course_structure(self, course_id: UUID, value: CoursesStructureDTO) -> None:
        self.course_structures[course_id] = copy.deepcopy(value)

    async def invalidate_course(self, course_id: UUID) -> None:
        self.course_cards.pop(course_id, None)
        self.course_structures.pop(course_id, None)
        self.catalogs.clear()
