import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import (
    BaseModel,
    Extra,
    Field,
    PositiveInt,
    StrictBool,
    conlist,
    constr,
    validator,
)
from typing_extensions import Annotated


class SchemaModelV30(BaseModel):
    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True


class CVSSSeverityLabels(Enum):
    UNKNOWN = "unknown"
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EPSSExploitabilityLabels(Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityUpdatesLimits(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


class AllowedFileType(Enum):
    REQUIREMENTS_TXT = "requirements.txt"
    POETRY_LOCK = "poetry.lock"
    PIPENV_LOCK = "Pipfile.lock"


class PythonEcosystemSettings(SchemaModelV30):
    ignore_environment_results: Annotated[
        Optional[StrictBool], Field(alias="environment-results")
    ] = True
    ignore_unpinned_requirements: Annotated[
        Optional[StrictBool], Field(alias="unpinned-requirements")
    ] = True


class IgnoredVulnerability(SchemaModelV30):
    reason: Annotated[
        constr(
            strip_whitespace=True, strict=True, min_length=10, max_length=255
        ),  # type: ignore
        Field(),
    ]
    expires: Annotated[datetime.date, Field()]
    specifications: Optional[List[str]]


class AutoIgnoreInReportDependencyVulnerabilities(SchemaModelV30):
    python: Annotated[
        Optional[PythonEcosystemSettings], Field()
    ] = PythonEcosystemSettings()
    vulnerabilities: Annotated[
        Optional[Dict[str, IgnoredVulnerability]], Field(alias="vulnerabilities")
    ] = {}
    cvss_severity: Annotated[
        Optional[conlist(CVSSSeverityLabels, unique_items=True)],  # type: ignore
        Field(alias="cvss-severity"),
    ] = []


class ReportDependencyVulnerabilities(SchemaModelV30):
    enabled: Annotated[Optional[StrictBool], Field()] = True
    auto_ignore: Annotated[
        Optional[AutoIgnoreInReportDependencyVulnerabilities],
        Field(alias="auto-ignore-in-report"),
    ] = AutoIgnoreInReportDependencyVulnerabilities()


## FailScan


class FailOnAnyOf(SchemaModelV30):
    cvss_severity: Annotated[
        conlist(CVSSSeverityLabels, unique_items=True),  # type: ignore
        Field(alias="cvss-severity"),
    ] = [
        CVSSSeverityLabels.CRITICAL,
        CVSSSeverityLabels.HIGH,
        CVSSSeverityLabels.MEDIUM,
    ]
    exploitability: Annotated[
        conlist(EPSSExploitabilityLabels, unique_items=True), Field()  # type: ignore
    ] = [
        EPSSExploitabilityLabels.CRITICAL,
        EPSSExploitabilityLabels.HIGH,
        EPSSExploitabilityLabels.MEDIUM,
    ]


class FailScanDependencyVulnerabilities(SchemaModelV30):
    enabled: Annotated[Optional[StrictBool], Field()] = True
    fail_on_any_of: Annotated[
        Optional[FailOnAnyOf], Field(alias="fail-on-any-of")
    ] = FailOnAnyOf()


class SecurityUpdatesDependencyVulnerabilities(SchemaModelV30):
    auto_security_updates_limit: Annotated[
        Optional[conlist(SecurityUpdatesLimits, min_items=1)],  # type: ignore
        Field(alias="auto-security-updates-limit"),
    ] = [SecurityUpdatesLimits.PATCH]


class System(SchemaModelV30):
    targets: Annotated[
        List[constr(strip_whitespace=True, strict=True, min_length=1)], 
        Field()
        ] = ["/"]

class IncludeFile(SchemaModelV30):
    path: Annotated[
        constr(strip_whitespace=True, strict=True, min_length=1),
        Field()
    ]
    file_type: Annotated[AllowedFileType, 
        Field(alias="file-type")]


# Main sections

class ScanSettings(SchemaModelV30):
    max_depth: Annotated[Optional[PositiveInt], Field(alias="max-depth")] = 6
    exclude: Annotated[
        Optional[
            List[constr(strip_whitespace=True, strict=True, min_length=1)]
        ],  # type: ignore
        Field(),
    ]
    include_files: Annotated[
        Optional[List[IncludeFile]], 
        Field(alias="include-files")
    ] = []
    system: Annotated[Optional[System], Field()] = System()


class Report(SchemaModelV30):
    dependency_vulnerabilities: Annotated[
        Optional[ReportDependencyVulnerabilities],
        Field(alias="dependency-vulnerabilities"),
    ]


class FailScan(SchemaModelV30):
    dependency_vulnerabilities: Annotated[
        Optional[FailScanDependencyVulnerabilities],
        Field(alias="dependency-vulnerabilities"),
    ]


class SecurityUpdatesSettings(SchemaModelV30):
    dependency_vulnerabilities: Annotated[
        Optional[SecurityUpdatesDependencyVulnerabilities],
        Field(alias="dependency-vulnerabilities"),
    ]


class Config(SchemaModelV30):
    version: Annotated[Optional[str], Field()] = "3.0"
    scan: Annotated[Optional[ScanSettings], Field(alias="scanning-settings")]
    report: Annotated[Optional[Report], Field()]
    fail_scan: Annotated[Optional[FailScan], Field(alias="fail-scan-with-exit-code")]
    security_updates: Annotated[
        Optional[SecurityUpdatesSettings], Field(alias="security-updates")
    ]

    @validator("version")
    def version_must_be_valid(cls, v):
        if v not in ["3.0", "3"]:
            raise ValueError("Wrong version value.")

        return v
