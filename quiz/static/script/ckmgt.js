
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }
  
  function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  
  function checkUserCookie() {
    var user = getCookie('playerid');
    if (user != "") {
      alert("Welcome again " + user);
    } else {
      user = prompt("Please enter your mobile number:", "");
      if (user != "" && user != null) {
        setCookie("playerid", user, 1);
      }
    }
  }

  function deleteCookie(cname) {
    var d = new Date();
    d.setTime(d.getTime() + -1);
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=;" + expires + ";path=/";
  }