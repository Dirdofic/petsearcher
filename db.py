import pandas as pd

# Define the CSV file names
FOUND_PETS_CSV_FILE_NAME = 'found_pets.csv'
LOST_PETS_CSV_FILE_NAME = 'lost_pets.csv'

# Define the CSV headers
CSV_HEADERS = ['TelegramUname', 'PetInfo']

# Create the CSV files if they don't exist
try:
    df_found = pd.read_csv(FOUND_PETS_CSV_FILE_NAME)
except FileNotFoundError:
    df_found = pd.DataFrame(columns=CSV_HEADERS)
    df_found.to_csv(FOUND_PETS_CSV_FILE_NAME, index=False)

try:
    df_lost = pd.read_csv(LOST_PETS_CSV_FILE_NAME)
except FileNotFoundError:
    df_lost = pd.DataFrame(columns=CSV_HEADERS)
    df_lost.to_csv(LOST_PETS_CSV_FILE_NAME, index=False)

def write_found_pet_to_csv(username, info):
    new_row = pd.DataFrame([[username, info]], columns=CSV_HEADERS)
    df = pd.read_csv(FOUND_PETS_CSV_FILE_NAME)
    df = pd.concat([df, new_row])
    df.to_csv(FOUND_PETS_CSV_FILE_NAME, index=False)

def write_lost_pet_to_csv(username, info):
    new_row = pd.DataFrame([[username, info]], columns=CSV_HEADERS)
    df = pd.read_csv(LOST_PETS_CSV_FILE_NAME)
    df = pd.concat([df, new_row])
    df.to_csv(LOST_PETS_CSV_FILE_NAME, index=False)

def read_found_pets_csv():
    return pd.read_csv(FOUND_PETS_CSV_FILE_NAME)

def read_lost_pets_csv():
    return pd.read_csv(LOST_PETS_CSV_FILE_NAME)