function geyFunction() {

	console.log("button pressed");
	
	const ledData = '{"led":false}'
	const obj = JSON.parse(text);

	if (obj.led == false){
		obj.led = true;
		document.getElementById("gey").innerHTML = "Led is ON";
		console.log("1");
	}
	else if (obj.led == true){
		obj.led = false;
		document.getElementById("gey").innerHTML = "Led is OFF";
		console.log("2");
	}
}