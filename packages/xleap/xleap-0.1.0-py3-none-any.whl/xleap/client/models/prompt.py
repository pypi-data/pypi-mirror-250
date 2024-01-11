from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Prompt")


@_attrs_define
class Prompt:
    """
    Attributes:
        prompt (str):
        id (Union[Unset, str]):
        version (Union[Unset, int]):
        root (Union[None, Unset, str]):
        parent (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
    """

    prompt: str
    id: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    root: Union[None, Unset, str] = UNSET
    parent: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt = self.prompt

        id = self.id

        version = self.version

        root: Union[None, Unset, str]
        if isinstance(self.root, Unset):
            root = UNSET
        else:
            root = self.root

        parent: Union[None, Unset, str]
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if version is not UNSET:
            field_dict["version"] = version
        if root is not UNSET:
            field_dict["root"] = root
        if parent is not UNSET:
            field_dict["parent"] = parent
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        id = d.pop("id", UNSET)

        version = d.pop("version", UNSET)

        def _parse_root(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        root = _parse_root(d.pop("root", UNSET))

        def _parse_parent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent = _parse_parent(d.pop("parent", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        prompt = cls(
            prompt=prompt,
            id=id,
            version=version,
            root=root,
            parent=parent,
            project=project,
        )

        prompt.additional_properties = d
        return prompt

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
