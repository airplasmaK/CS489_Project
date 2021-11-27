// Initialize butotn with users's prefered color


let changeColor = document.getElementById("changeColor");

chrome.storage.sync.get("color", ({ color }) => {
  //var a_s= document.querySelectorAll('a')
  //for (var i = 0, l = a_s.length; i < l; i++){
    //a_s[i].style.backgroundColor = color
  //} 
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
    for (var i = 0, l = a_s.length; i < l; i++){
      if (a_s[i].getAttribute('href').slice(0,4)=='http'){
        child = a_s[i].childNodes
        tagornot = true
        for (var j=0; j<child.length;j++){
          if (child[j].nodeName=='IMG' || child[j].nodeName=='I' ){
            tagornot = false
          }
          else if (child[j].nodeName=='SPAN'){
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
    }

    console.log(as_url.toString())
    urls = as_url.toString()


    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:1024',
      data: {urls:urls},
      dataType :'json',
      success: function(d){
        console.log("hihi")
        console.log(d)
      },
      error: function(err){
        console.log("nothing")
      }
    })



    clear_as = []
    for (var i = 0, l = new_as.length; i < l; i++){
      new_as[i].insertAdjacentHTML('beforeend','<img class = safety  width = "15px"  src = "https://cdn-icons-png.flaticon.com/512/1161/1161388.png" alt="safe">')

      //console.log(new_as[i])
    }

  });
}