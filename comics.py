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
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    characters = db.relationship('Character', backref='company', cascade="delete")


class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    year = db.Column(db.Integer)
    creator = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/companies')
def show_all_companies():
    companies = company.query.all()
    return render_template('company-all.html', companies=companies)


@app.route('/company/add', methods=['GET', 'POST'])
def add_companies():
    if request.method == 'GET':
        return render_template('company-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        about = request.form['about']

        # insert the data into the database
        company = company(name=name, about=about)
        db.session.add(company)
        db.session.commit()
        return redirect(url_for('show_all_companies'))


@app.route('/api/company/add', methods=['POST'])
def add_ajax_companies():
    # get data from the form
    name = request.form['name']
    about = request.form['about']

    # insert the data into the data

    company = company(name=name, about=about)
    db.session.add(company)
    db.session.commit()
    # flash message type: success, info, warning, and danger from bootstrap
    flash('company Inserted', 'success')
    return jsonify({"id": str(company.id), "name": company.name})


@app.route('/company/edit/<int:id>', methods=['GET', 'POST'])
def edit_company(id):
    company = company.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('company-edit.html', company=company)
    if request.method == 'POST':
        # update data based on the form data
        company.name = request.form['name']
        company.about = request.form['about']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_companies'))


@app.route('/company/delete/<int:id>', methods=['GET', 'POST'])
def delete_company(id):
    company = company.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('company-delete.html', company=company)
    if request.method == 'POST':
        # delete the company by id
        # all related characters are deleted as well
        db.session.delete(company)
        db.session.commit()
        return redirect(url_for('show_all_companies'))


@app.route('/api/company/<int:id>', methods=['DELETE'])
def delete_ajax_company(id):
    company = company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    return jsonify({"id": str(company.id), "name": company.name})


# character-all.html adds character id to the edit button using a hidden input
@app.route('/characters')
def show_all_characters():
    characters = Character.query.all()
    return render_template('character-all.html', characters=characters)


@app.route('/character/add', methods=['GET', 'POST'])
def add_characters():
    if request.method == 'GET':
        companies = company.query.all()
        return render_template('character-add.html', companies=companies)
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        year = request.form['year']
        creators = request.form['creators']
        company_name = request.form['company']
        company = company.query.filter_by(name=company_name).first()
        character = Character(name=name, year=year, creators=creators, company=company)

        # insert the data into the database
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('show_all_characters'))


@app.route('/character/edit/<int:id>', methods=['GET', 'POST'])
def edit_character(id):
    character = Character.query.filter_by(id=id).first()
    companies = company.query.all()
    if request.method == 'GET':
        return render_template('character-edit.html', character=character, companies=companies)
    if request.method == 'POST':
        # update data based on the form data
        character.name = request.form['name']
        character.year = request.form['year']
        character.creators = request.form['creators']
        company_name = request.form['company']
        company = company.query.filter_by(name=company_name).first()
        character.company = company
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_characters'))


@app.route('/character/delete/<int:id>', methods=['GET', 'POST'])
def delete_character(id):
    character = Character.query.filter_by(id=id).first()
    companies = company.query.all()
    if request.method == 'GET':
        return render_template('character-delete.html', character=character, companies=companies)
    if request.method == 'POST':
        # use the id to delete the character
        # character.query.filter_by(id=id).delete()
        db.session.delete(character)
        db.session.commit()
        return redirect(url_for('show_all_characters'))


@app.route('/api/character/<int:id>', methods=['DELETE'])
def delete_ajax_character(id):
    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({"id": str(character.id), "name": character.name})


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


@app.route('/character/<int:id>/')
def get_character_id(id):
    # return "This character's ID is " + str(id)
    return "Hi, this is %s and the character's id is %d" % ('administrator', id)



if __name__ == '__main__':
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)
