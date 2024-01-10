from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class DataSource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    s3_url: str
    metadata: Optional[dict[str, Any]]


class ExecutionResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    result: dict[str, DataSource]


class Operation(BaseModel):
    """Formalized `Instruction`."""

    input: list[str]
    output: list[str]
    command: str
    args: dict[str, Any]

    @field_validator("input")
    @classmethod
    def validate_input_length(cls, val: list) -> list:
        if len(val) < 1:
            raise ValueError(f"input must have at least one  item.")
        return val

    @field_validator("output")
    @classmethod
    def validate_output_length(cls, val: list) -> list:
        if len(val) != 1:
            raise ValueError(f"Tablegpt-operator must be one and only one output.")
        return val


class SingleOperation(BaseModel):
    data_sources: Optional[Dict[str, DataSource]] = None
    operation: Operation


class BatchOperation(BaseModel):
    """Formalized `Instruction`."""

    data_sources: Optional[Dict[str, DataSource]] = None
    operations: list[Operation]

    @field_validator("operations")
    @classmethod
    def validate_operations_length(cls, val: list) -> list:
        if len(val) < 1:
            raise ValueError(f"operations must have at least one 'operation' item.")
        return val
