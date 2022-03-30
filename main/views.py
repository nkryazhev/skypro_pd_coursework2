from flask import Blueprint, render_template, request
from utils import PostManager, BookmarkManager
import logging

main_bp = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_bp.route('/')
def page_index():
    logging.info("Главная страница запрошена")

    # Create PostManager and get posts
    post_mngr = PostManager()
    posts = post_mngr.get_all_posts()

    # Create BookmarkManager and get bookmarks
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()
    bookmarks_num = bkm_mngr.get_bookmarks_num()

    return render_template("index.html", posts=posts,
                           bookmarks=bookmarks, bookmarks_num=bookmarks_num)


@main_bp.route('/posts/<int:post_id>')
def post_page(post_id):
    logging.info(f"Запрошена страница поста ID {post_id}")

    # Create PostManager and get post by ID
    post_mngr = PostManager()
    post = post_mngr.get_post_by_pk(post_id)

    # Create BookmarkManager and get bookmarks
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    return render_template("post.html", post=post, bookmarks=bookmarks)


@main_bp.route('/search')
def page_search():
    req = request.args['s']
    logging.info(f"Запрошен поиск постов по слову: {req}")

    # Create PostManager and get posts by words
    post_mngr = PostManager()
    posts_by_word = post_mngr.search_for_posts(req)

    # Create BookmarkManager and get bookmarks
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    if posts_by_word:
        logging.info(f"Найдено {len(posts_by_word)} постов")
        return render_template("search.html", posts=posts_by_word,
                               req=req, bookmarks=bookmarks)
    else:
        logging.info(f"Постов не найдено")
        return f"По запросу {req} ничего ненайдено"


@main_bp.route('/tag/<tagname>')
def tag_page(tagname):
    logging.info(f"Запрошен поиск постов по тэгу: {tagname}")

    # Create PostManager and get posts by words
    post_mngr = PostManager()
    posts_by_tag = post_mngr.search_for_posts(tagname)

    # Create BookmarkManager and get bookmarks
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    return render_template("tag.html", posts=posts_by_tag,
                           tagname=tagname, bookmarks=bookmarks)


@main_bp.route('/users/<username>')
def user_feed_page(username):
    logging.info("Запрошена лента пользователя")

    # Create PostManager and get posts by words
    post_mngr = PostManager()
    posts = post_mngr.get_posts_by_user(username)

    # Create BookmarkManager and get bookmarks
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    return render_template("user-feed.html", posts=posts,
                           username=username, bookmarks=bookmarks)
