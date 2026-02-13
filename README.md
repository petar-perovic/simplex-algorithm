# Simplex Algorithm GUI

This project is a **Tkinter-based graphical application** for solving **Linear Programming (LP) maximization problems** using the **Simplex algorithm**.

The application provides a **full tableau visualization**, including:

- Basic variables (B)
- Cost coefficients (CB)
- RHS values (b)
- Zj row
- Cj − Zj row
- Pivot highlighting
- Step-by-step iteration navigation

---

## Requirements

- Python 3.8+
- numpy

Install dependencies:

```bash
pip install numpy
```

Tkinter comes preinstalled with most Python distributions.

---

## How to Run

Run the Python file:

```bash
python simplex_gui.py
```

The GUI window will open automatically.

---

# How to Use the Application

## Step 1 – Define Problem Size

When the program starts, enter:

- **Number of variables (x)**
- **Number of constraints**

Click **OK**.

---

## Step 2 – Enter the Linear Programming Problem

You will now enter:

- Objective function coefficients
- Constraint coefficients
- Right-hand side (b values)

The problem must be in standard form:

Maximize:

\[
Z = c_1 x_1 + c_2 x_2 + ... + c_n x_n
\]

Subject to:

\[
a_{11}x_1 + a_{12}x_2 + ... \le b_1
\]

All constraints must be of type:

\[
\le
\]

---

# Example Problem

Let’s solve the following LP problem:

Maximize:

\[
Z = 3x_1 + 5x_2
\]

Subject to:

\[
2x_1 + x_2 \le 8
\]
\[
x_1 + 2x_2 \le 8
\]

\[
x_1, x_2 \ge 0
\]

---

## How to Enter This in the GUI

### First screen:

Number of variables:
```
2
```

Number of constraints:
```
2
```

Click **OK**.

---

### Objective Function (Max Z =)

Enter:

| x1 | x2 |
|----|----|
| 3  | 5  |

---

### Constraints

First constraint:
```
2   1   <=   8
```

Second constraint:
```
1   2   <=   8
```

Then click **Pocni**.

---

# Understanding the Output

The application displays:

- Full Simplex tableau
- Highlighted pivot element (red)
- Pivot row (blue)
- Pivot column (green)
- Zj row
- Cj − Zj row

Click **Next iteration** to move step-by-step.

When finished, the program displays:

```
Optimal solution reached
```

---

# Educational Purpose

This project is designed for:

- Students learning Linear Programming
- Understanding Simplex tableau mechanics
- Visualizing pivot operations
- My personal exam preparation

---

# Limitations

- Supports only maximization problems
- Supports only ≤ constraints
- Does not support artificial variables (Big M / Two-Phase method)
- Does not detect degeneracy or unbounded solutions

---

# Possible Improvements

- Add ≥ and = constraints
- Add minimization problems
- Add Big-M / Two-Phase method