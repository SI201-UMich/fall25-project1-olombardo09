import csv
import os

# ------------------------------------------------------
# 1. Read CSV
# ------------------------------------------------------
def read_csv(filename):
    """
    Reads the dataset into a list of dictionaries,
    where each dictionary represents one penguin’s data.

    Input:
        filename (str): the name of the CSV file to read
    Output:
        data (list of dicts): each dict represents one penguin's data
    """
    data = []
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, filename)

    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    return data


# ------------------------------------------------------
# 2. Helper Functions for calculate_average_bill_length
# ------------------------------------------------------
def group_by_species_and_island(data):
    """
    Groups penguins' bill lengths by (species, island) pairs.

    Input:
        data (list of dicts): penguin dataset
    Output:
        groups (dict): keys = (species, island)
                       values = list of bill lengths (floats)
    """
    groups = {}

    for penguin in data:
        species = penguin['species']
        island = penguin['island']
        bill_length = penguin['bill_length_mm']  # ensures bill_length is a float

        if bill_length in ("", "NA", "NaN", None):
            continue    # skip missing or invalid data

        try:
            bill_length = float(bill_length)
        except ValueError:
            continue  # if conversion fails, skip this record

        key = (species, island)
        if key not in groups:
            groups[key] = []  # key should be (species, island) pairing; value should be a list of bill lengths

        groups[key].append(bill_length)
    
    return groups 
    # should return a dictionary with (species, island) pairings as the keys and lists of bill_lengths as the values


def compute_average(values):
    """
    Calculates and returns the mean of a list of numerical values.
    Returns 0 if list is empty.

    Input:
        values (list of floats or ints)
    Output:
        average (float)
    """

    if len(values) == 0:
        return 0
    
    # general function to find the average of a list of floats or ints
    # useful for both calculation functions
    return sum(values) / len(values)


# ------------------------------------------------------
# 3. calculate_average_bill_length Function
# ------------------------------------------------------
def calculate_average_bill_length(data):
    """
    Calculates average bill length for each species and island combination.

    Input:
        data (list of dicts)
    Output:
        results (list of dicts):
            Each dict contains 'Species', 'Island', 'Average_bill_length_mm'
    """

    # using helper function to get (species, island) pairings & list of bill lengths
    groups = group_by_species_and_island(data)
    results = []

    for (species, island), lengths in groups.items():
        avg_length = compute_average(lengths)
        results.append({'Species': species, 
                        'Island': island,
                        'Average_bill_length_mm': round(avg_length, 2)
                        })
    return results
        







# ------------------------------------------------------
# 2. Main function (controls program flow)
# ------------------------------------------------------
def main():
    # Step 1: Read the penguin dataset
    data = read_csv("penguins.csv")
    print(f"Loaded {len(data)} penguin records.")

    # Step 2: Perform calculations
    # (you’ll later plug in your calculate_average_bill_length()
    #  and calculate_body_mass_percentage() here)
    # bill_results = calculate_average_bill_length(data)
    # mass_results = calculate_body_mass_percentage(data)

    # Step 3: Write results to output file
    # write_csv("penguins_results.csv", bill_results, mass_results)

    # For now, just check that reading worked
    print("First record example:")
    print(data[0])


    bill_results = calculate_average_bill_length(data)
    print("Average Bill Length Results:")
    for row in bill_results:
        print(row)

# ------------------------------------------------------
# 3. Run program
# ------------------------------------------------------
if __name__ == "__main__":
    main()
