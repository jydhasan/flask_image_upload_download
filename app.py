from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '124055'

# model image
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/images')
def images():
    images = Image.query.all()
    return render_template('images.html', images=images)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully')
        return redirect(url_for('users'))
    return render_template('add_user.html')


@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        image.save('static/uploads/'+image.filename)
        image = Image(name=name, image=image.filename)
        db.session.add(image)
        db.session.commit()
        flash('Image added successfully')
        return redirect(url_for('images'))
    return render_template('add_image.html')


@app.route('/download_image/<int:image_id>')
def download_image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_from_directory('static/uploads', image.image, as_attachment=True)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        flash('User updated successfully')
        return redirect(url_for('users'))
    return render_template('edit.html', user=user)


@app.route('/edit_image/<int:id>', methods=['GET', 'POST'])
def edit_image(id):
    image = Image.query.get(id)
    if request.method == 'POST':
        image.name = request.form['name']
        image.image = request.files['image'].filename
        db.session.commit()
        flash('Image updated successfully')
        return redirect(url_for('images'))
    return render_template('edit_image.html', image=image)


@app.route('/delete/<int:id>')
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('users'))


@app.route('/delete_image/<int:id>')
def delete_image(id):
    image = Image.query.get(id)
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted successfully')
    return redirect(url_for('images'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
