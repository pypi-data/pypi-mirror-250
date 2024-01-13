from datetime import datetime, timedelta
from logging import Logger
from typing import (
    Any,
    Awaitable,
    Callable,
    Optional,
    ParamSpec,
    TypeVar,
)

from pydantic import ValidationError
from tradelink._src.Requester import Requester
from tradelink._src.errors.TradeLinkAPIResponseError import (
    TradeLinkAPIResponseError,
)
from tradelink._src.utils.logging import get_logger
from tradelink._src.models.Portfolio import (
    PortfolioModel,
    TradeLinkStep,
)
from functools import wraps


T = TypeVar("T")
P = ParamSpec("P")


class Portfolio:
    id: str
    step: TradeLinkStep
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    requester: Requester

    cached_portfolio: PortfolioModel
    cache_updated_at: Optional[datetime] = None

    time_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

    _logger: Logger

    def __init__(
        self,
        _id: str,
        step: TradeLinkStep = TradeLinkStep.day,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        self.id = _id
        self.step = step
        self.start_date = start_date
        self.end_date = end_date
        self.requester = Requester()
        self._logger = get_logger(__name__)

    @staticmethod
    def _portfolio_method(
        func: Callable[[Any], Awaitable[T]]
    ) -> Callable[[Any], Awaitable[T]]:
        @wraps(func)
        async def wrapper(
            self: "Portfolio", *args: P.args, **kwargs: P.kwargs
        ) -> T:
            if not self.cache_updated_at:
                await self.update_info()
            else:
                if (
                    self.cache_updated_at
                    and datetime.utcnow() - self.cache_updated_at
                    > timedelta(hours=1)
                ):
                    await self.update_info()

            return await func(self, *args, **kwargs)

        return wrapper

    async def update_info(self) -> "Portfolio":
        self._logger.debug(f"Started updating portfolio {self.id}")
        try:
            response = await self.requester.get_portfolio(
                self.id,
                step=self.step,
                start_date=self.start_date,
                end_date=self.end_date,
            )
        except (ValidationError, ValueError) as e:
            self._logger.error(f"Failed to update info of portfolio {self.id}")
            self._logger.error(f"Validation error. {e}")
            raise TradeLinkAPIResponseError(
                f"API response didn't pass the validation. Most certainly this is the problem of the library"
            )

        if isinstance(response, str):
            self._logger.error(f"Failed to update info of portfolio {self.id}")
            return self

        self.cached_portfolio = response
        self.cache_updated_at = datetime.utcnow()

        self._logger.info(f"Succesfully updated portfolio {self.id}")
        return self

    @_portfolio_method
    async def get_total_return(self) -> float:
        """In percents"""
        return self.cached_portfolio.extended.lastProfit * 100

    @_portfolio_method
    async def get_total_volume(self) -> float:
        """Absolute value"""
        return self.cached_portfolio.extended.feeStat.volume

    @_portfolio_method
    async def get_last_valid_data_date(self) -> datetime:
        return datetime.strptime(
            self.cached_portfolio.extended.lastValidDataDate, self.time_format
        )

    @_portfolio_method
    async def get_start_date(self) -> datetime:
        return datetime.strptime(
            self.cached_portfolio.extended.startDate, self.time_format
        )

    @_portfolio_method
    async def get_end_date(self) -> datetime:
        return datetime.strptime(
            self.cached_portfolio.extended.endDate, self.time_format
        )

    @_portfolio_method
    async def get_unrpnl_deposit_of_the_first_point(self) -> float:
        """Absolute unrealized value"""
        if (
            self.cached_portfolio.extended.balances
            and self.cached_portfolio.extended.profits
            and self.cached_portfolio.extended.balances[0]
            and self.cached_portfolio.extended.profits[0]
        ):
            return self.cached_portfolio.extended.balances[0].value / (
                1 + self.cached_portfolio.extended.profits[0].value
            )
        else:
            return 0

    @_portfolio_method
    async def get_total_deposits(self) -> float:
        """Absolute value"""
        return self.cached_portfolio.extended.feeStat.deps

    @_portfolio_method
    async def get_total_withdraws(self) -> float:
        """Absolute value"""
        return self.cached_portfolio.extended.feeStat.wths

    @_portfolio_method
    async def get_unrpnl_last_balance(self) -> float:
        """Absolute value"""
        if (
            self.cached_portfolio.extended.balances
            and self.cached_portfolio.extended.balances[0]
        ):
            return self.cached_portfolio.extended.balances[-1].value
        else:
            return 0

    @_portfolio_method
    async def get_unrpnl_last_netpnl(self) -> float:
        """Absolute value"""
        return sum([x.value for x in self.cached_portfolio.extended.dailyPnL])  # type: ignore
