"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, request, flash
import time
import smtplib


##Secret Key to allow flashing
app.secret_key='mysecretkey'


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
    
#----------------------------------------------------------------------------------    
    

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        from_name=request.form['name']
        from_addr=request.form['address']
        subject=request.form['subject']
        msg=request.form['message']
        send_mail(from_name, from_addr, subject, msg)
        flash('Message Sent Successfully')
        return redirect(url_for('home'))
    return render_template('contact.html')


def send_mail(from_name, from_addr, subject, msg):
    to_name = "John Brown"
    to_addr = ""
    message = """From: {} <{}>\nTo: {} <{}>\nSubject: {}\n{}"""
    message_to_send = message.format(from_name, from_addr, to_name, to_addr, subject, msg)
    # Credentials (if needed)
    username = ''
    password = ''
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, message_to_send)
    server.quit()


#----------------------------------------------------------------------------------------------------------




@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")
    
def timeinfo():
    return time.strftime("%a, %d %b %Y")
    
@app.route('/profile/')
def profile():
    return render_template('profile.html', currenttime=(timeinfo()))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")