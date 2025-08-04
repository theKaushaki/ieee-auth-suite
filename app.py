from flask import Flask, render_template
import database

app = Flask(__name__)

@app.route('/validate/<public_id>')
def validate_certificate(public_id):
    conn = database.get_db_connection()
    certificate = conn.execute(
        'SELECT * FROM certificates WHERE public_id = ?', (public_id,)
    ).fetchone()
    conn.close()

    if certificate:
        return render_template('validation_success.html', certificate=certificate)
    else:
        return render_template('validation_error.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)