function time_of_day(which){

	$("#tod_dropdown").html(which);
	switch(which){
		case "Morning":
			$("#id_tod").val("M");
			break;
		case "Afternoon":
			$("#id_tod").val("A");
			break;
		case "Evening":
			$("#id_tod").val("E");
			break;
		case "Night":
			$("#id_tod").val("N");
			break;
	}
}