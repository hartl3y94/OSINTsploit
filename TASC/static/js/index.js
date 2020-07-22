function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function Clearactivity(){
  
  $.ajax({
    url: "",
    headers: {'X-CSRFToken': getCookie("csrftoken")},
    type: "POST",
    data: {'clear':true},
    cache:false,
    success: function(resp){
      document.getElementById("activitybar").innerHTML='<p class="text-muted">No Activity</p>';
    }
  }).done(function(){
    document.getElementById("clearactivity").removeAttribute("data-original-title");
    document.getElementById("clearactivity").setAttribute('data-original-title', "Cleared");
  });
  setTimeout(function(){
    document.getElementById("clearactivity").removeAttribute("data-original-title");
    document.getElementById("clearactivity").setAttribute('data-original-title', "Clear Activity");
  },2000)
}

function onSubmit() {
  toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  };
  if(validation()==true){
    toastr.success("Scan added to the queue");
    $.ajax({
        url: "/",
        headers: {'X-CSRFToken': '{{ csrf_token }}'},
        type: "POST",
        data: {'query':document.getElementById('query').value,"ajax":"True"},
        cache:false,
        success: function(resp){
          return false;
        }
    }).done(function () {
      toastr.success("Scan Completed");
  });
  return false;
  }else{
    toastr.error("Enter a Valid Query");
    return false;
  }
}

function validation(){
  var i;
  var query_type;

  var flag=false;
  var query=document.getElementById('searchquery').value;;
  if (/((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))/.test(query)==true) {
    query_type="ip";
    flag=true;
  }
  else if (/^(?:[0-9a-fA-F]{2}[:]?){5}(?:[0-9a-fA-F]{2}?)$/.test(query)==true){
    query_type="mac";
    flag=true;
  }
  else if (/^\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$/.test(query)==true){
    query_type="phone";
    flag=true;
  }
  else if (/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(query)==true){
    query_type="email";
    flag=true;
  }
  else if (/^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(query)==true){
    query_type="domain";
    flag=true;
  }
  else if (/^[A-Z]{2}[0-9]{2}[A-Z]{0,2}[0-9]{4}$/.test(query.toUpperCase())==true){
    query_type="vehicle";
    flag=true;
  }
  else if(/^[13][a-km-zA-HJ-NP-Z0-9]{26,33}$/.test(query)==true){
    query_type="btc";
    flag=true;
  }
  else if (/^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+[._-]?)*$/.test(query)==true){
    query_type="social";
    flag=true;
  }
  else if(/^[a-zA-Z0-9]{4,20}$/.test(query)==true){
    query_type="fbsearch";
    flag=true;
  }
  
  if(flag==true){
    document.getElementById('query').value=query_type+":"+document.getElementById('searchquery').value;
    return true;
  }
  else{
    return false;
  }

}