function loader() {
  $('#loader').show(); 
}

function validation(){
  if(document.getElementById("g-recaptcha-response").value==""){
    document.getElementById("recaptcha").click();
  }
  var i;
  //document.getElementById('query').value=document.getElementById("query").placeholder+":"+document.getElementById('query').value;
  var query_type;
  var mainquery=document.getElementById('searchquery').value;
  if (mainquery.split(":")[0]=="cluster"){
    mainquery=mainquery.split(":")[1].replace(/=/g,":");
    mainquery=mainquery.split(",");
  }else{
    mainquery=[mainquery];
  }
  
  for( i in mainquery){
    var flag=false;
    var query=mainquery[i];
    if (/((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))/.test(mainquery[i].split(':').slice(1).join(':'))==true) {
      alert("ip")
      query_type="ip";
      flag=true;break;
    }
    else if (/^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+[._-]?)*$/.test(query)==true){
      query_type="social";
      flag=true;break;
    }
    else if (/^(?:[0-9a-fA-F]{2}[:]?){5}(?:[0-9a-fA-F]{2}?)$/.test(query)==true){
      query_type="mac";
      flag=true;break;
    }
    else if (/^\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$/.test(query)==true){
      query_type="phone";
      flag=true;break;
    }
    else if (/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(query)==true){
      query_type="email";
      flag=true;break;
    }
    else if (/^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(query)==true){
      query_type="domain";
      flag=true;break;
    }
    else if (/^[A-Z]{2}[0-9]{2}[A-Z]{0,2}[0-9]{4}$/.test(query.toUpperCase())==true){
      query_type="vehicle";
      flag=true;break;
    }
    else if(/^[13][a-km-zA-HJ-NP-Z0-9]{26,33}$/.test(query)==true){
      query_type="btc";
      flag=true;break;
    }
    else if(/^[a-zA-Z0-9]{4,20}$/.test(query)==true){
      query_type="fbsearch";
      flag=true;break;
    }
  }
  if(flag==true){
    document.getElementById('query').value=query_type+":"+document.getElementById('searchquery').value;
    //alert(document.getElementById('query').value);
    //document.getElementById("recaptcha").click();
    return true;
  }
  else{
    $('.toast').toast('show');
    document.getElementById("toast").style.zIndex="1";
    return false;
  }

}