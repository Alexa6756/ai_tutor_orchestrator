from src.state_postgres import PostgresStateManager

def test_upsert_get_user():
    state = PostgresStateManager()
    user_info = {"user_id":"test123","name":"Test User"}
    state.upsert_user(user_info)
    fetched = state.get_user("test123")
    assert fetched['name'] == "Test User"
