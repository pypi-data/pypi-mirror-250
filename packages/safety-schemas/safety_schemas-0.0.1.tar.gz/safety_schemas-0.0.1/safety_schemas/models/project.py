from dataclasses import asdict, field
from pathlib import Path
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass
from typing_extensions import Self

from ..report.schemas.v3_0 import main as v3_0
from .base import SafetyBaseModel
from .file import FileModel
from .git import GITModel
from .policy_file import PolicyFileModel


@dataclass
class ProjectModel(SafetyBaseModel):
    id: str
    upload_request_id: Optional[str] = None
    project_path: Optional[Path] = None
    name: Optional[str] = None
    url_path: Optional[str] = None
    policy: Optional[PolicyFileModel] = None
    git: Optional[GITModel] = None
    files: List[FileModel] = field(default_factory=lambda: [])

    def as_v30(self, full: bool = True) -> Union[v3_0.Projects, v3_0.ProjectsScan]:
        kwargs = {"id": self.id, "upload_request_id": self.upload_request_id}
        project_repr = v3_0.Projects

        if full:
            project_repr = v3_0.ProjectsScan
            git_repr = None
            policy = None
            location = None  # Let it fail on the Pydantic side

            if self.project_path:
                location = str(self.project_path.resolve().parent)

            if self.policy:
                policy = self.policy.as_v30()
            if self.git:
                git_repr = v3_0.Git(**asdict(self.git))

            kwargs = {
                "id": self.id,
                "policy": policy,
                "git": git_repr,
                "location": location,
                "files": [f.as_v30() for f in self.files],
            }

        return project_repr(**kwargs)

    @classmethod
    def from_v30(cls, obj: Union[v3_0.Projects, v3_0.ProjectsScan]) -> Self:
        if isinstance(obj, v3_0.ProjectsScan):
            git_model_inst = None

            if obj.git:
                git_model_inst = GITModel(**obj.git.dict())

            return ProjectModel(
                id=obj.id,
                project_path=Path(obj.location),
                upload_request_id=obj.upload_request_id,
                git=git_model_inst,
                files=[FileModel.from_v30(f) for f in obj.files],
            )

        return ProjectModel(id=obj.id, upload_request_id=obj.upload_request_id)
