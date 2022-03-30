from flask import Blueprint, render_template, redirect
from utils import PostManager, BookmarkManager
import logging

bookmarks_bp = Blueprint('bookmarks_blueprint', __name__, template_folder='templates')


@bookmarks_bp.route('/')
def page_bookmarks():
    logging.info("Запрошена страница закладок")

    # Create BookmarkManager and get bookmarks
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    # Create PostManager and get posts
    post_mngr = PostManager()
    posts = post_mngr.get_bookmarked_posts(bookmarks)

    return render_template("bookmarks.html", posts=posts, bookmarks=bookmarks)


@bookmarks_bp.route('/add/<int:post_id>', methods=['POST'])
def add_bookmark_view(post_id):
    logging.info(f"Запрос добавить пост ID: {post_id} в закладки")

    # Create BookmarkManager and add bookmark
    bkm_mngr = BookmarkManager()
    bkm_mngr.add_bookmark(post_id)

    return redirect("/", code=302)


@bookmarks_bp.route('/remove/<int:post_id>', methods=['POST'])
def remove_bookmark_view(post_id):
    logging.info(f"Запрос удалить пост ID: {post_id} из закладок")

    # Create BookmarkManager and remove bookmark
    bkm_mngr = BookmarkManager()
    bkm_mngr.remove_bookmark(post_id)

    return redirect("/", code=302)
