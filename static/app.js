console.log('hello!');

$(document).foundation();

$(document).ready(function() {
	$('#dp1').fdatepicker({
	  format: 'mm-dd-yyyy',
	  disableDblClickSelection: true
	});
});