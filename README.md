AI Campus Path Finder

This project is a Python-based Artificial Intelligence application that determines optimal paths between various buildings and landmarks on a university campus.
It demonstrates the practical implementation of classic AI search algorithms to solve routing and graph-traversal problems.

The application features a fully functional command-line interface (CLI) with integrated support for rendering right-to-left Arabic text in the console.

Features

Multiple AI Search Algorithms:

BFS (Breadth-First Search) - Finds the shortest path in terms of steps.

DFS (Depth-First Search) - Explores deep into a graph before backtracking.

UCS (Uniform Cost Search) - Finds the path with the absolute lowest cost/distance.

Best-First Search - A greedy algorithm that uses a hop-based heuristic to navigate towards the goal.

A* (A-Star) Search - Combines UCS and Best-First to find the most cost-effective path efficiently.

Graph Representation: The campus map is modeled as a weighted adjacency list representing distances between nodes.

Arabic CLI Support: Utilizes reshaping and bidirectional text algorithms to ensure Arabic terminal output is highly readable and correctly formatted.

Prerequisites

To run this project, you will need Python 3.x installed on your machine, along with two external libraries for handling the Arabic text formatting.

Install the required dependencies using pip:
pip install arabic-reshaper python-bidi

Usage

Clone this repository to your local machine.

Open your terminal or command prompt in the project directory.

Run the Python script:
python AI_Project_fixed.py

The program will display a list of all available campus locations.

Select your desired search algorithm by entering a number (1-5).

Enter your Start Point and Goal (using the exact Arabic names printed in the list).

Example Output

Select The Algorithm :
1 - BFS
2 - DFS
3 - UCS
4 - Best First
5 - A*
Your Select: 5

Enter The Start Point: كلية IT
Enter The Goal: دوار التربية

Path Using A*:
كلية IT -> المكتبة -> دوار التربية
Cost : 250

System Architecture

The graph is initialized within the Graph class. Each node represents a specific campus location (e.g., "كلية IT", "المكتبة", "كلية الطب"),
and edges represent the walkable distance or weight between them. The heuristic used for informed search algorithms (A* and Best-First) is computed dynamically based on the number of hops to the destination node. 
