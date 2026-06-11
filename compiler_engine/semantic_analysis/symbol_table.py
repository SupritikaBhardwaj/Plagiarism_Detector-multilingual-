from dataclasses import dataclass, field
import re


@dataclass
class Symbol:
    name: str
    kind: str
    scope: str


@dataclass
class SymbolTable:
    symbols: list[Symbol] = field(default_factory=list)


class SymbolTableBuilder:
    def build(self, source: str) -> SymbolTable:
        table = SymbolTable()
        for match in re.finditer(r"\b(def|function|class)\s+([A-Za-z_]\w*)", source):
            table.symbols.append(Symbol(match.group(2), match.group(1), "global"))
        for match in re.finditer(r"\b([A-Za-z_]\w*)\s*=", source):
            table.symbols.append(Symbol(match.group(1), "variable", "local"))
        return table

