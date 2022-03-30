import pytest

from utils import Post, PostManager


@pytest.fixture()
def create_post():
    return Post(1, 'user', '/static/img/ava1.png',
                '/static/img/post1.png', '#test', 100, 200)

@pytest.fixture()
def create_p_manager():
    return PostManager()



class TestPost:

    def test_post_init(self, create_post):
        assert create_post.pk == 1, "Неправильный ID поста"
        assert create_post.poster == 'user', "Неправильное имя автора"
        assert create_post.poster_pic == '/static/img/ava1.png', "Неправильный адрес изображения"
        assert create_post.pic == '/static/img/post1.png', "Неправильный адрес изображения"
        assert create_post.content_raw == '#test', "Неправильный текст поста"
        assert create_post.views_count == 100, "Неправильное количество просмотров"
        assert create_post.likes_count == 200, "Неправильный количество лайков"

    def test_view_counter(self, create_post):
        create_post.add_view()
        assert create_post.views_count == 101, "Неправильное количество просмотров"

    def test_like_counter(self, create_post):
        create_post.add_like()
        assert create_post.likes_count == 201, "Неправильное количество лайков"

    def test_get_content(self, create_post):
        assert create_post.content == f'<a href="/tag/test">#test</a>', "Неправильно обработан хэштег"

    def test_get_preview(self, create_post):
        create_post.content_raw = 'test' * 30
        assert len(create_post.get_preview()) == 53, "Неправильный длина превью"

class TestPostManager:

    def test_p_manager_init(self, create_p_manager):
        assert create_p_manager.posts_path == 'data.json', "Неправильное название файла"
        assert create_p_manager.comments_path == 'comments.json', "Неправильное название файла"

    def test_p_manager_get_all_posts(self, create_p_manager):
        posts = create_p_manager.get_all_posts()
        assert bool(posts) is True, "get_all_posts вернул пустой список"

    def test_p_manager_get_post_by_pk(self, create_p_manager):
        post = create_p_manager.get_post_by_pk(2)
        assert bool(post) is True, "get_post_by_pk не вернул пост"
        assert post.pk == 2, "Найден пост с неправильным ID"

    def test_p_manager_get_posts_by_user(self, create_p_manager):
        posts = create_p_manager.get_posts_by_user('leo')
        assert bool(posts) is True, "get_posts_by_user вернул пустой список"
        for post in posts:
            assert post.poster == 'leo', "Найден пост с другого автора"

    def test_p_manager_search_for_posts(self,  create_p_manager):
        posts = create_p_manager.search_for_posts('кот')
        assert bool(posts) is True, "search_for_posts вернул пустой список"
        for post in posts:
            assert 'кот' in post.content_raw, "В посте не встречается искомое слово"




