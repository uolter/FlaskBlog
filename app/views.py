from models import Person, Article, Category
from flask import render_template, request, session, url_for, redirect
from forms import SignupForm, ArticleCreateForm, ArticleUpdateForm, SigninForm, CategoryCreateForm
from app import app, db

@app.route('/')
def index():
    articles = Article.all()
    return render_template('index.html', articles=articles)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        newperson = Person(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
        db.session.add(newperson)
        db.session.commit()
        session['email'] = newperson.email
        return redirect(url_for('profile'))
    return render_template('signup.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))
    person = Person.query.filter_by(email=session['email']).first()
    if person:
        article = Article()
        form = ArticleCreateForm()
        form.person_name.data = person.firstname
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('create.html', form=form, person=person)
    return render_template('profile.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if form.validate_on_submit():
      session['email'] = form.email.data
      return redirect(url_for('profile'))
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
        person_name = article.person_name
        return render_template('show_article.html', article=article, person=person, person_name=person_name)
    return render_template('show_article.html', article=article)

@app.route('/article/<int:id>/<slug>/edit', methods=['GET', 'POST'])
def article_update(id, slug):
    article = Article.find_by_id(id)
    if not article:
        return HTTPNotFound(404)
    form = ArticleUpdateForm(request.form, article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/category/create', methods=['GET', 'POST'])
def category():
    form = CategoryCreateForm()
    category = Category()
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('cat_create.html', form=form)

@app.route('/author/<name>', methods=['GET'])
def author(name):
    author_articles = Article.find_by_author(name)
    return render_template('author.html', author_articles=author_articles)

@app.route('/category/<category>', methods=['GET'])
def category_articles(category):
    category_articles = Article.find_by_category(category)
    return render_template('category_view.html', category_articles=category_articles)