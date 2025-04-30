import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

###############################################################################
#                                CONSTANTS                                    #
###############################################################################


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STORAGE_PATH = os.path.join(BASE_DIR, os.environ.get('STORAGE_PATH', 'data'))


###############################################################################
#                               FLASK SETUP                                   #
###############################################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{STORAGE_PATH}/metadata.db"
db = SQLAlchemy(app)

###############################################################################
#                                  MODEL                                      #
###############################################################################


class Dataset(db.Model):
    """
    Model representing a dataset in the database.
    - Id
    - Name
    - Description
    - Samples
    - Size (in bytes)
    - Labels
    - Created At
    - Updated At
    - Created by
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    samples = db.Column(db.Integer, nullable=False, default=0)
    size = db.Column(db.Integer, nullable=False, default=0)
    labels = db.Column(db.String(500), unique=False, nullable=False, default='')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_by = db.Column(db.String(120), nullable=False, default='user')

    def __repr__(self):
        return f'<Dataset {self.id}>'


class Sample(db.Model):
    """
    Model representing a sample in the database.
    - Id
    - Text
    - Label
    - Dataset Id
    - Size (in bytes)
    - Created At
    - Updated At
    - Created by
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), unique=False, nullable=False)
    label = db.Column(db.String(80), unique=False, nullable=False)
    ds_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    size = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_by = db.Column(db.String(120), nullable=False, default='user')

    def __repr__(self):
        return f'<Sample {self.id}>'


def init_db():
    """
    Inicializa la base de datos si no existe.
    """
    # Asegurar que el directorio existe
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    db_path = os.path.join(STORAGE_PATH, 'metadata.db')
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            logging.info("Tables created successfully")
    else:
        logging.info("Database already exists, no action needed")

###############################################################################
#                                 ENDPOINTS                                   #
###############################################################################


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Render the index page with a form, dedicated to the datasets management.
    """
    if request.method == 'POST':
        new_dataset = Dataset(
            name=request.form['ds_name'],
            description=request.form['ds_desc'],
            labels=request.form['ds_labels'],
        )

        try:
            db.session.add(new_dataset)
            db.session.commit()
            return redirect('/')

        except Exception as e:
            logging.error(f"Error adding dataset: {e}")
            return "Error adding dataset", 500

    else:
        dss: list[Dataset] = Dataset.query.order_by(Dataset.updated_at).all()
        return render_template('index.html', datasets=dss)


@app.route('/dataset/view/<int:id>', methods=['GET'])
def view_dataset(id: int):
    """
    Update a dataset in the database.
    """
    ds_to_update = Dataset.query.get_or_404(id)
    smp: list[Sample] = Sample.query.filter_by(ds_id=id).all()

    try:
        return render_template('ds_view.html',
                               dataset=ds_to_update,
                               samples=smp)

    except Exception as e:
        logging.error(f"Error accessing dataset: {e}")
        return "Error accesssing dataset", 500


@app.route('/dataset/delete/<int:id>', methods=['GET'])
def proc_delete_dataset(id: int):
    """
    Delete a dataset from the database.
    """
    ds_to_del = Dataset.query.get_or_404(id)
    try:
        db.session.delete(ds_to_del)
        db.session.commit()
        return redirect('/')

    except Exception as e:
        logging.error(f"Error deleting dataset: {e}")
        return "Error deleting dataset", 500


@app.route('/dataset/update/<int:id>', methods=['GET'])
def view_update_dataset(id: int):
    """
    Go to the view to update a dataset.
    """
    ds_to_update = Dataset.query.get_or_404(id)

    try:
        return render_template('ds_update.html',
                               dataset=ds_to_update)

    except Exception as e:
        logging.error(f"Error going to update dataset: {e}")
        return "Error going to update dataset", 500


@app.route('/dataset/update/<int:id>', methods=['POST'])
def proc_update_dataset(id: int):
    """
    Update a dataset in the database.
    """
    ds_to_update = Dataset.query.get_or_404(id)

    try:
        ds_to_update.name = request.form['ds_name']
        ds_to_update.description = request.form['ds_desc']
        ds_to_update.labels = request.form['ds_labels']
        db.session.commit()
        return redirect('/')

    except Exception as e:
        logging.error(f"Error updating dataset: {e}")
        return "Error updating dataset", 500


@app.route('/sample/create', methods=['POST'])
def proc_create_sample():
    """
    Create a sample for a dataset.
    """
    new_sample = Sample(
        text=request.form['s_text'],
        label=request.form['s_label'],
        ds_id=request.form['ds_id'],
    )

    try:
        db.session.add(new_sample)
        db.session.commit()

        return redirect('/dataset/view/' + str(request.form['ds_id']))

    except Exception as e:
        logging.error(f"Error creating sample: {e}")
        return "Error creating sample", 500


@app.route('/sample/delete/<int:id>', methods=['GET'])
def proc_delete_sample(id: int):
    """
    Delete a sample from a dataset.
    """
    smp_to_del = Sample.query.get_or_404(id)
    ds_id = smp_to_del.ds_id

    try:
        db.session.delete(smp_to_del)
        db.session.commit()
        return redirect('/dataset/view/' + str(ds_id))

    except Exception as e:
        logging.error(f"Error deleting sample: {e}")
        return "Error deleting sample", 500


@app.route('/sample/update/<int:id>', methods=['GET'])
def view_update_sample(id: int):
    """
    Edit a sample from a dataset.
    """
    smp_to_edit = Sample.query.get_or_404(id)
    dataset: Dataset = Dataset.query.get_or_404(smp_to_edit.ds_id)

    try:
        return render_template('s_update.html',
                               sample=smp_to_edit,
                               dataset=dataset)

    except Exception as e:
        logging.error(f"Error editing sample: {e}")
        return "Error editing sample", 500


@app.route('/sample/update/<int:id>', methods=['POST'])
def proc_update_sample(id: int):
    """
    Update a sample in the database.
    """
    smp_to_edit = Sample.query.get_or_404(id)
    ds_id = smp_to_edit.ds_id

    try:
        smp_to_edit.text = request.form['s_text']
        smp_to_edit.label = request.form['s_label']
        smp_to_edit.updated_at = datetime.now()
        db.session.commit()
        return redirect('/dataset/view/' + str(ds_id))

    except Exception as e:
        logging.error(f"Error updating sample: {e}")
        return "Error updating sample", 500

###############################################################################
#                                  MAIN                                       #
###############################################################################


init_db()

if __name__ == '__main__':
    app.run(debug=True)
