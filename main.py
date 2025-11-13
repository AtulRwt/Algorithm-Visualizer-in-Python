import sys


def main_menu():
    while True:
        print("\nAlgorithm Visualizer Hub")
        print("=======================")
        print("1. Sorting Algorithms")
        print("2. Binary Search")
        print("3. Graph Traversal (BFS/DFS)")
        print("4. Dijkstra's Shortest Path")
        print("5. Graph Traversal (Enhanced, Tk)")
        print("6. Dijkstra (Enhanced, Tk)")
        print("7. Kruskal's Minimum Spanning Tree")
        print("8. Prim's Minimum Spanning Tree")
        print("9. Bellman–Ford Shortest Paths")
        print("10. Floyd–Warshall (APSP)")
        print("11. 0/1 Knapsack (Dynamic Programming)")
        print("12. Exit")
        choice = input("\nSelect an option (1-12): ").strip()

        if choice == "1":
            try:
                import sorting_interactive
                sorting_interactive.main()
            except Exception as e:
                print(f"Error running Sorting visualizer: {e}")
        elif choice == "2":
            try:
                import binary_search
                binary_search.main()
            except Exception as e:
                print(f"Error running Binary Search visualizer: {e}")
        elif choice == "3":
            try:
                import graph_traversal
                graph_traversal.main()
            except Exception as e:
                print(f"Error running Graph Traversal visualizer: {e}")
        elif choice == "4":
            try:
                import dijkstra
                dijkstra.main()
            except Exception as e:
                print(f"Error running Dijkstra visualizer: {e}")
        elif choice == "5":
            try:
                import graph_traversal_enhanced
                graph_traversal_enhanced.main()
            except Exception as e:
                print(f"Error running Enhanced Graph Traversal: {e}")
        elif choice == "6":
            try:
                import dijkstra_enhanced
                dijkstra_enhanced.main()
            except Exception as e:
                print(f"Error running Enhanced Dijkstra: {e}")
        elif choice == "7":
            try:
                import kruskal_mst
                kruskal_mst.main()
            except Exception as e:
                print(f"Error running Kruskal MST: {e}")
        elif choice == "8":
            try:
                import prim_mst
                prim_mst.main()
            except Exception as e:
                print(f"Error running Prim MST: {e}")
        elif choice == "9":
            try:
                import bellman_ford
                bellman_ford.main()
            except Exception as e:
                print(f"Error running Bellman–Ford: {e}")
        elif choice == "10":
            try:
                import floyd_warshall
                floyd_warshall.main()
            except Exception as e:
                print(f"Error running Floyd–Warshall: {e}")
        elif choice == "11":
            try:
                import knapsack_01
                knapsack_01.main()
            except Exception as e:
                print(f"Error running 0/1 Knapsack: {e}")
        elif choice == "12":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 12.")


if __name__ == "__main__":
    main_menu()
