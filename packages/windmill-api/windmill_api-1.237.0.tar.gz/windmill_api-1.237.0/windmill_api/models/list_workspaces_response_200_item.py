from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListWorkspacesResponse200Item")


@_attrs_define
class ListWorkspacesResponse200Item:
    """
    Attributes:
        id (str):
        name (str):
        owner (str):
        domain (Union[Unset, str]):
    """

    id: str
    name: str
    owner: str
    domain: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        owner = self.owner
        domain = self.domain

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "owner": owner,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        owner = d.pop("owner")

        domain = d.pop("domain", UNSET)

        list_workspaces_response_200_item = cls(
            id=id,
            name=name,
            owner=owner,
            domain=domain,
        )

        list_workspaces_response_200_item.additional_properties = d
        return list_workspaces_response_200_item

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
