/*comparator(){
	var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
        }
    };
    xmlhttp.open("GET", "161.116.56.65", true);
    xmlhttp.send();
}*/
comparator(){
	var misCabeceras = new Headers();

	var miInit= {
		method:'GET',
		headers:misCabeceras,
		mode:'cors',
		cache:'default'
	};

	var resp = fetch('161.116.56.65',miInit);

	document.getElementById('prova').innerHTML=prova;
}