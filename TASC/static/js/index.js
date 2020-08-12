function caseload(){
  alert(1);
}

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

function ClearActivityConfirmation(){
  swal({
    title: "Are you sure?",
    text: "Reports of the Deleted Scans will still remain safe",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {
      swal("All Activities has been deleted!", {
        icon: "success",
      });
      Clearactivity();
    }
  });
}

function Clearactivity(){

  $.ajax({
    url: "",
    headers: {'X-CSRFToken': getCookie("csrftoken")},
    type: "POST",
    data: {'clear':true},
    cache:false,
    success: function(resp){
      document.getElementById("activitybar").innerHTML='<p class="text-muted text-center">No Activity</p>';
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

function deleteReport(rowindex){

  console.log(rowindex)

  swal({
    title: "Are you sure?",
    text: "Report once deleted cannot be retrieved",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {
      swal("The Report has been deleted!", {
        icon: "success",
      });

      $.ajax({
        url: "deletereport",
        headers: {'X-CSRFToken': getCookie("csrftoken")},
        type: "POST",
        data: {'rowindex':rowindex},
        cache:false,
        success: function(resp){
          location.reload();
        }
      });

    }
  });

}

async function onSubmit() {
  var casedata;
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
    "autoDismisss":true,
    "maxOpened": 1,
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  };
  if(validation()==true){
    //document.getElementById("trigger").click();
    casedata={"casename":document.getElementsByName("casename").value,"caseno":document.getElementsByName("caseno").value,"casedescription":document.getElementsByName("casedescription").value};
    var name=document.getElementsByName("name").value;
    var email=document.getElementsByName("email").value;
    var phone=document.getElementsByName("phone").value;
    var username=document.getElementsByName("username").value;
    
    toastr.success("Scan added to the queue");    
    $.ajax({
        url: "/",
        headers: {"X-CSRFToken":getCookie('csrftoken')},
        type: "POST",
        data: {'query':document.getElementById('query').value,"name":name,"phone":phone,"email":email,"username":username,"ajax":"True","case":casedata},
        cache:false,
        success: function(resp){
          if(typeof(resp) != "undefined"){
            toastr.remove();
            toastr.clear();
            toastr.warning(resp['Message']);
          }
          return false;
        }
    });
    return false;
  }
  else
  {
    toastr.error("Enter a Valid Query");
    return false;
  }
  return false;
}

function validation(){
  var i;
  var query_type;
  var index;
  var flag;

  var misc = $("#misc").val().split(",");
  
  $.each( misc, function( key, query ) {
    flag=false;
    
    if (/((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))/.test(query)==true) {
      query_type="ip";
      flag=true;
    }
    else if (/^(?:[0-9a-fA-F]{2}[:]?){5}(?:[0-9a-fA-F]{2}?)$/.test(query)==true){
      query_type="mac";
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
    else if(/^[a-zA-Z0-9]{4,20}$/.test(query)==true){
      query_type="tag";
      flag=true;
    }

    if(flag==true){
      //document.getElementById('query').value=query_type+":"+document.getElementById('searchquery').value;
      if(query_type=="tag"){
        document.getElementById("tag").value=query;}
      else{
        document.getElementById("query").value+=query_type+":"+query+",";}
    }
    else{
      return false;
    }
  });
  return flag;
}