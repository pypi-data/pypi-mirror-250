from dataclasses import dataclass
from typing import Any

from .parameter import Parameter, get_parameters_dict


@dataclass
class Project:
    id: str
    name: str
    parameters: dict[str, Parameter]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Project":
        return Project(
            id=data["id"],
            name=data["name"],
            parameters=get_parameters_dict(data.get("parameters", [])),
        )
