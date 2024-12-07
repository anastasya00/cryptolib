from rgr.graph_coloring import *

def main():
    input_file = "files/graph_input.txt"
    graph, colors = load_graph(input_file)
    print(f"Граф: {len(graph)} вершин и {sum(len(edges) for edges in graph.values()) // 2} рёбер.")
    
    print("Запуск протокола доказательства...")
    rounds = 5  # Параметр a, задающий количество проверок для повышения надёжности
    success = run_protocol(graph, colors, rounds)
    
    if success:
        print("Протокол завершён: доказательство корректности раскраски успешно.")
    else:
        print("Протокол завершён: корректность раскраски не подтверждена.")

if __name__ == "__main__":
    main()
