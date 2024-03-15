var firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const database = firebase.database();

function register() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var full_name = document.getElementById('full_name').value;
    var vehicle_number = document.getElementById('vehicle_number').value;

    if (validate_email(email) === false) {
        alert('Please Enter your Email');
        return;
    }

    if (validate_password(password) === false) {
        alert('Please Enter your Password');
        return;
    }

    if (validate_field(full_name) === false) {
        alert('Please Enter your Name');
        return;
    }

    if (validate_field(vehicle_number) === false) {
        alert('Please Enter your Registered Vehicle Number');
        return;
    }

    vehicle_number = vehicle_number.replace(/\s/g, '');
    vehicle_number = vehicle_number.toUpperCase();

    var vehicleNumberPattern = /^[A-Za-z]{2}\d{2}[A-Za-z]{1,2}\d{4}$/;
    if (!vehicleNumberPattern.test(vehicle_number)) {
        alert('Vehicle Number is not in the correct format\n Please Enter it in XY 12 Z 3456 format');
        return;
    }

    auth.createUserWithEmailAndPassword(email, password)
        .then(function () {
            var user = auth.currentUser;
            var database_ref = database.ref();
            var user_data = {
                Name: full_name,
                Registered_Vehicle_Number: vehicle_number,
                Wallet_Balance: 0 // Initial wallet balance set to 0
            };

            database_ref.child('users/' + user.uid).set(user_data);

            alert('Registered Successfully\n Kindly Login with your email and password');
        })
        .catch(function (error) {
            var error_message = error.message;
            alert(error_message);
        });
}

function login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    if (validate_email(email) === false) {
        alert('Please Enter your Email');
        return;
    }

    if (validate_password(password) === false) {
        alert('Please Enter your Password');
        return;
    }

    auth.signInWithEmailAndPassword(email, password)
        .then(function () {
            window.location.href = "dashboard.html";
        })
        .catch(function (error) {
            var error_message = error.message;
            alert(error_message);
        });
}

function validate_email(email) {
    var expression = /^[^@]+@\w+(\.\w+)+\w$/;
    return expression.test(email);
}

function validate_password(password) {
    return password.length >= 6;
}

function validate_field(field) {
    return field !== null && field.length > 0;
}
