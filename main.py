import random

from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, Generator


@dataclass()
class Genotype:
    genes: str

    def __post_init__(self):
        if len(self.genes) % 2 == 1:
            raise ValueError("Only accepts pairs of alleles, was passed an odd number of s.")
        for pair in self.pairs:
            if pair.lower()[0] != pair.lower()[1]:
                raise ValueError(f"Each corresponding allele pair letter must be the same, Ex. Aa, hh, ZZ. Got {pair}")

    @property
    def pairs(self):
        temp = ""
        for i, char in enumerate(self.genes):
            temp += char
            if i % 2 == 1:
                yield temp
                temp = ""

    def crossing_combos(self, *args: Tuple[str]) -> Generator[str, None, None]:
        if len(args) > 0:
            gene, *args = args
            for allele in gene:
                for other_alleles in self.crossing_combos(*args):
                    yield allele + other_alleles
        else:
            yield from [""]
    
    def __mul__(self, other: "Genotype") -> "Probability[Genotype]":
        return Probability((*map(Genotype, self.cross_options(other)),))

    def cross_options(self, other: "Genotype") -> Generator[str, None, None]:
        for y_combo in self.crossing_combos(*self.pairs):
            for x_combo in self.crossing_combos(*other.pairs):
                yield self.cross_alleles(x_combo, y_combo)

    def cross_alleles(self, x_allele: str, y_allele: str) -> str:
        if len(x_allele) != len(y_allele):
            raise ValueError(f"Both allele combination must be of the same length. Got {x_allele} and {y_allele}")
        combos = ""
        for a, b in zip(x_allele, y_allele):
            combos += "".join(sorted(a + b))
        return combos
        

@dataclass()
class Probability:
    _options: Tuple[Genotype]

    def resolve(self) -> Genotype:
        return random.choice(self._options)

    def probabilities(self):
        table = defaultdict(int)
        for option in self._options:
            table[option.genes] += 1
        for key in table:
            table[key] /= len(self._options)
        return dict(table)

if __name__ == "__main__"
    a = Genotype("BbCcDdMmNn")
    b = Genotype("BbCcddMmNn")
    
    print((a * b).probabilities())