var firebaseConfig = {
    apiKey: "AIzaSyCEbevoIw6HvbRiOK5kJNbNoZ9Nou7ARow",
    authDomain: "parkeasetesting-f25e5.firebaseapp.com",
    projectId: "parkeasetesting-f25e5",
    storageBucket: "parkeasetesting-f25e5.appspot.com",
    messagingSenderId: "375046177762",
    appId: "1:375046177762:web:95de52543187fce13bafbb",
    measurementId: "G-YWB6FVTTTV"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const database = firebase.database();

auth.onAuthStateChanged(function(user) {
    if (user) {
        var userRef = database.ref('users/' + user.uid);
        userRef.once('value').then(function(snapshot) {
            var userData = snapshot.val();
            if (userData && userData.Name && userData.Registered_Vehicle_Number && userData.Wallet_Balance !== undefined) {
                document.getElementById('welcome_message').innerHTML = '<p>Welcome, <strong>' + userData.Name + '</strong><br>Vehicle number : <strong>' + userData.Registered_Vehicle_Number + '</strong></p>';
                document.getElementById('background-container').innerHTML = '<p>Wallet Balance: <strong>' + userData.Wallet_Balance + '</strong></p>';
                var contactEmail = 'parkeasetesting@gmail.com';
                var termsContent = '<p>Click to read Parkease\'s <a href="t&c.html">Terms & Conditions</a>, <a href="privacypolicy.html">Privacy Policy</a>, <a href="refundpolicy.html">Refund Policy</a> || <a href="mailto:' + contactEmail + '">Contact Us</a>.</p>';
                var termsContainer = document.getElementById("terms-container");
                termsContainer.innerHTML = termsContent;
            }
        }).catch(function(error) {
            console.error("Error retrieving user data:", error);
        });
    } else {
        window.location.href = "index.html";
    }
});

const logoutButton = document.getElementById('logout-button');
logoutButton.addEventListener('click', function() {
    auth.signOut().then(function() {
        window.location.href = "index.html";
    }).catch(function(error) {
        console.error("Error signing out:", error);
    });
});

const addMoneyButton = document.getElementById('add-money-button');
addMoneyButton.addEventListener('click', function() {
    window.location.href = "https://rzp.io/l/PuoKXYYu"; 
});

