import pathlib


class BingoBoard:
    BOARD_SIZE = 5

    def __init__(self, raw_board: str):
        self.board = raw_board.strip().split()
        self.numbers = set(self.board)
        self.found = set([])
        self.columns_score = [0] * self.BOARD_SIZE
        self.rows_score = [0] * self.BOARD_SIZE

    def draw(self, number: str):
        if number not in self.numbers:
            return

        self.found.add(number)
        where = self.board.index(number)
        row, col = divmod(where, 5)
        self.rows_score[row] += 1
        self.columns_score[col] += 1
        if (
            self.rows_score[row] == self.BOARD_SIZE or
            self.columns_score[col] == self.BOARD_SIZE
        ):
            sum_of_found = sum(map(int, self.found))
            sum_of_all = sum(map(int, self.numbers))
            return int(number) * (sum_of_all - sum_of_found)


def parse_bingo(path: pathlib.Path):
    numbers, *boards = path.read_text().split('\n\n')
    return numbers.strip().split(','), boards


# Part 1
def play_bingo(numbers: list[str], boards: list[BingoBoard]):
    for number in numbers:
        for board in boards:
            if winner_score := board.draw(number):
                return winner_score


# Part 2
def play_bingo(numbers: list[str], boards: list[BingoBoard]):
    is_board_won = [False] * len(boards)
    winner_score = None
    winners = 0

    for number in numbers:
        for i, board in enumerate(boards):
            if not is_board_won[i] and (winner_score := board.draw(number)):
                winners += 1
                is_board_won[i] = True
                if winners == len(boards):
                    return winner_score

    # If not all the boards win, return the last winner
    return winner_score


numbers, raw_boards = parse_bingo(pathlib.Path('input.txt'))
boards = [BingoBoard(board) for board in raw_boards]
print(play_bingo(numbers, boards))
