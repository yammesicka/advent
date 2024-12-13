from dataclasses import dataclass
from itertools import accumulate, islice
from pathlib import Path


FILES = list(map(int, (Path(__file__).parent / "input.txt").read_text().strip()))
END_OF_FRAGMENT = (None, 0)


@dataclass
class File:
    id: int
    index: int
    size: int

    @property
    def checksum(self):
        return self.id * (self.size * (self.size + self.index * 2 - 1) // 2)


file_idxs = islice(accumulate(FILES, initial=0), None, None, 2)
space_idxs = islice(accumulate(FILES, initial=0), 1, None, 2)

files = [File(fid, idx, sz) for fid, (idx, sz) in enumerate(zip(file_idxs, FILES[::2]))]
spaces = zip(space_idxs, FILES[1::2])

fragmented = []
tail_files = reversed(files)
pointer, free_space = next(spaces, END_OF_FRAGMENT)

while tail_file := next(tail_files, None):
    while 0 <= free_space <= tail_file.size and pointer is not None:
        fragmented.append(File(tail_file.id, pointer, free_space))
        tail_file.size -= free_space
        pointer, free_space = next(spaces, END_OF_FRAGMENT)
    if 0 < tail_file.size <= free_space and pointer is not None and pointer < tail_file.index:
        fragmented.append(File(tail_file.id, pointer, tail_file.size))
        pointer += tail_file.size
        free_space -= tail_file.size
        tail_file.size = 0
    if pointer is None or (pointer is not None and tail_file.index <= pointer):
        break

rest_files = list(tail_files) + ([tail_file] if tail_file else [])
print(sum(f.checksum for f in rest_files + fragmented))
