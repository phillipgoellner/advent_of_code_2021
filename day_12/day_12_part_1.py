from typing import List

from test_dsl import ReadableTestCase


class Cave:
    def __init__(self, cave_string: str):
        self._name = cave_string
        self._is_start = cave_string == 'start'
        self._is_end = cave_string == 'end'
        self._is_big = cave_string.isupper()

        self._connections = set()

    @property
    def name(self):
        return self._name

    @property
    def is_start(self):
        return self._is_start

    @property
    def is_end(self):
        return self._is_end

    @property
    def is_big(self):
        return self._is_big

    @property
    def connections(self):
        return self._connections

    def add_connection(self, other_cave):
        self._connections.add(other_cave)

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return self._name == other.name

    def __str__(self):
        return self._name


class CaveSystem:
    def __init__(self, cave_strings: List[str]):
        self.caves = {}
        for cave_string in cave_strings:
            first_cave, second_cave = tuple(cave_string.split('-'))
            first_cave, second_cave = Cave(first_cave), Cave(second_cave)

            if first_cave.is_start:
                self.start = first_cave
            elif second_cave.is_start:
                self.start = second_cave

            self.add_if_not_exists(first_cave)
            self.add_if_not_exists(second_cave)

            self.add_connection(first_cave, second_cave)

    def add_if_not_exists(self, cave):
        if cave.name not in self.caves:
            self.caves[cave.name] = cave

    def add_connection(self, cave_one, cave_two):
        cave_one: Cave = self.caves[cave_one.name]
        cave_two: Cave = self.caves[cave_two.name]

        cave_one.add_connection(cave_two)
        cave_two.add_connection(cave_one)

    def get_connected_caves(self, cave: Cave):
        return self.caves[cave.name].connections


class Path:
    def __init__(self):
        self.current_cave = None
        self.previous_caves = []

    def add_cave(self, cave_to_add: Cave):
        if self.current_cave is None:
            self.current_cave = cave_to_add
        else:
            self.previous_caves.append(self.current_cave)
            self.current_cave = cave_to_add

    def branch_off(self, new_current_cave: Cave):
        new_path = Path()

        new_path.current_cave = self.current_cave
        new_path.previous_caves = [cave for cave in self.previous_caves]
        new_path.add_cave(new_current_cave)

        return new_path

    def is_valid(self) -> bool:
        return self.current_cave.is_big or self.current_cave not in self.previous_caves

    def __str__(self):
        return ','.join([f'{cave}' for cave in self.previous_caves]) + f',{self.current_cave}'


def get_paths(initial_path, cave_system, path_cache=None):
    if path_cache is None:
        path_cache = []

    if not initial_path.is_valid():
        return []

    if initial_path.current_cave.is_end:
        return [*path_cache, initial_path]

    new_paths = []

    for path in [initial_path.branch_off(cave) for cave in cave_system.get_connected_caves(initial_path.current_cave)]:

        new_paths += get_paths(path, cave_system, path_cache=new_paths)

    return new_paths


def get_number_of_distinct_paths(cave_input_string: str):
    cave_system = CaveSystem(cave_input_string.split('\n'))

    path = Path()
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
        self.expect(actual).to_be(10)

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
        self.expect(actual).to_be(19)

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
        self.expect(actual).to_be(226)

    def test_should_build_a_valid_path(self):
        path = Path()
        path.add_cave(Cave('start'))
        path.add_cave(Cave('A'))
        path.add_cave(Cave('end'))

        self.expect(path.__str__()).to_be('start,A,end')

    def test_get_paths(self):
        cave_system_string = ['start-A', 'A-end']

        cave_system = CaveSystem(cave_system_string)

        path = Path()
        path.add_cave(Cave('start'))
        path.add_cave(Cave('A'))
        path.add_cave(Cave('end'))

        actual = get_paths(path, cave_system)

        self.expect(actual).to_be([path])


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
