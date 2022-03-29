import pytest

from utils import Post, Comment


class TestPost:
    post_pk = 1
    poster_name = 'user'
    poster_avatar = '/static/img/ava1.png'
    pic = '/static/img/post1.png'
    content = '#test'
    views = 100
    likes = 200

    def test_post_init(self):

        post = Post(
                TestPost.post_pk,
                TestPost.poster_name,
                TestPost.poster_avatar,
                TestPost.pic,
                TestPost.content,
                TestPost.views,
                TestPost.likes
        )

        assert post.pk == TestPost.post_pk, "Неправильный ID поста"
        assert post.poster == TestPost.poster_name, "Неправильное имя автора"
        assert post.poster_pic == TestPost.poster_avatar, "Неправильный адрес изображения"
        assert post.pic == TestPost.pic, "Неправильный адрес изображения"
        assert post.content_raw == TestPost.content, "Неправильный текст поста"
        assert post.views_count == TestPost.views, "Неправильное количество просмотров"
        assert post.likes_count == TestPost.likes, "Неправильный количество лайков"

    def test_view_counter(self):
        post = Post(
            TestPost.post_pk,
            TestPost.poster_name,
            TestPost.poster_avatar,
            TestPost.pic,
            TestPost.content,
            TestPost.views,
            TestPost.likes
        )
        post.add_view()

        assert post.views_count == TestPost.views + 1, "Неправильное количество просмотров"

    def test_like_counter(self):
        post = Post(
            TestPost.post_pk,
            TestPost.poster_name,
            TestPost.poster_avatar,
            TestPost.pic,
            TestPost.content,
            TestPost.views,
            TestPost.likes
        )
        post.add_like()

        assert post.likes_count == TestPost.likes + 1, "Неправильный количество лайков"

    def test_get_content(self):
        post = Post(
            TestPost.post_pk,
            TestPost.poster_name,
            TestPost.poster_avatar,
            TestPost.pic,
            TestPost.content,
            TestPost.views,
            TestPost.likes
        )

        assert post.content == f'<a href="/tag/test">#test</a>', "Неправильный количество лайков"

    def test_get_preview(self):
        post = Post(
            TestPost.post_pk,
            TestPost.poster_name,
            TestPost.poster_avatar,
            TestPost.pic,
            'test' * 30,
            TestPost.views,
            TestPost.likes
        )

        assert len(post.get_preview()) == 53, "Неправильный длина превью"