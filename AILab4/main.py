import queue
from collections import deque
from functools import total_ordering
import random


def find_solution(balls):
    n = len(balls)

    pq = queue.PriorityQueue()
    pq.put((clc_priority(balls), balls, []))  # Inital state

    passes = 0

    # To stop adding already generated stated
    visited = set()
    visited.add(tuple(balls))  # Tuple for hashing, list is mutable

    # modified BFS with priority queue
    while not pq.empty():
        current_priority, current_balls, current_swaps = pq.get()  # Pop the state with the lowest priority

        # early return
        if correct_order(current_balls):
            #print(f'Passes: {passes}')
            return current_balls, current_swaps

        # Try all swaps for current state
        for i in range(n - 1):
            # Swap balls
            new_balls = current_balls[:]
            new_balls[i], new_balls[i + 1] = new_balls[i + 1], new_balls[i]

            passes += 1
            # if not visited add to visited states
            if tuple(new_balls) not in visited:
                visited.add(tuple(new_balls))
                # Record the swap and enqueue the new state with its priority
                pq.put((clc_priority(new_balls), new_balls, current_swaps + [(i, i + 1)]))

    #print(f'Passes: {passes}')
    return [], []  # if not found, return something, I hope it won't happen

def clc_priority(list):
    seq_ball_count = len(list) / 3 #ima 3 boja

    curr_count = 1

    total_priority = 1

    for i in range(1, len(list)):
        if list[i] == list[i - 1]: #brojanje sekvencijalnih elemenata
            total_priority -= 1

        if curr_count < seq_ball_count and list[i] != list[i-1]:
            curr_count += 1
            total_priority += 1

        elif curr_count == seq_ball_count:
            curr_count = 1
        else:
           total_priority -= 1

    return total_priority


def correct_order(list):
    seq_ball_count = len(list) / 3 #ima 3 boja

    curr_count = 1

    for i in range(1, len(list)):
        if curr_count < seq_ball_count and list[i] != list[i-1]:
            return False
        elif curr_count == seq_ball_count:
            curr_count = 1
        else:
            curr_count += 1

    return True

def average_path_length(lst, count):
    total_sum = 0
    for _ in range(count):
        random.shuffle(lst)
        total_sum += len(find_solution(lst)[1])

    return total_sum / count


if __name__ == "__main__":

    list =  ['G', 'R', 'B', 'R', 'G', 'B', 'B', 'R', 'G', 'G', 'B', 'R']

    ordered, put = find_solution(list)

    print(ordered)
    print(put)
    print(f'Broj koraka: {len(put)}')

    #print(average_path_length(ordered, 1000))