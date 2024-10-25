import requests
import random
import string

# URL of your API endpoint for breeders and pets
breeder_url = "http://localhost:8080/api/v1/breeders/"
pet_url = "http://localhost:8082/api/v1/pets"

# Fetch the breeder IDs from the API
def fetch_breeder_ids():
    response = requests.get(breeder_url)
    if response.status_code == 200:
        breeders = response.json()  # Assuming the data is returned as a JSON array
        # Extracting all breeder_ids
        breeder_ids = [breeder['id'] for breeder in breeders['data']]  # Ensure correct key names
        print(f"Fetched {len(breeder_ids)} breeders")
        return breeder_ids
    else:
        print(f"Failed to fetch breeders. Status Code: {response.status_code}")
        return []

# Function to generate random dummy pet data
def generate_dummy_pet(breeder_ids):
    pet_types = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Fish', 'Hamster', 'Lizard', 'Snake', 'Turtle', 'Horse']
    
    # Generate random pet name
    pet_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))

    # Choose random pet type
    pet_type = random.choice(pet_types)

    # Generate a random price between 50 and 500
    price = round(random.uniform(50, 500), 2)

    # Randomly select a breeder ID
    breeder_id = random.choice(breeder_ids)

    return {
        "name": pet_name,
        "type": pet_type,
        "price": price,
        "breeder_id": breeder_id
    }

# Main function to fetch breeders and add dummy pets
def create_dummy_pets():
    # Step 1: Fetch the breeder IDs
    breeder_ids = fetch_breeder_ids()
    if not breeder_ids:
        print("No breeders found. Exiting.")
        return

    # Step 2: Create dummy pets linked to the fetched breeders
    for _ in range(20):  # Adjust the number of dummy pets as needed
        dummy_pet = generate_dummy_pet(breeder_ids)

        # Sending the POST request to add the pet
        response = requests.post(pet_url, json=dummy_pet)

        # Checking if the request was successful
        if response.status_code == 201:
            print(f"Successfully added pet: {dummy_pet['name']}")
        else:
            print(f"Failed to add pet: {dummy_pet['name']} - Status Code: {response.status_code}")

# Run the function to create dummy pets
create_dummy_pets()
