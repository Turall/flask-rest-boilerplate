class TestHealthController:
    def test__search_hello(self, client, session):
        res = client.get("/api/hello")
        assert res.status_code == 200
        assert res.json == {"message": "Hello, World!"}
