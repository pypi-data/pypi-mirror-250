from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Generator, Optional, Union


class RunMode(Enum):
    CONTINUOUS = "continuous"
    DURATION = "duration"


@dataclass
class JobTime:
    """Contains information about the job runtime."""

    run_mode: RunMode
    start: datetime
    end: Optional[datetime]
    duration: Optional[timedelta]
    current_time: Optional[datetime] = field(default=None, init=False)
    _last_hibernate_time: Optional[datetime] = field(default=None)

    @staticmethod
    def from_document(
        job_data: dict[str, Any], last_hibernate_time: Optional[datetime]
    ) -> "JobTime":
        run_settings: dict[str, Any] = job_data["runSettings"]
        run_mode = RunMode(run_settings["runMode"])
        start = datetime.fromisoformat(run_settings["startDate"])
        end = (
            datetime.fromisoformat(run_settings["endDate"])
            if run_settings.get("endDate") is not None
            else None
        )
        return JobTime(
            run_mode=run_mode,
            start=start,
            end=end,
            duration=None if end is None else end - start,
            _last_hibernate_time=last_hibernate_time,
        )

    def range(
        self, step: Union[timedelta, float] = 1.0, start: Optional[datetime] = None
    ) -> Generator[datetime, None, None]:
        """Range over the runtime of the job, from :attr:`start` to :attr:`end`,
        inclusive. If :attr:`end` is not defined, range forever. If the job is resumed
        from hibernation, the start time will be the job time before hibernation.

        :param step: The step in time between yielded time value. If it is a `float` it
            is interpreted as seconds.
        :param start: If specified, it is used instead of the job start time.
        """
        if self.current_time is not None:
            raise RuntimeError("You can only range over job time once")

        step_ = step if isinstance(step, timedelta) else timedelta(seconds=step)
        if start is not None:
            self.current_time = start
        elif self._last_hibernate_time is not None:
            self.current_time = self._last_hibernate_time
        else:
            self.current_time = self.start

        while self.end is None or self.current_time <= self.end:
            yield self.current_time
            self.current_time += step_
