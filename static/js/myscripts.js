$('document').ready(function(){
    console.log("All set")
    var phoneCall = false;
    $('#record').on('click', function(e){
        console.log("hey there")
        startDictate();
    })


    $('#labnol').submit(function(e){

        var inp_txt = $('#transcript').val();
        phoneCall = false
       console.log(inp_txt);
       $.ajax({
              type : 'POST',
              url : '/api/get_text/',
              contentType: 'application/json;charset=UTF-8',
              data : inp_txt,
              success: got_reply,
                error: error_occured
            });
       e.preventDefault();
       return false
    });

function submit_form(){
}

function got_reply(response){
    console.log(response)

    $("#ans").text(response);
    $("#ans").show();
    if(phoneCall){
    console.log("reading the message")
        var msg = new SpeechSynthesisUtterance(response);
        window.speechSynthesis.speak(msg);
    }

}

function error_occured(response){
    console.log(response)
}

function startDictate(event) {
        console.log(" In start dictation app")
        if (window.hasOwnProperty('webkitSpeechRecognition')) {

          var recognition = new webkitSpeechRecognition();
          phoneCall = true;
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.lang = "en-US";
          console.log("started recording")
          recognition.start();
          console.log("stopped recording")

          recognition.onresult = function(e) {
            document.getElementById('transcript').value
                                     = e.results[0][0].transcript;
            recognition.stop();
            console.log("submitting the form")
            var inp_txt = $('#transcript').val();
            console.log(inp_txt);
            $.ajax({
              type : 'POST',
              url : '/api/get_text/',
              contentType: 'application/json;charset=UTF-8',
              data : inp_txt,
              success: got_reply,
                error: error_occured
            });
            return false
          };

          recognition.onerror = function(e) {
            recognition.stop();
          }

        }
  }
});