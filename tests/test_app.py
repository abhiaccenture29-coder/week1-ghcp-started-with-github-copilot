"""
FastAPI test suite for the Mergington High School Activities API.
Tests follow the AAA (Arrange-Act-Assert) pattern.
"""

from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_success(self, reset_activities):
        """
        Test that GET /activities returns 200 with expected structure.

        ARRANGE: TestClient is initialized
        ACT: Send GET request to /activities
        ASSERT: Verify 200 status and response contains activity data
        """
        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

        # Verify structure of an activity
        assert "description" in data["Chess Club"]
        assert "schedule" in data["Chess Club"]
        assert "max_participants" in data["Chess Club"]
        assert "participants" in data["Chess Club"]
        assert isinstance(data["Chess Club"]["participants"], list)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_email_success(self, reset_activities):
        """
        Test successful signup of a new student.

        ARRANGE: New email address that is not yet registered
        ACT: POST request to signup endpoint
        ASSERT: Verify 200 status, success message, and participant is added
        """
        # ARRANGE
        test_email = "newstudent@mergington.edu"
        activity_name = "Chess Club"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # ASSERT
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert test_email in activities[activity_name]["participants"]

    def test_signup_duplicate_email_error(self, reset_activities):
        """
        Test signup with an email already registered for the activity.

        ARRANGE: Email that already exists in the activity's participants
        ACT: POST request to signup with duplicate email
        ASSERT: Verify 400 status and error detail
        """
        # ARRANGE
        existing_email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found_error(self, reset_activities):
        """
        Test signup to a non-existent activity.

        ARRANGE: Activity that does not exist
        ACT: POST request to non-existent activity
        ASSERT: Verify 404 status and error detail
        """
        # ARRANGE
        fake_activity = "Fake Activity"
        test_email = "test@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": test_email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/participants endpoint."""

    def test_unregister_success(self, reset_activities):
        """
        Test successful unregistration of a participant.

        ARRANGE: Participant that exists in an activity
        ACT: DELETE request to unregister
        ASSERT: Verify 200 status, success message, and participant is removed
        """
        # ARRANGE
        email_to_unregister = "michael@mergington.edu"
        activity_name = "Chess Club"
        # Verify participant exists before test
        assert email_to_unregister in activities[activity_name]["participants"]

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_unregister}
        )

        # ASSERT
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email_to_unregister not in activities[activity_name]["participants"]

    def test_unregister_participant_not_found_error(self, reset_activities):
        """
        Test unregister for a participant not in the activity.

        ARRANGE: Email that does not exist in the activity
        ACT: DELETE request with non-existent email
        ASSERT: Verify 404 status and error detail
        """
        # ARRANGE
        nonexistent_email = "nonexistent@mergington.edu"
        activity_name = "Chess Club"

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": nonexistent_email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_unregister_activity_not_found_error(self, reset_activities):
        """
        Test unregister from a non-existent activity.

        ARRANGE: Activity that does not exist
        ACT: DELETE request from non-existent activity
        ASSERT: Verify 404 status and error detail
        """
        # ARRANGE
        fake_activity = "Fake Activity"
        test_email = "test@mergington.edu"

        # ACT
        response = client.delete(
            f"/activities/{fake_activity}/participants",
            params={"email": test_email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
