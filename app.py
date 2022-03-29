from flask import Flask, request, render_template, send_from_directory, g
import logging

from werkzeug.utils import redirect

from utils import PostManager, BookmarkManager

logging.basicConfig(filename="basic.log", level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def page_index():
    logging.info("Главная страница запрошена")
    post_mngr = PostManager()
    bkm_mngr = BookmarkManager()
    posts = post_mngr.get_all_posts()
    bookmarks = bkm_mngr.get_bookmarks()
    bookmarks_num = bkm_mngr.get_bookmarks_num()

    if not bookmarks:
        bookmarks = [0]
    return render_template("index.html",
                           posts=posts,
                           bookmarks=bookmarks,
                           bookmarks_num=bookmarks_num
                           )

@app.route('/bookmarks')
def page_bookmarks():
    logging.info("Главная страница запрошена")
    post_mngr = PostManager()
    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()
    posts = post_mngr.get_bookmarked_posts(bookmarks)

    return render_template("bookmarks.html",
                           posts=posts,
                           bookmarks=bookmarks)


# view /
@app.route('/posts/<int:post_id>')
def post_page(post_id):
    logging.info("Главная страница запрошена")
    post_mngr = PostManager()
    post = post_mngr.get_post_by_pk(post_id)

    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    return render_template("post.html",
                           post=post,
                           bookmarks=bookmarks
                           )


# view /search
@app.route('/search')
def page_search():
    req = request.args['s']
    logging.info(f"Запрошен поиск постов по слову: {req}")

    post_mngr = PostManager()

    # try:
    posts_by_word = post_mngr.search_for_posts(req)

    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    if posts_by_word:
        logging.info(f"Найдено {len(posts_by_word)} постов")
        return render_template("search.html",
                               posts=posts_by_word,
                               req=req,
                               bookmarks=bookmarks
                               )
    else:
        logging.info(f"Постов не найдено")
        return f"По запросу {req} ничего ненайдено"
    # except DataLayerError:
    #     logging.info(f"Возникла ошибка с чтением из файла")
    #     return "Ошибка чтения файла с данными"


# view /
@app.route('/tag/<tagname>')
def tag_page(tagname):
    logging.info("Главная страница запрошена")
    post_mngr = PostManager()
    posts_by_tag = post_mngr.search_for_posts(tagname)

    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()
    return render_template(
        "tag.html",
        posts=posts_by_tag,
        tagname=tagname,
        bookmarks=bookmarks
    )

# view /
@app.route('/bookmarks/add/<int:post_id>', methods=['POST'])
def add_bookmark_view(post_id):
    logging.info("Главная страница запрошена")
    bkm_mngr = BookmarkManager()
    bkm_mngr.add_bookmark(post_id)

    #  Для переадресации (редиректа) используйте
    return redirect("/", code=302)

@app.route('/bookmarks/remove/<int:post_id>', methods=['POST'])
def remove_bookmark_view(post_id):
    logging.info("Главная страница запрошена")
    bkm_mngr = BookmarkManager()
    bkm_mngr.remove_bookmark(post_id)

    #  Для переадресации (редиректа) используйте
    return redirect("/", code=302)




# view /
@app.route('/users/<username>')
def user_feed_page(username):
    logging.info("Главная страница запрошена")
    post_mngr = PostManager()

    bkm_mngr = BookmarkManager()
    bookmarks = bkm_mngr.get_bookmarks()

    return render_template(
        "user-feed.html",
        posts=post_mngr.get_posts_by_user(username),
        username=username,
        bookmarks=bookmarks
    )


if __name__ == '__main__':
    app.run(debug=True)
