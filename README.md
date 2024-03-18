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

## Methodology

PARKEASE is an automated parking system designed to provide hassle-free parking solutions for users. Below is a detailed overview of how PARKEASE operates:

1. **User Registration:**
   - Registered users visit [parkease.vercel.app](https://parkease.vercel.app) to register by providing their vehicle number, name, and basic details.
   - Upon registration, a digital wallet is created for the user, allowing them to add money using preferred payment methods.

2. **Parking Entry:**
   - When a vehicle enters the parking lot, sensors detect its presence and trigger the camera.
   - The camera captures the vehicle number plate, which is processed using Optical Character Recognition (OCR) or Tesseract.
   - The extracted number along with the timestamp is sent to the database (Firebase), and a parking slot is assigned.
   - For registered users, the system checks their wallet balance. A minimum balance of 5 rupees is required for parking.

3. **Parking Duration:**
   - The system records the entry time and calculates the duration of parking based on the entry and exit times.

4. **Exit Process:**
   - When the vehicle exits, the exit time is recorded.
   - For registered users, the system automatically deducts the parking fee from their wallet if they have a sufficient balance.
   - Guest users receive a dynamic QR code containing the bill amount, which they pay upon exit.

5. **Billing:**
   - The billing system calculates the parking fee based on the time parked, with a standard rate of 20 rupees per hour.

## License
Distributed under the MIT License. See [LICENSE](https://github.com/Shivanaik11/PARKEASE/blob/main/LICENSE.md) for more information.




