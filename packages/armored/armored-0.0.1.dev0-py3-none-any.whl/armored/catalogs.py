import re
from typing import (
    Annotated,
    Any,
    Literal,
    Optional,
    Union,
)

from pydantic import (
    Field,
    field_validator,
    model_validator,
)

from .base import BaseUpdatableModel
from .settings import ColumnSetting
from .utils import (
    catch_str,
    only_one,
    split_dtype,
)


class BaseType(BaseUpdatableModel):
    """Base Type"""

    type: Annotated[str, Field(description="Type of implemented data")]


class IntType(BaseUpdatableModel):
    """Integer Type"""

    type: Literal["int", "integer"]

    @field_validator("type", mode="after")
    def prepare_type(cls, _: Literal["int", "integer"]) -> Literal["integer"]:
        return "integer"


class VarcharType(BaseType):
    """Variable Character Type"""

    type: Literal["varchar"]
    max_length: Optional[int] = Field(default=None, le=8000, ge=-1)


class NVarcharType(VarcharType):
    """N Variable Character Type"""

    type: Literal["nvarchar"]


class NumericType(BaseType):
    """Numeric Type"""

    type: Literal["numeric"]
    precision: Optional[int] = Field(default=None, description="")
    scale: Optional[int] = Field(default=None)


class TimestampType(BaseType):
    """Time Type"""

    type: Literal["timestamp"]
    precision: Optional[int] = Field(default=None)
    timezone: bool = Field(default=False, description="Time zone flag")


DTypes = Union[
    VarcharType,
    NVarcharType,
    NumericType,
    TimestampType,
    IntType,
    BaseType,
]


class BaseColumn(BaseUpdatableModel):
    name: Annotated[
        str,
        Field(
            description="Name of Column",
            alias="ColumnName",
        ),
    ]
    dtype: DTypes = Field(union_mode="smart")


class Column(BaseUpdatableModel):
    """Column model"""

    name: Annotated[
        str,
        Field(
            description="Name of Column that match in database",
            alias="ColumnName",
        ),
    ]
    dtype: Annotated[
        Union[dict, str],
        Field(
            description="Data type of value of this column",
            alias="DataType",
        ),
    ]

    # Default value
    nullable: Annotated[
        bool,
        Field(description="Nullable flag", alias="Nullable"),
    ] = True
    unique: Annotated[
        bool,
        Field(
            description="Unique key flag which can contain null value",
            alias="Unique",
        ),
    ] = False
    default: Optional[Union[int, str]] = Field(
        default=None,
        description="Default value of this column",
        alias="Default",
    )
    check: Optional[str] = Field(
        default=None,
        description="Check statement before insert to database",
        alias="Check",
    )

    # Special value that effect to parent model that include this model
    pk: Annotated[
        bool,
        Field(
            description="Primary key flag which can not contain null value",
            alias="PrimaryKey",
        ),
    ] = False
    fk: Annotated[
        dict,
        Field(
            default_factory=dict,
            description="Foreign key reference",
            alias="ForeignKey",
        ),
    ]

    @model_validator(mode="before")
    def prepare_datatype_from_string(cls, values):
        """Prepare datatype value that parsing to this model with different
        types, string or dict type.

        This filter will prepare datatype value from the format,
            {DATATYPE} {UNIQUE} {NULLABLE} {DEFAULT}
            {PRIMARY KEY|FOREIGN KEY} {CHECK}

        Examples:
        - varchar( 100 ) not null default 'O' check( <name> <> 'test' )
        - serial not null primary key
        """
        if not (
            datatype_key := only_one(
                values, ColumnSetting.datatype, default=False
            )
        ):
            raise ValueError("datatype does not contain in values")

        pre_datatype = values.pop(datatype_key)
        if not isinstance(pre_datatype, str):
            raise TypeError(
                f"datatype value does not support for this type, "
                f"{type(pre_datatype)}"
            )

        _datatype, _nullable = split_dtype(pre_datatype)
        values_update: dict[str, Any] = {"nullable": False}

        # Remove unique value from datatype
        _datatype, values_update["unique"] = catch_str(_datatype, key="unique")

        # Remove primary key value from datatype
        _datatype, values_update["pk"] = catch_str(_datatype, key="primary key")

        # Rename serial value to int from datatype
        _datatype, _ = catch_str(_datatype, key="serial", replace="int")

        # Check for check value
        if "check" in _datatype:
            if m := re.search(
                r"check\s?\((?P<check>[^()]*(?:\(.*\))*[^()]*)\)",
                _datatype,
            ):
                _datatype, values_update["check"] = catch_str(
                    _datatype, m.group(), flag=False
                )
            else:
                raise ValueError(
                    "datatype with type string does not support for "
                    "this format of check"
                )

        if re.search("default", _datatype):
            values["datatype"] = _datatype.split("default")[0].strip()
        else:
            values["datatype"] = _datatype
            values_update["nullable"] = not re.search("not null", _nullable)

        return values_update | values

    @field_validator("name")
    def prepare_name(cls, value) -> str:
        """Prepare name"""
        return "".join(value.strip().split())

    @model_validator(mode="after")
    def validate_and_check_logic_values(self):
        """Validate and check logic of values"""
        pk: bool = self.pk
        nullable: bool = self.nullable

        # primary key and nullable does not True together
        if pk and nullable:
            raise ValueError("pk and nullable can not be True together")
        return self
