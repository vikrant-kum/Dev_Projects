from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="devops_app",
        password="Devops@123",
        database="devops_panda_db"
    )
    return connection


@app.route("/")
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, name, department, salary
        FROM employees
        ORDER BY id DESC
        LIMIT 2
    """

    cursor.execute(query)
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", employees=employees)

@app.route("/add_employee", methods=["POST"])
def add_employee():

    emp_id = request.form["id"]
    name = request.form["name"]
    department = request.form["department"]
    salary = request.form["salary"]

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO employees
        (id, name, department, salary)
        VALUES (%s, %s, %s, %s)
    """

    values = (emp_id, name, department, salary)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return "Employee added successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
