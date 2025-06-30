from core.api.tests.conftest import LIST_SERVER_COUNT


def check_search_response(
    client,
    search,
    expected_length: int = None,
    expected_name: str = None,
):
    response = client.post("/api/servers", search, content_type="application/json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if expected_length is not None:
        assert len(data) == expected_length
    if expected_name:
        assert data[0]["name"] == expected_name

    return data


def test_search_result_fields(client, db, simple_server):
    data = check_search_response(
        client,
        {},
        expected_length=1,
    )
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
    check_search_response(
        client,
        search,
        expected_length=LIST_SERVER_COUNT,
    )


def test_search_query(client, db, server_list):
    search = {
        "query": "4",  # 4 is not included in the default ip addresses for the servers
    }
    data = check_search_response(
        client,
        search,
        expected_length=6,
    )

    assert [server["name"] for server in data] == [
        "Test Server 12",  # bedrock ip address has a 4 in it
        "Test Server 13",  # java ip address has a 4 in it
        "Test Server 14",
        "Test Server 2",  # bedrock ip address has a 4 in it
        "Test Server 3",  # java ip address has a 4 in it
        "Test Server 4",
    ]


def test_search_version(
    client,
    db,
    server_list,
    server_with_version_121,
    server_with_version_1211,
):
    search = {
        "versions": ["1.21"],
    }
    data = check_search_response(
        client,
        search,
        expected_length=2,
    )
    assert {server["name"] for server in data} == {
        "Test Server with Version 1.21",
        "Test Server with Version 1.21.1",
    }


def test_search_edition(
    client,
    db,
    server_list,
    server_with_no_java_ip,
    server_with_no_bedrock_ip,
):
    search = {
        "edition": "java",
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=21,  # All servers except the one without a Java IP
    )

    search = {
        "edition": "bedrock",
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=21,  # All servers except the one without a Bedrock IP
    )

    search = {
        "edition": "both",
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=20,  # All servers except the ones without either IP
    )


def test_search_players_online(
    client,
    db,
    server_list,
    server_with_high_players_online,
    server_with_low_players_online,
):
    search = {
        "players_online_min": 10,
        "players_online_max": 50,
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=20,  # All servers except specific ones have players online in this range
    )

    search = {
        "players_online_min": 50,
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with High Players Online",
    )

    search = {
        "players_online_max": 5,
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Low Players Online",
    )


def test_search_max_players(
    client,
    db,
    server_list,
    server_with_high_max_players,
    server_with_low_max_players,
):
    search = {
        "max_players_min": 50,
        "max_players_max": 150,
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=20,  # All servers except specific ones have max players in this range
    )

    search = {
        "max_players_min": 150,
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with High Max Players",
    )

    search = {
        "max_players_max": 10,
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Low Max Players",
    )


def test_search_added_at(
    client,
    db,
    server_list,
    server_added_recently,
    server_added_long_ago,
):
    search = {
        "added_at": "31d",  # 31 days
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=21,  # All servers except the one added long ago
    )

    search = {
        "added_at": "2d",  # 2 days
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server Added Recently",
    )

    search = {
        "added_at": "366d",  # 1 year
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=22,  # All servers
    )


def test_search_statuses(
    client,
    db,
    server_list,
    server_with_status_offline,
    server_with_status_unknown,
):
    search = {
        "statuses": ["online"],
        "page_size": 30,
    }
    # All servers except the offline and unknown status
    check_search_response(
        client,
        search,
        expected_length=20,
    )

    search = {
        "statuses": ["offline"],
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Status Offline",
    )

    search = {
        "statuses": ["unknown"],
    }

    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Status Unknown",
    )


def test_search_total_votes(
    client,
    db,
    server_list,
    server_with_high_total_votes,
    server_with_low_total_votes,
):
    search = {
        "total_votes_min": 500,
        "total_votes_max": 700,
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=20,  # All servers except specific ones have total votes in this range
    )

    search = {
        "total_votes_min": 800,
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with High Total Votes",
    )

    search = {
        "total_votes_max": 5,
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Low Total Votes",
    )


def test_search_countries(
    client,
    db,
    server_list,
    server_with_country_ca,
):
    search = {
        "countries": ["ca"],
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Country CA",
    )

    search = {
        "countries": ["fr"],
    }
    check_search_response(
        client,
        search,
        expected_length=0,  # No servers with country 'us'
    )

    search = {
        "countries": ["ca", "us"],
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=21,  # All servers
    )


def test_search_languages(
    client,
    db,
    server_list,
    server_with_language_es,
):
    search = {
        "languages": ["es"],
    }
    check_search_response(
        client,
        search,
        expected_length=1,
        expected_name="Test Server with Language ES",
    )

    search = {
        "languages": ["fr"],
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=20,
    )

    search = {
        "languages": ["it"],
    }
    check_search_response(
        client,
        search,
        expected_length=0,  # No servers with language 'it'
    )

    search = {
        "languages": ["es", "en"],
        "page_size": 30,
    }
    check_search_response(
        client,
        search,
        expected_length=21,  # All servers
    )


def test_search_tags(
    client,
    db,
    server_list,
    server_with_3tags,
    server_with_5tags,
    settings,
):
    settings.DEBUG = True  # Enable debug mode for tag search

    search = {
        "tags": ["tag1", "tag2"],
    }
    check_search_response(
        client,
        search,
        expected_length=2,  # Only specific servers
    )

    search = {
        "tags": ["tag1", "tag2", "tag4"],
    }
    check_search_response(
        client,
        search,
        expected_length=1,  # Only the server with 5 tags
        expected_name="Test Server with 5 Tags",
    )
