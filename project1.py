# SI 201 Project 1
# Your name: Olivia Lombardo
# Your student id: 1877 2895
# Your email: livlomb@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): generative AI (ChatGPT)
# If you worked with generative AI also add a statement for how you used it: 
# I used ChatGPT to help me understand the project outline, identify useful helper functions, and define my research questions.
# I also used it to help me debug some of my functions once I completed the general structure and code.

import csv
import os

# ------------------------------------------------------
# 1. Read CSV
# ------------------------------------------------------
def read_csv(filename):
    """
    Reads the dataset into a list of dictionaries,
    where each dictionary represents one penguins data.

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
        groups (dict): keys = (species, island), values = list of bill lengths (floats)
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
# 4. Helper Functions for calculate_body_mass_percentage
# ------------------------------------------------------

def compute_species_avg_body_mass(data):
    """
    Computes the average body mass for each species.

    Input:
        data (list of dicts)
    Output:
        species_avg (dictionary): keys = species, values = average body mass (float)
    """
    species_groups = {}
    for penguin in data:
        species = penguin['species']
        mass = penguin['body_mass_g']

        if mass in ("", "NA", "NaN", None):
            continue  # skip missing data

        try:
            mass = float(mass)
        except ValueError:
            continue  # if conversion fails, skip this record

        if species not in species_groups:
            species_groups[species] = []
        species_groups[species].append(mass)

        # Now computing averages per species
    species_avg = {}
    for species, masses in species_groups.items():
        if masses:
            avg = sum(masses) / len(masses)
            species_avg[species] = round(avg, 2)
        else:
            species_avg[species] = 0.0

    return species_avg


def filter_by_species_and_sex(data, species, sex):
    """
    Filters dataset for penguins of a specific species and sex.

    Input:
        data (list of dicts), species (string), sex (string)

    Output:
        values (list of floats (body masses))
    """
    values = []

    for penguin in data:
        if penguin['species'] != species or penguin['sex'] != sex:
            continue

        mass = penguin['body_mass_g']

        if mass in ("", "NA", "NaN", None):
            continue

        try:
            mass = float(mass)
        except ValueError:
            continue

        values.append(mass)

    return values


def compute_percentage_above_avg(values, avg_mass):
    """
    Calculates the percentage of penguins with body mass greater than the species' average.

    Input:
        values (list of floats)
        avg_mass (float)
    Output:
        percentage (float)
    """
    if len(values) == 0:  # checking if the list is empty
        return 0.0

    count_above = 0
    for val in values:
        if val > avg_mass:
            count_above += 1
    
    percentage = (count_above / len(values)) * 100
    return round(percentage, 2)

# ------------------------------------------------------
# 5. calculate_body_mass_percentage Function
# ------------------------------------------------------
def calculate_body_mass_percentage(data):
    """
    Calculates, for each species and sex, the % of penguins above their species average body mass.

    Input:
        data (list of dicts)
    Output:
        results (list of dicts):
            Each dict contains 'Species', 'Sex', '%_above_avg_bodymass'
    """
    results = []

    species_avg = compute_species_avg_body_mass(data)
    
    for species, avg_mass in species_avg.items():
        for sex in ['male', 'female']:
            values = filter_by_species_and_sex(data, species, sex)
            percent_above = compute_percentage_above_avg(values, avg_mass)

            results.append({
                    "Species": species,
                    "Sex": sex,
                    "%_above_avg_bodymass": percent_above
                })

    return results

# ------------------------------------------------------
# 6. Main function (controls program flow)
# ------------------------------------------------------
def main():
    # Step 1: Read the penguin dataset
    data = read_csv("penguins.csv")
    print(f"Loaded {len(data)} penguin records.")

    # check that reading worked
    print("First record example:")
    print(data[0])


    bill_results = calculate_average_bill_length(data)
    print("\nAverage bill length results:")
    for row in bill_results:
        print(row)

    mass_results = calculate_body_mass_percentage(data)
    print("\nPercentage of penguins above their species average body mass results:")
    for row in mass_results:
        print(row)


if __name__ == "__main__":
    main()