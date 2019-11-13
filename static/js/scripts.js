// Make tables interactive
$(document).ready(function () {
  const dt = $('#list').DataTable({
    columnDefs:[{
      "targets": 0,
      "orderable": false,
    }],
    "pageLength": 25,
    "order": [],
  });

  dt.on('order', (e, settings) => {
    dt.column(0).nodes().each((cell, i) => {
      cell.innerText = i + 1;
    });
  }).draw();
});
