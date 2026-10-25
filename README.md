# Python Data Analytics Projects

## Capstone Project: Employee and Project Analysis (Python Fundamentals)

A pandas project that builds three related datasets (Project, Employee, Seniority), cleans and combines them, applies business rules, and visualises the results with matplotlib and seaborn.

## Tools Used
- Python 3
- pandas and numpy for data handling
- matplotlib and seaborn for visualisation

## What the Script Does

| Task | Description |
|------|-------------|
| 1 | Create the three dataframes and save them as CSV files |
| 2 | Fill missing project costs with a running average using a `for` loop |
| 3 | Split `name` into `First Name` and `Last Name`, then drop `name` |
| 4 | Merge all three dataframes into one final dataframe |
| 5 | Add a 5% bonus on project cost for finished projects only |
| 6 | Demote designation level (+1) for failed projects and remove levels above 4 |
| 7 | Add "Mr." / "Mrs." to first names and drop the `Gender` column |
| 8 | Promote designation level (-1) for employees older than 29, using an `if` condition |
| 9 | Calculate total project cost per employee (`TotalProjCost`) |
| 10 | List employees whose city contains the letter "o" |

## Charts
Running the script creates a `charts` folder with:
1. Project cost by project and status
2. Number of projects by status
3. Total project cost per employee
4. Total bonus per employee
5. Heatmap of projects per employee by status

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
python project_data.py
```
The script creates the CSV files and the `charts` folder in the folder it runs from.

## Key Concepts Practised
- Running-average imputation with a loop
- String splitting and column transformations
- Merging dataframes
- Conditional logic with `np.where` and `apply`
- Grouping and aggregation
- Data visualisation with seaborn

  ## Files
- `Python_Capstone_Project.ipynb` – notebook with outputs and charts
- `project_data.py` – full script (run with `python project_data.py`)
- `*.csv` – input and result datasets
- `charts/` – saved visualisations
