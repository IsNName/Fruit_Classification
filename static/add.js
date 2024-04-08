// add.js
function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
      
      // When image is uploaded, call updatePrediction() function
      updatePrediction();
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
  $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
  $('.image-upload-wrap').removeClass('image-dropping');
});

function updatePrediction() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/get_predict', true);
  xhr.onreadystatechange = function () {
      if (xhr.readyState == XMLHttpRequest.DONE) {
          if (xhr.status == 200) {
              document.getElementById('predict').textContent = xhr.responseText;
          } else {
              console.error('Request failed: ' + xhr.status);
          }
      }
  };
  xhr.send();
}

$('form').submit(function(e) {
  e.preventDefault();
  var formData = new FormData(this);
  $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data: formData,
      contentType: false,
      processData: false,
      success: function(response) {
          console.log(response);
      }
  });
});
