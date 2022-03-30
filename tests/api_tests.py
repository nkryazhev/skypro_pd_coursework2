import pytest

from app import app

VALID_KEYS = ['pk', 'poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count']


def test_posts_endpoint():
    response = app.test_client().get('/api/posts')
    posts = response.json
    assert response.status_code == 200
    assert isinstance(posts, list) is True, "api выдало неверный тип"
    for post in posts:
        for key in post.keys():
            assert key in VALID_KEYS, "Поле невалидно"


def test_single_post_endpoint():
    response = app.test_client().get(f'/api/posts/5')
    post = response.json

    assert response.status_code == 200
    assert isinstance(post, dict) is True, "api выдало неверный тип"
    for key in post.keys():
        assert key in VALID_KEYS, "Поле невалидно"
