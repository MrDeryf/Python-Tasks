# Python Course Tasks

This repository contains tasks completed during the **Python** course at [MIREA – Russian Technological University](https://www.mirea.ru/) (2023–2024 academic year).

All tasks are divided into two folders:

1. **Notebooks** — folder with 5 subfolders for the 5 main assignments. Each assignment contains a notebook and additional files created along the way.
2. **KIS** — 12 additional small tasks, each in a `.py` file.

## 📁 Folder Contents

### Notebooks

Topics covered in each assignment:

1. **Basic Python**  
   This assignment includes:
   - data types
   - loops
   - conditional statements
   - error types
   - arithmetic and logical operations
   - graphics

2. **Intermediate Python**  
   This assignment includes:
   - PEP 8 code formatting
   - language features
   - list comprehensions
   - Hamming distance
   - text generation

3. **Modules and Graphics**  
   This assignment includes:
   - modules (`My_module1.py` and `My_module2.py` are for this part)
   - random sprites generation
   - data visualization

4. **Advanced Python**  
   This assignment includes:
   - OOP
   - hash implementation from scratch
   - expression trees implementation from scratch
   - HTML parser implementation from scratch
   - graph visualization
   - programming language implementation from scratch (`Fortic.py` is for this part)

5. **Testing**  
   This assignment includes:
   - basic testing with doctests, `assert`, and context managers
   - testing with `pytest` and `coverage` (`test_monkey_patch.py` is for this part)
   - mutation testing (`Mutant.py` is for this part)
   - testing with `deal` (`test_deal.py` is for this part)
   - testing with `hypothesis`
   - game verification (`FormalTesting.py` and `state_graph.gv` are for this part)

### KIS

Topics of each small task:

1. Arithmetic operations
2. Conditional statements
3. Recursion — part 1
4. Recursion — part 2
5. Loops
6. Set comprehensions
7. Tree processing
8. Encryption and decryption
9. Dictionary parsing
10. Email generation
11. Testing
12. Binary string decoding

## 🛠️ Technologies Used

| Category      | Libraries                                                 |
|---------------|-----------------------------------------------------------|
| Core          | Python 3.13, Jupyter Notebook                             |
| Visualization | `matplotlib`                                              |
| Testing       | `pytest`, `pytest-cov`, `deal`, `icontract`, `hypothesis` |

🔗 See [`pyproject.toml`](./pyproject.toml) for the complete dependency list.

## ▶️ How to Run

To run the project content locally, do the following steps

1. Clone this repository:  

   ```bash
   git clone https://github.com/MrDeryf/Python-Tasks
   ```

2. Install dependencies using [Poetry](https://python-poetry.org/):

    ```bash
   poetry install
   ```

3. Launch Jupyter Notebook (for `.ipynb` files):  

    ```bash
   jupyter notebook
   ```

4. Run Python scripts (for `.py` files):

   ```bash
   poetry run python <filename>.py
   ```
