function get_query(){ 
    var url = document.location.href; 
    var qs = url.substring(url.indexOf('?') + 1).split('&'); 
    for(var i = 0, result = {}; i < qs.length; i++){ 
        qs[i] = qs[i].split('='); result[qs[i][0]] = decodeURIComponent(qs[i][1]);
     } 
     return result; }

var params = get_query()


function getWage(){
    let xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === xhttp.DONE) {
            if (xhttp.status === 200) {
            // do something with xhttp.responseText
                var val = xhttp.responseText;
                var parser = new DOMParser();
                var htmlDoc = parser.parseFromString(val,"text/html");
                var wage = htmlDoc.getElementById("wage");
                var divToBeChanged = document.getElementById("wage");
                divToBeChanged.innerHTML = wage.innerHTML;

            } else {
            // handle errors
            }
        }
        };

    xhttp.open("GET", `https://realtime-wagebot.herokuapp.com/mywage?wage=${params['wage']}&the_day=${params['the_day']}&the_time=${params['the_time']}&start=${params['start']}&end=${params['end']}`, true);
    xhttp.send();
}

function init(){
    setInterval(getWage, 1000);
}

init();