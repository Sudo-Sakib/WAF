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


// Add a custom rule

$(document).ready(function() {
    // Load existing custom rules
    loadCustomRules();

    // Handle form submission to add new rule
    $('#customRuleForm').submit(function(event) {
        event.preventDefault();

        let ruleName = $('#ruleName').val();
        let rulePattern = $('#rulePattern').val();
        let ruleDescription = $('#ruleDescription').val();

        $.ajax({
            url: "{{ url_for('custom_rule.add_custom_rule') }}",
            type: "POST",
            data: {
                name: ruleName,
                pattern: rulePattern,
                description: ruleDescription
            },
            success: function(response) {
                alert(response.message);
                // Reload rules
                loadCustomRules();
                $('#customRuleForm')[0].reset();
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    });

    // Function to load and display custom rules
    function loadCustomRules() {
        $.get("{{ url_for('custom_rule.custom_rules') }}", function(data) {
            let customRules = data.rules;
            let tableContent = '';

            customRules.forEach(function(rule, index) {
                tableContent += `
                    <tr>
                        <td>${rule.name}</td>
                        <td>${rule.pattern}</td>
                        <td>${rule.description}</td>
                        <td>
                            <button class="btn btn-danger deleteRuleBtn" data-index="${index}">Delete</button>
                        </td>
                    </tr>
                `;
            });

            $('#customRulesTable').html(tableContent);

            // Handle rule deletion
            $('.deleteRuleBtn').click(function() {
                let index = $(this).data('index');
                deleteCustomRule(index);
            });
        });
    }

    // Function to delete a custom rule
    function deleteCustomRule(index) {
        $.post("{{ url_for('custom_rule.delete_custom_rule') }}", { index: index }, function(response) {
            alert(response.message);
            loadCustomRules();
        }).fail(function(response) {
            alert(response.responseJSON.error);
        });
    }
});
