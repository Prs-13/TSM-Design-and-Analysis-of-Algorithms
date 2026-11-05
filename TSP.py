import json
import time

def TSP_exe(name, algo, matrix):

    start = time.perf_counter()
    if algo == "tsp_dp":
        path, cost = TSP_dp(matrix)

    elif algo == "multi_fragment":
        path, cost = multi_fragment(matrix)

    else:
        path, cost = insertion_between(matrix)

    end = time.perf_counter()
    time_len = (end - start) * 1000

    print("\n",name,sep='')
    print("path:", path)
    print("cost:", cost)
    print(f"Execution Time: {time_len:.3f} ms")

    # print(matrix)
    # print(path) 
    # print(cost)

def load_data(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["matrix"]

def path_cost(path, matrix):
    cost = 0
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i + 1]]
    return cost

def subset_generator(arr, k):

    res = []

    def backtrack(start, current):

        if len(current) == k:
            res.append(current[:])
            return

        for i in range(start, len(arr)):
            current.append(arr[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return res

def TSP_dp(matrix):
    num_of_cities = len(matrix)

    dp = {}
    parent = {}

    # base case
    for city in range(1, num_of_cities):
        dp[(frozenset([city]), city)] = matrix[0][city]

    for size in range(2, num_of_cities):
        subsets = subset_generator(list(range(1, num_of_cities)), size)

        for subset in subsets:
            S = frozenset(subset)

            for last in subset:
                prev_set = S - {last}
                best_cost = float('inf')
                best_prev = None

                for prev in prev_set:
                    cost = (dp[(prev_set, prev)] + matrix[prev][last])

                    if cost < best_cost:
                        best_cost = cost
                        best_prev = prev

                dp[(S, last)] = best_cost
                parent[(S, last)] = best_prev

    full_set = frozenset(range(1, num_of_cities))
    best_cost = float('inf')
    last_city = None

    for city in range(1, num_of_cities):
        cost = dp[(full_set, city)] + matrix[city][0]

        if cost < best_cost:
            best_cost = cost
            last_city = city

    path = [0]
    current = last_city
    S = full_set

    while S:
        path.append(current)
        prev = parent.get((S, current))
        S = S - {current}
        if prev is None:
            break
        current = prev

    path[1:] = reversed(path[1:])
    path.append(0)

    return path, best_cost


def insertion_between(matrix):

    num_of_cities = len(matrix)
    path = [0, 1, 0]
    not_visited = set(range(2, num_of_cities))

    while not_visited:

        city_to_insert = None
        position = None
        best_increase_of_insertion_between = float('inf')

        for city in not_visited:

            for i in range(len(path)-1):

                increase_of_insertion_between = (matrix[path[i]][city] + matrix[city][path[i+1]] - matrix[path[i]][path[i+1]])

                if increase_of_insertion_between < best_increase_of_insertion_between:
                    best_increase_of_insertion_between = increase_of_insertion_between
                    city_to_insert = city
                    position = i + 1

        path.insert(position, city_to_insert)
        not_visited.remove(city_to_insert)

    return path, path_cost(path, matrix)


def uf_find(parent, x):

    if parent[x] != x:
        parent[x] = uf_find(parent, parent[x])

    return parent[x]


def uf_union(parent, rank, a, b):

    root_a = uf_find(parent, a)
    root_b = uf_find(parent, b)

    if root_a == root_b:
        return False

    if rank[root_a] < rank[root_b]:
        parent[root_a] = root_b

    elif rank[root_a] > rank[root_b]:
        parent[root_b] = root_a

    else:
        parent[root_b] = root_a
        rank[root_a] += 1

    return True


def multi_fragment(matrix):

    n = len(matrix)

    if n == 1:
        return [0, 0], 0

    if n == 2:
        path = [0, 1, 0]
        return path, path_cost(path, matrix)

    # -----------------------------------------
    # Generate all edges
    # -----------------------------------------

    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            edges.append((matrix[i][j], i, j))

    edges.sort()

    # -----------------------------------------
    # Greedy edge selection
    # -----------------------------------------

    parent = list(range(n))
    rank = [0] * n

    degree = [0] * n

    chosen_edges = []

    for weight, u, v in edges:

        if degree[u] >= 2:
            continue

        if degree[v] >= 2:
            continue

        same_component = (uf_find(parent, u) == uf_find(parent, v))

        # Prevent premature cycles
        if same_component:

            if len(chosen_edges) != n - 1:
                continue

        chosen_edges.append((u, v))

        degree[u] += 1
        degree[v] += 1

        if not same_component:
            uf_union(parent, rank, u, v)

        if len(chosen_edges) == n:
            break

    # -----------------------------------------
    # Build adjacency list
    # -----------------------------------------

    adj = []

    for i in range(n):
        adj.append([])

    for u, v in chosen_edges:
        adj[u].append(v)
        adj[v].append(u)

    # -----------------------------------------
    # Reconstruct Hamiltonian cycle
    # -----------------------------------------

    path = [0]

    prev = -1
    current = 0

    while True:

        neighbors = adj[current]

        next_city = None

        for city in neighbors:
            if city != prev:
                next_city = city
                break

        if next_city is None:
            break

        if next_city == 0:
            path.append(0)
            break

        path.append(next_city)

        prev = current
        current = next_city

    return path, path_cost(path, matrix)



# matrix = load_data("C:/Users/Parsa/Desktop/Courses References/Sem4/Design & Analysis of Algorithms/Project/dp.json")
# TSP_exe("Dynamic Programming", "tsp_dp", matrix)
# TSP_exe("Insertion_between","insertion_between", matrix)
# TSP_exe("Multi Fragment", "multi_fragment", matrix)

matrix = load_data("C:/Users/Parsa/Desktop/Courses References/Sem4/Design & Analysis of Algorithms/Project/speed.json")
TSP_exe("Insertion_between","insertion_between", matrix)
TSP_exe("Multi Fragment", "multi_fragment", matrix)
# TSP_exe("Dynamic Programming", "tsp_dp", matrix)