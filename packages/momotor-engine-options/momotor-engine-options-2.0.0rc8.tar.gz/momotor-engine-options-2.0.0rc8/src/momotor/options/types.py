import typing

from typing_extensions import TypeAlias  # Python 3.10+


StepTasksType: TypeAlias = tuple[int, ...]
StepTaskNumberType: TypeAlias = typing.Optional[tuple[int, ...]]

OptionTypeLiteral: TypeAlias = typing.Literal['string', 'boolean', 'integer', 'float']
OptionDeprecatedTypeLiteral: TypeAlias = typing.Literal['str', 'bool', 'int']
LocationLiteral: TypeAlias = typing.Literal['step', 'recipe', 'config', 'product']

SubDomainDefinitionType: TypeAlias = dict[
    LocationLiteral,
    typing.Union[str, typing.Sequence[typing.Optional[str]], None]
]
