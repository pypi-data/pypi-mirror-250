from plugp100.api.hub.hub_device import HubDevice

from plugp100.common.functional.tri import Try
from plugp100.requests.tapo_request import TapoRequest
from plugp100.requests.trigger_logs_params import GetTriggerLogsParams
from plugp100.responses.components import Components
from plugp100.responses.hub_childs.t100_device_state import (
    T100MotionSensorState,
    T100Event,
    parse_t100_event,
)
from plugp100.responses.hub_childs.trigger_log_response import TriggerLogResponse


class T100MotionSensor:
    def __init__(self, hub: HubDevice, device_id: str):
        self._hub = hub
        self._device_id = device_id

    async def get_device_state(self) -> Try[T100MotionSensorState]:
        return (
            await self._hub.control_child(self._device_id, TapoRequest.get_device_info())
        ).flat_map(T100MotionSensorState.from_json)

    async def get_event_logs(
        self,
        page_size: int,
        start_id: int = 0,
    ) -> Try[TriggerLogResponse[T100Event]]:
        request = TapoRequest.get_child_event_logs(
            GetTriggerLogsParams(page_size, start_id)
        )
        return (await self._hub.control_child(self._device_id, request)).flat_map(
            lambda x: TriggerLogResponse[T100Event].try_from_json(x, parse_t100_event)
        )

    async def get_component_negotiation(self) -> Try[Components]:
        return (
            await self._hub.control_child(
                self._device_id, TapoRequest.component_negotiation()
            )
        ).map(Components.try_from_json)
