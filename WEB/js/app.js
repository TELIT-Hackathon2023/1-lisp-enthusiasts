function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();



document.getElementById('boss').addEventListener('click', function (event) {
    event.preventDefault();
});
