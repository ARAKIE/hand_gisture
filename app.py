import base64
import cv2
import tensorflow as tf
import logging
from flask import Flask, url_for, request, session, g
from flask import Flask, request, jsonify
import numpy as np
from flask.templating import render_template
from werkzeug.utils import redirect
from database import get_database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from PIL import Image
import bcrypt





from flask import Flask, request, jsonify

app = Flask(__name__)


app.secret_key = 'your_secret_key'





# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO)

# Load your Python model here
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model = tf.keras.models.load_model('Mm.h5', compile=False)
model.compile(optimizer=optimizer)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})

    if 'image_data' not in request.json:
        return jsonify({'error': 'Missing image_data'})

    # Get the image data from the request body
    data = request.json.get('image_data')

    try:
        # Decode the base64-encoded image data to a numpy array
        data = base64.b64decode(data.split(',')[1])
        data = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)

    except Exception as e:
        logging.error('Failed to decode image: {}'.format(str(e)))
        return jsonify({'error': 'Failed to decode image: {}'.format(str(e))})

    try:
        # Convert the grayscale image to a 3-channel color image
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # Resize the image to 32x32 pixels
        img = cv2.resize(img, (32, 32))

        # Make the prediction using your model
        img = img.reshape(1, 32, 32, 3) # Reshape the image array to match the input shape
        pred = model.predict(img)

        logging.info('Request: {}\nPrediction: {}\n'.format(request.json, pred.tolist()))

    except Exception as e:
        logging.error('Failed to make prediction: {}'.format(str(e)))
        return jsonify({'error': 'Failed to make prediction: {}'.format(str(e))})
    

    # Return the prediction result as JSON
    return jsonify({'prediction': pred.tolist()})



app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'handrecogintion_db'):
        g.handrecogintion_db.close()


def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()
    return user

@app.route('/')
def index():
    user = get_current_user()
    return render_template('index.html', user = user)


@app.route('/login', methods = ["POST", "GET"])
def login():
    user = get_current_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('index') + '#courses')
            else:
                error = "Username or Password did not match, Try again."
        else:
            error = 'Username or password did not match, Try again.'
            
            
    return render_template('login.html', loginerror = error, user = user)




@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Get the email address from the form
        email = request.form['email']
        
        # Perform the logic to send the password reset link
        # Replace the print statement with your actual code for sending the reset link
        
        print("Sending password reset link to:", email)
        
        # Redirect to a success page or display a success message
        return redirect('/password_reset_success')

    # Render the forgot password page
    return render_template('forgot_password.html')

@app.route('/password_reset_success')
def password_reset_success():
    return render_template('password_reset_success.html')






@app.route('/camer')
def camer():

    return render_template('camer.html')



@app.route('/camera2')
def camera2():

    return render_template('camera2.html')



@app.route('/register', methods=["POST", "GET"])
def register():
    user = get_current_user()
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        dbuser_cur = db.execute('select * from users where name = ?', [name])
        existing_username = dbuser_cur.fetchone()
        if existing_username:
            return render_template('register.html', registererror = 'Username already taken , try different username.')
        db.execute('insert into users ( name, password) values (?, ?)',[name, hashed_password])
        db.commit()
        return redirect(url_for('index') + '#courses')
    return render_template('register.html', user = user)

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp')
    allemp = emp_cur.fetchall()
    return render_template('dashboard.html', user = user, allemp = allemp)

@app.route('/addnewemployee', methods = ["POST", "GET"])
def addnewemployee():
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('insert into emp (name, email, phone ,address) values (?,?,?,?)', [name, email, phone, address])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html', user = user)

@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('singleemployee.html', user = user, single_emp = single_emp)


@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user = user, single_emp = single_emp)



@app.route('/updateemployee', methods=["POST", "GET"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        password = request.form['password']
        if password == 'arakey###':
            empid = request.form['empid']
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            db = get_database()
            db.execute('UPDATE emp SET name = ?, email = ?, phone = ?, address = ? WHERE empid = ?',
                       [name, email, phone, address, empid])
            db.commit()
            return redirect(url_for('dashboard'))
        else:
            return "Unauthorized access. Please provide the correct admin password to update the information."
    
    return render_template('updateemployee.html', user=user)







@app.route('/deleteemp/<int:empid>', methods=["GET", "POST"])
def deleteemp(empid):
    user = get_current_user()

    # Check if the user is logged in
    if not user:
        # Store the empid in the session to use after login
        session['empid'] = empid
        return redirect(url_for('login'))

    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE FROM emp WHERE empid = ?', [empid])
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=user)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html')
@app.route('/arab')
def arab():
    return render_template('arab.html')

@app.route('/<page>')
def show_page(page):
    return render_template(f'{page}.html')





if __name__ == '__main__':
    app.run(debug = True)
