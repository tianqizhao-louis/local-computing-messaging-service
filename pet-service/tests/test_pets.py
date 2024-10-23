import pytest


@pytest.mark.asyncio
async def test_database_connection(test_database):
    """Test that we're using SQLite in memory database"""
    # Check if the connection is SQLite
    assert str(test_database.url).startswith("sqlite:")
    assert "memory" in str(test_database.url)

    # Verify we can execute a simple query
    query = (
        "SELECT 1;"  # Changed to a simpler query that works in both SQLite and Postgres
    )
    result = await test_database.fetch_one(query)
    assert result is not None


@pytest.fixture
def sample_pet():
    return {
        "name": "Test Pet",
        "type": "Dog",
        "price": 99.99,
        "breeder_id": "123",
    }


@pytest.fixture
def updated_pet():
    return {
        "name": "Updated Pet",
        "type": "Cat",
        "price": 199.99,
        "breeder_id": "456",
    }


@pytest.mark.asyncio
async def test_get_pets(test_client):
    response = test_client.get("/api/v1/pets/")
    assert response.status_code == 200
    assert response.json()["links"] is not None


@pytest.mark.asyncio
async def test_create_and_get_pet(test_client, sample_pet):
    response = test_client.post("/api/v1/pets/", json=sample_pet)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == sample_pet["name"]
    assert data["type"] == sample_pet["type"]
    assert data["price"] == sample_pet["price"]
    assert data["breeder_id"] == sample_pet["breeder_id"]
    assert "id" in data

    # Verify it was created
    get_response = test_client.get("/api/v1/pets/")
    assert get_response.status_code == 200
    assert len(get_response.json()["data"]) == 1

    # Get specific breeder
    get_one_response = test_client.get(f"/api/v1/pets/{data['id']}")
    assert get_one_response.status_code == 200
    assert get_one_response.json() == data


@pytest.mark.asyncio
async def test_update_pet(test_client, sample_pet, updated_pet):
    create_response = test_client.post("/api/v1/pets/", json=sample_pet)
    assert create_response.status_code == 201
    pet_id = create_response.json()["id"]

    # Update the breeder
    update_response = test_client.put(
        f"/api/v1/pets/{pet_id}", 
        json=updated_pet
    )
    assert update_response.status_code == 200
    
    updated_data = update_response.json()
    assert updated_data["id"] == pet_id
    assert updated_data["name"] == updated_pet["name"]
    assert updated_data["type"] == updated_pet["type"]
    assert updated_data["price"] == updated_pet["price"]
    assert updated_data["breeder_id"] == updated_pet["breeder_id"]

    # Verify the update
    get_response = test_client.get(f"/api/v1/pets/{pet_id}")
    assert get_response.status_code == 200
    assert get_response.json() == updated_data


@pytest.mark.asyncio
async def test_update_pet_invalid_id(test_client, updated_pet):
    """Test PUT with invalid breeder ID"""
    response = test_client.put(
        "/api/v1/pets/invalid-id",
        json=updated_pet
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_pet(test_client, sample_pet):
    """Test DELETE /api/v1/pets/{id} endpoint"""
    # First create a breeder
    create_response = test_client.post("/api/v1/pets/", json=sample_pet)
    assert create_response.status_code == 201
    pet_id = create_response.json()["id"]

    # Delete the breeder
    delete_response = test_client.delete(f"/api/v1/pets/{pet_id}")
    assert delete_response.status_code == 200

    # Verify the breeder was deleted
    get_response = test_client.get(f"/api/v1/pets/{pet_id}")
    assert get_response.status_code == 404

    # Verify the breeder is not in the list
    list_response = test_client.get("/api/v1/pets/")
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 0


@pytest.mark.asyncio
async def test_delete_pet_invalid_id(test_client):
    """Test DELETE with invalid breeder ID"""
    response = test_client.delete("/api/v1/pets/invalid-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_pet_invalid_data(test_client):
    """Test GET with invalid data"""
    response = test_client.get("/api/v1/pets/123")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_cleanup_between_tests(test_client, test_database):
    """Verify that the database is clean between tests"""
    # This should be empty as it's a fresh database
    response = test_client.get("/api/v1/pets/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 0
