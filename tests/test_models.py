from models.user import User

def test_user_creation():
    user = User(clerk_id="clk_123", email="test@test.com", locale="en", tier="free")
    assert user.clerk_id == "clk_123"
