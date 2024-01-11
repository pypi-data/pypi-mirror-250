from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_create_events_type_0 import RunCreateEventsType0
    from ..models.run_create_extra_type_0 import RunCreateExtraType0
    from ..models.run_create_inputs_type_0 import RunCreateInputsType0
    from ..models.run_create_outputs_type_0 import RunCreateOutputsType0
    from ..models.run_create_serialized_type_0 import RunCreateSerializedType0


T = TypeVar("T", bound="RunCreate")


@_attrs_define
class RunCreate:
    """
    Attributes:
        start_time (str):
        id (Union[Unset, str]):
        session_name (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        reference_example_id (Union[None, Unset, str]):
        end_time (Union[None, Unset, str]):
        extra (Union['RunCreateExtraType0', None, Unset]):
        events (Union['RunCreateEventsType0', None, Unset]):
        outputs (Union['RunCreateOutputsType0', None, Unset]):
        serialized (Union['RunCreateSerializedType0', None, Unset]):
        inputs (Union['RunCreateInputsType0', None, Unset]):
        error (Union[None, Unset, str]):
        run_type (Union[None, Unset, str]):
        execution_order (Union[None, Unset, int]):
        child_execution_order (Union[None, Unset, str]):
        parent_run_id (Union[None, Unset, str]):
    """

    start_time: str
    id: Union[Unset, str] = UNSET
    session_name: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    reference_example_id: Union[None, Unset, str] = UNSET
    end_time: Union[None, Unset, str] = UNSET
    extra: Union["RunCreateExtraType0", None, Unset] = UNSET
    events: Union["RunCreateEventsType0", None, Unset] = UNSET
    outputs: Union["RunCreateOutputsType0", None, Unset] = UNSET
    serialized: Union["RunCreateSerializedType0", None, Unset] = UNSET
    inputs: Union["RunCreateInputsType0", None, Unset] = UNSET
    error: Union[None, Unset, str] = UNSET
    run_type: Union[None, Unset, str] = UNSET
    execution_order: Union[None, Unset, int] = UNSET
    child_execution_order: Union[None, Unset, str] = UNSET
    parent_run_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.run_create_events_type_0 import RunCreateEventsType0
        from ..models.run_create_extra_type_0 import RunCreateExtraType0
        from ..models.run_create_inputs_type_0 import RunCreateInputsType0
        from ..models.run_create_outputs_type_0 import RunCreateOutputsType0
        from ..models.run_create_serialized_type_0 import RunCreateSerializedType0

        start_time = self.start_time

        id = self.id

        session_name: Union[None, Unset, str]
        if isinstance(self.session_name, Unset):
            session_name = UNSET
        else:
            session_name = self.session_name

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        reference_example_id: Union[None, Unset, str]
        if isinstance(self.reference_example_id, Unset):
            reference_example_id = UNSET
        else:
            reference_example_id = self.reference_example_id

        end_time: Union[None, Unset, str]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        else:
            end_time = self.end_time

        extra: Union[Dict[str, Any], None, Unset]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, RunCreateExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        events: Union[Dict[str, Any], None, Unset]
        if isinstance(self.events, Unset):
            events = UNSET
        elif isinstance(self.events, RunCreateEventsType0):
            events = self.events.to_dict()
        else:
            events = self.events

        outputs: Union[Dict[str, Any], None, Unset]
        if isinstance(self.outputs, Unset):
            outputs = UNSET
        elif isinstance(self.outputs, RunCreateOutputsType0):
            outputs = self.outputs.to_dict()
        else:
            outputs = self.outputs

        serialized: Union[Dict[str, Any], None, Unset]
        if isinstance(self.serialized, Unset):
            serialized = UNSET
        elif isinstance(self.serialized, RunCreateSerializedType0):
            serialized = self.serialized.to_dict()
        else:
            serialized = self.serialized

        inputs: Union[Dict[str, Any], None, Unset]
        if isinstance(self.inputs, Unset):
            inputs = UNSET
        elif isinstance(self.inputs, RunCreateInputsType0):
            inputs = self.inputs.to_dict()
        else:
            inputs = self.inputs

        error: Union[None, Unset, str]
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        run_type: Union[None, Unset, str]
        if isinstance(self.run_type, Unset):
            run_type = UNSET
        else:
            run_type = self.run_type

        execution_order: Union[None, Unset, int]
        if isinstance(self.execution_order, Unset):
            execution_order = UNSET
        else:
            execution_order = self.execution_order

        child_execution_order: Union[None, Unset, str]
        if isinstance(self.child_execution_order, Unset):
            child_execution_order = UNSET
        else:
            child_execution_order = self.child_execution_order

        parent_run_id: Union[None, Unset, str]
        if isinstance(self.parent_run_id, Unset):
            parent_run_id = UNSET
        else:
            parent_run_id = self.parent_run_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if session_name is not UNSET:
            field_dict["session_name"] = session_name
        if name is not UNSET:
            field_dict["name"] = name
        if reference_example_id is not UNSET:
            field_dict["reference_example_id"] = reference_example_id
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if extra is not UNSET:
            field_dict["extra"] = extra
        if events is not UNSET:
            field_dict["events"] = events
        if outputs is not UNSET:
            field_dict["outputs"] = outputs
        if serialized is not UNSET:
            field_dict["serialized"] = serialized
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if error is not UNSET:
            field_dict["error"] = error
        if run_type is not UNSET:
            field_dict["run_type"] = run_type
        if execution_order is not UNSET:
            field_dict["execution_order"] = execution_order
        if child_execution_order is not UNSET:
            field_dict["child_execution_order"] = child_execution_order
        if parent_run_id is not UNSET:
            field_dict["parent_run_id"] = parent_run_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_create_events_type_0 import RunCreateEventsType0
        from ..models.run_create_extra_type_0 import RunCreateExtraType0
        from ..models.run_create_inputs_type_0 import RunCreateInputsType0
        from ..models.run_create_outputs_type_0 import RunCreateOutputsType0
        from ..models.run_create_serialized_type_0 import RunCreateSerializedType0

        d = src_dict.copy()
        start_time = d.pop("start_time")

        id = d.pop("id", UNSET)

        def _parse_session_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        session_name = _parse_session_name(d.pop("session_name", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_reference_example_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        reference_example_id = _parse_reference_example_id(
            d.pop("reference_example_id", UNSET)
        )

        def _parse_end_time(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_extra(data: object) -> Union["RunCreateExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = RunCreateExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunCreateExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        def _parse_events(data: object) -> Union["RunCreateEventsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                events_type_0 = RunCreateEventsType0.from_dict(data)

                return events_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunCreateEventsType0", None, Unset], data)

        events = _parse_events(d.pop("events", UNSET))

        def _parse_outputs(data: object) -> Union["RunCreateOutputsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                outputs_type_0 = RunCreateOutputsType0.from_dict(data)

                return outputs_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunCreateOutputsType0", None, Unset], data)

        outputs = _parse_outputs(d.pop("outputs", UNSET))

        def _parse_serialized(
            data: object,
        ) -> Union["RunCreateSerializedType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                serialized_type_0 = RunCreateSerializedType0.from_dict(data)

                return serialized_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunCreateSerializedType0", None, Unset], data)

        serialized = _parse_serialized(d.pop("serialized", UNSET))

        def _parse_inputs(data: object) -> Union["RunCreateInputsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                inputs_type_0 = RunCreateInputsType0.from_dict(data)

                return inputs_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunCreateInputsType0", None, Unset], data)

        inputs = _parse_inputs(d.pop("inputs", UNSET))

        def _parse_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_run_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        run_type = _parse_run_type(d.pop("run_type", UNSET))

        def _parse_execution_order(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        execution_order = _parse_execution_order(d.pop("execution_order", UNSET))

        def _parse_child_execution_order(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        child_execution_order = _parse_child_execution_order(
            d.pop("child_execution_order", UNSET)
        )

        def _parse_parent_run_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_run_id = _parse_parent_run_id(d.pop("parent_run_id", UNSET))

        run_create = cls(
            start_time=start_time,
            id=id,
            session_name=session_name,
            name=name,
            reference_example_id=reference_example_id,
            end_time=end_time,
            extra=extra,
            events=events,
            outputs=outputs,
            serialized=serialized,
            inputs=inputs,
            error=error,
            run_type=run_type,
            execution_order=execution_order,
            child_execution_order=child_execution_order,
            parent_run_id=parent_run_id,
        )

        run_create.additional_properties = d
        return run_create

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
