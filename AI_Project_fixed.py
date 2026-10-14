import sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import deque
import heapq
import arabic_reshaper
from bidi.algorithm import get_display

def get_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        node = node.strip()
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node1, node2, weight):
        node1 = node1.strip()
        node2 = node2.strip()
        self.add_node(node1)
        self.add_node(node2)
        self.graph[node1].append((node2, weight))
        self.graph[node2].append((node1, weight))

    def display_nodes(self):
        print(get_arabic("\n قائمة المباني:"))
        for node in sorted(self.graph.keys()):
            print("-", get_arabic(node))

def bfs(graph, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if goal not in parent:
        return None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)

    return path[::-1]

def dfs(graph, start, goal):
    stack = [start]
    visited = set()
    parent = {start: None}

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.add(current)

            if current == goal:
                break

            for neighbor, _ in graph.get(current, []):
                if neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in parent:
                        parent[neighbor] = current

    if goal not in parent:
        return None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)

    return path[::-1]

def ucs(graph, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))

    visited = set()
    parent = {start: None}
    cost_so_far = {start: 0}

    while pq:
        current_cost, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            break

        for neighbor, weight in graph.get(current, []):
            new_cost = current_cost + weight

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    if goal not in parent:
        return None, None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    return path[::-1], cost_so_far[goal]

def best_first(graph, start, goal, heuristic):
    pq = []
    heapq.heappush(pq, (heuristic.get(start, 0), start))

    visited = set()
    parent = {start: None}

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            break

        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(pq, (heuristic.get(neighbor, 0), neighbor))

    if goal not in parent:
        return None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    return path[::-1]

def a_star(graph, start, goal, heuristic):
    pq = []
    heapq.heappush(pq, (0, start))

    visited = set()
    parent = {start: None}
    g_cost = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor, weight in graph.get(current, []):
            new_cost = g_cost[current] + weight

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                f_cost = new_cost + heuristic.get(neighbor, 0)

                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, neighbor))

    if goal not in parent:
        return None, None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]

    return path[::-1], g_cost[goal]

def calculate_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        for neighbor, weight in graph[path[i]]:
            if neighbor == path[i + 1]:
                total += weight
                break
    return total

def compute_heuristic(graph, goal):
    heuristic = {goal: 0}
    queue = deque([goal])

    while queue:
        current = queue.popleft()
        for neighbor, _ in graph.get(current, []):
            if neighbor not in heuristic:
                heuristic[neighbor] = heuristic[current] + 1
                queue.append(neighbor)

    for node in graph:
        if node not in heuristic:
            heuristic[node] = float("inf")

    return heuristic

if __name__ == "__main__":

    g = Graph()

    g.add_edge("دوار الشريعة", "كلية الشريعة", 60)
    g.add_edge("دوار الشريعة", "كلية القانون", 140)
    g.add_edge("دوار الشريعة", "كلية الحجاوي", 290)
    g.add_edge("كلية الحجاوي", "كلية الآثار", 60)
    g.add_edge("كلية القانون", "كلية الآثار", 220)
    g.add_edge("كلية الشريعة", "كلية الاقتصاد", 640)
    g.add_edge("كلية الاقتصاد", "كلية الطب", 110)
    g.add_edge("دوار الشريعة", "دوار التربية", 480)
    g.add_edge("PH", "دوار التربية", 220)
    g.add_edge("دوار التربية", "كلية الآداب", 260)
    g.add_edge("كلية الآداب", "كلية الفنون", 170)
    g.add_edge("دوار التربية", "المكتبة", 170)
    g.add_edge("دوار التربية", "كلية التربية", 100)
    g.add_edge("كلية IT", "المكتبة", 80)
    g.add_edge("كلية التربية", "كلية الرياضة", 190)
    g.add_edge("المسجد", "عمادة شؤون الطلبة", 90)
    g.add_edge("المسجد", "كلية IT", 60)
    g.add_edge("كلية IT", "مبنى الخوارزمي", 70)
    g.add_edge("مبنى الخوارزمي", "كلية الرياضة", 290)
    g.add_edge("كلية التربية", "قسم الكيمياء", 80)
    g.add_edge("مبنى الخوارزمي", "قسم الجيولوجيا", 100)
    g.add_edge("كلية IT", "كلية العلوم", 80)

    g.display_nodes()

    print("\n Select The Algorithm :")
    print("1 - BFS")
    print("2 - DFS")
    print("3 - UCS")
    print("4 - Best First")
    print("5 - A*")

    choice = input(" Your Select: ").strip()
    start = input("\n Enter The Start Point: ").strip()
    goal = input("\n Enter The Goal: ").strip()

    if start in g.graph and goal in g.graph:

        if choice == "1":
            path = bfs(g.graph, start, goal)
            cost = calculate_cost(g.graph, path) if path else None
            algo = "BFS"

        elif choice == "2":
            path = dfs(g.graph, start, goal)
            cost = calculate_cost(g.graph, path) if path else None
            algo = "DFS"

        elif choice == "3":
            path, cost = ucs(g.graph, start, goal)
            algo = "UCS"

        elif choice == "4":
            heuristic = compute_heuristic(g.graph, goal)
            path = best_first(g.graph, start, goal, heuristic)
            cost = calculate_cost(g.graph, path) if path else None
            algo = "Best First"

        elif choice == "5":
            heuristic = compute_heuristic(g.graph, goal)
            path, cost = a_star(g.graph, start, goal, heuristic)
            algo = "A*"

        else:
            print(" Incorrect Selection ")
            exit()

        if path:
            print(f"\n Path Using {algo}:")
            fixed_path = [get_arabic(n) for n in path]
            print(" -> ".join(fixed_path))
            print(" Cost :", cost)
        else:
            print("\n There is no Path")

    else:
        print("\n Bulding Name Not Found !!! ")