# Disk Scheduling Visualizer
# Capstone Project - Operating System (ENCS351)
# Algorithms: FCFS, SSTF, SCAN, C-SCAN

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# Scheduling algorithms. Each function returns the complete path
# followed by the head (starting from the initial position).
# ---------------------------------------------------------------

def fcfs(head, requests, disk_size):
    # requests are served in the order in which they arrive
    return [head] + list(requests)


def sstf(head, requests, disk_size):
    # always serve the request nearest to the current head position
    pending = list(requests)
    path = [head]
    current = head
    while pending:
        nearest = min(pending, key=lambda r: abs(r - current))
        pending.remove(nearest)
        path.append(nearest)
        current = nearest
    return path


def scan(head, requests, disk_size, direction="left"):
    # head moves in one direction up to the disk end, then reverses
    left = sorted(r for r in requests if r < head)
    right = sorted(r for r in requests if r >= head)
    path = [head]
    if direction == "left":
        path += left[::-1]
        path.append(0)
        path += right
    else:
        path += right
        path.append(disk_size - 1)
        path += left[::-1]
    return path


def cscan(head, requests, disk_size, direction="right"):
    # head moves in one direction, jumps to the other end, continues
    left = sorted(r for r in requests if r < head)
    right = sorted(r for r in requests if r >= head)
    path = [head]
    if direction == "right":
        path += right
        path.append(disk_size - 1)
        path.append(0)
        path += left
    else:
        path += left[::-1]
        path.append(0)
        path.append(disk_size - 1)
        path += right[::-1]
    return path


# ---------------------------------------------------------------
# Calculations
# ---------------------------------------------------------------

def total_movement(path):
    total = 0
    for i in range(1, len(path)):
        total += abs(path[i] - path[i - 1])
    return total


# ---------------------------------------------------------------
# Graph
# ---------------------------------------------------------------

def draw_graph(path, title, filename, disk_size):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = path
    y = list(range(len(path)))
    ax.plot(x, y, marker="o", color="black", linewidth=1.3, markersize=5)
    for i in range(len(path)):
        ax.annotate(str(path[i]), (x[i], y[i]), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=9)
    ax.set_xlim(-5, disk_size + 4)
    ax.set_ylim(len(path) - 0.3, -0.8)
    ax.set_xlabel("Cylinder number", fontsize=11)
    ax.set_ylabel("Order of service", fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.set_yticks(y)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.grid(True, linestyle=":", linewidth=0.6, color="gray")
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------

def read_int(message, minimum, maximum):
    while True:
        text = input(message).strip()
        try:
            value = int(text)
        except ValueError:
            print("  Error: please enter a whole number.")
            continue
        if value < minimum or value > maximum:
            print("  Error: value must be between %d and %d." % (minimum, maximum))
            continue
        return value


def read_requests(disk_size):
    while True:
        text = input("Enter request queue (space separated) : ").split()
        if len(text) == 0:
            print("  Error: request queue cannot be empty.")
            continue
        try:
            values = [int(v) for v in text]
        except ValueError:
            print("  Error: requests must be whole numbers.")
            continue
        if min(values) < 0 or max(values) >= disk_size:
            print("  Error: every request must be between 0 and %d." % (disk_size - 1))
            continue
        return values


def read_direction(message, default):
    while True:
        text = input(message).strip().lower()
        if text == "":
            return default
        if text in ("left", "right"):
            return text
        print("  Error: type left or right.")


def get_input():
    print("=" * 60)
    print("            DISK SCHEDULING VISUALIZER")
    print("=" * 60)
    disk_size = read_int("Enter disk size (number of cylinders) : ", 2, 100000)
    head = read_int("Enter initial head position : ", 0, disk_size - 1)
    requests = read_requests(disk_size)
    d1 = read_direction("SCAN direction   [left/right, default left]   : ", "left")
    d2 = read_direction("C-SCAN direction [left/right, default right]  : ", "right")
    return head, requests, disk_size, d1, d2


# ---------------------------------------------------------------
# Output
# ---------------------------------------------------------------

def show_result(name, path, requests):
    total = total_movement(path)
    avg = total / len(requests)
    print()
    print("-" * 60)
    print("Algorithm :", name)
    print("Seek order :", " -> ".join(str(p) for p in path))
    print("Total head movement   :", total, "cylinders")
    print("Average head movement : %.2f cylinders" % avg)
    return total, avg


def main():
    head, requests, disk_size, d1, d2 = get_input()
    results = {}
    algos = [
        ("FCFS", fcfs(head, requests, disk_size)),
        ("SSTF", sstf(head, requests, disk_size)),
        ("SCAN", scan(head, requests, disk_size, d1)),
        ("C-SCAN", cscan(head, requests, disk_size, d2)),
    ]
    for name, path in algos:
        results[name] = show_result(name, path, requests)
        draw_graph(path, name + " Disk Scheduling (initial head = %d)" % head,
                   name.lower().replace("-", "") + "_graph.png", disk_size)

    print()
    print("=" * 60)
    print("%-10s %-22s %-18s" % ("Algorithm", "Total movement", "Average movement"))
    print("-" * 60)
    for name in results:
        print("%-10s %-22d %-18.2f" % (name, results[name][0], results[name][1]))
    best = min(results, key=lambda k: results[k][0])
    print("=" * 60)
    print("Least head movement :", best)
    print("Graphs saved as PNG files in the current folder.")


if __name__ == "__main__":
    main()
