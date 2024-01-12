from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_multiple import LogMultiple


T = TypeVar("T", bound="LogRequest")


@_attrs_define
class LogRequest:
    """
    Attributes:
        multiple (LogMultiple):
        dataset_id (Union[Unset, str]):
        timestamp (Union[None, Unset, int]):
    """

    multiple: "LogMultiple"
    dataset_id: Union[Unset, str] = UNSET
    timestamp: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        multiple = self.multiple.to_dict()

        dataset_id = self.dataset_id
        timestamp: Union[None, Unset, int]
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET

        else:
            timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "multiple": multiple,
            }
        )
        if dataset_id is not UNSET:
            field_dict["datasetId"] = dataset_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_multiple import LogMultiple

        d = src_dict.copy()
        multiple = LogMultiple.from_dict(d.pop("multiple"))

        dataset_id = d.pop("datasetId", UNSET)

        def _parse_timestamp(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        log_request = cls(
            multiple=multiple,
            dataset_id=dataset_id,
            timestamp=timestamp,
        )

        log_request.additional_properties = d
        return log_request

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
