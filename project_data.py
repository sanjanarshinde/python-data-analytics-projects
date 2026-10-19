"""
Capstone Project - Python Fundamentals
--------------------------------------
Employee / Project / Seniority analysis with pandas, plus matplotlib and
seaborn charts.

Run:  python project_data.py
Output: CSV files in the current folder and PNG charts in ./charts
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


# =============================================================================
# TASK 1: Create three dataframes and save them as .csv files
# (From Task 2 onwards, only the saved .csv files are used.)
# =============================================================================
project_data = {
    "ID": ["A001", "A002", "A003", "A004", "A005", "A002", "A005",
           "A003", "A001", "A003", "A001", "A004", "A004", "A005"],
    "Project": [f"project{i}" for i in range(1, 15)],
    "cost": [1002000, 2000000, 4500000, 5500000, np.nan, 680000, 400000,
             350000, np.nan, 300000, 2000000, 1000000, 3000000, 200000],
    "status": ["finished", "ongoing", "finished", "ongoing", "finished",
               "failed", "finished", "failed", "ongoing", "finished",
               "failed", "ongoing", "finished", "finished"],
}
project = pd.DataFrame(project_data)

employee_data = {
    "ID": ["A001", "A002", "A003", "A004", "A005"],
    "name": ["John Alter", "Alice Luxumberg", "Tom Sabestine",
             "Nina Adgra", "Amy Johny"],
    "Gender": ["M", "F", "M", "F", "F"],
    "city": ["Paris", "London", "Berlin", "Newyork", "Madrid"],
    "age": [25, 27, 29, 31, 30],
}
employee = pd.DataFrame(employee_data)

seniority_data = {
    "ID": ["A001", "A002", "A003", "A004", "A005"],
    "Designation Level": [2, 2, 3, 2, 3],
}
seniority = pd.DataFrame(seniority_data)

project.to_csv("project.csv", index=False)
employee.to_csv("employee.csv", index=False)
seniority.to_csv("seniority.csv", index=False)

print("TASK 1: CSV files created -> project.csv, employee.csv, seniority.csv")
print(project, "\n")
print(employee, "\n")
print(seniority, "\n")


# =============================================================================
# TASK 2: Replace missing values in "cost" with the running average (For loop)
# Running average = mean of all actual (non-missing) costs seen so far.
# =============================================================================
project = pd.read_csv("project.csv")

running_sum = 0
running_count = 0

for i in range(len(project)):
    cost_value = project.loc[i, "cost"]
    if pd.isna(cost_value):
        if running_count > 0:  # guard: first row can't have a previous average
            project.loc[i, "cost"] = running_sum / running_count
    else:
        running_sum += cost_value
        running_count += 1

project["cost"] = project["cost"].round(2)
project.to_csv("project.csv", index=False)

print("TASK 2: Missing costs replaced with running average")
print(project, "\n")


# =============================================================================
# TASK 3: Split "name" into "First Name" and "Last Name", drop old "name"
# =============================================================================
employee = pd.read_csv("employee.csv")

employee[["First Name", "Last Name"]] = employee["name"].str.split(" ", n=1, expand=True)
employee = employee.drop(columns="name")
employee.to_csv("employee.csv", index=False)

print("TASK 3: Name split into First Name / Last Name")
print(employee, "\n")


# =============================================================================
# TASK 4: Join all three dataframes into one ("Final")
# =============================================================================
employee = pd.read_csv("employee.csv")
seniority = pd.read_csv("seniority.csv")
project = pd.read_csv("project.csv")

final_df = (
    employee
    .merge(seniority, on="ID", how="inner")
    .merge(project, on="ID", how="inner")
)
final_df.to_csv("final_df.csv", index=False)

print("TASK 4: Final dataframe (employee + seniority + project)")
print(final_df, "\n")


# =============================================================================
# TASK 5: Bonus column - 5% of project cost, only for finished projects
# =============================================================================
final_df["Bonus"] = np.where(
    final_df["status"].str.lower() == "finished",
    (final_df["cost"] * 0.05).round(2),
    0,
)
final_df.to_csv("final_df.csv", index=False)

print("TASK 5: Bonus column added")
print(final_df, "\n")


# =============================================================================
# TASK 6: Demote designation level by 1 where project status is "failed".
# In this scheme a HIGHER number means a LOWER rank, so demotion = +1.
# Then delete employees whose designation level is above 4.
# =============================================================================
failed_mask = final_df["status"].str.lower() == "failed"
final_df.loc[failed_mask, "Designation Level"] += 1

final_df = final_df[final_df["Designation Level"] <= 4]
final_df = final_df.reset_index(drop=True)
final_df.to_csv("final_df.csv", index=False)

print("TASK 6: Demoted failed-project rows (+1) and removed levels above 4")
print(final_df, "\n")


# =============================================================================
# TASK 7: Add "Mr." / "Mrs." to First Name and drop the Gender column
# =============================================================================
final_df["First Name"] = final_df["Gender"].map({"M": "Mr. ", "F": "Mrs. "}) + final_df["First Name"]
final_df = final_df.drop(columns="Gender")
final_df.to_csv("final_df.csv", index=False)

print("TASK 7: Titles added and Gender column dropped")
print(final_df, "\n")


# =============================================================================
# TASK 8: Promote designation level by 1 for employees older than 29 (IF)
# Promotion is the opposite of demotion, so it is -1 here.
# =============================================================================
def promote(row):
    if row["age"] > 29:
        return row["Designation Level"] - 1
    else:
        return row["Designation Level"]


final_df["Designation Level"] = final_df.apply(promote, axis=1)
final_df.to_csv("final_df.csv", index=False)

print("TASK 8: Employees older than 29 promoted")
print(final_df, "\n")


# =============================================================================
# TASK 9: Total project cost per employee -> "TotalProjCost"
# Columns: ID, First Name, Total cost
# =============================================================================
TotalProjCost = (
    final_df
    .groupby(["ID", "First Name"], as_index=False)["cost"]
    .sum()
    .rename(columns={"cost": "Total cost"})
)
TotalProjCost.to_csv("TotalProjCost.csv", index=False)

print("TASK 9: TotalProjCost")
print(TotalProjCost, "\n")


# =============================================================================
# TASK 10: Print employee details whose city name contains the letter "o"
# (case-insensitive, one row per employee)
# =============================================================================
employee = pd.read_csv("employee.csv")
o_city = employee[employee["city"].str.contains("o", case=False)]

print('TASK 10: Employees whose city contains the letter "o"')
print(o_city, "\n")


# =============================================================================
# DATA VISUALISATION (matplotlib + seaborn)
# Charts are saved to ./charts and then displayed.
# =============================================================================
os.makedirs("charts", exist_ok=True)
sns.set_theme(style="whitegrid")

status_palette = {"finished": "#2a9d8f", "ongoing": "#e9c46a", "failed": "#e76f51"}


def save_and_show(filename):
    plt.tight_layout()
    plt.savefig(os.path.join("charts", filename), dpi=150)
    plt.show()
    plt.close()


# Chart 1: cost of every project, coloured by status
plt.figure(figsize=(11, 5))
sns.barplot(data=project, x="Project", y="cost", hue="status",
            palette=status_palette, dodge=False)
plt.title("Project Cost by Project and Status")
plt.xlabel("Project")
plt.ylabel("Cost")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Status")
save_and_show("1_project_cost_by_status.png")

# Chart 2: how many projects are finished / ongoing / failed
plt.figure(figsize=(6, 4))
ax = sns.countplot(data=project, x="status",
                   order=["finished", "ongoing", "failed"],
                   hue="status", palette=status_palette, legend=False)
for container in ax.containers:
    ax.bar_label(container)
plt.title("Number of Projects by Status")
plt.xlabel("Status")
plt.ylabel("Number of projects")
save_and_show("2_project_status_count.png")

# Chart 3: total project cost per employee (Task 9 output)
plt.figure(figsize=(8, 5))
sns.barplot(data=TotalProjCost, x="First Name", y="Total cost",
            hue="First Name", palette="viridis", legend=False)
plt.title("Total Project Cost per Employee")
plt.xlabel("Employee")
plt.ylabel("Total cost")
plt.xticks(rotation=20)
save_and_show("3_total_cost_per_employee.png")

# Chart 4: total bonus earned per employee (Task 5 output)
bonus_by_emp = final_df.groupby("First Name", as_index=False)["Bonus"].sum()
plt.figure(figsize=(8, 5))
sns.barplot(data=bonus_by_emp, x="First Name", y="Bonus",
            hue="First Name", palette="mako", legend=False)
plt.title("Total Bonus per Employee (5% of finished project cost)")
plt.xlabel("Employee")
plt.ylabel("Bonus")
plt.xticks(rotation=20)
save_and_show("4_bonus_per_employee.png")

# Chart 5: heatmap of project count by employee and status
status_matrix = final_df.pivot_table(index="First Name", columns="status",
                                     values="Project", aggfunc="count",
                                     fill_value=0)
plt.figure(figsize=(7, 5))
sns.heatmap(status_matrix, annot=True, fmt="d", cmap="YlGnBu", cbar=False)
plt.title("Projects per Employee by Status")
plt.xlabel("Status")
plt.ylabel("Employee")
save_and_show("5_employee_status_heatmap.png")

print("Done. Charts saved in the 'charts' folder.")
