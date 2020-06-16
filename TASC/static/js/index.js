function loader() {
    $('#loader').show(); 
  }

  function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }

  function validation(){
    if(document.getElementById("g-recaptcha-response").value==""){
      document.getElementById("recaptcha").click();
    }
    var i;
    var mainquery=document.getElementById('query');
    if (mainquery.value.split(":")[0]=="cluster"){
      mainquery=mainquery.value.split(":")[1].replace(/=/g,":");
      mainquery=mainquery.split(","); 
    }else{
      mainquery=[mainquery.value];
    }
    for( i in mainquery){
      var flag=true;
      var query=mainquery[i].split(":");
      if(query.length>=2){
        if(["social","facebook","instagram","twitter","github"].indexOf(query[0])>=0){
          if (/^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*$/.test(query[1])==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Username or Account Name";
            $('.toast').toast('show');
            flag=false;break;
          }        
        }
        else if (query[0]=="ip"){
            if (/((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))/.test(document.getElementById('query').value.split(':').slice(1).join(':'))==false) {
              document.getElementById("error-msg").innerHTML="You have entered Invalid IP Address";
              $('.toast').toast('show');
              flag=false;break;
            }
        }
        else if(query[0]=="mac"){
          if (/^(?:[0-9A-F]{2}[:]?){5}(?:[0-9A-F]{2}?)$/.test(document.getElementById('query').value.split(':').slice(1).join(':'))==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid MAC Address";
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else if(query[0]=="phone"){
          if (/^\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$/.test(query[1])==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Phone Number";
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else if(query[0]=="email"){
          if (/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(query[1])==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Email Address"
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else if(query[0]=="domain"){
          if (/^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(query[1])==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Domain Address";
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else if(query[0]=="vehicle"){
          if (/^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$/.test(query[1].toUpperCase())==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Vechile Number";
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else if(query[0]=="btc"){
          if(/^[13][a-km-zA-HJ-NP-Z0-9]{26,33}$/.test(query[1])==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Bitcoin Address";
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else if(query[0]=="fbsearch"){
          if(/^[a-zA-Z0-9]{4,20}$/.test(query(1))==false){
            document.getElementById("error-msg").innerHTML="You have entered Invalid Keyword or Long Keyword";
            $('.toast').toast('show');
            flag=false;break;
          }
        }
        else{
          $('.toast').toast('show');
          flag=false;break;
        }
      }
      else{
        document.getElementById("error-msg").innerHTML="Do check your with the query format";
        $('.toast').toast('show');
        flag=false;break;
      }
    }

    //pop up alert
    if(flag==true){
      return true;
    }
    else{
      $('.toast').toast('show');
      document.getElementById("toast").style.zIndex="1";
      return false;
    }
  }