from flask import Flask, request, render_template_string
import os
import pandas as pd
import csv
from datetime import datetime
from PIL import Image
import uuid

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CSV_FOLDER'] = 'csv'
app.config['IMAGES_SUBFOLDER'] = 'images'

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
        <h1>Welcome to UME Potts Point</h1><br>
        <div class="buttons">
            <a href="/house-rules" class="button">House Rules</a>
            <a href="/room-list" class="button">Room List</a>
            <a href="/maintenance" class="button">Maintenance Request</a>
            <a href="/guest-form" class="button">Guest Form</a>
            <a href="https://chat.whatsapp.com/GDHSNY6TZbSEkvGmen0kFu" class="button">WhatsApp Group</a>
            <a href="/dep-guide" class="button">Departure Guidelines</a>
            <a href="/contact" class="button">Emergency Contacts</a>
        </div>
        <br>
        <p>Hi, my name is Hemang, and I am your House Manager. Welcome to UME Potts Point! Here, you will find important links and information designed to ensure you have a comfortable and enjoyable stay. If you have questions related to mail, dryers, etc visit House Rules Section.</p>
        <p>If you need any assistance, please feel free to message me at +61 450 595 354.</p>
        <p>
            <h2>Your Rooms Should Have:</h2>
            <ol>
                <li>Quilt/Duvet + Cover</li>
                <li>Bedsheet</li>
                <li>Pillow and Pillow Cover</li>
                <li>Mini Fridge</li>
                <li>Table Lamp</li>
            </ol>
            You have to buy a fan or a heater based on your needs.
        </p>
        <p>
            <h2>Essentials Guide</h2>
                <h3>Supermarkets</h3>
                <ul>
                    <li>Coles</li>
                    <li>Woolworth / Woolies</li>
                    <li>Harris Farm Markets</li>
                    <li>ALDI</li>
                </ul>
                <h3>Appliance Stores</h3>
                <ul>
                    <li>Bunnnings</li>
                    <li>JB Hi-Fi</li>
                    <li>Harvey Norman</li>
                </ul>
                <h3>Departmental Stores</h3>
                <ul>
                    <li>Target</li>
                    <li>Kmart</li>
                    <li>Big W</li>
                    <li>IKEA</li>
                    <li>Myer</li>
                </ul>
                <h3>Restaurants</h3>
                <ul>
                    <li>The Apollo</li>
                    <li>Cho Cho San</li>
                    <li>Ms.G's</li>
                    <li>Ezra</li>
                    <li>Malabar South Indian Restaurant</li>
                </ul>
                <h3>Love to party?</h3>
                <ul>
                    <li>The Roosevelt</li>
                    <li>Potts Point Hotel</li>
                    <li>The New Hampton Hotel</li>
                    <li>Kings Cross Hotel</li>
                </ul>
        </p>
    </div>
</body>
</html>

 """

house_rules = """ 

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UME House Rules</title>
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
            h2 {
                text-align: center;
                color: #333;
            }
            p, li {
                font-size: 14px;
                color: #555;
                line-height: 1.6;
            }
            ul {
                list-style-type: disc;
                padding-left: 20px;
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
            <h2>UME Potts Point House Rules</h2>
            <h3>GENERAL RULES OF CONDUCT</h3>
            <ul>
                <li>Disrespectful behavior toward other guests or house manager will not be tolerated and may lead to termination of the agreement.</li>
                <li>All tenants are entitled to quiet enjoyment of their home.</li>
                <li>Tenants involved in fighting will be evicted.</li>
                <li>Harassment in any form will not be tolerated and may result in immediate eviction.</li>
                <li>All tenants must be respectful of other people’s property.</li>
                <li>Most common areas are monitored with closed circuit television cameras (CCTV) 24 hours a day for security purposes. Private areas, such as bedrooms or bathrooms, are not monitored.</li>
                <li>Resident must pre declare their guest. Residents’ guests must adhere to UME house rules and vacate the property by 10:00 PM. Late check outs after 10 PM will incur a fee of <b>$100</b>.</li>
                <li>Each occupant of the house must only take the studio assigned to their actual agreement. It is not permitted to change your studio unless given authorization from UME. The resident agrees to always lock doors and gates behind them at the premises and is responsible for the security of their own studio.</li>
            </ul>

            <h3>MAILS</h3>
            <ul>
                <li>You can find your new mails on gorund floor.</li>
                <li>All the older mails are moved to study area after a day.</li>
                <li>All the uncollected mails get discraded after a month.</li>
            </ul>

            <h3>WASHING MACHINES AND DRYERS</h3>
            <ul>
                <li>You will find two washing machines and two dryers on rooftop.</li>
                <li>Please clean the filters of dryers after and before use.</li>
                <li>Please let washing machine dry after use, in order to avoid mold.</li>
            </ul>
            
            <h3>COMMUNAL AREAS AND BATHROOMS</h3>
            <ul>
                <li>The use of smoking products of any sort, including all cigarette products and all smoke-producing products (cigars, pipes, e-cigarettes, hookahs, vaporizers, etc.) is prohibited in the studio, in the common areas, or in hallways. Any tenant found smoking will be fined <b>$250.</b></li>
                <li>Kitchen and communal areas must be always clean and tidy. Residents found leaving the kitchen unclean and untidy will be searched via cameras to determine ownership or responsibility. Leaving the kitchen unclean and untidy will incur a fee of <b>$50</b>.</li>
                <li>UME is not responsible for food stored in the kitchen. It’s recommended to use a lockable refrigerator bag for any food that you are storing in the common fridges. Food can only be stored in the fridge for up to one week and freezer for up to 2 weeks.</li>
                <li>Tenants using the communal kitchens must always monitor their cooking and are required to keep the kitchens clean and hygienic and to turn all appliances off when not in use. Dishes left unwashed in communal kitchen areas will be removed and disposed off.</li>
                <li>It’s the tenant’s responsibility to bring their rubbish out and not to leave them at their door or outside the bins provided.</li>
                <li>If the smoke alarms and/or sprinklers are activated, the resident responsible will be instructed to pay the full cost of a call-out fee charged by the NSW Fire Brigade. The fee is <b>$2000</b>.</li>
                <li>We do not allow pets to stay at the property.</li>
                <li>There should be no personal belongings left in the common areas as you are sharing your living space with other residents. Community Managers and House Managers have been given authority to discard any items they find laying around in the common areas.</li>
            </ul>
            
            <h3>BEDROOMS</h3>
            <ul>
                <li>Please be mindful of what you use to hang or stick things on the walls of your room. Should there be any damage to the walls or furniture, the cost of repairing this damage will be taken from the security deposit.</li>
                <li>Residents are responsible to keep their rooms clean and tidy throughout the duration of the agreement.</li>
            </ul>

            <h3>VACUUM CLEANERS</h3>
            <ul>
                <li>There are 6 vacuum cleaner on ground floor.</li>
                <li>It is resident's responsibility to clean and empty vacuum cleaners after use.</li>
            </ul>
            <h3>BBQ</h3>
            <ul>
                <li>Residents must inform House Manager before using the BBQ.</li>
                <li>It is resident's responsibility to clean BBQ after use.</li>
            </ul>
            <h3>FIRE & SAFETY</h3>
            <ul>
                <li><b>Do not obstruct pathways leading to fire exits:</b> Ensure that all corridors, stairwells, and paths leading to fire exits are always clear and accessible.</li>
                <li><b>Do not keep big objects in hallways that can act as hurdles:</b> Large items can block escape routes and hinder evacuation efforts during an emergency.</li>
                <li><b>Keep fire doors closed at all times:</b> Fire doors are designed to contain the spread of fire and smoke. Ensure they are not propped open.</li>
                <li><b>Do not tamper with fire safety equipment:</b> Fire alarms, smoke detectors, and sprinkler systems are critical for your safety. Do not disable or interfere with them.</li>
            </ul>
            <div class="buttons">
                <a href="/" class="button">Home</a>
            </div>
        </div>
        </div>
    </body>
    </html>
"""

maintenance_form_template = """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UME Potts Point Maintenance Request Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
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
            input[type="text"], textarea, select, input[type="file"] {
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
                border-radius: 10px;
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
            .progress-container {
                display: none;
                margin-top: 20px;
                text-align: center;
            }
            .progress-bar {
                width: 100%;
                background-color: #f3f3f3;
                border-radius: 3px;
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) inset;
            }
            .progress-bar-inner {
                height: 20px;
                width: 0;
                background-color: #28a745;
                transition: width 0.4s ease;
            }
            @media (max-width: 600px) {
                body {
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
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>UME Potts Point Maintenance Request Form</h2>
            <form id="maintenance-form" action="/submit-maintenance" method="post" enctype="multipart/form-data">
                <label for="name">Resident's Name:</label>
                <input type="text" id="name" name="name" required>
                <label for="room">Resident's Room Number:</label>
                <select id="room" name="room" required>
                    <option value="No Room">Select Room</option>
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
                <label for="category">Category:</label>
                <select id="category" name="category" required>
                    <option value="No Category">Select Category</option>
                    <option value="Electrical">Electrical</option>
                    <option value="Plumbing">Plumbing</option>
                    <option value="General Maintenance">General Maintenance</option>
                    <option value="Missing Item">Missing Item</option>
                    <option value="Door/DoorLock/Locks">Door / Door Lock / Locks</option>
                    <option value="Wifi">Wifi</option>
                    <option value="Refill">Soap / Toilet Paper Refill</option>
                    <option value="Delivery">Linen Delivery</option>
                    <option value="Other">Other</option>
                </select>
                <label for="description">Description of Problem:</label>
                <textarea id="description" name="description" required></textarea>
                <label for="area">Affected Area / Room:</label>
                <input type="text" id="area" name="area" required>
                <label for="image1">Upload Image 1:</label>
                <input type="file" id="image1" name="image1" accept="image/*">
                <label for="image2">Upload Image 2:</label>
                <input type="file" id="image2" name="image2" accept="image/*">
                <input type="submit" value="Submit">
            </form>
            <div class="progress-container">
                <div class="progress-bar">
                    <div class="progress-bar-inner"></div>
                </div>
            </div>
            <div class="notification" id="notification"></div>
            <div class="buttons">
                <a href="/" class="button">Home</a>
            </div>
        </div>
        <script>
            document.getElementById('maintenance-form').addEventListener('submit', function(e) {
                e.preventDefault();

                var form = e.target;
                var formData = new FormData(form);
                var xhr = new XMLHttpRequest();

                xhr.open('POST', form.action, true);

                xhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        var percentComplete = (e.loaded / e.total) * 100;
                        var progressBar = document.querySelector('.progress-bar-inner');
                        progressBar.style.width = percentComplete + '%';
                    }
                });

                xhr.onloadstart = function() {
                    document.querySelector('.progress-container').style.display = 'block';
                };

                xhr.onload = function() {
                    if (xhr.status === 200) {
                        document.querySelector('.notification').textContent = 'Your maintenance request has been submitted successfully.';
                    } else {
                        document.querySelector('.notification').textContent = 'Failed to submit the maintenance request.';
                    }
                    document.querySelector('.progress-container').style.display = 'none';
                    document.querySelector('.progress-bar-inner').style.width = '0';
                };

                xhr.onerror = function() {
                    document.querySelector('.notification').textContent = 'An error occurred during the upload.';
                    document.querySelector('.progress-container').style.display = 'none';
                    document.querySelector('.progress-bar-inner').style.width = '0';
                };

                xhr.send(formData);
            });
        </script>
    </body>
    </html>
 """

guest_form_template = """ 
    <!DOCTYPE html>
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
                background-color: #f4f4f4;
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
            input[type="text"], input[type="tel"], select, input[type="date"] {
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
                border-radius: 10px;
            }
            input[type="submit"]:hover {
                background-color: #218838;
            }
            .notification {
                text-align: center;
                margin-top: 10px;
                color: green;
            }
            .error {
                color: red;
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
                border-radius: 10px;
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
            const form = document.getElementById('guest-form');
            const notificationDiv = document.getElementById('notification');

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

                    const phoneLabel = document.createElement('label');
                    phoneLabel.setAttribute('for', `guest_phone_${i}`);
                    phoneLabel.textContent = `Guest ${i} Phone Number:`;
                    const phoneInput = document.createElement('input');
                    phoneInput.setAttribute('type', 'tel');
                    phoneInput.setAttribute('id', `guest_phone_${i}`);
                    phoneInput.setAttribute('name', `guest_phone_${i}`);
                    phoneInput.required = true;

                    guestsContainer.appendChild(guestLabel);
                    guestsContainer.appendChild(guestInput);
                    guestsContainer.appendChild(phoneLabel);
                    guestsContainer.appendChild(phoneInput);
                }
            }

            numGuestsSelect.addEventListener('change', updateGuestFields);
            updateGuestFields();

            form.addEventListener('submit', function(event) {
                event.preventDefault();

                const formData = new FormData(form);
                fetch('/submit-guest', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.text())
                .then(data => {
                    notificationDiv.textContent = data;
                    notificationDiv.classList.remove('error');
                })
                .catch(error => {
                    notificationDiv.textContent = `An error occurred: ${error}`;
                    notificationDiv.classList.add('error');
                });
            });
        </script>
    </body>
    </html>
"""

room_list_template = """ 
    <!DOCTYPE html>
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
                margin-bottom: 20px; /* Space between tables */
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
                body {
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
                        <th>Floor</th>
                        <th>Room Numbers / Facilities</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Basement</td>
                        <td>Communal Kitchen, Communal Fridges, Kitchen Cabinets, Study Area, Studio A & B, Bin Area</td>
                    </tr>
                    <tr>
                        <td>Ground Floor</td>
                        <td>1 to 7</td>
                    </tr>
                    <tr>
                        <td>First Floor</td>
                        <td>8 to 18</td>
                    </tr>
                    <tr>
                        <td>Second Floor</td>
                        <td>19 to 29</td>
                    </tr>
                    <tr>
                        <td>Third Floor</td>
                        <td>30 to 40</td>
                    </tr>
                    <tr>
                        <td>Rooftop</td>
                        <td>Washing Machine, Dryer, BBQ, Communal Kitchen</td>
                    </tr>
                </tbody>
            </table>
            <table>
                <thead>
                    <tr>
                        <th>Room Number</th>
                        <th>Resident Name</th>
                        <th>Resident Name</th>
                    </tr>
                </thead>
                <tbody>
                    {% for room in rooms %}
                    <tr>
                        <td>{{ room['Unit'] }}</td>
                        <td>{{ room['Resident Name'] }}</td>
                        <td>{{ room['Second Resident Name'] }}</td>
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

departure_guide = """ 

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UME House Rules</title>
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
            h2 {
                text-align: center;
                color: #333;
            }
            p, li {
                font-size: 14px;
                color: #555;
                line-height: 1.6;
            }
            ul {
                list-style-type: disc;
                padding-left: 20px;
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
            <h2>UME Potts Point Departure Guidelines</h2>
            <h3></h3>
            <ul>
                <b><li>Message House Manager about your departure</li></b>
            </ul>
            
            <h3>Room</h3>
            <ul>
                <li>The provided bed sheet, quilt/duvet, and pillow are exclusively assigned for your personal use. Kindly ensure to take these items with you upon departure.</li>
                <li>Failure to remove rubbish and personal belongings may incur additional cleaning fees, up to <b>$250</b>.</li>
            </ul>
            
            <h3>Kitchen Cabinet And Fridge Space</h3>
            <ul>
                <li>Before leaving, please empty your kitchen cabinet, trash bins and fridge space.</li>
                <li>Unlock your kitchen cabinet.</li>
            </ul>
            
            <h3>MATTERS PROTECTOR</h3>
            <ul>
                <li>Please do not take the mattress protector. It is a part of the property. Removal will result in a replacement fee of <b>$100</b>.</li>
            </ul>
            <div class="buttons">
                <a href="/" class="button">Home</a>
            </div>
        </div>
        </div>
    </body>
    </html>
"""

emergency_contacts = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UME Potts Point Emergency Contacts</title>
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
            h2 {
                text-align: center;
                color: #333;
            }
            p, li {
                font-size: 14px;
                color: #555;
                line-height: 1.6;
            }
            ul {
                list-style-type: disc;
                padding-left: 20px;
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
            <h2>UME Potts Point Emergency Contacts</h2>
            <h3>PLUMBER</h3>
            <p>NAME: BRANDON<br>PHONE: 0423263393</p>
            <h3>ELECTRICIAN</h3>
            <p>NAME: TANGO<br>PHONE: 0430467527</p>
            <h3>LOCKSMITH</h3>
            <p>NAME: YATES CONTROL ROOM<br>PHONE: 131911<br>PHONE: 02 95783000 </p>
            <h3>POLICE / AMBULANCE / FIREBRIGADE</h3>
            <p>PHONE: 000</p>
            <center><b><p>IF YOU ARE CONTACTING POLICE OR AMBULANCE OR FIREBRIGADE, PLEASE INFORM HOUSE MANAGER AS WELL ABOUT THE INCIDENT</p></b></center>
            <br>
            <p>
                <b>WHAT TO DO WHEN YOU ARE LOCKED OUT?</b><br>
                <u>AFTER HOURS LOCK OUT:</u> PLEASE CONTACT 'YATES' AT YOUR OWN EXPENSE. (YATES CHARGES <b>A$110</b> FOR LOCKOUT FEE).<br><br>
                <b>LOST YOUR KEY?</b><br>
                PLEASE LET THE HOUSE MANAGER KNOW AND YOU WILL BE CHARGED FOR REPLACEMENT.
            </p>
            
            <div class="buttons">
                <a href="/" class="button">Home</a>
            </div>
        </div>
        </div>
    </body>
    </html>

"""

@app.route('/')
def home():
    return render_template_string(home_template)

@app.route('/house-rules')
def house_rules_page():
    return render_template_string(house_rules)

@app.route('/dep-guide')
def dep_guide_page():
    return render_template_string(departure_guide)

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
        df = df.dropna(subset=['Resident Name'])
        df['Second Resident Name'] = df['Second Resident Name'].fillna('-')
        
        room_data = df.to_dict(orient='records')
    except FileNotFoundError:
        room_data = []

    return render_template_string(room_list_template, rooms=room_data)


@app.route('/submit-maintenance', methods=['POST'])
def submit_maintenance():
    name = request.form['name']
    room = request.form['room']
    category = request.form['category']
    description = request.form['description']
    area = request.form['area']

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    # Create unique IDs for the request and images
    image_ids = []

    # Ensure the images subfolder exists
    images_folder = os.path.join(app.config['CSV_FOLDER'], app.config['IMAGES_SUBFOLDER'])
    os.makedirs(images_folder, exist_ok=True)

    # Handle image uploads
    for i in range(1, 3):
        image = request.files.get(f'image{i}')
        if image:
            image_id = str(uuid.uuid4())
            image_ids.append(image_id)
            image_path = os.path.join(images_folder, f'{image_id}.jpg')
            
            # Open the image and convert it to RGB if necessary
            img = Image.open(image)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(image_path, format='JPEG', optimize=True, quality=85)

    os.makedirs(app.config['CSV_FOLDER'], exist_ok=True)

    filename = os.path.join(app.config['CSV_FOLDER'], 'maintenance_requests.csv')
    fieldnames = ['timestamp', 'Requester Name', 'Requester Room No', 'Category', 'Description of Problem', 'Area Affected', 'Image IDs']

    if not os.path.isfile(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'timestamp': timestamp,
                'Requester Name': name,
                'Requester Room No': room,
                'Category': category,
                'Description of Problem': description,
                'Area Affected': area,
                'Image IDs': ', '.join(image_ids)
            })
    else:
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({
                'timestamp': timestamp,
                'Requester Name': name,
                'Requester Room No': room,
                'Category': category,
                'Description of Problem': description,
                'Area Affected': area,
                'Image IDs': ', '.join(image_ids)
            })

    return 'Data submitted successfully!'



@app.route('/submit-guest', methods=['POST'])
def submit_guest():
    try:
        resident_name = request.form['resident_name']
        room = request.form['room']
        num_guests = int(request.form['num_guests'])
        arrival_date = request.form['arrival_date']
        departure_date = request.form['departure_date']

        # Retrieve guest names and phone numbers dynamically
        guest_data = []
        for i in range(1, num_guests + 1):
            guest_name = request.form.get(f'guest_name_{i}', '')
            guest_phone = request.form.get(f'guest_phone_{i}', '')
            if guest_name and guest_phone:
                guest_data.append({'name': guest_name, 'phone': guest_phone})

        # Get the current date and time
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

        # Ensure the uploads folder exists
        os.makedirs(app.config['CSV_FOLDER'], exist_ok=True)

        # Save the data to a CSV file
        filename = os.path.join(app.config['CSV_FOLDER'], 'guest_requests.csv')
        fieldnames = ['timestamp', 'resident_name', 'room', 'guest_data', 'arrival_date', 'departure_date']

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
                'guest_data': ', '.join([f"{guest['name']} ({guest['phone']})" for guest in guest_data]),
                'arrival_date': arrival_date,
                'departure_date': departure_date
            })

        return 'Data submitted successfully!'

    except KeyError as e:
        return f"Error: Missing field {e}", 400
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

@app.route('/contact')
def contact_page():
    return render_template_string(emergency_contacts)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
