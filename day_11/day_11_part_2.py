from day_11.conf import input_energy_levels
from day_11.day_11_part_1 import one_step


def get_first_step_synchronized(octopuses, steps):
    for step in range(steps):
        octopuses, flashes = one_step(octopuses)
        if flashes == 100:
            return step + 1
    return 0


if __name__ == "__main__":
    print(get_first_step_synchronized(input_energy_levels, 100000))
