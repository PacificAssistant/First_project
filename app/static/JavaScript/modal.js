document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("openModalBtn");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function () {
        console.log("Button pushed"); // Перевірка
        modal.style.display = "block";
    };

    span.onclick = function () {
        console.log("Closed modal!");
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            console.log("click outside the frame!");
            modal.style.display = "none";
        }
    };
});