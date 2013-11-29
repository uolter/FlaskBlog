from models import Person, Article, Category
from flask import render_template, request, session, url_for, redirect, flash
from forms import SignupForm, ArticleCreateForm, ArticleUpdateForm, SigninForm, CategoryCreateForm, PersonUpdateForm
from app import app, db

@app.route('/')
def index():
    articles = Article.all()
    if 'email' in session:
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        return render_template('index.html', articles=articles, name=name)
    return render_template('index.html', articles=articles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        newperson = Person(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
        db.session.add(newperson)
        db.session.commit()
        session['email'] = newperson.email
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname

        return redirect(url_for('dashboard',name=name))
    return render_template('signup.html', form=form)

@app.route('/create', methods=['GET', 'POST'])
def article_create():
    if 'email' not in session:
        return redirect(url_for('signin'))
    person = Person.query.filter_by(email=session['email']).first()
    name = person.firstname
    article = Article()
    form = ArticleCreateForm()
    form.person_name.data = person.firstname
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=form, person=person, name=name)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if form.validate_on_submit():
      session['email'] = form.email.data
      person = Person.query.filter_by(email=session['email']).first()
      name = person.firstname
      flash('You are logged in')
      return redirect(url_for('dashboard', name=name))
  return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
    session.pop('email', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404

@app.route('/article/<int:id>/<slug>')
def show_article(id, slug):
    article = Article.find_by_id(id)
    if 'email' in session:
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        return render_template('show_article.html', article=article, name=name)
    return render_template('show_article.html', article=article)

@app.route('/article/<int:id>/<slug>/edit', methods=['GET', 'POST'])
def article_update(id, slug):
    article = Article.find_by_id(id)
    if not article:
        return HTTPNotFound(404)
    form = ArticleUpdateForm(request.form, article)
    person = Person.query.filter_by(email=session['email']).first()
    name = person.firstname
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=form, name=name)

@app.route('/category/create', methods=['GET', 'POST'])
def category():
    form = CategoryCreateForm()
    category = Category()
    person = Person.query.filter_by(email=session['email']).first()
    name = person.firstname
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('dashboard', name=name))
    return render_template('cat_create.html', form=form)

@app.route('/author/<name>', methods=['GET'])
def author(name):
    author_articles = Article.find_by_author(name)
    if 'email' in session:
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        return render_template('author.html', author_articles=author_articles, name=name)
    return render_template('author.html', author_articles=author_articles)

@app.route('/category/<category>', methods=['GET'])
def category_articles(category):
    category_articles = Article.find_by_category(category)
    if 'email' in session:
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        return render_template('category_view.html', category_articles=category_articles, name=name)
    return render_template('category_view.html', category_articles=category_articles)

@app.route('/dashboard/<name>')
def dashboard(name):
    if 'email' not in session:
        return redirect(url_for('index'))
    person = Person.query.filter_by(email=session['email']).first()
    if name == person.firstname:
        articles = Article.find_by_author(name)
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        return render_template('dashboard.html', articles=articles, person=person, name=name)
    return redirect(url_for('index'))

@app.route('/article/<int:id>/<slug>/delete', methods=['GET','POST'])
def delete(id, slug):
    article = Article.find_by_id(id)
    person = Person.query.filter_by(email=session['email']).first()
    name = person.firstname
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('dashboard', name=name))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    articles = Article.all()
    if 'email' in session:
        person = Person.query.filter_by(email=session['email']).first()
        form = PersonUpdateForm(request.form, person)
        name = person.firstname
        if form.validate_on_submit():
            form.populate_obj(person)
            db.session.merge(person)
            db.session.commit()
            return render_template('index.html', articles=articles)
        return render_template('settings.html', form=form, name=name)
    return render_template('index.html', articles=articles)

@app.route('/author/delete', methods=['GET','POST'])
def delete_profile():
    person = Person.query.filter_by(email=session['email']).first()
    articles = Article.find_by_author(person.firstname)
    for article in articles:
        db.session.delete(article)
    db.session.delete(person)
    db.session.commit()
    session.pop('email', None)
    return redirect(url_for('index'))
