window.onload = function() {
    showButtonFunctionality();
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
            'date': selectedDate
        });
        xml.send(dataSend);
    });
}

function showTimeSlots(dataReply) {
    dateAndTimesDiv = document.getElementById("dates-and-times");
    dateAndTimesDiv.innerHTML = "";

    for (const [key, value] of Object.entries(dataReply)) {
        if (value.length > 0) {
            dateAndTimesDiv.innerHTML += (
                "<br><h4 class=\"time-slot-date\">" + key + "</h4>" + "<br>");
            for (let i = 0; i < value.length; i++) {
                value[i] = convertTo12Hour(value[i]);
                dateAndTimesDiv.innerHTML += (
                    "<label class=\"radio-label-text\"><input type=\"radio\" class=\"time-radio-button\" name=\"time-slot" + "\" value=\"" + value[i] + "\">" + value[i] + " (3 hours)</label><br>"
                );
            }
        }
    }
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