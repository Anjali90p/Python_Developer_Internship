from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # In a real application, you would send an email or save to a database here.
    # For now, we will simply flash a success message back to the user.
    flash(f"Thank you, {name}! Your message has been received.", "success")
    return redirect(url_for('home') + "#contact")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
