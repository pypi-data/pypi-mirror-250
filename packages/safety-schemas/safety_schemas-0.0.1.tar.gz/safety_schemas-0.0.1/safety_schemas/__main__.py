from pathlib import Path
import sys

from pydantic import ValidationError
from safety_schemas.models.base import FileType
from .models import ReportSchemaVersion, ReportModel

from .models import ConfigModel, VulnerabilitySeverityLabels, IgnoredItemDetail

if __name__ == "__main__":

    root_path = Path("~/Developments/safety_schemas/")

    PRJ_SCAN = root_path / Path("source-scan.json")
    SYSTEM_SCAN = root_path / Path("source-system-scan.json")

    try:
        report = ReportModel.parse_report(raw_report=SYSTEM_SCAN, 
                                          schema=ReportSchemaVersion.v3_0)
    except ValidationError as e:
        print(f"Wrong report... Reason {e}")
        sys.exit(1)
    
    print([project.id for project in report.projects]) # type: ignore

    print(report.as_v30().json())

    try:
        prj_report = ReportModel.parse_report(raw_report=PRJ_SCAN, 
                                          schema=ReportSchemaVersion.v3_0)
    except ValidationError as e:
        print(f"Wrong report... Reason {e}")
        sys.exit(1)
    
    print([prj.id for prj in prj_report.projects]) # type: ignore    
    
    print(prj_report.as_v30().json())



    # raw["scan"]["ignore"] = ["foo", "bar", "too"]
    # raw["report_on"]["ignore_cvss_severity"] = []
    # raw["report_on"]["ignore_vulnerabilities"] = {"32323": {"reason": "foo", "expires": "bar"}}

    # from ruamel.yaml import YAML

    # default_config = ConfigModel()
    # raw = default_config.as_v30().dict()
    # yaml = YAML(typ='safe', pure=True)
    # yaml.default_flow_style = False
    # yaml.sort_base_mapping_type_on_output = False
    
    # with open("demo-policy.yml", "w") as f:
    #     safety_policy = yaml.dump(raw, f)

    # p = root_path / Path(".safety-policy.yml")
    # # p = Path("~/Developments/safety/.safety-policy-schema-test.yml")

    # p = Path("~/Developments/safety_schemas/source-scan.json")

    # config = ConfigModel.parse_policy_file(p)

    # print(config.scan.max_depth) # type: ignore

    # file_type = FileType("poetry.lock")
    # if not file_type in config.scan.include_files:
    #     config.scan.include_files[file_type] = []

    # config.scan.include_files[file_type].extend([Path("foo"), Path("/absolute/path/to/foo")])

    # config.scan.max_depth = 26
    # config.depedendency_vulnerability.fail_on.cvss_severity.append(VulnerabilitySeverityLabels.LOW)

    # config.save_policy_file(Path("~/Developments/safety/.safety-policy-schema-test.yml"))


    # if config.depedendency_vulnerability.ignore_vulnerabilities:
    #     for k, value in config.depedendency_vulnerability.ignore_vulnerabilities.items():
    #         value.reason = "This needs many chars"