import json
import pprint


class PostManager:

    def __init__(self):
        self.posts_path = 'data/data.json'
        self.comments_path = 'data/comments.json'
        self.bookmarks_path = 'data/bookmarks.json'

    def load_posts(self):
        post_list = {}
        with open(self.posts_path, 'r', encoding='utf-8') as file:
            for post in json.load(file):

                _pk = post['pk']
                _user = post['poster_name']
                _user_pic = post['poster_avatar']
                _pic = post['pic']
                _content = post['content']
                _views = post['views_count']
                _likes = post['likes_count']

                post_list[_pk] = Post(_pk, _user, _user_pic, _pic, _content, _views, _likes)

        return post_list

    def load_comments(self):

        comment_list = []
        with open(self.comments_path, 'r', encoding='utf-8') as file:
            for comment in json.load(file):

                _post_id = comment['post_id']
                _pk = comment['pk']
                _user = comment['commenter_name']
                _comment = comment['comment']

                comment_list.append(Comment(_pk, _post_id, _user, _comment))
        if comment_list:
            return comment_list

    def save_json(self):
        pass

    def get_all_posts(self):
        posts = self.load_posts()
        return posts

    def get_posts_by_user(self, user_name):
        pass

    def get_comments_by_post_id(self, post_id):
        comments = self.load_comments()
        found_comments = []
        for comment in comments:
            if comment.pk == post_id:
                found_comments.append(comment)
        if found_comments:
            return found_comments

    def get_post_by_pk(self, pk):
        posts = self.load_posts()
        return posts[pk]

    def search_for_posts(self, query):
        pass

class




class Post:

    def __init__(self, pk, user, user_pic, pic, content, views, likes):
        self.pk = pk
        self.poster = user
        self.poster_pic = user_pic
        self.pic = pic
        self.content = content
        self.views_count = views
        self.likes_count = likes

    def __repr__(self):
        rep = 'Post(ID: ' + str(self.pk) + ', user: ' + self.poster + ', comments: ' + str(len(self.comments)) + ')'
        return rep

    # def add_comment(self, comment):
    #     self.comments.append(comment)
    #
    # def get_comments(self):
    #     return self.comments

    def add_view(self):
        self.views_count += 1

    def add_like(self):
        self.likes_count += 1

    def get_preview(self) -> str:
        """Function returns post content preview string"""
        if len(self.content) > 80:
            return self.content[0:80] + '...'
        else:
            return self.content

    def get_comments_num(self):
        comment_num = len(self.comments)
        return f'{comment_num} комментариев'

class Comment:

    def __init__(self, pk, post_id, user, comment):
        self.pk = pk
        self.post_id = post_id
        self.commenter = user
        self.comment = comment

    def __repr__(self):
        rep = 'Comment(ID: ' + str(self.pk) + ', user: ' + self.commenter + ', post_id: ' + str(self.post_id) + ')'
        return rep


# pmanager = PostManager()
# a = pmanager.load_json()
# pprint.pprint(a)