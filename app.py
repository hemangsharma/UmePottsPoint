from flask import Flask, request, render_template_string
import os
import pandas as pd
import csv
from datetime import datetime

app = Flask(__name__)

# Define the folder to store uploaded files
app.config['UPLOAD_FOLDER'] = 'uploads'  # Adjust the folder name as needed
app.config['CSV_FOLDER'] = 'csv'

# HTML templates
home_template = """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UME Potts Point</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        p {
            line-height: 1.6;
            margin: 10px 0;
        }
        .buttons {
            text-align: center;
            margin: 20px 0;
        }
        .button {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #555;
        }
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgb(0,0,0);
            background-color: rgba(0,0,0,0.4);
            padding-top: 60px;
        }
        .modal-content {
            background-color: #fefefe;
            margin: 5% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
        .modal-body {
            margin-top: 20px;
            text-align: center;
        }
        .modal-body iframe {
            width: 100%;
            height: 600px;
            border: none;
        }

        @media (max-width: 600px) {

            body{
                padding-top: 50px;
                padding-left:20px;
                padding-right:20px;
                height: auto;
                width: auto;
                overflow-x: auto;
            }
            .container {
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 20%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to UME Potts Point</h1>
        <p>UME Potts Point, 2011, is a comfortable, convenient, and modern Sydney accommodation. Located near Potts Point Veterinary Hospital.</p>
        <p>There are many restaurants near UME Potts Point to ensure residents don’t have to worry about food. Residents can satiate their taste buds with diverse cuisines served at these restaurants, which include The Apollo Restaurant, Cho Cho San, Ms.G's, Ezra, and Malabar South Indian Restaurant.</p>
        <p>Love to party? Then, The Roosevelt, Potts Point Hotel, The New Hampton Hotel, Kings Cross Hotel, and Darlo Bar are the places for you where you can enjoy nice drinks and groove till your feet get tired.</p>
        <div class="buttons">
            <button class="button" id="openModal">House Rules</button>
            <a href="/room-list" class="button">Room List</a>
            <a href="/maintenance" class="button">Maintenance Request</a>
            <a href="/guest-form" class="button">Guest Form</a>
            <a href="https://chat.whatsapp.com/GDHSNY6TZbSEkvGmen0kFu" class="button">WhatsApp Group</a>
        </div>
    </div>

    <!-- The Modal -->
    <div id="myModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div class="modal-body">
                <iframe src=" static/HouseRules.pdf" frameborder="0"></iframe>
            </div>
        </div>
    </div>
    <script>
        var modal = document.getElementById("myModal");
        var btn = document.getElementById("openModal");
        var span = document.getElementsByClassName("close")[0];
        btn.onclick = function() {
            modal.style.display = "block";
        }
        span.onclick = function() {
            modal.style.display = "none";
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    </script>
</body>
</html>

 """

maintenance_form_template = """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UME Potts Point Maintenance Request Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 5%;
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 500px;
            box-sizing: border-box;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
            color: #555;
        }
        input[type="text"], textarea, select {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 3px;
            width: 100%;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #28a745;
            color: #fff;
            border: none;
            padding: 10px;
            cursor: pointer;
            border-radius: 3px;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
        .notification {
            text-align: center;
            margin-top: 10px;
            color: green;
        }
        .buttons {
            text-align: center;
            margin-top: 20px;
        }
        .button {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #555;
        }

        @media (max-width: 600px) {

            body{
                padding-top: 50px;
                padding-left:20px;
                padding-right:20px;
                height: auto;
                width: auto;
                overflow-x: auto;
            }
            .container {
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 20%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>UME Potts Point Maintenance Request Form</h2>
        <form action="/submit-maintenance" method="post">
            <label for="name">Resident's Name:</label>
            <input type="text" id="name" name="name" required>
            <label for="room">Your Room Number:</label>
            <select id="room" name="room" required>
                <option value="">Select Room</option>
                <option value="Studio A">Studio A</option>
                <option value="Studio B">Studio B</option>
                <option value="01">Unit 1</option>
                <option value="02">Unit 2</option>
                <option value="03">Unit 3</option>
                <option value="04">Unit 4</option>
                <option value="05">Unit 5</option>
                <option value="06">Unit 6</option>
                <option value="07">Unit 7</option>
                <option value="08">Unit 8</option>
                <option value="09">Unit 9</option>
                <option value="10">Unit 10</option>
                <option value="11">Unit 11</option>
                <option value="12">Unit 12</option>
                <option value="13">Unit 13</option>
                <option value="14">Unit 14</option>
                <option value="15">Unit 15</option>
                <option value="16">Unit 16</option>
                <option value="17">Unit 17</option>
                <option value="18">Unit 18</option>
                <option value="19">Unit 19</option>
                <option value="20">Unit 20</option>
                <option value="21">Unit 21</option>
                <option value="22">Unit 22</option>
                <option value="23">Unit 23</option>
                <option value="24">Unit 24</option>
                <option value="25">Unit 25</option>
                <option value="26">Unit 26</option>
                <option value="27">Unit 27</option>
                <option value="28">Unit 28</option>
                <option value="29">Unit 29</option>
                <option value="30">Unit 30</option>
                <option value="31">Unit 31</option>
                <option value="32">Unit 32</option>
                <option value="33">Unit 33</option>
                <option value="34">Unit 34</option>
                <option value="35">Unit 35</option>
                <option value="36">Unit 36</option>
                <option value="37">Unit 37</option>
                <option value="38">Unit 38</option>
                <option value="39">Unit 39</option>
                <option value="40">Unit 40</option>
            </select>
            <label for="description">Description of Problem:</label>
            <textarea id="description" name="description" required></textarea>
            <label for="area">Affected Area/Unit/Room:</label>
            <input type="text" id="area" name="area" required>
            <input type="submit" value="Submit">
        </form>
        <div class="notification" id="notification"></div>
        <div class="buttons">
            <a href="/" class="button">Home</a>
        </div>
    </div>
</body>
</html>
 """

guest_form_template = """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UME Potts Point Guest Request Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 500px;
            box-sizing: border-box;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
            color: #555;
        }
        input[type="text"], select, input[type="date"] {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 3px;
            width: 100%;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #28a745;
            color: #fff;
            border: none;
            padding: 10px;
            cursor: pointer;
            border-radius: 3px;
        }
        input[type="submit"]:hover {
            background-color: #218838;
        }
        .notification {
            text-align: center;
            margin-top: 10px;
            color: green;
        }
        .guest-fields {
            margin-bottom: 15px;
        }
        .guest-fields input {
            margin-bottom: 5px;
        }
        .buttons {
            text-align: center;
            margin-top: 20px;
        }
        .button {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #555;
        }
        @media (max-width: 600px) {

            body{
                padding-top: 50px;
                padding-left:20px;
                padding-right:20px;
                height: auto;
                width: auto;
                overflow-x: auto;
            }
            .container {
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 20%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>UME Potts Point Guest Request Form</h2>
        <form id="guest-form" action="/submit-guest" method="post">
            <label for="resident_name">Resident's Name:</label>
            <input type="text" id="resident_name" name="resident_name" required>
            <label for="room">Your Room Number:</label>
            <select id="room" name="room" required>
                <option value="">Select Room</option>
                <option value="Studio A">Studio A</option>
                <option value="Studio B">Studio B</option>
                <option value="01">Unit 1</option>
                <option value="02">Unit 2</option>
                <option value="03">Unit 3</option>
                <option value="04">Unit 4</option>
                <option value="05">Unit 5</option>
                <option value="06">Unit 6</option>
                <option value="07">Unit 7</option>
                <option value="08">Unit 8</option>
                <option value="09">Unit 9</option>
                <option value="10">Unit 10</option>
                <option value="11">Unit 11</option>
                <option value="12">Unit 12</option>
                <option value="13">Unit 13</option>
                <option value="14">Unit 14</option>
                <option value="15">Unit 15</option>
                <option value="16">Unit 16</option>
                <option value="17">Unit 17</option>
                <option value="18">Unit 18</option>
                <option value="19">Unit 19</option>
                <option value="20">Unit 20</option>
                <option value="21">Unit 21</option>
                <option value="22">Unit 22</option>
                <option value="23">Unit 23</option>
                <option value="24">Unit 24</option>
                <option value="25">Unit 25</option>
                <option value="26">Unit 26</option>
                <option value="27">Unit 27</option>
                <option value="28">Unit 28</option>
                <option value="29">Unit 29</option>
                <option value="30">Unit 30</option>
                <option value="31">Unit 31</option>
                <option value="32">Unit 32</option>
                <option value="33">Unit 33</option>
                <option value="34">Unit 34</option>
                <option value="35">Unit 35</option>
                <option value="36">Unit 36</option>
                <option value="37">Unit 37</option>
                <option value="38">Unit 38</option>
                <option value="39">Unit 39</option>
                <option value="40">Unit 40</option>
            </select>
            <label for="num_guests">Number of Guests:</label>
            <select id="num_guests" name="num_guests" required>
                <option value="">Select Number of Guests</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </select>
            <div id="guests-container">
                <!-- Guest name fields will be dynamically added here -->
            </div>
            <label for="arrival_date">Arrival Date:</label>
            <input type="date" id="arrival_date" name="arrival_date" required>
            <label for="departure_date">Departure Date:</label>
            <input type="date" id="departure_date" name="departure_date" required>
            <input type="submit" value="Submit">
        </form>
        <div class="notification" id="notification"></div>
        <div class="buttons">
            <a href="/" class="button">Home</a>
        </div>
    </div>
    <script>
        const numGuestsSelect = document.getElementById('num_guests');
        const guestsContainer = document.getElementById('guests-container');

        function updateGuestFields() {
            const numGuests = parseInt(numGuestsSelect.value);
            guestsContainer.innerHTML = '';  // Clear existing guest fields

            for (let i = 1; i <= numGuests; i++) {
                const guestLabel = document.createElement('label');
                guestLabel.setAttribute('for', `guest_name_${i}`);
                guestLabel.textContent = `Guest ${i} Name:`;
                const guestInput = document.createElement('input');
                guestInput.setAttribute('type', 'text');
                guestInput.setAttribute('id', `guest_name_${i}`);
                guestInput.setAttribute('name', `guest_name_${i}`);
                guestInput.required = true;

                guestsContainer.appendChild(guestLabel);
                guestsContainer.appendChild(guestInput);
            }
        }

        numGuestsSelect.addEventListener('change', updateGuestFields);
        updateGuestFields();  // Initialize fields based on the default value
    </script>
</body>
</html>
"""

room_list_template = """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UME Potts Point Room List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 2%;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
            box-sizing: border-box;
            overflow: hidden;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 800px;
            box-sizing: border-box;
            max-height: calc(100vh - 4%);
            overflow-y: auto;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-top: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            overflow-x: auto; /* Add horizontal scroll if needed */
        }
        table, th, td {
            border: 1px solid #ccc;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .buttons {
            text-align: center;
            margin-top: 20px;
        }
        .button {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #555;
        }
        @media (max-width: 600px) {

            body{
                padding-top: 50px;
                height: auto;
                width: auto;
                overflow-x: auto;
            }
            .container {
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 20%;
            }
            table, th, td {
                font-size: 14px;
            }
            .button {
                width: 50%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>UME Potts Point Room List</h2>
        <table>
            <thead>
                <tr>
                    <th>Room Number</th>
                    <th>Resident Name</th>
                    <th>Contact Email</th>
                </tr>
            </thead>
            <tbody>
                {% for room in rooms %}
                <tr>
                    <td>{{ room['Unit'] }}</td>
                    <td>{{ room['Occupant 1 [Full name]'] }}</td>
                    <td>{{ room['Contact Email For Occupant 1'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="buttons">
            <a href="/" class="button">Home</a>
        </div>
    </div>
</body>
</html>

"""
 # Paste the room list template HTML here

@app.route('/')
def home():
    return render_template_string(home_template)

@app.route('/maintenance')
def maintenance():
    return render_template_string(maintenance_form_template)

@app.route('/guest-form')
def guest_form():
    return render_template_string(guest_form_template)

@app.route('/room-list', methods=['GET'])
def room_list():
    room_data = []
    try:
        room_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'room_list.csv')
        df = pd.read_csv(room_csv_path)
        
        # Drop rows where "Occupant 1 [Full name]" is empty
        df = df.dropna(subset=['Occupant 1 [Full name]'])
        
        room_data = df.to_dict(orient='records')
    except FileNotFoundError:
        room_data = []

    return render_template_string(room_list_template, rooms=room_data)


@app.route('/submit-maintenance', methods=['POST'])
def submit_maintenance():
    name = request.form['name']
    room = request.form['room']
    description = request.form['description']
    area = request.form['area']

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    # Ensure the uploads folder exists
    os.makedirs(app.config['CSV_FOLDER'], exist_ok=True)

    # Save the data to a CSV file
    filename = os.path.join(app.config['CSV_FOLDER'], 'maintenance_requests.csv')
    fieldnames = ['timestamp', 'name', 'room', 'description', 'area']

    if not os.path.isfile(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'timestamp': timestamp, 'name': name, 'room': room, 'description': description, 'area': area})
    else:
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'timestamp': timestamp, 'name': name, 'room': room, 'description': description, 'area': area})

    return 'Data submitted successfully!'

@app.route('/submit-guest', methods=['POST'])
def submit_guest():
    try:
        resident_name = request.form['resident_name']
        room = request.form['room']
        num_guests = int(request.form['num_guests'])
        arrival_date = request.form['arrival_date']
        departure_date = request.form['departure_date']

        # Retrieve guest names dynamically
        guest_names = []
        for i in range(1, num_guests + 1):
            guest_name = request.form.get(f'guest_name_{i}', '')
            if guest_name:
                guest_names.append(guest_name)
        
        # Get the current date and time
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

        # Ensure the uploads folder exists
        os.makedirs(app.config['CSV_FOLDER'], exist_ok=True)

        # Save the data to a CSV file
        filename = os.path.join(app.config['CSV_FOLDER'], 'guest_requests.csv')
        fieldnames = ['timestamp', 'resident_name', 'room', 'guest_names', 'arrival_date', 'departure_date']

        if not os.path.isfile(filename):
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({
                'timestamp': timestamp,
                'resident_name': resident_name,
                'room': room,
                'guest_names': ', '.join(guest_names),  # Join guest names with a comma
                'arrival_date': arrival_date,
                'departure_date': departure_date
            })

        return 'Data submitted successfully!'

    except KeyError as e:
        return f"Error: Missing field {e}", 400
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
