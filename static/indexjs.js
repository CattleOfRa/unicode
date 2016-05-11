$(document).keydown(function(e){
    if(e.which === 13){
        var txt = document.getElementsByName('tbchannel')[0].value;
        txt = txt.replace(/#/g, '')
        if(txt.length === 0){            
            alert("Hashtag can't be empty");
        }else{
            window.location.href = ("/tag/" + txt);
        }    
    }   
});


