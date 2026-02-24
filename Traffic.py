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

# ------------------------ UCS part ------------------------

def ucs(dataset, time, day):    # ucs stands for Uniform Cost Search algorithm

    cost_grid = extract_avg_cost(dataset, time, day)

    print(cost_grid)

    start = (0, 0)
    goal = (19, 19)

    priority_queue = []
    heapq.heappush(priority_queue, (cost_grid[0][0], start))

    dist = {start: cost_grid[0][0]}     # cost to reach each node

    parent = {}     # for reconstructing path

    moves = [(1,0), (-1,0), (0,1), (0,-1)]

    # performing UCS
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

    print("\n===== UCS RESULT =====\n")
    print("Best Path:")
    for (i, j) in path:
        if (i, j) == (19, 19) :
            print('({i}, {j})'.format(i=i, j=j))
            break
        print('({i}, {j})'.format(i=i, j=j) + "--->")

    print("Total Cost:", dist[goal])

# ------------------------ A* part ------------------------

def heuristic(i, j, min_cost):
    return min_cost * (abs(i - 19) + abs(j - 19))

def a_star(dataset, time, day):
    cost_grid = extract_avg_cost(dataset, time, day)

    min_cost = cost_grid[0][0]
    for i in range(0, len(cost_grid)):
        for j in range(0, len(cost_grid[i])):
            if cost_grid[i][j] < min_cost:
                min_cost = cost_grid[i][j]

    start = (0, 0)
    goal  = (19, 19)

    open_pq = []
    g_cost = {start: cost_grid[0][0]}        # real path cost
    f_cost = {start: g_cost[start] + heuristic(0, 0, min_cost)}
    parent_A = {}

    moves = [(1,0), (-1,0), (0,1), (0,-1)]

    heapq.heappush(open_pq, (f_cost[start], start))

    while open_pq:
        f, (ci, cj) = heapq.heappop(open_pq)

        if (ci, cj) == goal:
            break

        for di, dj in moves:
            ni, nj = ci + di, cj + dj
            if 0 <= ni < 20 and 0 <= nj < 20:

                tentative_g = g_cost[(ci, cj)] + cost_grid[ni][nj]

                if (ni, nj) not in g_cost or tentative_g < g_cost[(ni, nj)]:
                    g_cost[(ni, nj)] = tentative_g
                    f_cost[(ni, nj)] = tentative_g + heuristic(ni, nj, min_cost)
                    parent_A[(ni, nj)] = (ci, cj)
                    heapq.heappush(open_pq, (f_cost[(ni, nj)], (ni, nj)))

    # reconstruct A* path
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent_A[node]
    path.append(start)
    path.reverse()

    print("\n===== A* RESULT =====\n")
    print("Best Path:")
    for (i, j) in path:
        if (i, j) == (19, 19) :
            print('({i}, {j})'.format(i=i, j=j))
            break
        print('({i}, {j})'.format(i=i, j=j) + "--->")
    print("Total Cost:", g_cost[goal])