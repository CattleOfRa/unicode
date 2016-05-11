$(document).keydown(function(e){
    if(e.which === 13){
        var ans = document.getElementsByName('tbans')[0].value;
        if(ans != ""){
               submits ++;
               $.get("http://michaelpetersenior.com:5000/api/v1.0/checkanswer/" + sid + "^" + tweetid + "^" + ans, function(data, status){
                    if(data === "False"){
                        updatebar();
                        document.getElementById("tbans").value = ""
                        document.getElementById("tbans").placeholder = "Ooops, try again...";
                    }else{
                        correct ++;
                        updatebar();
                        document.getElementById("tbans").value = ""
                        document.getElementById("tbans").placeholder = "Correct!";                    
                        $.get("http://michaelpetersenior.com:5000/api/v1.0/getquestion/" + sid + "^" + document.getElementById("channeldiv").innerHTML, function(data, status){               
                            var lst = data.split("^", "2");
                            tweetid = lst[0];
                            if(typeof lst[1] === "undefined"){
                                alert("No more questions");
                                $("questiontext").fadeOut("slow");
                                
                            }else{
                                document.getElementById("questiontext").innerHTML = lst[1];
                            }
                        });                    
                    }
               });                  
        }
    }   
});

function updatebar(){
    document.getElementById("progress-bar").style.width = (correct/submits)*100 + "%";
    document.getElementById("progress-text").innerHTML = correct + " / " + submits;
    document.getElementById("tweetbtn").outerHTML = "<a href='http://twitter.com/home?status=I%20got%20" + correct + "/" + submits + "%20on%20the%20%23UNIcode%20challenge%21' id='tweetbtn' target='_blank' class='btn-social btn-outline'><i class='fa fa-fw fa-twitter'></i></a>"
}
var submits = 0;
var correct = 0;
var tweetid = "";
var sid = "";
$( document ).ready(function() {   
       var scookie = getCookie("sid");
       sid = scookie;
       if(typeof scookie === "undefined"){           
           $.get("http://michaelpetersenior.com:5000/api/v1.0/getsid", function(data, status){
                createCookie("sid", data, 365);
           });
       }
    
    $.get("http://michaelpetersenior.com:5000/api/v1.0/getquestion/" + sid + "^" + document.getElementById("channeldiv").innerHTML, function(data, status){
                var lst = data.split("^", "2");
                tweetid = lst[0];
                document.getElementById("questiontext").innerHTML = lst[1];
           });
});


function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}
function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}
