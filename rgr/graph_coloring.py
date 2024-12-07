import random
from sympy import isprime, nextprime
from math import gcd

# Чтение графа из файла с проверкой
def load_graph(filename):
    with open(filename, "r") as file:
        # Чтение первой строки (n и m)
        first_line = file.readline().strip()
        try:
            n, m = map(int, first_line.split())
            if not (1 <= n <= 1000):
                raise ValueError("Число вершин должно быть от 1 до 1000.")
            if not (0 <= m <= n**2):
                raise ValueError("Число рёбер должно быть от 0 до n^2.")
        except ValueError as e:
            raise ValueError(f"Ошибка в первой строке файла: {e}")

        # Чтение рёбер
        graph = {i: [] for i in range(1, n + 1)}
        for _ in range(m):
            edge_line = file.readline().strip()
            try:
                u, v = map(int, edge_line.split())
                if not (1 <= u <= n and 1 <= v <= n):
                    raise ValueError(f"Номер вершины выходит за пределы 1..{n}.")
                if u == v:
                    raise ValueError("Рёбра не могут соединять вершину саму с собой.")
                graph[u].append(v)
                graph[v].append(u)
            except ValueError as e:
                raise ValueError(f"Ошибка в описании рёбер: {e}")

        # Чтение цветов
        colors_line = file.readline().strip()
        colors = colors_line.split()
        if len(colors) != n:
            raise ValueError(f"Число цветов ({len(colors)}) не соответствует числу вершин ({n}).")
        if any(color not in "RBY" for color in colors):
            raise ValueError("Цвета вершин должны быть 'R', 'B' или 'Y'.")

    return graph, colors

# Генерация ключей RSA
def generate_rsa_keys():
    p = nextprime(random.randint(10**4, 10**5))
    q = nextprime(random.randint(10**4, 10**5))
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    d = pow(e, -1, phi)
    return n, e, d

# Протокол доказательства
def run_protocol(graph, colors, rounds):
    n_vertices = len(graph)
    rsa_keys = {v: generate_rsa_keys() for v in range(1, n_vertices + 1)}
    
    for _ in range(rounds * len(graph)):
        # Шаг 1: Алиса переставляет цвета
        permutation = list("RBY")
        random.shuffle(permutation)
        permuted_colors = [permutation["RBY".index(color)] for color in colors]
        
        # Шаг 2: Генерация случайных чисел
        random_numbers = {v: (random.randint(10**5, 10**6) & ~3) + "RBY".index(permuted_colors[v - 1]) for v in range(1, n_vertices + 1)}
        
        # Шаг 3: Алиса шифрует данные
        encrypted_data = {}
        for v in range(1, n_vertices + 1):
            n, _, d = rsa_keys[v]
            encrypted_data[v] = pow(random_numbers[v], d, n)
        
        # Шаг 4: Боб выбирает случайное ребро
        edge = random.choice([(u, v) for u in graph for v in graph[u] if u < v])
        v1, v2 = edge
        
        # Алиса отправляет cv1, cv2
        _, e1, _ = rsa_keys[v1]
        _, e2, _ = rsa_keys[v2]
        rv1 = pow(encrypted_data[v1], e1, rsa_keys[v1][0])
        rv2 = pow(encrypted_data[v2], e2, rsa_keys[v2][0])
        
        # Проверка младших бит
        if (rv1 & 3) == (rv2 & 3):
            print(f"Ошибка: вершины {v1} и {v2} имеют одинаковый цвет!")
            return False
    
    return True
