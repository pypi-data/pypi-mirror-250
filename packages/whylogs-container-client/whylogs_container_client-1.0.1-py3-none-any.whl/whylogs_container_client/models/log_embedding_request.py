from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.log_embedding_request_embeddings import LogEmbeddingRequestEmbeddings


T = TypeVar("T", bound="LogEmbeddingRequest")


@_attrs_define
class LogEmbeddingRequest:
    """
    Attributes:
        timestamp (int):
        embeddings (LogEmbeddingRequestEmbeddings):
        dataset_id (Union[Unset, str]):
    """

    timestamp: int
    embeddings: "LogEmbeddingRequestEmbeddings"
    dataset_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp
        embeddings = self.embeddings.to_dict()

        dataset_id = self.dataset_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "embeddings": embeddings,
            }
        )
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_embedding_request_embeddings import LogEmbeddingRequestEmbeddings

        d = src_dict.copy()
        timestamp = d.pop("timestamp")

        embeddings = LogEmbeddingRequestEmbeddings.from_dict(d.pop("embeddings"))

        dataset_id = d.pop("dataset_id", UNSET)

        log_embedding_request = cls(
            timestamp=timestamp,
            embeddings=embeddings,
            dataset_id=dataset_id,
        )

        log_embedding_request.additional_properties = d
        return log_embedding_request

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
