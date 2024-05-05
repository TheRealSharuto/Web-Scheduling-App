window.onload = function () {
    showButtonFunctionality();
    sendSubmittedData();
};

function showButtonFunctionality() {
    document.getElementById("show-schedule").addEventListener("click", function () {
        console.log("Button clicked!");
        let selectedDate = document.getElementById("date").value;

        const xml = new XMLHttpRequest();

        xml.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                // Check if the content type of the response is JSON
                const contentType = this.getResponseHeader("content-type");
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    // Parse the JSON response
                    const dataReply = JSON.parse(this.responseText);
                    console.log(dataReply);
                    // Use the information that the Python function returns here
                    showTimeSlots(dataReply);
                } else {
                    console.log("Response is not JSON");
                    // Handle the response accordingly if it's not JSON
                }
            }
        };

        xml.open("POST", "/telescope_time", true);
        xml.setRequestHeader("Content-type", "application/json");
        const dataSend = JSON.stringify({
            'date': selectedDate,
            'type': 'calendar'
        });
        xml.send(dataSend);
    });
}

function showTimeSlots(dataReply) {
    dateAndTimesDiv = document.getElementById("dates-and-times");
    dateAndTimesDiv.innerHTML = "";

    let html = ""; // Initialize an empty string to hold the HTML content

    for (const [key, value] of Object.entries(dataReply)) {
        if (value.length > 0) {
            // Open the div tag for each set of radio buttons
            html += "<div id=\"" + key + "\">";
            html += "<br><h4 class=\"time-slot-date\" data-date=\"" + key + "\">" + key + "</h4>" + "<br>";
            for (let i = 0; i < value.length; i++) {
                value[i] = convertTo12Hour(value[i]);
                html += "<label class=\"radio-label-text\"><input type=\"radio\" class=\"time-radio-button\" id=\"" + value[i] + "\" name=\"time-slot" + "\" value=\"" + value[i] + "\">" + value[i] + " (3 hours)</label><br>";
            }
            // Close the div tag for each set of radio buttons
            html += "</div>";
        }
    }

    // Set innerHTML after the loop has completed
    dateAndTimesDiv.innerHTML = html;
}

function convertTo12Hour(timeStr) {
    // Split the time string into hours, minutes, and seconds
    const [hours, minutes, seconds] = timeStr.split(':');

    // Create a Date object and set the time
    const dateObj = new Date();
    dateObj.setHours(hours);
    dateObj.setMinutes(minutes);

    // Get the 12-hour format time string
    const time12Hour = dateObj.toLocaleString('en-US', {
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });

    console.log("time 12 hour:" + time12Hour);

    return time12Hour;
}

function sendSubmittedData(submittedDate) {
    // Create new XMLHttpRequest object
    const submitForm = document.getElementById('submit-form');

    submitForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Get value of radio button

        const selectedTime = document.querySelector('input[name="time-slot"]:checked');
        let selectedValue = null;

        if (selectedTime) {
            selectedValue = selectedTime.value;
            console.log("selected value:", selectedValue);
           
            let chosenDate = selectedTime.parentNode.parentNode.id;
            console.log("Chosen date:", chosenDate);
            
            sendFormToPython(chosenDate, selectedValue);

        } else {
            alert('Please select a time under one of the presented dates');
        }
    });
    
}

function sendFormToPython(chosenDate, selectedTime) {

    const xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                // Check if the content type of the response is JSON
                const contentType = this.getResponseHeader("content-type");
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    // Parse the JSON response
                    const dataReply = JSON.parse(this.responseText);
                    console.log(dataReply);
                    
                    location.reload();
                    alert('Reservation was successfully made');
                } else {
                    console.log("Response is not JSON");
                    // Handle the response accordingly if it's not JSON
                }
                
            }
        };

        xhr.open("POST", "/telescope_time", true);
        xhr.setRequestHeader("Content-type", "application/json");
        const formDataSend = JSON.stringify({
            'date': chosenDate,
            'time': selectedTime,
            'type' : 'form'
        });
        xhr.send(formDataSend);
    }