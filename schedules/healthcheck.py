from core.implementations.schedule import BaseSchedule


class HealthcheckSchedule(BaseSchedule):
    delay_seconds = 300

    async def execute(self) -> None:
        self.client.logger.info("[schedule] healthcheck tick")
