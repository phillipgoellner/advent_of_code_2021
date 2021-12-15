from day_12.day_12_part_1 import CaveSystem, Path, get_paths, Cave
from test_dsl import ReadableTestCase


class SmallTwicePath(Path):
    def __init__(self):
        super().__init__()
        self.has_small_cave_twice = False

    def branch_off(self, new_current_cave: Cave):
        new_path = SmallTwicePath()

        new_path.current_cave = self.current_cave
        new_path.previous_caves = [cave for cave in self.previous_caves]
        new_path.add_cave(new_current_cave)
        new_path.has_small_cave_twice = self.has_small_cave_twice

        return new_path

    def is_valid(self) -> bool:
        if self.current_cave.is_big or self.current_cave not in self.previous_caves:
            return True

        if self.current_cave.is_start and len(self.previous_caves) != 0:
            return False

        if self.has_small_cave_twice:
            return False

        self.has_small_cave_twice = True
        return True


def get_number_of_distinct_paths(cave_input_string: str):
    cave_system = CaveSystem(cave_input_string.split('\n'))

    path = SmallTwicePath()
    path.add_cave(cave_system.start)

    distinct_caves = set([path for path in get_paths(path, cave_system)])

    return len(distinct_caves)


class CavePathTest(ReadableTestCase):
    def setUp(self) -> None:
        self.cave_system_string = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
        self.cave_system = CaveSystem(self.cave_system_string.split('\n'))

    def test_calculate_number_of_distinct_paths(self):
        actual = get_number_of_distinct_paths(self.cave_system_string)
        self.expect(actual).to_be(36)

    def test_calculate_number_of_distinct_paths_medium(self):
        actual = get_number_of_distinct_paths("""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""")
        self.expect(actual).to_be(103)

    def test_calculate_number_of_distinct_paths_large(self):
        actual = get_number_of_distinct_paths("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""")
        self.expect(actual).to_be(3509)


if __name__ == "__main__":
    print(get_number_of_distinct_paths("""YW-end
DK-la
la-XG
end-gy
zq-ci
XG-gz
TF-la
xm-la
gy-gz
ci-start
YW-ci
TF-zq
ci-DK
la-TS
zq-YW
gz-YW
zq-gz
end-gz
ci-TF
DK-zq
gy-YW
start-DK
gz-DK
zq-la
start-TF"""))
