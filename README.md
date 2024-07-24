# UmePottsPoint

This project contains the house rules for <a href="https://www.ume.com.au"> UME Potts Point</a>, presented in a digital format to streamline communication and ensure easy access for all residents.<br>

The purpose of this repository is to provide a clear, accessible, and digital version of the house rules for UME accommodations. This ensures that all residents have easy access to the rules, helping to maintain a safe, respectful, and enjoyable living environment. <br>

This digital version of the UME House Rules solves several problems and reduces reliance on manual work and paperwork in the following ways:

## Benefits

- **Accessibility**: Residents can easily access the rules online at any time, ensuring they are always aware of the guidelines.
- **Environmentally Friendly**: Reduces the need for printed materials, saving paper and contributing to environmental sustainability.
- **Efficiency**: Streamlines the onboarding process by providing new residents with immediate access to the rules, reducing the need for physical handouts and meetings.
- **Transparency**: Ensures that all residents have access to the same information, promoting fairness and consistency.
- **Security**: By clearly outlining the rules, potential disputes can be minimized, and the safety and enjoyment of all residents can be maintained.

## Features

- Responsive web form for submitting maintenance requests
- Stores submission data in a CSV file
- Data fields include resident's name, room number, problem description, and area/unit/room
- Automatic creation of new CSV files based on the current month and year


## Screenshot

![Maintenance Form](Screenshot.png)

## Prerequisites

- Python 3.6 or higher
- Flask library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/hemangsharma/UME-Potts-Point-Maintenance-Form.git
    cd UME-Potts-Point-Maintenance-Form
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install Flask
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to access the maintenance form.

3. Fill out the form with the necessary information and submit it. The data will be saved to a CSV file named with the current month and year (e.g., `July_2024.csv`).


## Security

To ensure the security of the CSV file, only the application server should have access to it. Do not expose the CSV file directly through the web server. Consider using appropriate file permissions and server configurations to protect the data.

## Contact

For any questions or inquiries, please contact sharmahemang2000@gmail.com.
