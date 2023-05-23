frame = document.getElementById("myFrame");
link = document.getElementById("myLink");
link.addEventListener("click", function(event) {
    event.preventDefault();
    frame.src = "https://open.spotify.com/embed/track/" + link.className + "?utm_source=generator";
});

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
    window.onclick = function(event) {
        if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
            }
        }
        }
    } 
}

function showModal(){
    var frm = document.getElementById("form");
    var btn = document.getElementById("btn");
    var cls = document.getElementById("cls");

    btn.onclick = function(){
        frm.style.display = "block";
    }

    cls.onclick = function() {
        frm.style.display = "none";
    }
}

function rateModal(){
    var frm = document.getElementById("rateform");
    var btn = document.getElementById("dropdown-link1");
    var cls = document.getElementById("ratecls");

    btn.addEventListener("click", function(event){
        event.preventDefault();
        frm.style.display="block";
    });

    cls.onclick = function() {
        frm.style.display = "none";
    }
}

function plMenu(){
    var list = document.getElementById("plmenu");
    var btn = document.getElementById("dropdown-link2");
    var cls = document.getElementById("plmenucls");

    btn.addEventListener("click", function(event){
        event.preventDefault();
        list.style.display="block";
    });

    cls.onclick = function() {
        list.style.display = "none";
    }
}