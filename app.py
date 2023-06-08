from flask import Flask, request, redirect, render_template, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pet_agency_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()


@app.route('/')
def home_page():
    """Shows the home page."""
    pets = Pet.query.all()
    return render_template("index.html", pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Adds a new pet."""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(name=name, species=species,
                      photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()

        flash('New pet added successfully!', 'success')
        return redirect(url_for('home_page'))

    return render_template('add_pet.html', form=form)


@app.route('/edit/<int:pet_id>', methods=['GET', 'POST'])
def display_edit_pet(pet_id):
    """Shows the edit page and makes the edit."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('home_page'))
    else:
        return render_template("display_edit_pet.html", form=form, pet=pet)
