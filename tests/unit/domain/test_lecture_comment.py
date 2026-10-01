from uuid import uuid4

import pytest

from app.domain.entities.lecture_comment import LectureComment
from app.domain.exceptions import InvalidLectureCommentError


def test_lecture_comment_raises_error_when_text_is_empty() -> None:
    with pytest.raises(InvalidLectureCommentError):
        LectureComment(
            id=uuid4(),
            lecture_id=uuid4(),
            user_id=uuid4(),
            text='',
        )

def test_lecture_comment_raises_error_when_text_len_is_invalid() -> None:
    with pytest.raises(InvalidLectureCommentError):
        LectureComment(
            id=uuid4(),
            lecture_id=uuid4(),
            user_id=uuid4(),
            text='*' * 2001,
        )

def test_ensure_lecture_comment_text_remove_spaces() -> None:
    lecture_comment = LectureComment(
        id=uuid4(),
        lecture_id=uuid4(),
        user_id=uuid4(),
        text=' Basic lecture comment ' ,
    )

    assert lecture_comment.text == 'Basic lecture comment'

def test_lecture_comment_ensure_update_text_and_updated_at() -> None:
    lecture_comment = LectureComment(
        id=uuid4(),
        lecture_id=uuid4(),
        user_id=uuid4(),
        text='Basic lecture comment',
    )

    lecture_comment.update(
        text='New basic lecture comment',
    )

    assert lecture_comment.text == 'New basic lecture comment'
    assert lecture_comment.updated_at is not None