// index for form's element ids and placeholder,
// e.g. member_<index>, id=delete-member-<index> etc
var member_index = 1;

// add new row in calculator form and increment member_index
function add_member() {
  var $row = $(`
    <div class="input-group mb-1" id="member-row-${member_index}" style="max-width: 800px;">
      <label for="member-name-${member_index}" class="visually-hidden">Name</label>
      <input type="text" class="form-control me-2" id="member-name-${member_index}" placeholder="Name" value="member_${member_index}">

      <label for="member-paid-${member_index}" class="visually-hidden">Paid</label>
      <input type="number" step=".01" class="form-control me-2" id="member-paid-${member_index}" type="number" placeholder="Paid" value=0>

      <label for="member-need-to-pay-${member_index}" class="visually-hidden">Paid</label>
      <input type="text" class="form-control me-2" id="member-need-to-pay-${member_index}" placeholder="Need to pay" disabled>

      <button type="button" class="btn btn-danger" id="delete-member-${member_index}">Del</button>
    </div>
  `);
  $('#calculate-form').append($row);
  member_index += 1;
}

function get_form_data() {
  var data_array = [];

  $('div[id^=member-row-]').each(function () {
    var name = $(this).find("input[id^='member-name-']").val();
    var paid = $(this).find("input[id^='member-paid-']").val();
    data_array.push({'name': name, 'paid': paid});
  });

  return data_array;
}

// disable/enable main interface of calculator
function switch_state(state) {
    $("#calculate-button").prop("disabled", state);
    $("#add-button").prop("disabled", state);
    $("button[id^='delete-member-']").prop('disabled', state);
    $("input[id^='member-name-']").prop('disabled', state);
    $("input[id^='member-paid-']").prop('disabled', state);
    $("#edit-button").prop("disabled", !state);
}

// add values to need-to-pay inputs or reset their values if data is undefined
function fill_need_to_pay(data) {
    $('input[id^=member-need-to-pay-]').map(function (index, element) {
        if (data == undefined) {
            value = '';
        } else {
            value = data[index]['need_to_pay'];
        }
        $(this).val(value);
    });
}

add_member();  // add first initial row in the form

// ------------------
// event listeners

// click on "Add" button
$("#add-button").click(function (event) {
  add_member();
  event.preventDefault();
});

// click on any of "Del" buttons
// event listener on body to attach to all further dynamically added elements
$("body").on('click', "button[id^='delete-member-']", function() {
  $(this).parent().remove();
});

// submit form (Calculate button)
$("#calculate-form").submit(function (event) {
  var data_array = get_form_data();

  $.ajax({
    type: 'POST',
    url: '/party-calc/calculate',
    async: false,
    data: JSON.stringify({ 'members': data_array }),
    dataType: 'json',
    contentType: 'application/json',
  }).done(function (data) {
    switch_state(true);
    fill_need_to_pay(data['members']);
  }).fail(function (data) {
    if (data.status == 400 && data.responseJSON.code == 'VALIDATION_ERROR') {
        alert(data.responseJSON.message);
    } else if (data.status >= 500) {
        alert('something went wrong on server side =(');
    };
    console.log(data);
  })
  ;
  event.preventDefault();
});

// click on "edit" button
$("#edit-button").on('click', function() {
    switch_state(false);
    fill_need_to_pay();
});
