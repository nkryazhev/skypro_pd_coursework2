import json
import config


def read_json(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, 'w', encoding="utf-8") as file:
        if isinstance(data, set):
            return json.dump(data, file, cls=SetEncoder, ensure_ascii=False, indent=4)
        else:
            return json.dump(data, file, ensure_ascii=False, indent=4)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class BookmarkManager:

    def __init__(self):
        self.bookmarks_path = config.BOOKMARKS_PATH

    def add_bookmark(self, post_id):

        bookmarks = read_json(self.bookmarks_path)
        bookmarks.append(post_id)
        save_json(self.bookmarks_path, set(bookmarks))

    def remove_bookmark(self, post_id):

        bookmarks = read_json(self.bookmarks_path)
        bookmarks.remove(post_id)
        save_json(self.bookmarks_path, set(bookmarks))

    def get_bookmarks(self):
        return read_json(self.bookmarks_path)

    def get_bookmarks_num(self):
        bookmarks = read_json(self.bookmarks_path)
        if bookmarks:
            return len(bookmarks)
        else:
            return 0


class PostManager:

    def __init__(self):
        self.posts_path = config.POSTS_PATH
        self.comments_path = config.COMMENTS_PATH

    def load_posts(self) -> dict:

        posts_dict = {}
        posts = read_json(self.posts_path)
        comments = read_json(self.comments_path)

        # Create Post objects for data from json
        for post in posts:
            posts_dict[post['pk']] = Post(
                post['pk'],
                post['poster_name'],
                post['poster_avatar'],
                post['pic'],
                post['content'],
                post['views_count'],
                post['likes_count']
            )

        for comment in comments:
            post_id = comment['post_id']

            # if comment from database reference existing post
            # than create Comment object and link it to Post
            if post_id in posts_dict.keys():
                posts_dict[post_id].add_comment(
                    Comment(comment['pk'],
                            comment['post_id'],
                            comment['commenter_name'],
                            comment['comment']
                            )
                )
        return posts_dict

    def get_all_posts(self) -> list:
        posts = self.load_posts()
        return posts

    def get_post_by_pk(self, pk) -> object:
        posts = self.load_posts()
        return posts[pk]

    def get_posts_by_user(self, user_name) -> list:
        found_posts = []
        posts = self.load_posts()
        for post in posts.values():
            if post.poster == user_name:
                found_posts.append(post)
        if found_posts:
            return found_posts

    def get_bookmarked_posts(self, bookmarks) -> list:
        found_posts = []
        posts = self.load_posts()
        for post_id in bookmarks:
            found_posts.append(posts[post_id])
        if found_posts:
            return found_posts

    def search_for_posts(self, query) -> list:
        found_posts = []
        posts = self.load_posts()
        for post in posts.values():
            if post.has_substring(query):
                found_posts.append(post)
        if found_posts:
            return found_posts


class Post:

    def __init__(self, pk, user, user_pic, pic, content, views, likes):
        self.pk = pk
        self.poster = user
        self.poster_pic = user_pic
        self.pic = pic
        self.content_raw = content
        self.content = self.convert_tags_to_links(self.content_raw)
        self.views_count = views
        self.likes_count = likes
        self.comments = []

    def __repr__(self):
        rep = 'Post(ID: ' + str(self.pk) + ', user: ' + self.poster + ', comments: ' + str(len(self.comments)) + ')'
        return rep

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments

    def add_view(self):
        self.views_count += 1

    def add_like(self):
        self.likes_count += 1

    def get_preview(self) -> str:
        """Function returns post content preview string"""
        if len(self.content) > config.PREVIEW_LIM:
            preview = self.content[0:config.PREVIEW_LIM] + '...'
        else:
            preview = self.content
        return self.convert_tags_to_links(preview)

    def get_comments_num(self):
        comment_num = len(self.comments)

        if 11 <= comment_num <= 19:
            comment_num_str = f'{comment_num} комментариев'
        elif comment_num == 0:
            comment_num_str = f'Нет комментариев'
        else:
            _n = comment_num % 10
            if _n == 1:
                comment_num_str = f'{comment_num} комментарий'
            elif _n in [2, 3, 4]:
                comment_num_str = f'{comment_num} комментария'
            else:
                comment_num_str = f'{comment_num} комментариев'

        return comment_num_str

    def has_substring(self, substring) -> bool:
        """Check if post content has requested substring"""
        if substring.lower() in self.content_raw.lower():
            return True
        else:
            return False

    @staticmethod
    def convert_tags_to_links(text):
        text_list = text.split()

        for index, word in enumerate(text_list):
            if word.startswith('#'):
                text_list[index] = f'<a href="/tag/{word[1:]}">{word}</a>'
        return ' '.join(text_list)


class Comment:

    def __init__(self, pk, post_id, user, comment):
        self.pk = pk
        self.post_id = post_id
        self.commenter = user
        self.comment = comment

    def __repr__(self):
        rep = 'Comment(ID: ' + str(self.pk) + ', user: ' + self.commenter + ', post_id: ' + str(self.post_id) + ')'
        return rep

