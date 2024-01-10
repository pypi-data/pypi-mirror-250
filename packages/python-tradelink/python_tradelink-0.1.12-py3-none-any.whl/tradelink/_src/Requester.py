from logging import Logger
from typing import Any
import aiohttp
from pydantic import ValidationError
from tradelink._src.models.RequestTypes import (
    RequestTypes,
    RequestMethod,
)
from tradelink._src.models.Portfolio import (
    PortfolioModel,
    TradeLinkStep,
)
from tradelink._src.utils.logging import get_logger
from tradelink._src.models.ApiResponse import ApiResponse
from datetime import datetime


class Requester:
    base_url: str
    _logger: Logger

    def __init__(self, base_url: str = "api.tradelink.pro") -> None:
        self.base_url = base_url
        self._logger = get_logger(__name__)

    async def get_portfolio(
        self,
        portfolioId: str,
        *, 
        step: TradeLinkStep = TradeLinkStep.day,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> str | PortfolioModel:
        request_args = {
            "portfolioId": portfolioId,
            "extended": "1",
            "step": step.value,
            "lang": "en",
        }

        if start_date:
            request_args["startDate"] = await self._format_datetime(start_date)
        if end_date:
            request_args["endDate"] = await self._format_datetime(end_date)

        request_path = await self._generate_request_link(
            RequestTypes.portfolio,
            RequestMethod.get,
            request_args=request_args,
        )
        response = await self._request(
            RequestMethod.get,
            request_path,
        )
        return (
            "Error"
            if isinstance(response, str)
            else PortfolioModel(**response)
        )

    @staticmethod
    async def _format_datetime(date_to_format: datetime) -> str:
        return (
            f"{date_to_format.year}-"
            f"{str(date_to_format.month).zfill(2)}-"
            f"{str(date_to_format.day).zfill(2)}"
        )

    async def _generate_request_link(
        self,
        request_type: RequestTypes,
        request_method: RequestMethod,
        connection_type: str = "https",
        **kwargs: dict[str, str],
    ) -> str:
        request_path: str = (
            f"{connection_type}://{self.base_url}/"
            + f"{request_type.value}/{request_method.value}?"
        )
        request_path += "&".join(
            [
                f"{key}={value}"
                for key, value in zip(
                    kwargs.get("request_args", {}).keys(),
                    kwargs.get("request_args", {}).values(),
                )
            ]
        )
        self._logger.debug(f"Generated request link {request_path}")
        return request_path

    async def _request(
        self,
        request_method: RequestMethod,
        request_path: str,
    ) -> str | dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            match request_method.value:
                case RequestMethod.get.value:
                    self._logger.debug(
                        f"Sent {RequestMethod.get.value.upper()} to {request_path}"
                    )
                    async with session.get(request_path) as response:
                        response_json = await response.json(content_type=None)
                        try:
                            data: ApiResponse = ApiResponse(
                                **response_json
                            )
                        except ValidationError:
                            self._logger.error(
                                f"Wrong response from the "
                                f"TradeLink API. {response_json if len(str(response_json)) < 1000 else ''}"
                            )
                            raise ValueError("Wrong TradeLink response")
                case RequestMethod.post.value:
                    self._logger.debug(
                        f"Sent {RequestMethod.get.value.upper()} to {request_path}"
                    )
                    async with session.post(request_path) as response:
                        response_json = await response.json(content_type=None)
                        try:
                            data = ApiResponse(**response_json)
                        except ValueError:
                            self._logger.error(
                                f"Wrong response from the "
                                f"TradeLink API. {response_json if len(str(response_json)) < 1000 else ''}"
                            )
                            raise ValidationError("Wrong TradeLink response")

            if data.code != 200:
                self._logger.error(
                    f"Response code from {request_path} is not 200"
                )
                self._logger.error(f"The error is {data.error}")
                return str(data.error)

            return data.data
