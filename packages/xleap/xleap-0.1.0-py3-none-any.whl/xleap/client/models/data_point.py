from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_point_result_type_0 import DataPointResultType0


T = TypeVar("T", bound="DataPoint")


@_attrs_define
class DataPoint:
    """
    Attributes:
        id (Union[Unset, str]):
        question (Union[None, Unset, str]):
        answer (Union[None, Unset, str]):
        contexts (Union[Unset, List[str]]):
        ground_truths (Union[Unset, List[str]]):
        result (Union['DataPointResultType0', None, Unset]):
        project (Union[None, Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    question: Union[None, Unset, str] = UNSET
    answer: Union[None, Unset, str] = UNSET
    contexts: Union[Unset, List[str]] = UNSET
    ground_truths: Union[Unset, List[str]] = UNSET
    result: Union["DataPointResultType0", None, Unset] = UNSET
    project: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.data_point_result_type_0 import DataPointResultType0

        id = self.id

        question: Union[None, Unset, str]
        if isinstance(self.question, Unset):
            question = UNSET
        else:
            question = self.question

        answer: Union[None, Unset, str]
        if isinstance(self.answer, Unset):
            answer = UNSET
        else:
            answer = self.answer

        contexts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.contexts, Unset):
            contexts = self.contexts

        ground_truths: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ground_truths, Unset):
            ground_truths = self.ground_truths

        result: Union[Dict[str, Any], None, Unset]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, DataPointResultType0):
            result = self.result.to_dict()
        else:
            result = self.result

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if question is not UNSET:
            field_dict["question"] = question
        if answer is not UNSET:
            field_dict["answer"] = answer
        if contexts is not UNSET:
            field_dict["contexts"] = contexts
        if ground_truths is not UNSET:
            field_dict["ground_truths"] = ground_truths
        if result is not UNSET:
            field_dict["result"] = result
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_point_result_type_0 import DataPointResultType0

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        def _parse_question(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        question = _parse_question(d.pop("question", UNSET))

        def _parse_answer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        answer = _parse_answer(d.pop("answer", UNSET))

        contexts = cast(List[str], d.pop("contexts", UNSET))

        ground_truths = cast(List[str], d.pop("ground_truths", UNSET))

        def _parse_result(data: object) -> Union["DataPointResultType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = DataPointResultType0.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DataPointResultType0", None, Unset], data)

        result = _parse_result(d.pop("result", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        data_point = cls(
            id=id,
            question=question,
            answer=answer,
            contexts=contexts,
            ground_truths=ground_truths,
            result=result,
            project=project,
        )

        data_point.additional_properties = d
        return data_point

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
