import os
from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# define database tables
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    comics = db.relationship('Comic', backref='author', cascade="delete")


class Comic(db.Model):
    __tablename__ = 'comics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    year = db.Column(db.Integer)
    lyrics = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/authors')
def show_all_authors():
    authors = Author.query.all()
    return render_template('author-all.html', authors=authors)


@app.route('/author/add', methods=['GET', 'POST'])
def add_authors():
    if request.method == 'GET':
        return render_template('author-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        about = request.form['about']

        # insert the data into the database
        author = Author(name=name, about=about)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('show_all_authors'))


@app.route('/api/author/add', methods=['POST'])
def add_ajax_authors():
    # get data from the form
    name = request.form['name']
    about = request.form['about']

    # insert the data into the database
    author = Author(name=name, about=about)
    db.session.add(author)
    db.session.commit()
    # flash message type: success, info, warning, and danger from bootstrap
    flash('Author Inserted', 'success')
    return jsonify({"id": str(author.id), "name": author.name})


@app.route('/author/edit/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    author = Author.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('author-edit.html', author=author)
    if request.method == 'POST':
        # update data based on the form data
        author.name = request.form['name']
        author.about = request.form['about']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_authors'))


@app.route('/author/delete/<int:id>', methods=['GET', 'POST'])
def delete_author(id):
    author = Author.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('author-delete.html', author=author)
    if request.method == 'POST':
        # delete the author by id
        # all related comics are deleted as well
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('show_all_authors'))


@app.route('/api/author/<int:id>', methods=['DELETE'])
def delete_ajax_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"id": str(author.id), "name": author.name})


# comic-all.html adds comic id to the edit button using a hidden input
@app.route('/comics')
def show_all_comics():
    comics = Comic.query.all()
    return render_template('comic-all.html', comics=comics)


@app.route('/comic/add', methods=['GET', 'POST'])
def add_comics():
    if request.method == 'GET':
        authors = Author.query.all()
        return render_template('comic-add.html', authors=authors)
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        year = request.form['year']
        lyrics = request.form['lyrics']
        author_name = request.form['author']
        author = Author.query.filter_by(name=author_name).first()
        comic = Comic(name=name, year=year, lyrics=lyrics, author=author)

        # insert the data into the database
        db.session.add(comic)
        db.session.commit()
        return redirect(url_for('show_all_comics'))


@app.route('/comic/edit/<int:id>', methods=['GET', 'POST'])
def edit_comic(id):
    comic = Comic.query.filter_by(id=id).first()
    authors = Author.query.all()
    if request.method == 'GET':
        return render_template('comic-edit.html', comic=comic, authors=authors)
    if request.method == 'POST':
        # update data based on the form data
        comic.name = request.form['name']
        comic.year = request.form['year']
        comic.lyrics = request.form['lyrics']
        author_name = request.form['author']
        author = Author.query.filter_by(name=author_name).first()
        comic.author = author
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_comics'))


@app.route('/comic/delete/<int:id>', methods=['GET', 'POST'])
def delete_comic(id):
    comic = Comic.query.filter_by(id=id).first()
    authors = Author.query.all()
    if request.method == 'GET':
        return render_template('comic-delete.html', comic=comic, authors=authors)
    if request.method == 'POST':
        # use the id to delete the comic
        # comic.query.filter_by(id=id).delete()
        db.session.delete(comic)
        db.session.commit()
        return redirect(url_for('show_all_comics'))


@app.route('/api/comic/<int:id>', methods=['DELETE'])
def delete_ajax_comic(id):
    comic = Comic.query.get_or_404(id)
    db.session.delete(comic)
    db.session.commit()
    return jsonify({"id": str(comic.id), "name": comic.name})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def show_all_users():
    return render_template('user-all.html')


@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    # how to get form data is different for GET vs. POST
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        # return render_template('form-demo.html', first_name=first_name)
        return redirect(url_for('form_demo'))


@app.route('/user/<string:name>/')
def get_user_name(name):
    # return "hello " + name
    # return "Hello %s, this is %s" % (name, 'administrator')
    return render_template('user.html', name=name)


@app.route('/comic/<int:id>/')
def get_comic_id(id):
    # return "This comic's ID is " + str(id)
    return "Hi, this is %s and the comic's id is %d" % ('administrator', id)


# https://goo.gl/Pc39w8 explains the following line
if __name__ == '__main__':

    # activates the debugger and the reloader during development
    # app.run(debug=True)
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)
