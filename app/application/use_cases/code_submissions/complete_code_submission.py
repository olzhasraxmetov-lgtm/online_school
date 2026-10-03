from dataclasses import dataclass
from uuid import UUID, uuid4

from app.domain.entities import Progress, StudentActivity, StudentActivityType
from app.domain.entities.execution_result import ExecutionStatus


@dataclass(slots=True)
class CompleteCodeSubmissionCommand:
    submission_id: UUID
    status: ExecutionStatus
    passed_test_cases: int = 0
    total_test_cases: int = 0
    stdout: str = ''
    stderr: str = ''
    error_message: str = ''
    exit_code: int | None = None

from app.application.exceptions import CodeSubmissionNotFoundError, CodeTaskNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.student_activity_service import StudentActivityService
from app.domain.entities.execution_result import ExecutionResult


class CompleteCodeSubmissionUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.student_activity_service = StudentActivityService(uow)

    async def execute(self, command: CompleteCodeSubmissionCommand):
        async with self.uow:
            submission = await self.uow.code_submissions.get_by_id(command.submission_id)
            if submission is None:
                raise CodeSubmissionNotFoundError('CodeSubmission not found.')

            result = ExecutionResult(
                submission_id=submission.id,
                status=command.status,
                passed_test_cases=command.passed_test_cases,
                total_test_cases=command.total_test_cases,
                stdout=command.stdout,
                stderr=command.stderr,
                error_message=command.error_message,
                exit_code=command.exit_code,
            )

            if submission.status == 'pending':
                submission.mark_running()

            submission.apply_execution_result(result)
            await self.uow.code_submissions.update(submission)

            if result.status.value == 'passed':
                code_task = await self.uow.code_tasks.get_by_id(submission.code_task_id)
                if code_task is None:
                    raise CodeTaskNotFoundError('CodeTask not found.')

                section = await self.uow.sections.get_by_id(code_task.section_id)
                if section is None:
                    raise CodeTaskNotFoundError('CodeTask not found.')

                module = await self.uow.modules.get_by_id(section.module_id)
                if module is None:
                    raise CodeTaskNotFoundError('CodeTask not found.')

                progress = await self.uow.progress.get_by_student_and_course(
                    student_id=submission.student_id,
                    course_id=module.course_id,
                )

                progress_is_new = progress is None
                if progress is None:
                    progress = Progress(
                        id=uuid4(),
                        student_id=submission.student_id,
                        course_id=module.course_id,
                    )

                progress_changed = progress.complete_code_task(
                    code_task.id,
                    code_task.reward_points,
                )
                if progress_changed:
                    await self.uow.student_activities.add(
                        StudentActivity(
                            id=uuid4(),
                            student_id=submission.student_id,
                            course_id=module.course_id,
                            activity_type=StudentActivityType.CODE_TASK_COMPLETED,
                            entity_id=code_task.id,
                            title=code_task.title,
                            details={
                                'awarded_points': code_task.reward_points,
                                'attempt_number': submission.attempt_number,
                            },
                        )
                    )

                    await self.student_activity_service.record_structure_completion(
                        progress=progress,
                        section=section,
                        module=module,
                        student_id=submission.student_id,
                    )

                    if progress_is_new:
                        await self.uow.progress.add(progress)
                    else:
                        await self.uow.progress.update(progress)
            await self.uow.commit()
            return submission