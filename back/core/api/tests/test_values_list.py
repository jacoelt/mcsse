def test_values_list(
    client,
    db,
    server_list_with_specific_servers,
):
    """
    Test the values list endpoint.
    """
    response = client.get("/api/values-lists")
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    data = response.json()

    assert "versions" in data, "Versions list is missing"
    assert "editions" in data, "Editions list is missing"
    assert "countries" in data, "Countries list is missing"
    assert "languages" in data, "Languages list is missing"
    assert "tags" in data, "Tags list is missing"
    assert "dates" in data, "Dates list is missing"
    assert "statuses" in data, "Statuses list is missing"
    assert "max_votes" in data, "Max votes value is missing"
    assert "max_online_players" in data, "Max online players value is missing"
    assert "max_max_players" in data, "Max max players value is missing"

    assert data["versions"] == [
        "1.16",
        "1.17",
        "1.18",
        "1.19",
        "1.19.1",
        "1.19.2",
        "1.19.3",
        "1.20",
        "1.21",
        "1.21.1",
    ], "Versions list does not match expected values"

    assert data["editions"] == [
        {"value": "java", "label": "Java"},
        {"value": "bedrock", "label": "Bedrock"},
        {"value": "both", "label": "Java & Bedrock"},
    ], "Editions list does not match expected values"

    assert data["countries"] == [
        "ca",
        "us",
    ], "Countries list does not match expected values"

    assert data["languages"] == [
        "en",
        "es",
        "fr",
    ], "Languages list does not match expected values"

    assert data["tags"] == [
        {
            "name": f"tag{i}",
            "description": f"Tag {i}",
            "relevance": i,
        }
        for i in range(1, 20)
    ], "Tags list does not match expected values"

    assert data["dates"] == [
        {"label": "Last 24 hours", "value": 1},
        {"label": "Last 7 days", "value": 7},
        {"label": "Last month", "value": 30},
        {"label": "Last 3 months", "value": 90},
        {"label": "Last 6 months", "value": 180},
        {"label": "Last year", "value": 365},
        {"label": "Last 5 years", "value": 1825},
        {"label": "All time", "value": -1},  # -1 for all time
    ], "Dates list does not match expected values"

    assert data["statuses"] == [
        {"value": "online", "label": "Online"},
        {"value": "offline", "label": "Offline"},
        {"value": "unknown", "label": "Unknown"},
    ], "Statuses list does not match expected values"

    assert data["max_votes"] == 1000, "Max votes value does not match expected value"

    assert (
        data["max_online_players"] == 99
    ), "Max online players value does not match expected value"

    assert (
        data["max_max_players"] == 200
    ), "Max max players value does not match expected value"
