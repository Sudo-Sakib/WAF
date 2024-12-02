$(document).ready(function() {
    // Filter functionality
    $("#logFilter").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#logTableBody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Pagination functionality (add your logic to handle table rows)
    var currentPage = 1;
    var rowsPerPage = 10;

    function paginateTable() {
        var rows = $("#logTableBody tr");
        var totalRows = rows.length;
        var totalPages = Math.ceil(totalRows / rowsPerPage);

        // Show or hide pagination buttons
        $("#prevBtn").toggleClass("disabled", currentPage <= 1);
        $("#nextBtn").toggleClass("disabled", currentPage >= totalPages);

        // Hide all rows
        rows.hide();

        // Show rows for current page
        rows.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage).show();
    }

    // Handle "Next" button
    $("#nextBtn").click(function() {
        currentPage++;
        paginateTable();
    });

    // Handle "Previous" button
    $("#prevBtn").click(function() {
        currentPage--;
        paginateTable();
    });

    // Initialize pagination on page load
    paginateTable();
});

function fetchLogs() {
    $.get('/logs/logs', function (data) {
        let tableBody = $('#logTableBody');
        tableBody.empty(); // Clear existing rows
        data.logs.forEach(log => {
            tableBody.append(`
                <tr>
                    <td>${log.timestamp}</td>
                    <td>${log.ip}</td>
                    <td>${log.method}</td>
                    <td>${log.payload}</td>
                    <td>${log.result}</td>
                </tr>
            `);
        });
    });
}

// Fetch logs every 5 seconds
setInterval(fetchLogs, 5000);
fetchLogs();

// Clear logs
$(document).ready(function () {
    $("#clearLogs").click(function () {
        $.post("/logs/clear_logs", function () {
            $("#logTableBody").empty(); // Clear the table
        });
    });
});


