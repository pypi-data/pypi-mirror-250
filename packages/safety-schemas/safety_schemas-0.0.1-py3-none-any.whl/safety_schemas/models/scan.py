import importlib
from dataclasses import field
from pathlib import Path
from typing import List, Union

from pydantic import ValidationError, validator
from pydantic.dataclasses import dataclass
from typing_extensions import Self

from ..report.schemas.v3_0 import main as v3_0
from .base import ReportSchemaVersion, SafetyBaseModel, ScanType
from .file import FileModel
from .metadata import MetadataModel
from .project import ProjectModel
from .telemetry import TelemetryModel


@dataclass
class ReportModel(SafetyBaseModel):
    """
    Used as an entrypoint to keep backwards compatibility with old formats.
    Use this model if you want to generate a standard JSON report.
    """

    DEFAULT_SCHEMA_VERSION = ReportSchemaVersion.v3_0

    telemetry: TelemetryModel
    metadata: MetadataModel
    files: List[FileModel]
    projects: List[ProjectModel] = field(default_factory=lambda: [])
    version: ReportSchemaVersion = DEFAULT_SCHEMA_VERSION

    @validator("version", pre=True, always=True)
    def validate_version(cls, version: ReportSchemaVersion) -> ReportSchemaVersion:
        versions = list(ReportSchemaVersion)
        if version not in (versions):
            raise ValueError(f"Invalid version, allowed versions are {versions}")
        return version

    def as_v30(self) -> v3_0.Report:
        full = self.metadata.scan_type is ScanType.scan
        results = v3_0.ScanResults(
            files=[f.as_v30() for f in self.files],
            projects=[p.as_v30(full=full) for p in self.projects],
        )  # type: ignore

        report = v3_0.Report(meta=self.metadata.as_v30(), scan_results=results)

        return report

    @classmethod
    def from_v30(cls, obj: v3_0.Report) -> Self:
        return ReportModel(
            version=ReportSchemaVersion(obj.meta.schema_version),
            telemetry=TelemetryModel.from_v30(obj.meta.telemetry),
            metadata=MetadataModel.from_v30(obj.meta),
            projects=[ProjectModel.from_v30(p) for p in obj.scan_results.projects],
            files=[FileModel.from_v30(f) for f in obj.scan_results.files],
        )

    @classmethod
    def parse_report(
        cls, raw_report: Union[str, Path], schema: ReportSchemaVersion
    ) -> Union[Self, ValidationError]:
        parse = "parse_raw"

        if isinstance(raw_report, Path):
            raw_report = raw_report.expanduser().resolve()
            parse = "parse_file"

        target_schema = schema.value.replace(".", "_")
        module_name = "safety_schemas.report.schemas." f"v{target_schema}.main"

        module = importlib.import_module(module_name)
        report_model = module.Report

        # This will raise a validation error if the content is wrong
        validated_report = getattr(report_model, parse)(raw_report)

        # TODO: Select the from from the version passed
        return ReportModel.from_v30(obj=validated_report)
