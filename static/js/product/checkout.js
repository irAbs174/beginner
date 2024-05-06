$(document).ready(function () {
  function separateDigitsWithComma() {
    // Convert the number to a string
    let total = $('input[name=TOTAL_CART_NAME]').val();
    var numberString = String(total);
    // Split the string into an array of characters
    var digitsArray = numberString.split('');
    // Reverse the array to process digits from right to left
    digitsArray.reverse();
    // Iterate over the array and insert commas after every third digit
    for (var i = 3; i < digitsArray.length; i += 4) {
      digitsArray.splice(i, 0, ',');
    }
    // Reverse the array again to get the original order
    digitsArray.reverse();

    // Join the array into a string
    var result = digitsArray.join('');

    $('#CART_P_TOTAL').html(`<td id="CART_P_TOTAL">${result}</td>`);
  }
  separateDigitsWithComma();
});
// end readfy
function order() {
  let token = $('input[name=csrfmiddlewaretoken]').val();
  firstName = document.getElementById('floatingInputName').value;
  lastName = document.getElementById('floatingInputLName').value;
  address = document.getElementById('address').value;
  tel = document.getElementById('floatingInputTel').value;
  State = document.getElementById('floatingInputOstan').value;
  City = document.getElementById('floatingInputCity').value;
  postalcode = document.getElementById('floatingInputPOST').value;
  shipping = $('input[name=shippng_number]').val();
  payment_method = $('input[name=shippng_number]').val();
  let data = {
    csrfmiddlewaretoken: token,
    'firstName': firstName,
    'lastName': lastName,
    'tel': tel,
    'State': State,
    'City': City,
    'postalcode': postalcode,
    'address': address,
    'SEND_METHOD': shipping,
    'PAYMENT_METHOD': payment_method,
  };
  // Send request to server
  $.ajax({
    url: '/cart/test/',
    type: 'POST',
    data: data,
    success: function (response) {
      if (response.success === false) {
        Swal.fire({
          icon: "error",
          title: response.status,
          showConfirmButton: false,
          timer: 3000,
        });
      } else {
        Swal.fire({
          icon: "success",
          title: response.status,
          showConfirmButton: false,
          timer: 3000,
        });
        window.location.href = response.status;
      }
    },
    error: function (xhr, status, error) {
      console.log(status);
      Swal.fire({
        icon: "error",
        title: status,
        showConfirmButton: false,
        timer: 3000,
      });
    }
  });
}
$('.click_fadax_btn').click(function (e) {
  e.preventDefault();
  data = {
    'task': 'recive_payment_token',
  }
  $.ajax({
    url: 'fadax/',
    type: 'POST',
    data: data,
    success: function (response) {
      if (response.success === false) {
        Swal.fire({
          icon: "error",
          title: response.status,
          showConfirmButton: false,
          timer: 3000,
        });
      } else {
        Swal.fire({
          icon: "success",
          title: 'در حال انتقال به درگاخ فدکس',
          showConfirmButton: false,
          timer: 2000,
        });
        window.location.href = response.status;
      }
    },
    error: function (xhr, status, error) {
      console.log(status);
      Swal.fire({
        icon: "error",
        title: status,
        showConfirmButton: false,
        timer: 3000,
      });
    }
  });
});