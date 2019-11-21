var return_date = document.getElementById("return_date");
var oneWayButton = document.getElementById("oneWayButton");
var roundTripButton = document.getElementById("roundTripButton");
var searchButton = document.getElementById("searchButton");
var checkButton = document.getElementById("checkButton");

var searchBlock = document.getElementById("searchBlock");
var checkBlock = document.getElementById("checkBlock");

function oneWay(){
    return_date.style.display = "none";
    oneWayButton.className = "active";
    roundTripButton.className = "";
}

function roundTrip(){
    return_date.style.display = "block";
    roundTripButton.className = "active";
    oneWayButton.className = "";
}

function search(){
    checkBlock.style.display = "none";
    searchBlock.style.display = "block";
    searchButton.className = "chosen";
    checkButton.className = "";
}

function check(){
    searchBlock.style.display = "none";
    checkBlock.style.display = "block";
    checkButton.className = "chosen";
    searchButton.className = "";
}