$(document).ready(function() {
	$(document).foundation();

	$('#filter-date').fdatepicker({
	  format: 'mm-dd-yyyy',
	  disableDblClickSelection: true
	});

	menuBarViewModel = {
		admin_password: ko.observable(''),
		submitAdminLogin: function() {
			console.log('should submit');
			$.ajax({
				url: 'api/admin/login',
				type: 'POST',
				data: ko.toJSON(menuBarViewModel),
				contentType: 'application/json; charset=utf-8',
				success: function(result) {
					console.log(result);
				},
				error: function(result, message, status) {
					console.log(result, message, status);
					if (result && result.status == 401) {
						$('#wrongAdminPassword').css('display', 'block');
					}
				},
				complete: function() {
					$('#loginAdminModal').foundation('close');
					menuBarViewModel.admin_password('');
				}
			});
		}
	}


	ko.applyBindings(menuBarViewModel)
});