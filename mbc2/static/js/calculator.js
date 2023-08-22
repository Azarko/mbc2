// index for form's element ids and placeholder,
// e.g. member_<index>, id=delete-member-<index> etc
var member_index = 1;

// add new row in calculator form and increment member_index
function add_member() {
  var $row = $(`
    <div class="row" id="member-${member_index}">
      <div class="col-auto">
        <label for="member-name-${member_index}" class="visually-hidden">Name</label>
        <input type="text" class="form-control" id="member-name-${member_index}" placeholder="Name" value="member_${member_index}">
      </div>
      <div class="col-auto">
        <label for="member-paid-${member_index}" class="visually-hidden">Paid</label>
        <input type="text" class="form-control" id="member-paid-${member_index}" placeholder="Paid">
      </div>
      <div class="col-auto">
        <button type="button" class="btn btn-danger mb-3" id="delete-member-${member_index}">Del</button>
      </div>
    </div>
  `);
  $('#calculate-form').append($row);
  member_index += 1;
}

add_member();  // add first initial row in the form

// ------
// event listeners

// click on "Add" button
$("#add-button").click(function (event) {
  add_member();
  event.preventDefault();
});


// click on any of "Del" buttons
// event listener on body to attach to all further dynamically added elements
$("body").on('click', "button[id^='delete-member-']", function() {
  $(this).parent().parent().remove();
});


// submit form (Calculate button)
$("#calculate-form").submit(function (event) {
  $.ajax({
    type: "POST",
    url: "/party-calc/calculate",
    async: false,
    data: JSON.stringify(
      { members: [
        {name: "Vasya", paid: 100},
        {name: "Petya", paid: 50},
        ],
      },
    ),
    contentType: "application/json",
  }).done(function (data) {
    console.log(data);
  });
  event.preventDefault();
});
