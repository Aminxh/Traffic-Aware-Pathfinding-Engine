import pandas as pd
import heapq
from numpy.ma.extras import average

def extract_avg_cost(dataset, time, day):
    extracted_dataset = dataset[(dataset['weekday'] == day) & (dataset['hour'] == time)]

    averaged_dataset = []
    for i in range(0, 20):
        for j in range(0, 20):
            i_j_dataset = extracted_dataset[(extracted_dataset['i'] == i) & (extracted_dataset['j'] == j)].copy()
            i_j_dataset.drop(['timestamp', 'week_index', 'day_index', 'weekday', 'hour'], axis=1, inplace=True)

            avg = average(i_j_dataset, axis=0)
            averaged_dataset.append((i, j, float(avg[2])))

    cost_grid = [[None for _ in range(20)] for _ in range(20)]
    for (i, j, cost) in averaged_dataset:
        cost_grid[i][j] = cost

    return cost_grid

def increment_time(time, day):
    time += 1
    if time == 24:
        time = 0
        day = (day + 1) % 7
    return time, day

# ------------------------ UCS part ------------------------

def ucs_single_hour(cost_grid, start, goal):    #ucs stands for Uniform Cost Search
    priority_queue = []
    heapq.heappush(priority_queue, (cost_grid[start[0]][start[1]], start))

    dist = {start: cost_grid[start[0]][start[1]]}   # cost to reach each node
    parent = {}
    moves = [(1,0), (-1,0), (0,1), (0,-1)]

    while priority_queue:
        current_cost, (ci, cj) = heapq.heappop(priority_queue)

        if (ci, cj) == goal:
            break

        for di, dj in moves:
            ni = ci + di    # current node_i + move_i
            nj = cj + dj    # current node_j + move_j

            if 0 <= ni < 20 and 0 <= nj < 20:
                new_cost = current_cost + cost_grid[ni][nj]

                if (ni, nj) not in dist or new_cost < dist[(ni, nj)]:
                    dist[(ni, nj)] = new_cost
                    parent[(ni, nj)] = (ci, cj)
                    heapq.heappush(priority_queue, (new_cost, (ni, nj)))

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()

    return path

def ucs(dataset, time, day):    # main ucs
    start = (0,0)
    goal = (19,19)

    current = start
    total_path = [(0,0)]
    total_cost = 0
    elapsed_hour_time = 0

    while current != goal:

        cost_grid = extract_avg_cost(dataset, time, day)

        path = ucs_single_hour(cost_grid, current, goal)

        for idx in range(1, len(path)):
            ni, nj = path[idx]
            step_cost = cost_grid[ni][nj]

            if elapsed_hour_time + step_cost <= 60:
                elapsed_hour_time += step_cost
                total_cost += step_cost
                total_path.append((ni, nj))
                current = (ni, nj)
            else:

                total_cost += step_cost
                current = (ni, nj)
                total_path.append((ni, nj))

                # next hour
                time, day = increment_time(time, day)
                elapsed_hour_time = 0
                break

            if current == goal:
                break

    print("\n===== UCS =====\n")
    print("Final Path:", total_path)
    print("Total Cost:", total_cost)

# ------------------------ A* part ------------------------

def heuristic(i, j, min_cost):
    return min_cost * (abs(i - 19) + abs(j - 19))

def a_star_single_hour(cost_grid, start, goal):
    min_cost = cost_grid[0][0]
    for i in range(20):
        for j in range(20):
            if cost_grid[i][j] < min_cost:
                min_cost = cost_grid[i][j]

    g_cost = {start: cost_grid[start[0]][start[1]]}
    f_cost = {start: g_cost[start] + heuristic(start[0], start[1], min_cost)}
    parent = {}

    open_pq = []
    heapq.heappush(open_pq, (f_cost[start], start))

    moves = [(1,0), (-1,0), (0,1), (0,-1)]

    while open_pq:
        f, (ci, cj) = heapq.heappop(open_pq)

        if (ci, cj) == goal:
            break

        for di, dj in moves:
            ni = ci + di
            nj = cj + dj

            if 0 <= ni < 20 and 0 <= nj < 20:
                new_cost = g_cost[(ci, cj)] + cost_grid[ni][nj]

                if (ni, nj) not in g_cost or new_cost < g_cost[(ni, nj)]:
                    g_cost[(ni, nj)] = new_cost
                    f_cost[(ni, nj)] = new_cost + heuristic(ni, nj, min_cost)
                    parent[(ni, nj)] = (ci, cj)
                    heapq.heappush(open_pq, (f_cost[(ni, nj)], (ni, nj)))

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()

    return path

def a_star(dataset, time, day): # main A*
    start = (0,0)
    goal = (19,19)

    current = start
    total_path = [(0,0)]
    total_cost = 0
    elapsed_hour_time = 0

    while current != goal:

        cost_grid = extract_avg_cost(dataset, time, day)

        path = a_star_single_hour(cost_grid, current, goal)

        for idx in range(1, len(path)):
            ni, nj = path[idx]
            step_cost = cost_grid[ni][nj]

            if elapsed_hour_time + step_cost <= 60:
                elapsed_hour_time += step_cost
                total_cost += step_cost
                total_path.append((ni, nj))
                current = (ni, nj)
            else:
                total_cost += step_cost
                current = (ni, nj)
                total_path.append((ni, nj))

                time, day = increment_time(time, day)
                elapsed_hour_time = 0
                break

            if current == goal:
                break

    print("\n===== A* =====\n")
    print("Final Path:", total_path)
    print("Total Cost:", total_cost)

# testing the algorithms ...
trafficDataSet = pd.read_csv("D:\\AI_HW\\CHW1\\traffic_4weeks_clean.csv")
days = 5
times = 12

ucs(trafficDataSet, times, days)
a_star(trafficDataSet, times, days)