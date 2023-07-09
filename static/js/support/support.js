const messageInputDom = document.querySelector('#support_message');
const submitButtonDom = document.querySelector('#support_submit');
const token = $('input[name=csrfmiddlewaretoken]').val();

// Focus on the message input field when the page loads
messageInputDom.focus();

// Handle enter key press on the message input field
messageInputDom.addEventListener('keyup', function(e) {
  if (e.keyCode === 13) {  // Enter key pressed
    submitButtonDom.click();
  }
});

// Handle submit button click
submitButtonDom.addEventListener('click', function(e) {
  let currentPath = window.location.pathname;
  let slug = currentPath.split('/').filter(Boolean).pop();
  const message = messageInputDom.value;
  if (message) {
    const support_status = "active";
    const data = {
      'support_room': slug,
      'support_message': message,
      'support_status': support_status,
      'csrfmiddlewaretoken': token,
    };
    $.ajax({
      url: '/support/post_message',
      type: 'POST',
      data: data,
      success: function(response) {
        if (response.success === false) {
          Swal.fire({
            icon: "error",
            title: response.status,
            showConfirmButton: false,
            timer: 3000,
          });
        } else {
          // Handle success case if needed
        }
      },
      error: function(xhr, status, error) {
        Swal.fire({
          icon: "error",
          title: status,
          showConfirmButton: false,
          timer: 3000,
        });
      }
    });
  } else {
    Swal.fire({
      icon: "error",
      title: "پیام پشتیبانی نمیتواند خالی باشد",
      showConfirmButton: false,
      timer: 2000,
    });
  }
  messageInputDom.value = '';
});

// Function to poll for new messages
function pollMessages(timestamp) {
  let currentPath = window.location.pathname;
  let slug = currentPath.split('/').filter(Boolean).pop();
  $.ajax({
    url: '/support/get_message',
    data: { 'timestamp': timestamp, 'support_room': slug,},
    success: function(data) {
      const messages = data.messages;
      for (const message of messages) {
        $("#support_log").prepend(`<h2>${message.message}</h2>`);
      }
      if (messages.length > 0) {
        const lastTimestamp = messages[messages.length - 1].timestamp;
        pollMessages(lastTimestamp);
      } else {
        setTimeout(function() {
          pollMessages(timestamp);
        }, 2000);
      }
    },
    error: function(xhr, status, error) {
      setTimeout(function() {
        pollMessages(timestamp);
      }, 2000);
    },
    timeout: 30000,
    dataType: 'json'
  });
}

// Initial function to fetch latest messages and start long polling
function fetchLatestMessages() {
  let search_user = $('input[name=Supported_user]').val();
  $.ajax({
    url: `/api/support/?search=${search_user}`,
    type: 'GET',
    dataType: 'json',
    success: function(response) {
      // Handle the response data here
      var results = response.results;
      if (results.length > 0) {
        let support_timestamp = results[results.length - 1].timestamp;
        pollMessages(support_timestamp);
      } else {
        setTimeout(fetchLatestMessages, 2000);
      }
    },
    error: function(xhr, status, error) {
      setTimeout(fetchLatestMessages, 2000);
    }
  });
}

fetchLatestMessages();