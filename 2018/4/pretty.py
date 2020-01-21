import collections
import functools
import re
from typing import Dict, Iterator, List, Optional, Tuple


def get_input() -> Iterator[int]:
    with open('input.txt', 'r') as challenge_input:
        yield from map(str.strip, challenge_input)


class Guard:
    def __init__(self) -> None:
        self.histogram = [0] * 60
        self.total_sleep = 0
        self.is_awake = True
        self.start_sleeping = None

    def sleep(self, minute: int) -> None:
        self.is_awake = False
        self.start_sleeping = minute
    
    def wakeup(self, current_minute: int) -> None:
        for minute in range(self.start_sleeping, current_minute):
            self.histogram[minute] += 1
        self.total_sleep += current_minute - self.start_sleeping
        self.is_awake = True
    
    @functools.lru_cache(maxsize=1)  # Python 3.8: @functools.cached_property
    def get_best_minute(self) -> None:
        return self.histogram.index(max(self.histogram))


LOG_LINE = re.compile(
    r"\["
    r"(?P<year>\d{4})-"
    r"(?P<month>\d{2})-"
    r"(?P<day>\d{2})\s*"
    r"(?P<hour>\d{2}):"
    r"(?P<minute>\d{2})"
    r"\]\s*?"
    r"(?:Guard #(?P<guard_id>\d+))?\s+"
    r"(?P<message>wakes up|falls asleep|begins shift)"
)
    

def is_input_valid(input_lines: List[str]) -> None:
    # Test:  assert is_input_valid(sorted(get_input()))
    only_datetimes = [line[:18] for line in input_lines]
    return len(set(only_datetimes)) == len(only_datetimes)


def parse_line(line: str) -> Tuple[int, Optional[int], str]:
    parsed_line = LOG_LINE.match(line).groupdict()
    guard_id = parsed_line.get('guard_id'),
    return (
        int(parsed_line['minute']),
        int(guard_id[0]) if guard_id[0] is not None else None,
        parsed_line['message']
    )


def get_guards_from_log(logfile: List[str]) -> Dict[int, Guard]:
    guards = collections.defaultdict(Guard)
    for line in sorted(logfile):
        minute, guard_id, message = parse_line(line)
        if message == "begins shift":
            current_guard = guards[guard_id]
        if message == "falls asleep":
            current_guard.sleep(minute)
        if message == "wakes up":
            current_guard.wakeup(minute)
    return guards


# Part A
def get_sleepiest_guard_id(guards: Dict[int, Guard]) -> int:
    max_sleeping_hours = 0
    for guard_id, guard in guards.items():
        if max_sleeping_hours < guard.total_sleep:
            sleepiest_guard_id = guard_id
            max_sleeping_hours = guard.total_sleep
    return sleepiest_guard_id


def get_strategy_a_answer(guards: int) -> int:
    sleepiest_guard = get_sleepiest_guard_id(guards)
    sleeped_most_during = guards[sleepiest_guard].get_best_minute()
    return sleeped_most_during * sleepiest_guard


guards = get_guards_from_log(get_input())
print(get_strategy_a_answer(guards))


# Part B
def get_strategy_b_answer(guards: Dict[int, Guard]) -> int:
    max_occurrences = 0
    for guard_id, guard in guards.items():
        max_guard_sleeped = guard.histogram[guard.get_best_minute()]
        if max_occurrences < max_guard_sleeped:
            sleepiest_guard_id = guard_id
            max_occurrences = max_guard_sleeped
    return sleepiest_guard_id * guards[sleepiest_guard_id].get_best_minute()
    

print(get_strategy_b_answer(guards))