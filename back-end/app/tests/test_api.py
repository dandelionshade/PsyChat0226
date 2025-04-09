import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.models import User
from app.core.security import get_password_hash

# 创建内存数据库用于测试
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 创建测试客户端
client = TestClient(app)

# 测试数据
test_user = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
}

test_navigation = {
    "title": "测试导航",
    "description": "这是一个测试导航内容",
    "url": "https://example.com"
}

test_chat = {
    "message": "这是一条测试消息"
}


@pytest.fixture(name="session")
def session_fixture():
    """创建数据库会话"""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="test_db_user")
def test_db_user(session: Session):
    """创建测试用户"""
    user = User(
        email=test_user["email"],
        username=test_user["username"],
        password_hash=get_password_hash(test_user["password"]),
        role="user"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_register():
    """测试用户注册"""
    response = client.post(
        "/api/register",
        json=test_user
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]
    assert "id" in data


def test_login():
    """测试用户登录"""
    # 先注册用户
    client.post("/api/register", json=test_user)
    
    # 测试登录
    response = client.post(
        "/api/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_chat_api(test_db_user):
    """测试聊天API"""
    # 先登录获取token
    login_response = client.post(
        "/api/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试发送消息
    response = client.post(
        "/api/chat/send",
        json=test_chat,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == test_chat["message"]
    assert "response" in data
    assert "id" in data
    
    # 测试获取历史记录
    response = client.get("/api/chat/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_navigation_api(test_db_user):
    """测试导航内容API"""
    # 先登录获取token
    login_response = client.post(
        "/api/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试创建导航内容
    response = client.post(
        "/api/navigation/",
        json=test_navigation,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_navigation["title"]
    assert data["description"] == test_navigation["description"]
    assert data["url"] == test_navigation["url"]
    assert "id" in data
    navigation_id = data["id"]
    
    # 测试获取导航内容列表
    response = client.get("/api/navigation/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
    # 测试获取特定导航内容
    response = client.get(f"/api/navigation/{navigation_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == navigation_id
    
    # 测试更新导航内容
    update_data = {"title": "更新的标题"}
    response = client.put(
        f"/api/navigation/{navigation_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    
    # 测试删除导航内容
    response = client.delete(f"/api/navigation/{navigation_id}", headers=headers)
    assert response.status_code == 204