$(document).ready(function(){

	var rootRef = firebase.database().ref().child("teachers_uploads");

	rootRef.on("child_added", snap=>{
		var name = snap.child("name").val();
		var description = snap.child("description").val();

		$("#table_body").append("<tr><td>" + name +"</td><td>" 
			+ description +"</td><td><button>Load Job</button></td></tr>");
		console.log(rootRef)

	});
}); 