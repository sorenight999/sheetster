from sheet_lookup import get_cell_value

# Read the cell list from range.txt - one cell reference per line
with open("range.txt") as f:
    c = [line.strip() for line in f if line.strip()]

for cell in c:
    print(cell + ": " + get_cell_value(cell))