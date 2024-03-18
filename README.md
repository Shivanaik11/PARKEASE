<br/>
<p align="center">
  <a href="https://github.com/Shivanaik11/PARKEASE">
    <img src="images/company_logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PARKEASE</h3>

  <p align="center">
    "Park with ease, pay with breeze - your hassle-free parking solution is here with PARKEASE!"
    <br/>
    <br/>
    <a href="https://github.com/Shivanaik11/PARKEASE"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://parkease.vercel.app">View Demo</a>
    .
    <a href="https://github.com/Shivanaik11/PARKEASE/issues">Report Bug</a>
    .
    <a href="https://github.com/Shivanaik11/PARKEASE/issues">Request Feature</a>
  </p>
</p>

![Contributors](https://img.shields.io/github/contributors/Shivanaik11/PARKEASE?color=dark-green) ![Forks](https://img.shields.io/github/forks/Shivanaik11/PARKEASE?style=social) ![Stargazers](https://img.shields.io/github/stars/Shivanaik11/PARKEASE?style=social) 

## Table Of Contents
* [About the Project](#about-the-project)
* [Usage](#usage)
* [License](#license)

## About The Project
Introducing PARKEASE, the revolutionary concept designed to streamline parking with zero human intervention. Say goodbye to the hassle of searching for parking spots and dealing with attendants. PARKEASE leverages cutting-edge technology to automate the entire parking process, ensuring a seamless experience for users.

## Usage
User Registration:

Registered users visit  <a href="https://parkease.vercel.app">parkease.vercel.app</a> and register by providing their vehicle number, name, and basic details.
Upon registration, a digital wallet is created for the user, linked to their account.
Parking Entry:

When a vehicle enters the parking lot, sensors detect its presence and trigger the camera.
The camera captures the vehicle number plate.
Optical Character Recognition (OCR) or Tesseract is used to extract the vehicle number.
The extracted number along with the timestamp is sent to the database (Firebase), and a parking slot is assigned.
If the user is registered, the system checks their wallet balance. A minimum balance of 5 rupees is required for parking.
Parking Duration:

The vehicle remains parked, and the entry time is recorded.
Time parked is calculated based on the entry and exit times.
Exit Process:

When the vehicle exits, the exit time is recorded.
For registered users, the system automatically deducts the parking fee from their wallet if they have a sufficient balance.
For guest users, a dynamic QR code is generated containing the bill amount.
The user can scan the QR code and make the payment through a preferred payment method.
After successful payment, the user is allowed to exit, and the slot becomes available for the next vehicle.
Billing:

The billing system calculates the parking fee based on the time parked.
The standard rate is 20 rupees per hour.
For registered users, the fee is deducted directly from their wallet.
For guest users, the QR code contains the bill amount which they pay upon exit.

## License
Distributed under the MIT License. See [LICENSE](https://github.com/Shivanaik11/PARKEASE/blob/main/LICENSE.md) for more information.




