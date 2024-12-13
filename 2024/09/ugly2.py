from dataclasses import dataclass
from itertools import accumulate, islice
from pathlib import Path


FILES = list(map(int, (Path(__file__).parent / "input.txt").read_text().strip()))


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
spaces = [File(0, idx, sz) for idx, sz in zip(space_idxs, FILES[1::2])]

for file in files[::-1]:
    for space in spaces:
        if 0 < file.size <= space.size and space.index < file.index:
            file.index = space.index
            space.size -= file.size
            space.index += file.size
            break

print(sum(f.checksum for f in files))
