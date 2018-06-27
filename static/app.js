$(document).ready(function() {
	$(document).foundation();

	$('#filter-date').fdatepicker({
	  format: 'mm-dd-yyyy',
	  disableDblClickSelection: true
	});

	menuBarViewModel = {
		admin_password: ko.observable(''),
		can_be_admin: ko.observable(serverData.can_be_admin),
		logged_as_admin: ko.observable(serverData.logged_as_admin),
		submitAdminLogin: function() {
			$.ajax({
				url: 'api/admin/login',
				type: 'POST',
				data: ko.toJSON(menuBarViewModel),
				contentType: 'application/json; charset=utf-8',
				success: function(result) {
					console.log(result);
					menuBarViewModel.logged_as_admin(true);
					hideCallout();
				},
				error: function(result) {
					if (result && result.status == 401) {
						showCallout('alert', 'Wrong admin password', 'You can try to login as admin again');
					}
				},
				complete: function() {
					$('#loginAdminModal').foundation('close');
					menuBarViewModel.admin_password('');
				}
			});
		},
		submitAdminLogout: function() {
			$.ajax({
				url: 'api/admin/logout',
				type: 'POST',
				data: ko.toJSON(menuBarViewModel),
				contentType: 'application/json; charset=utf-8',
				success: function(result) {
					console.log('Admin logged out')
					menuBarViewModel.logged_as_admin(false);
					showCallout('success', 'Logged out as admin', 'You are not logged in as admin now');
				},
				error: function(result) {
					console.error(result);
					$('#loggedOutAsAdmin').css('display', 'none')
				},
				complete: function() {
				}
			})
		}
	}


	ko.applyBindings(menuBarViewModel)
});

function showCallout(kind, title, message) {
	if (!kind) kind = success;
	$('#commonCallout').removeClass()
	$('#commonCallout').addClass('callout').addClass(kind);
	$('#commonCallout h5').text(title);
	$('#commonCallout p').text(message);
	$('#commonCallout').css('display', 'block');
}

function hideCallout() {
	$('#commonCallout').css('display', 'none');
}