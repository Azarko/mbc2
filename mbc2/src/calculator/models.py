import dataclasses
import logging
import typing

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Member:
    name: str
    paid: float
    need_to_pay: float = 0

    def calculate(self, each_pay: float) -> None:
        self.need_to_pay = round(each_pay - self.paid, 2)


@dataclasses.dataclass
class Members:
    members: typing.List[Member] = dataclasses.field(default_factory=list)

    @property
    def avg_paid(self) -> float:
        if not self.members:
            return 0
        return round(
            sum(member.paid for member in self.members) / len(self.members),
            2,
        )

    def calculate(self):
        logger.info(f'members before calculations: {self}')
        avg = self.avg_paid
        for member in self.members:
            member.calculate(avg)
        logger.info(f'members after calculations: {self}')
