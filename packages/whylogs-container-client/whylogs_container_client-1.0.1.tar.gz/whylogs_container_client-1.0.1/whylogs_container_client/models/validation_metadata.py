from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValidationMetadata")


@_attrs_define
class ValidationMetadata:
    """
    Attributes:
        prompt_id (Union[None, Unset, str]):
        validator_name (Union[None, Unset, str]):
        failed_metric (Union[None, Unset, str]):
        value (Union[None, Unset, float, int, str]):
        timestamp (Union[None, Unset, int]):
        is_valid (Union[None, Unset, bool]):
    """

    prompt_id: Union[None, Unset, str] = UNSET
    validator_name: Union[None, Unset, str] = UNSET
    failed_metric: Union[None, Unset, str] = UNSET
    value: Union[None, Unset, float, int, str] = UNSET
    timestamp: Union[None, Unset, int] = UNSET
    is_valid: Union[None, Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt_id: Union[None, Unset, str]
        if isinstance(self.prompt_id, Unset):
            prompt_id = UNSET

        else:
            prompt_id = self.prompt_id

        validator_name: Union[None, Unset, str]
        if isinstance(self.validator_name, Unset):
            validator_name = UNSET

        else:
            validator_name = self.validator_name

        failed_metric: Union[None, Unset, str]
        if isinstance(self.failed_metric, Unset):
            failed_metric = UNSET

        else:
            failed_metric = self.failed_metric

        value: Union[None, Unset, float, int, str]
        if isinstance(self.value, Unset):
            value = UNSET

        else:
            value = self.value

        timestamp: Union[None, Unset, int]
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET

        else:
            timestamp = self.timestamp

        is_valid: Union[None, Unset, bool]
        if isinstance(self.is_valid, Unset):
            is_valid = UNSET

        else:
            is_valid = self.is_valid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if prompt_id is not UNSET:
            field_dict["prompt_id"] = prompt_id
        if validator_name is not UNSET:
            field_dict["validator_name"] = validator_name
        if failed_metric is not UNSET:
            field_dict["failed_metric"] = failed_metric
        if value is not UNSET:
            field_dict["value"] = value
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if is_valid is not UNSET:
            field_dict["is_valid"] = is_valid

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_prompt_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_id = _parse_prompt_id(d.pop("prompt_id", UNSET))

        def _parse_validator_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        validator_name = _parse_validator_name(d.pop("validator_name", UNSET))

        def _parse_failed_metric(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        failed_metric = _parse_failed_metric(d.pop("failed_metric", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, float, int, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float, int, str], data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_timestamp(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        def _parse_is_valid(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_valid = _parse_is_valid(d.pop("is_valid", UNSET))

        validation_metadata = cls(
            prompt_id=prompt_id,
            validator_name=validator_name,
            failed_metric=failed_metric,
            value=value,
            timestamp=timestamp,
            is_valid=is_valid,
        )

        validation_metadata.additional_properties = d
        return validation_metadata

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
