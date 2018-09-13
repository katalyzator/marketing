// Initialize Firebase
var config = {
    apiKey: "AIzaSyB0uP3Amj2LDZv5c3tfcVDDHuYTiM7I4UY",
    authDomain: "newlife-dffd4.firebaseapp.com",
    databaseURL: "https://newlife-dffd4.firebaseio.com",
    projectId: "newlife-dffd4",
    storageBucket: "newlife-dffd4.appspot.com",
    messagingSenderId: "1082354059018"
};
var cashRequestForm = $('#cash-request');
var verifyNumberForm = $('#code-verification');
var sendPointsForm= $('#send-points');
firebase.initializeApp(config);
firebase.auth().useDeviceLanguage();

$(document).ready(function () {
    ajax_request(sendPointsForm);
    window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
        'size': 'normal',
        'callback': function (response) {
            // reCAPTCHA solved, allow signInWithPhoneNumber.
            // ...
        },
        'expired-callback': function () {
            // Response expired. Ask user to solve reCAPTCHA again.
            // ...
        }
    });
    recaptchaVerifier.render().then(function (widgetId) {
        window.recaptchaWidgetId = widgetId;
        var recaptchaResponse = grecaptcha.getResponse(window.recaptchaWidgetId);
    });

    function getPhoneNumberFromUserInput() {
        return '{{ request.user.phone }}';
    }

    var appVerifier = window.recaptchaVerifier;

    function isPhoneNumberValid() {
        var pattern = /^\+[0-9\s\-\(\)]+$/;
        var phoneNumber = getPhoneNumberFromUserInput();
        return phoneNumber.search(pattern) !== -1;
    }

    cashRequestForm.on('submit', function (e) {
        e.preventDefault();
        if (isPhoneNumberValid) {
            firebase.auth().signInWithPhoneNumber(getPhoneNumberFromUserInput(), appVerifier)
                .then(function (confirmationResult) {
                    // SMS sent. Prompt user to type the code from the message, then sign the
                    // user in with confirmationResult.confirm(code).
                    window.confirmationResult = confirmationResult;
                    cashRequestForm.fadeOut();
                    verifyNumberForm.fadeIn();
                    verifyNumberForm.on('submit', function (e) {
                        e.preventDefault();
                        confirmationResult.confirm($('#code').val()).then(function (result) {
                            console.log(cashRequestForm.serialize());
                            $.ajax({
                                url: '{% url 'cash_request' %}',
                                method: 'POST',
                                data: cashRequestForm.serialize(),
                                success: function (response) {
                                    console.log(response)
                                }
                            })
                            // User signed in successfully.;
                            // ...
                        }).catch(function (error) {
                            // User couldn't sign in (bad verification code?)
                            // ...
                        });
                    })
                }).catch(function (error) {
                console.log(error);
                grecaptcha.reset(window.recaptchaWidgetId);
                // Error; SMS not sent
                // ...
            });
        }
        else {
            $('form').prepend('<h1>Неправильный номер телефона</h1>')
        }
    })
});