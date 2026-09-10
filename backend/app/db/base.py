from sqlmodel import SQLModel

Base = SQLModel  # models inherit from this

from app.models.user import User  # noqa: E402, F401
from app.models.coach_student import CoachStudent  # noqa: E402, F401
from app.models.sport import Sport  # noqa: E402, F401
from app.models.skill import Skill  # noqa: E402, F401
from app.models.drill import Drill  # noqa: E402, F401
from app.models.training_plan import TrainingPlan  # noqa: E402, F401
from app.models.training_assignment import TrainingAssignment  # noqa: E402, F401
from app.models.student_skill_progress import StudentSkillProgress  # noqa: E402, F401
from app.models.practice_evidence import PracticeEvidence  # noqa: E402, F401
from app.models.embedding import DrillEmbedding, SkillEmbedding  # noqa: E402, F401
