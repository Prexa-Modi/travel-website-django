/*$(function() {
  'use strict';

  if($('#datePickerExample').length) {
    var date = new Date();
    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    $('#datePickerExample').datepicker({
      format: "mm/dd/yyyy",
      format: "yyyy/mm/dd",
      todayHighlight: true,
      autoclose: true
    });
    $('#datePickerExample').datepicker('setDate', today);
  }
});*/

    $(document).ready(function() {
        'use strict';

        if ($('#startDatePicker').length && $('#endDatePicker').length) {
            var startDate = new Date();
            var endDate = new Date();

            // Set the end date to be one week ahead of the current date
            endDate.setDate(endDate.getDate() + 7);

            // Initialize start date picker
            $('#startDatePicker').datepicker({
                format: "yyyy-mm-dd",
                todayHighlight: true,
                autoclose: true
            }).on('show', function() {
                $(this).datepicker('update');
            });

            // Initialize end date picker
            $('#endDatePicker').datepicker({
                format: "yyyy-mm-dd",
                todayHighlight: true,
                autoclose: true
            }).on('show', function() {
                $(this).datepicker('update');
            });

            // Example: Send dates to the backend when a button is clicked
            $('#submitDatesButton').on('click', function() {
                sendDatesToBackend();
            });
        }
    });




/*
$(document).ready(function() {
  'use strict';

  if ($('#startDatePicker').length && $('#endDatePicker').length) {
    var startDate = new Date();
    var endDate = new Date();

    // Set the end date to be one week ahead of the current date
    endDate.setDate(endDate.getDate() + 7);

    $('#startDatePicker').datepicker({
      format: "yyyy-mm-dd",
      todayHighlight: true,
      autoclose: true
    }).datepicker('setDate', startDate);

    $('#endDatePicker').datepicker({
      format: "yyyy-mm-dd",
      todayHighlight: true,
      autoclose: true
    }).datepicker('setDate', endDate);
     function sendDatesToBackend() {
      var startDateFormatted = startDate.getFullYear() + '-' + ('0' + (startDate.getMonth() + 1)).slice(-2) + '-' + ('0' + startDate.getDate()).slice(-2);
      var endDateFormatted = endDate.getFullYear() + '-' + ('0' + (endDate.getMonth() + 1)).slice(-2) + '-' + ('0' + endDate.getDate()).slice(-2);

      // Send formatted dates to the backend using AJAX or by appending them to the URL
      // Example AJAX request:
      $.ajax({
        url: '/fetchofferdata',
        method: 'GET',
        data: {
          start_date: startDateFormatted,
          end_date: endDateFormatted
        },
        success: function(response) {
          // Handle success response from the backend
        },
        error: function(xhr, status, error) {
          // Handle error response from the backend
        }
      });
    }

    // Example: Send dates to the backend when a button is clicked
    $('#submitDatesButton').on('click', function() {
      sendDatesToBackend();
    });
  }
});
  }
});
*/




// Convert dates to "YYYY-MM-DD" format before sending them to the backend
/*var startDateFormatted = startDate.getFullYear() + '-' + ('0' + (startDate.getMonth() + 1)).slice(-2) + '-' + ('0' + startDate.getDate()).slice(-2);
var endDateFormatted = endDate.getFullYear() + '-' + ('0' + (endDate.getMonth() + 1)).slice(-2) + '-' + ('0' + endDate.getDate()).slice(-2);*/

// Send formatted dates to the backend using AJAX or by appending them to the URL
