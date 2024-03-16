# PARKEASE: Modern Parking Management System

PARKEASE is an innovative solution to parking management, combining software and hardware components for enhanced efficiency and user satisfaction. By leveraging advanced technologies such as the ESP32 microprocessor, ultrasonic sensors, optical character recognition (OCR), computer vision, and Firebase Realtime Database, PARKEASE aims to revolutionize the parking experience.

## Overview
The project presents a comprehensive parking management system that automates crucial procedures, including vehicle identification, billing, and real-time monitoring. The system is designed to provide a hassle-free experience for users while optimizing space utilization and revenue generation for parking facility managers.

## Key Features
1. **Hardware Component:** Utilizes ESP32 microprocessor and ultrasonic sensors for precise vehicle identification at entry and exit points, ensuring reliable detection.
2. **Software Enhancements:** Incorporates OCR and computer vision technologies for seamless license plate detection and accurate vehicle identification, streamlining the parking process.
3. **Wallet System:** Offers a user-friendly payment method through a wallet system for both regular users and guests, allowing users to conveniently top up their wallet for parking fees.
4. **Dynamic QR Code:** Provides an alternative payment option via a dynamic QR code for guest users, enabling payments through the Unified Payments Interface (UPI).
5. **Real-time Monitoring:** Integrates Firebase Realtime Database for seamless data management and real-time monitoring of parking occupancy, entry, and exit logs.

## Objectives
1. **Efficient Entry and Exit:** Implement automated processes for vehicle entry and exit, including number plate detection and recognition.
2. **Accurate Billing:** Calculate parking duration and costs, incorporating discounts and payment options for user convenience.
3. **Real-time Monitoring:** Utilize Firebase Realtime Database for seamless data management, enabling real-time monitoring of parking occupancy, entry, and exit logs.
4. **User Registration and Authentication:** Implement user registration functionalities to provide personalized services.

## Problem Statement
Traditional parking systems face challenges such as ineffective vehicle identification, manual input and payment methods causing delays, and lack of quick payment choices. PARKEASE addresses these issues by automating crucial procedures, facilitating easy entry and exit, precise billing, and real-time monitoring.

## Components Requirements
### Software Requirements Specification
- OpenCV for image processing and vehicle plate detection.
- pytesseract for OCR (Optical Character Recognition) to extract text from images.
- Firebase Realtime Database for storing and retrieving parking information.
- QR Code Generation for payment processing.
- Development Environment: VS Code or other IDEs for code development and testing.
- Web Technologies: HTML, CSS, JavaScript for the website interface connected to Firebase.

### Hardware Requirements Specification
- Webcam for vehicle plate detection.
- ESP32 microprocessor for real-time communication.
- Ultrasonic Sensor for vehicle presence detection.

PARKEASE aims to improve parking management efficiency, maximize space utilization, and enhance the overall user experience.
