import itertools
import pathlib
from typing import TypeAlias

Shape: TypeAlias = str
WinStatus: TypeAlias = str

RPS = Rock, Paper, Scissors = "RPS"
WLD = Win, Lose, Draw = "WLD"
shape = dict(zip("ABCXYZ", (*RPS, *RPS), strict=True))
shape_scoring = dict(zip(RPS, (1, 2, 3), strict=True))
win_scoring = dict(zip(WLD, (6, 0, 3), strict=True))
FirstWinOverTheSecond = ((Rock, Scissors), (Scissors, Paper), (Paper, Rock))

# For second part
strategies = dict(zip("ZXY", WLD, strict=True))
worst_choice_against = dict(FirstWinOverTheSecond)
best_choice_against = {v: k for k, v in worst_choice_against.items()}


def round_outcome(me: Shape, opponent: Shape) -> WinStatus:
    if me == opponent:
        return Draw

    elif (me, opponent) in FirstWinOverTheSecond:
        return Win
    elif (opponent, me) in FirstWinOverTheSecond:
        return Lose

    assert False, "There should be no round like ({me=}, {opponent=})"


def get_score(me: Shape, opponent: Shape) -> int:
    game_score = win_scoring[round_outcome(me, opponent)]
    shape_score = shape_scoring[me]
    return game_score + shape_score


def tournament(f: pathlib.Path):
    rounds = (line.split() for line in f.read_text().splitlines())
    shape_choices = ((shape[me], shape[op]) for op, me in rounds)
    return sum(get_score(*round_) for round_ in shape_choices)


def choose_shape(opponent: Shape, strategy: WinStatus) -> Shape:
    if strategy == Draw:
        return opponent
    elif strategy == Win:
        return best_choice_against[opponent]
    elif strategy == Lose:
        return worst_choice_against[opponent]

    assert False, "There should be no round like ({opponent=}, {strategy=})"


def tournament_2(f: pathlib.Path):
    rounds = (line.split() for line in f.read_text().splitlines())
    secrets = ((shape[op], strategies[strategy]) for op, strategy in rounds)
    choices = ((choose_shape(op, strategy), op) for op, strategy in secrets)
    return sum(itertools.starmap(get_score, choices))


if __name__ == '__main__':
    file = pathlib.Path(__file__).parent / 'input.txt'
    print(f"Part 1: {tournament(file)}")
    print(f"Part 2: {tournament_2(file)}")
