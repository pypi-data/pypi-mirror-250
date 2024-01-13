from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from datetime import date
from enum import Enum
from functools import cached_property, reduce
from typing import ClassVar, Self, cast, overload

from dateutil.relativedelta import relativedelta
from isoweek import Week
from parsy import ParseError

from dbnomics_data_model.model.errors.periods import PeriodParseError
from dbnomics_data_model.model.periods.formatters import format_month_num, format_week_num, format_year_num

__all__ = [
    "BimesterPeriod",
    "DayPeriod",
    "MonthPeriod",
    "Period",
    "QuarterPeriod",
    "SemesterPeriod",
    "WeekPeriod",
    "YearPeriod",
]


class PeriodType(Enum):
    """Type of the period assigned to each Period sub-class instance in order to identify serialized values."""

    BIMESTER = "bimester"
    DAY = "day"
    MONTH = "month"
    QUARTER = "quarter"
    SEMESTER = "semester"
    WEEK = "week"
    YEAR = "year"


@dataclass(frozen=True, order=True)
class Period(ABC):
    type_: ClassVar[PeriodType]

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            period = cast(Self, parsers.period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return period

    def __add__(self, increment: int) -> Self:
        return reduce(lambda period, _: period.next if increment > 0 else period.previous, range(abs(increment)), self)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @overload
    def __sub__(self, other: int) -> Self:
        pass

    @overload
    def __sub__(self, other: Self) -> int:
        pass

    def __sub__(self, other: int | Self) -> Self | int:
        if isinstance(other, int):
            return self + (-other)

        if self.type_ != other.type_:
            msg = f"Can't substract {type(other)!r} from {type(self)!r}"
            raise TypeError(msg)

        return self._ordinal_difference(other)

    @abstractproperty
    def first_day(self) -> date:
        pass

    @abstractproperty
    def next(self) -> Self:
        pass

    @abstractproperty
    def previous(self) -> Self:
        pass

    @abstractmethod
    def _ordinal_difference(self, other: Self) -> int:
        pass


@dataclass(frozen=True, order=True)
class BimesterPeriod(Period):
    """A period of 2 consecutive months."""

    year_num: int
    bimester_num: int

    def __post_init__(self) -> None:
        if self.bimester_num < self.min_bimester_num or self.bimester_num > self.max_bimester_num:
            msg = f"bimester_num must be between {self.min_bimester_num} and {self.max_bimester_num}"
            raise ValueError(msg)

    max_bimester_num: ClassVar[int] = 6
    min_bimester_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.BIMESTER

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            bimester_period = cast(Self, parsers.bimester_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return bimester_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-B{self.bimester_num}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.first_month_num, 1)

    @property
    def first_month_num(self) -> int:
        return self.bimester_num * 2 - 1

    @property
    def next(self) -> Self:
        new_bimester_num = self.bimester_num + 1
        new_year_num = self.year_num
        if new_bimester_num > self.max_bimester_num:
            new_bimester_num = self.min_bimester_num
            new_year_num += 1
        return self.__class__(new_year_num, new_bimester_num)

    @property
    def previous(self) -> Self:
        new_bimester_num = self.bimester_num - 1
        new_year_num = self.year_num
        if new_bimester_num < self.min_bimester_num:
            new_bimester_num = self.max_bimester_num
            new_year_num -= 1
        return self.__class__(new_year_num, new_bimester_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        month_ordinal = delta.years * 12 + delta.months
        return month_ordinal // 2


@dataclass(frozen=True, order=True)
class DayPeriod(Period):
    year_num: int
    month_num: int
    day_num: int

    type_: ClassVar[PeriodType] = PeriodType.DAY

    def __post_init__(self) -> None:
        # Check that date is constructible.
        self.first_day  # noqa: B018

    @classmethod
    def from_date(cls, value: date) -> Self:
        return cls(value.year, value.month, value.day)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            day_period = cast(Self, parsers.day_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return day_period

    def __str__(self) -> str:
        return self.first_day.isoformat()

    @cached_property
    def first_day(self) -> date:
        return date(self.year_num, self.month_num, self.day_num)

    @property
    def next(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(days=1)
        return self.__class__.from_date(new_period_first_day)

    @property
    def previous(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(days=-1)
        return self.__class__.from_date(new_period_first_day)

    def _ordinal_difference(self, other: Self) -> int:
        return self.first_day.toordinal() - other.first_day.toordinal()


@dataclass(frozen=True, order=True)
class MonthPeriod(Period):
    year_num: int
    month_num: int

    max_month_num: ClassVar[int] = 12
    min_month_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.MONTH

    def __post_init__(self) -> None:
        if self.month_num < self.min_month_num or self.month_num > self.max_month_num:
            msg = f"month_num must be between {self.min_month_num} and {self.max_month_num}"
            raise ValueError(msg)

    @classmethod
    def from_date(cls, value: date) -> Self:
        return cls(value.year, value.month)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            month_period = cast(Self, parsers.month_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return month_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-{format_month_num(self.month_num)}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.month_num, self.min_month_num)

    @property
    def next(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(months=1)
        return self.__class__.from_date(new_period_first_day)

    @property
    def previous(self) -> Self:
        new_period_first_day = self.first_day + relativedelta(months=-1)
        return self.__class__.from_date(new_period_first_day)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        return delta.years * 12 + delta.months


@dataclass(frozen=True, order=True)
class QuarterPeriod(Period):
    """A period of 3 consecutive months."""

    year_num: int
    quarter_num: int

    max_quarter_num: ClassVar[int] = 4
    min_quarter_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.QUARTER

    def __post_init__(self) -> None:
        if self.quarter_num < self.min_quarter_num or self.quarter_num > self.max_quarter_num:
            msg = f"quarter_num must be between {self.min_quarter_num} and {self.max_quarter_num}"
            raise ValueError(msg)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            quarter_period = cast(Self, parsers.quarter_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return quarter_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-Q{self.quarter_num}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.first_month_num, 1)

    @property
    def first_month_num(self) -> int:
        return self.quarter_num * 3 - 2

    @property
    def next(self) -> Self:
        new_quarter_num = self.quarter_num + 1
        new_year_num = self.year_num
        if new_quarter_num > self.max_quarter_num:
            new_quarter_num = self.min_quarter_num
            new_year_num += 1
        return self.__class__(new_year_num, new_quarter_num)

    @property
    def previous(self) -> Self:
        new_quarter_num = self.quarter_num - 1
        new_year_num = self.year_num
        if new_quarter_num < self.min_quarter_num:
            new_quarter_num = self.max_quarter_num
            new_year_num -= 1
        return self.__class__(new_year_num, new_quarter_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        month_ordinal = delta.years * 12 + delta.months
        return month_ordinal // 3


@dataclass(frozen=True, order=True)
class SemesterPeriod(Period):
    """A period of 6 consecutive months."""

    year_num: int
    semester_num: int

    max_semester_num: ClassVar[int] = 2
    min_semester_num: ClassVar[int] = 1
    type_: ClassVar[PeriodType] = PeriodType.SEMESTER

    def __post_init__(self) -> None:
        if self.semester_num < self.min_semester_num or self.semester_num > self.max_semester_num:
            msg = f"semester_num must be between {self.min_semester_num} and {self.max_semester_num}"
            raise ValueError(msg)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            semester_period = cast(Self, parsers.semester_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return semester_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-S{self.semester_num}"

    @property
    def first_day(self) -> date:
        return date(self.year_num, self.first_month_num, 1)

    @property
    def first_month_num(self) -> int:
        return self.semester_num * 6 - 5

    @property
    def next(self) -> Self:
        new_semester_num = self.semester_num + 1
        new_year_num = self.year_num
        if new_semester_num > self.max_semester_num:
            new_semester_num = self.min_semester_num
            new_year_num += 1
        return self.__class__(new_year_num, new_semester_num)

    @property
    def previous(self) -> Self:
        new_semester_num = self.semester_num - 1
        new_year_num = self.year_num
        if new_semester_num < self.min_semester_num:
            new_semester_num = self.max_semester_num
            new_year_num -= 1
        return self.__class__(new_year_num, new_semester_num)

    def _ordinal_difference(self, other: Self) -> int:
        delta = relativedelta(self.first_day, other.first_day)
        month_ordinal = delta.years * 12 + delta.months
        return month_ordinal // 6


@dataclass(frozen=True, order=True)
class WeekPeriod(Period):
    year_num: int
    week_num: int

    type_: ClassVar[PeriodType] = PeriodType.WEEK

    def __post_init__(self) -> None:
        # Check that week is constructible.
        self._week  # noqa: B018

    @classmethod
    def from_week(cls, value: Week) -> Self:
        return cls(value.year, value.week)

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            week_period = cast(Self, parsers.week_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return week_period

    def __str__(self) -> str:
        return f"{format_year_num(self.year_num)}-W{format_week_num(self.week_num)}"

    @property
    def first_day(self) -> date:
        return cast(date, self._week.monday())

    @property
    def next(self) -> Self:
        new_week = cast(Week, self._week + 1)
        return self.__class__.from_week(new_week)

    @property
    def previous(self) -> Self:
        new_week = cast(Week, self._week - 1)
        return self.__class__.from_week(new_week)

    def _ordinal_difference(self, other: Self) -> int:
        return cast(int, self._week - other._week)  # noqa: SLF001

    @cached_property
    def _week(self) -> Week:
        return Week(self.year_num, self.week_num)


@dataclass(frozen=True, order=True)
class YearPeriod(Period):
    year_num: int

    type_: ClassVar[PeriodType] = PeriodType.YEAR

    def __post_init__(self) -> None:
        # Check that date is constructible.
        self.first_day  # noqa: B018

    @classmethod
    def parse(cls, value: str) -> Self:
        from . import parsers

        try:
            year_period = cast(Self, parsers.year_period.parse(value))
        except ParseError as exc:
            raise PeriodParseError(period_raw=value) from exc

        return year_period

    def __str__(self) -> str:
        return str(self.year_num)

    @property
    def first_day(self) -> date:
        return date(self.year_num, 1, 1)

    @property
    def next(self) -> Self:
        return self.__class__(self.year_num + 1)

    @property
    def previous(self) -> Self:
        return self.__class__(self.year_num - 1)

    def _ordinal_difference(self, other: Self) -> int:
        return self.year_num - other.year_num
