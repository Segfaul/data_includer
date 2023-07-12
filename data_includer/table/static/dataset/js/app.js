$(document).ready(function() {
    $(document).on('click', '.table-sortable th', function() {
        var column_index = $(this).index();
        var table = $(this).closest('table');
        var currentIsAscending = $(this).hasClass('th-sort-asc');

        table.find('th').removeClass('th-sort-asc th-sort-desc');

        if (currentIsAscending) {
            $(this).removeClass('th-sort-asc').addClass('th-sort-desc');
        } else {
            $(this).removeClass('th-sort-desc').addClass('th-sort-asc');
        }
      
        sortTable(table, column_index, currentIsAscending);
    });
});

function sortTable(table, column, isAscending) {
    var tbody = table.find('tbody');
    var rows = tbody.find('tr').toArray();

    rows.sort(function(a, b) {
      var aValue = $(a).find('td').eq(column).text();
      var bValue = $(b).find('td').eq(column).text();

        if (isAscending) {
            return aValue.localeCompare(bValue);
        } else {
            return bValue.localeCompare(aValue);
        }
    });

    tbody.empty();
    $.each(rows, function(index, row) {
        tbody.append(row);
    });
}

function toggleTable() {
    var table = document.getElementById('table');

    if (!table.style.display){
        table.style.display = 'none';
    }

    if (table.style.display === 'none') {
        table.style.display = 'table';
        document.getElementById('toggle-button').innerText = 'Collapse Table';
    } else {
        table.style.display = 'none';
        document.getElementById('toggle-button').innerText = 'Expand Table';
    }
}

function myFunction() {
    var copyText = document.getElementById("api_token");
    navigator.clipboard.writeText(copyText.textContent);

    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copied: " + copyText.textContent;
}

function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy to clipboard";
}
