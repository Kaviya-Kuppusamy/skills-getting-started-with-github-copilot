from fastapi.testclient import TestClient
import importlib

# Import the app module under test
app_module = importlib.import_module("src.app")
client = TestClient(app_module.app)


def test_get_activities():
    # Arrange: TestClient is ready and activities fixture provides initial state

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == set(app_module.activities.keys())


def test_signup_success():
    # Arrange
    activity_name = next(iter(app_module.activities.keys()))
    new_email = "testuser@example.com"
    assert new_email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Signed up" in body["message"]
    assert new_email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate():
    # Arrange
    activity_name = next(iter(app_module.activities.keys()))
    existing = app_module.activities[activity_name]["participants"][0]
    assert existing in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing}")

    # Assert
    assert response.status_code == 400


def test_remove_participant_success():
    # Arrange
    activity_name = next(iter(app_module.activities.keys()))
    existing = app_module.activities[activity_name]["participants"][0]
    assert existing in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={existing}")

    # Assert
    assert response.status_code == 200
    assert existing not in app_module.activities[activity_name]["participants"]


def test_remove_participant_not_found():
    # Arrange
    activity_name = next(iter(app_module.activities.keys()))
    nonexist = "noone@example.com"
    if nonexist in app_module.activities[activity_name]["participants"]:
        app_module.activities[activity_name]["participants"].remove(nonexist)

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={nonexist}")

    # Assert
    assert response.status_code == 404
