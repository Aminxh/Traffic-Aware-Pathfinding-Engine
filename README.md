# 🚦 Dynamic Traffic Pathfinding Engine

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Course: AI](https://img.shields.io/badge/Course-Artificial%20Intelligence-red.svg)]()

## 📖 Project Overview

[cite_start]This project implements an intelligent navigation system for a $20 \times 20$ urban grid, designed to find the optimal path under time-variant traffic conditions[cite: 6]. [cite_start]The core engine utilizes four weeks of historical traffic data to predict costs and optimizes routes using **Uniform Cost Search (UCS)** and **Informed A* Search** algorithms[cite: 15, 17].

[cite_start]The system distinguishes itself by handling **Dynamic State Transitions**: if the simulated travel time exceeds a one-hour threshold, the engine automatically updates the global cost-map based on the next hour's historical averages and re-calculates the optimal trajectory from the current coordinate[cite: 12, 14].



## 🛠️ Key Features

* [cite_start]**Historical Data Aggregation**: Aggregates 28 days of traffic logs into a predictive $20 \times 20$ cost-grid based on specific days and hours[cite: 11, 12].
* **Optimal Navigation (UCS)**: Guaranteed discovery of the mathematically shortest path in a weighted graph environment[cite: 15].
* [cite_start]**Heuristic-Driven Optimization (A*)**: Utilizes a custom-scaled Manhattan distance heuristic to significantly reduce the search space while maintaining optimality[cite: 17].
* **Time-Dynamic Re-routing**: A real-time simulator that monitors elapsed "simulated time" and refreshes traffic data as the hour increments.

## 🧠 Algorithmic Implementation

### 1. The Heuristic Function
The A* algorithm uses a **Consistent and Admissible Heuristic** to ensure the optimal path is found. [cite_start]The heuristic calculates the Manhattan distance to the goal, scaled by the minimum observed cost in the current grid to avoid overestimation[cite: 10]:

$$h(n) = \text{min\_cost} \times (|x_{goal} - x_n| + |y_{goal} - y_n|)$$

### 2. Search Strategy
* **Uniform Cost Search (UCS)**: Expands nodes in layers of increasing cumulative cost ($g(n)$). It is the baseline for absolute optimality[cite: 15].
* [cite_start]**A* Search**: Combines $g(n)$ with the heuristic $h(n)$ to prioritize nodes that are likely to lead to the goal faster[cite: 17].



## 📁 Repository Structure

| File | Description |
| :--- | :--- |
| `Traffic.py` | [cite_start]Contains the core `ucs` and `a_star` functions and data processing logic[cite: 10]. |
| `Traffic_test_implemention.py` | [cite_start]The dynamic simulation engine that handles hourly traffic updates during transit. |
| `test_traffic.py` | [cite_start]Utility script to run benchmarks on the provided dataset[cite: 11]. |
| `traffic_4weeks_clean.csv` | [cite_start]The raw historical dataset containing traffic counts per coordinate/hour[cite: 11]. |
