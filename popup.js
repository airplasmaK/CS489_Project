// Initialize butotn with users's prefered color


let changeColor = document.getElementById("changeColor");
var power=0;

chrome.storage.sync.get("color", () => {
  //var a_s= document.querySelectorAll('a')
  //for (var i = 0, l = a_s.length; i < l; i++){
    //a_s[i].style.backgroundColor = color
  //} 

  var level="";
  
  $(document).ready(function(){
    $("#check").change(function(){
        if($("#check").is(":checked")){
            power=1;
            alert(power);
        }
        else{
            alert("체크 해제");
        }
    });
    
  });
  
  $(document).ready(function () {
    $("button[name='low']").click(function () {
      power=1
      level="low";
      alert(level)
    });
  });
  
  
  $(document).ready(function () {
    $("button[name='mid']").click(function () {
      level="mid";
      alert(level)
    });
  });
  
  $(document).ready(function () {
    $("button[name='high']").click(function () {
      level="high";
      alert(level)
    });
  });
  
  setPageBackgroundColor();
});


function setPageBackgroundColor() {
  chrome.storage.sync.get("color", ({ color }) => {
    var a_s= document.querySelectorAll("a[href]")
    console.log(document.URL)

    url_ = document.URL

    list= null
    new_as = []
    as_url = []
    
    /*for (var i = 0, l = a_s.length; i < l; i++){
      if (a_s[i].getAttribute('href').slice(0,4)=='http'){
        child = a_s[i].childNodes
        tagornot = true
        for (var j=0; j<child.length;j++){
          if (child[j].nodeName=='IMG' || child[j].nodeName=='I' ){
            tagornot = false
          }
          else if (child[j].nodeName=='SPAN'||child[j].nodeName=='DIV'){
            t_child = child[j].childNodes
            for (var k=0; k<t_child.length;k++){
              if (t_child[k].nodeName=='IMG' || t_child[k].nodeName=='I' ){
                tagornot = false
              }
            }
          }
        }
        if (tagornot){
          new_as.push(a_s[i])
          as_url.push(a_s[i]["href"])
        }
      }
    }*/
    for (var i = 0, l = a_s.length; i < l; i++){
      if (a_s[i].getAttribute('href').slice(0,4)=='http'){
        child = a_s[i].childNodes
        
        for (var j=0; j<child.length;j++){
          //console.log(child[j].nodeName)
          if (child[j].nodeName=='H3'||child[j].nodeName=='#text'){
            new_as.push(a_s[i])
            as_url.push(a_s[i]["href"])
            break
          }
        }
      }
    }
    //console.log(as_url.toString())
    urls = as_url.toString()
    state = []


    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:1024',
      data: {urls:urls, power: power},
      dataType :'json',
      async: false,
      success: function(d){
        console.log("hihi")
        state = d
      },
      error: function(err){
        console.log("nothing")
      }
    })

    console.log(state)
    clear_as = []
    for (var i = 0, l = new_as.length; i < l; i++){
        child =new_as[i].childNodes
        if (Number(state[i])==0){
          console.log(new_as[i])
          new_as[i].style.color = 'gray'
          new_as[i].style.textDecoration = 'line-through'
          if (new_as[i].style.textDecoration!='line-through'){
            for (var j=0; j<child.length;j++){
              console.log(new_as[i])
              child[j].style.color = 'gray'
              child[j].style.textDecoration = 'line-through'
              t_child = child[j].childNodes
              if (child[j].style.textDecoration!='line-through'){
                for (var k=0; k<t_child.length;k++){
                  t_child[k].style.color = 'gray'
                  t_child[k].style.textDecoration = 'line-through'
                }
              }
            }
          }
        }
        /*for (var j=0; j<child.length;j++){
          //console.log(child[j].nodeName)
          if (child[j].nodeName=='H3'||child[j].nodeName=='#text'){
            //new_as[i].insertAdjacentHTML('beforeend','<img class = safety  width = "16px" height = "16px" src = "https://cdn-icons-png.flaticon.com/16/1161/1161388.png" alt="safe">')  
            new_as[i].style.color = 'gray'
            new_as[i].style.textDecoration = 'line-through'
            break
          }*/
          //else if (child[j].nodeName=='SPAN'||child[j].nodeName=='DIV'){
            //t_child = child[j].childNodes
            //for (var k=0; k<t_child.length;k++){
              //console.log(t_child[k])
              //if (t_child[k].nodeName=='#text'){
              //  child[j].insertAdjacentHTML('beforeEnd','<img class = safety  width = "15px"  src = "https://cdn-icons-png.flaticon.com/512/1161/1161388.png" alt="safe">')
              //}
              //else if (t_child[k].nodeName=='SPAN'||t_child[k].nodeName=='DIV'){
              //  tt_child = t_child[k].childNodes
              //  for (var m=0; m<tt_child.length;m++){
              //    //console.log(tt_child[m].nodeName)
              //  }
              //}
            //}
          //}
        
      }
  });
}