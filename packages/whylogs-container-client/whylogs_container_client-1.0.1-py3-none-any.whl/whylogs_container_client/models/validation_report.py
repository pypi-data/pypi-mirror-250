from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.validation_metadata import ValidationMetadata


T = TypeVar("T", bound="ValidationReport")


@_attrs_define
class ValidationReport:
    """
    Attributes:
        failures (List['ValidationMetadata']):
    """

    failures: List["ValidationMetadata"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        failures = []
        for failures_item_data in self.failures:
            failures_item = failures_item_data.to_dict()

            failures.append(failures_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failures": failures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.validation_metadata import ValidationMetadata

        d = src_dict.copy()
        failures = []
        _failures = d.pop("failures")
        for failures_item_data in _failures:
            failures_item = ValidationMetadata.from_dict(failures_item_data)

            failures.append(failures_item)

        validation_report = cls(
            failures=failures,
        )

        validation_report.additional_properties = d
        return validation_report

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
