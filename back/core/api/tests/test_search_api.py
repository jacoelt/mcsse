def test_search_result_fields(client, db, server_1):
    response = client.post("/api/servers", {}, content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    for server in data:
        assert "name" in server
        assert "ip_address_java" in server or "ip_address_bedrock" in server
        assert "versions" in server
        assert "players_online" in server
        assert "max_players" in server
        assert "added_at" in server
        assert "status" in server
        assert "total_votes" in server
        assert "country" in server
        assert "languages" in server
        assert "website" in server
        assert "discord" in server
        assert isinstance(server["tags"], list)


def test_search_all_results(client, db, server_list):
    search = {
        "page_size": 30,
    }
    response = client.post("/api/servers", search, content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 20


def test_search_query(client, db, server_list, server_with_java_url):
    search = {
        "query": "2",
    }
    response = client.post("/api/servers", search, content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    assert [server["name"] for server in data] == [
        "Test Server 12",
        "Test Server 2",
        "Test Server 20",
        "Test Server with Java url",
    ]
