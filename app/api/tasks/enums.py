from enum import StrEnum


class TaskPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class TaskType(StrEnum):
    HOMEWORK = "homework"
    LABWORK = "labwork"
    PRACTICIWORK = "particiwork"
    GENERAL = "general"
