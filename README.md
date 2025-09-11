# 📊 Sorting Algorithm Visualizer in Python

This project implements and **visualizes four classic sorting algorithms** — **Bubble Sort, Quick Sort, Merge Sort, and Radix Sort** using Python and `matplotlib` animation.

Unlike standard implementations, this project can run **multiple algorithms side-by-side in a single execution**, allowing users to **compare performance, execution steps, and visual behavior in real time**.

---

## 🧠 Project Overview

The main goal of this project is to combine **algorithm analysis** with **interactive visualization**. By tracking comparisons, swaps, pivots, and merges at each step, this project provides an **educational tool** to observe:

- Internal mechanics of sorting algorithms
- Relative **execution performance** on the same dataset
- Visualization of algorithm operations using animated bar charts

This makes it ideal for **learning, teaching, and analyzing sorting strategies**.

---

## ⚙️ Implemented Sorting Algorithms

### 🔹 Bubble Sort
- Iteratively compares adjacent elements.
- Demonstrates step-by-step **comparisons and swaps**.
- Simple but inefficient (`O(n²)`).

### 🔹 Quick Sort
- **Divide-and-conquer** strategy using pivots.
- Highlights **partitioning and recursive sorting**.
- Average `O(n log n)` time, worst-case `O(n²)`.

### 🔹 Merge Sort
- Recursive **divide + merge** approach.
- Tracks element **copies, comparisons, and merges**.
- Stable, always `O(n log n)` performance.

### 🔹 Radix Sort
- Non-comparative, digit-level sorting.
- Works for **non-negative integers only**.
- Complexity: `O(nk)` where `k` is number of digits.

---

## 🔁 Why Multiple Algorithms Together?

Running all four algorithms **simultaneously** emphasizes their differences:

| Feature | Bubble | Quick | Merge | Radix |
|--------:|:------:|:-----:|:-----:|:-----:|
| Complexity | `O(n²)` | `O(n log n)` avg | `O(n log n)` | `O(nk)` |
| In-place | ✅ | ✅ | ❌ | ✅ |
| Stable | ✅ | ❌ | ✅ | ✅ |
| Visualization | Comparisons & swaps | Pivot & partitions | Divide + merge | Digit passes |

Side-by-side execution allows a **direct performance and behavior comparison**.

---

## 🧩 Architecture Overview

The Python script is divided into these components:

- **Number Generator**: generates random numbers or reads from a file.
- **Sorting Implementations**: each algorithm logs its internal operations as a sequence of "states" for visualization.
- **State Tracker**: stores operations (`compare`, `swap`, `pivot`, `copy`, `copy_back`, `merged`, `digit`, `pass_complete`, `complete`) for animation.
- **Matplotlib Animation**: subplots display each chosen algorithm in real time.

### Color Legend (Animation)

| Color | Meaning |
|------|---------|
| 🟨 Yellow | Comparison (element(s) under comparison) |
| 🟥 Red | Swap / Copy (elements being swapped or copied) |
| 🟩 Green | Pivot or merged section |
| 🟦 Blue | Default / Idle |
| 🟩 Light Green | Sorted / Pass complete |

---

## 📷 Example Visualization

Run the script with:

```bash
python py sorting.py --mode random --n 50 --min_val 0 --max_val 100 --algo bubble --algo quick --algo merge --algo radix
```

![Visualization Example](https://github.com/VLSI-Shubh/Sorting-Algorithm-Visualizer-in-Python/blob/4a4e403a2b60c9e2b863971b782066f333d5b99f/images/sorting.gif)

---

## ⚡ Terminal Output

![Terminal Output](https://github.com/VLSI-Shubh/Sorting-Algorithm-Visualizer-in-Python/blob/4a4e403a2b60c9e2b863971b782066f333d5b99f/images/terminal%20output.png)

This output shows **algorithm efficiency**, number of steps, maximum frames for animation, and overall sorting performance comparison.

---

## 📊 Performance Summary Table

| Rank | Algorithm    | Steps | Time (ms) |
|:----:|:-------------|:-----:|:---------:|
| 1    | Radix Sort   | 153   | 0.07      |
| 2    | Quick Sort   | 378   | 0.15      |
| 3    | Merge Sort   | 621   | 0.26      |
| 4    | Bubble Sort  | 1863  | 2.72      |

- ✅ **Fastest:** Radix Sort (0.07 ms)
- ❌ **Slowest:** Bubble Sort (2.72 ms)

This table provides an **at-a-glance comparison** of algorithm performance and steps.

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `sorting.py` | Main Python script with sorting algorithms, state instrumentation, and visualization |
| `numbers.txt` | Optional input/output file for dataset (one number per line) |
| `images/` | Example GIFs or PNGs of visualization output  |

---

## ▶️ Usage Instructions

Run with command-line arguments:

```bash
# Randomly generate numbers
python sorting.py --mode random --n <number_of_elements> --algo <algorithm_names>

# Use numbers from a file
python sorting.py --mode file --file <file_path> --algo <algorithm_names>

# Customize animation speed (interval in ms)
python sorting.py --mode random --n <number_of_elements> --algo <algorithm_names> --interval <milliseconds>

```


## Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `--mode` | Input mode: `random` or `file` |
| `--algo` | Sorting algorithm(s) to visualize (`bubble`, `quick`, `merge`, `radix`) |
| `--n` | Number of elements (for random mode) |
| `--min_val` / `--max_val` | Range of generated numbers (for random mode) |
| `--file` | File path for input/output numbers |
| `--interval` | Animation frame interval in ms |

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Python 3** | Programming language |
| **matplotlib** | Visualization and animation |
| **argparse** | Command-line argument parsing |
| **time** | Performance measurement |

---

## ✅ Conclusion

This project serves as a **learning resource** and **visual tool** for understanding sorting algorithms:

- Shows **internal mechanics** of four classic sorting methods
- Highlights **trade-offs** between simplicity, speed, and stability
- Provides **interactive, side-by-side visual comparison** of multiple algorithms

It demonstrates how **algorithm choice impacts execution** beyond theoretical complexity.

---

## 📝 License

Open for educational and personal use under the [MIT License](https://github.com/VLSI-Shubh/Sorting-Algorithm-Visualizer-in-Python/blob/d3e629a2f03d3fc9f5fcd46af5248b3fbde45c28/License.txt)

