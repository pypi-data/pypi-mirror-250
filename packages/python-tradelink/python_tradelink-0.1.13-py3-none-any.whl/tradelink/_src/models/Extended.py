from typing import Optional
from pydantic import BaseModel


class ListElement(BaseModel):
    timestamp: int  # Should be converted to the datetime
    value: float


class OrderElement(BaseModel):
    abs: int | float
    rel: int | float


class SymbolElement(BaseModel):
    symbol: str
    volume: dict[str, float]
    pnl: dict[str, float]
    qty: dict[str, int | float]
    direction: dict[str, dict[str, float | int] | Optional[float]]


class FeeStats(BaseModel):
    paid: float
    rebate: float
    total: float
    fundingP: float
    fundingN: float
    fundingNet: float
    volume: float
    refs: float
    wths: float
    deps: float
    stake: float
    unstake: float
    unstakeFee: float
    optionVol: float
    optionFeeN: float
    optionFeeP: float


class User(BaseModel):
    links: list[Optional[dict[str, str]]]
    name: str
    avatar: None | str


class Orders(BaseModel):
    withRealizedPnl: bool
    type: dict[str, OrderElement]
    direction: dict[str, OrderElement | Optional[float]]
    volume: dict[str, float]
    distribution: dict[str, list[OrderElement]]
    symbols: list[Optional[SymbolElement]]


class Extended(BaseModel):
    # Charts
    balances: list[ListElement]
    balancesR: list[ListElement]
    profits: list[ListElement]
    profitsR: list[ListElement]
    monthly: list[ListElement]
    weekly: list[ListElement]
    daily: list[ListElement]
    dailyPnL: list[ListElement]
    indexDaily: list[ListElement]
    indexWeekly: list[ListElement]
    indexMonthly: list[ListElement]
    maxDDHistory: list[ListElement]
    maxDDDHistory: list[ListElement]
    monthDDHistory: list[ListElement]

    icp: list[ListElement]
    longPositions: list[ListElement]
    shortPositions: list[ListElement]
    longPositionsIcp: list[ListElement]
    shortPositionsIcp: list[ListElement]

    lastMonthlyProfit: ListElement
    lastWeeklyProfit: ListElement
    lastDailyProfit: ListElement
    lastMonthlyNetProfit: ListElement
    lastWeeklyNetProfit: ListElement
    lastDailyNetProfit: ListElement

    # Indicators
    feeStat: FeeStats
    weeklyFeeStat: FeeStats
    sourceFor: list[str]
    orders: Orders
    user: User
    tournament: dict[str, bool]

    activeDays: int
    ohr: float
    cagr: float
    trackingDays: int
    tradingDays: int
    maxDD: float
    maxDDDuration: int
    firstTrade: int  # Should be converted to the datetime
    winningDays: int
    losingDays: int
    breakevenDays: int
    winrate: float
    totalProfit: float
    totalLoss: float
    netProfit: float
    lastProfit: float
    lastWeekBalance: float
    lastWeekProfit: float
    lastWeekAverageMonthlyProfit: float
    averageMonthlyProfit: float
    averageDailyProfit: Optional[float]
    averageProfit: float
    averageLoss: float
    profitRatio: Optional[float]
    recoveryFactor: float
    expectedValue: Optional[float]
    kSortino: float
    kSharp: float
    kCalmar: float
    betaRatio: float
    ADL: float
    volatility: float
    rSquared: float
    informationRatio: float
    treynorRatio: float
    sterlingRatio: float
    schwagerRatio: float
    safetyFirstRatio: float
    averageBalance: float
    firstBalance: float
    maxBalance: float
    minBalance: float
    lastBalance: float
    maxIcp: float
    avgIcp: float
    lastMonthGrowth: float
    lastQuarterGrowth: float
    lastYearGrowth: float
    growthRate: float
    VaR: Optional[float]
    maxdddRatio: Optional[float]
    betaRating: Optional[float]
    usedMarkets: int
    totalTrades: int

    # Other
    keyId: str
    stockName: str
    stockNames: list[str]
    accountIds: list[str]
    baseAsset: str
    keyName: str
    keyStatus: bool
    active: bool
    progressPercent: int
    firstValidDataDate: str
    lastValidDataDate: str
    updatedAt: Optional[str]
    startDate: str
    endDate: str
    beginMoment: str
    selfPower: Optional[float]
    selfProfitRate: float
    integralEvaluation: Optional[float]
    riskFreeRate: float
