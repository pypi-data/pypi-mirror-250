from typing import Any as _Any

from leads import ShadowDevice as _ShadowDevice


class Throttle(_ShadowDevice):
    def read(self) -> _Any:
        pass

    def loop(self) -> None:
        pass
