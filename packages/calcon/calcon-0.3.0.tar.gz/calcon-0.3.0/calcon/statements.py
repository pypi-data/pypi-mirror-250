"""Module which contains the statement classes."""


from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional

from calcon.app import App
from calcon.expressions import Expression


@dataclass
class Statement:
    """Base class for all Statement classes."""

    @abstractmethod
    def execute(self, app: App, /) -> None:
        """Executes this statement in the context of the app."""


@dataclass
class DefineRootSymbolAliases(Statement):
    """Represents a statement which defines a root unit and its aliases. (For
    now, the symbol is treated as an alias.)"""

    unit: str
    symbol_alias: Optional[str]
    aliases: list[str]
    dimension: str

    def execute(self, app: App, /) -> None:
        app.define_root_unit(self.unit, self.dimension)
        if self.symbol_alias is not None:
            app.define_core_unit_symbol_alias(self.symbol_alias, self.unit)
        for alias in self.aliases:
            app.define_core_unit_alias(alias, self.unit)


@dataclass
class DefineDerivedSymbolAliases(Statement):
    """Represents a statement which defines a derived unit, its symbol alias,
    and its aliases."""

    unit: str
    symbol_alias: Optional[str]
    aliases: list[str]
    value: Expression

    def execute(self, app: App, /) -> None:
        app.define_derived_core_unit(self.unit, self.value.evaluate(app))
        if self.symbol_alias is not None:
            app.define_core_unit_symbol_alias(self.symbol_alias, self.unit)
        for alias in self.aliases:
            app.define_core_unit_alias(alias, self.unit)


@dataclass
class DefinePrefixSymbolAliases(Statement):
    """Represents a statement which defines a prefix, its symbol, and its
    aliases."""

    prefix: str
    symbol_alias: Optional[str]
    aliases: list[str]
    value: Expression

    def execute(self, app: App, /) -> None:
        app.define_canonical_prefix(self.prefix, self.value.evaluate(app))
        if self.symbol_alias is not None:
            app.define_prefix_symbol_alias(self.symbol_alias, self.prefix)
        for alias in self.aliases:
            app.define_prefix_alias(alias, self.prefix)
