from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_mock import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleMock,
    )
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_retry import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleRetry,
    )
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_sleep_type_0 import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0,
    )
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_sleep_type_1 import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1,
    )
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_stop_after_if import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleStopAfterIf,
    )
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend,
    )


T = TypeVar("T", bound="GetFlowByPathWithDraftResponse200DraftValueFailureModule")


@_attrs_define
class GetFlowByPathWithDraftResponse200DraftValueFailureModule:
    """
    Attributes:
        id (str):
        value (Any):
        stop_after_if (Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleStopAfterIf]):
        sleep (Union['GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0',
            'GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1', Unset]):
        cache_ttl (Union[Unset, float]):
        timeout (Union[Unset, float]):
        delete_after_use (Union[Unset, bool]):
        summary (Union[Unset, str]):
        mock (Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleMock]):
        suspend (Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend]):
        priority (Union[Unset, float]):
        retry (Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleRetry]):
    """

    id: str
    value: Any
    stop_after_if: Union[Unset, "GetFlowByPathWithDraftResponse200DraftValueFailureModuleStopAfterIf"] = UNSET
    sleep: Union[
        "GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0",
        "GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1",
        Unset,
    ] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    delete_after_use: Union[Unset, bool] = UNSET
    summary: Union[Unset, str] = UNSET
    mock: Union[Unset, "GetFlowByPathWithDraftResponse200DraftValueFailureModuleMock"] = UNSET
    suspend: Union[Unset, "GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend"] = UNSET
    priority: Union[Unset, float] = UNSET
    retry: Union[Unset, "GetFlowByPathWithDraftResponse200DraftValueFailureModuleRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_sleep_type_0 import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0,
        )

        id = self.id
        value = self.value
        stop_after_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_if, Unset):
            stop_after_if = self.stop_after_if.to_dict()

        sleep: Union[Dict[str, Any], Unset]
        if isinstance(self.sleep, Unset):
            sleep = UNSET

        elif isinstance(self.sleep, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0):
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        else:
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        cache_ttl = self.cache_ttl
        timeout = self.timeout
        delete_after_use = self.delete_after_use
        summary = self.summary
        mock: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mock, Unset):
            mock = self.mock.to_dict()

        suspend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suspend, Unset):
            suspend = self.suspend.to_dict()

        priority = self.priority
        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if stop_after_if is not UNSET:
            field_dict["stop_after_if"] = stop_after_if
        if sleep is not UNSET:
            field_dict["sleep"] = sleep
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if delete_after_use is not UNSET:
            field_dict["delete_after_use"] = delete_after_use
        if summary is not UNSET:
            field_dict["summary"] = summary
        if mock is not UNSET:
            field_dict["mock"] = mock
        if suspend is not UNSET:
            field_dict["suspend"] = suspend
        if priority is not UNSET:
            field_dict["priority"] = priority
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_mock import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleMock,
        )
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_retry import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleRetry,
        )
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_sleep_type_0 import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0,
        )
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_sleep_type_1 import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1,
        )
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_stop_after_if import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleStopAfterIf,
        )
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend,
        )

        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = GetFlowByPathWithDraftResponse200DraftValueFailureModuleStopAfterIf.from_dict(
                _stop_after_if
            )

        def _parse_sleep(
            data: object,
        ) -> Union[
            "GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0",
            "GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType0.from_dict(
                        _sleep_type_0
                    )

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = GetFlowByPathWithDraftResponse200DraftValueFailureModuleSleepType1.from_dict(
                    _sleep_type_1
                )

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        timeout = d.pop("timeout", UNSET)

        delete_after_use = d.pop("delete_after_use", UNSET)

        summary = d.pop("summary", UNSET)

        _mock = d.pop("mock", UNSET)
        mock: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleMock]
        if isinstance(_mock, Unset):
            mock = UNSET
        else:
            mock = GetFlowByPathWithDraftResponse200DraftValueFailureModuleMock.from_dict(_mock)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend.from_dict(_suspend)

        priority = d.pop("priority", UNSET)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetFlowByPathWithDraftResponse200DraftValueFailureModuleRetry.from_dict(_retry)

        get_flow_by_path_with_draft_response_200_draft_value_failure_module = cls(
            id=id,
            value=value,
            stop_after_if=stop_after_if,
            sleep=sleep,
            cache_ttl=cache_ttl,
            timeout=timeout,
            delete_after_use=delete_after_use,
            summary=summary,
            mock=mock,
            suspend=suspend,
            priority=priority,
            retry=retry,
        )

        get_flow_by_path_with_draft_response_200_draft_value_failure_module.additional_properties = d
        return get_flow_by_path_with_draft_response_200_draft_value_failure_module

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
