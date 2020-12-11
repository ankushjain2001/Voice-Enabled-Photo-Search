$('document').ready(function () {
    
  $("#x-search-form").on('submit', function (event) {
    event.preventDefault();
    var queryString = $("#transcript").val();
    // var params = {
    //   'q': queryString
    // };
    // var body = {};
    // console.log('Query String: ' + queryString);
    // console.log(params);
    // apigClient.searchGet(params, body)
    //   .then(function (result) {
    //     console.log(result.data);
    //   }).catch(function (result) {
    //     console.log("Error occurred");
    //   });
    $.ajax({
      // url: "https://a3te728nf2.execute-api.us-east-1.amazonaws.com/dev/search",
      url: "https://8953pmloz0.execute-api.us-east-1.amazonaws.com/dev/search",
      type: "GET",
      data: {
        q: queryString
      },
      beforeSend: function(xhr){
        $('#x-result-txt').text(' ');
        $('#x-hrule').css('display', 'none');
        xhr.setRequestHeader('x-api-key', 'UPpQWQNa8Q6mYWT2pHSg7aAjhqldY1vC1f6EWduq'); // Not safe but the HW doesn't ask for any secure way to do this
      },
      error: function(res) {console.log(res)},
      success: function(res) { 
        // console.log(res);
        // Append img tags with images to the grid div
        var s3Url = res['s3_base_url'];
        var images = res['images'];
        var imgUrl = "";
        $('#x-grid-div').empty();
        if (images.length > 0){
          $('#x-result-txt').text('Search results for ' + res['search_string']);
        }
        else {
          $('#x-result-txt').text('No results found');
        }
        
        $('#x-hrule').css('display', 'block');
        for (var i = 0; i < images.length; i++) {
          imgUrl = s3Url + images[i];
          $('#x-grid-div').append('<a href="'+imgUrl+'" target="_blank"><img src="'+imgUrl+'" alt="" class="img-thumbnail img-style m-2"></a>');
        }
      }
   });
  });
  

  $("#x-file-upload").on('click', function (event) {
    event.preventDefault();

    var file = $("#x-file-input")[0].files[0];
    var fileName = file.name;
    var fileType = file.type;

    // console.log(file);
    // console.log(fileName);
    // console.log(fileType);

    $.ajax({
      // url: "https://a3te728nf2.execute-api.us-east-1.amazonaws.com/dev/upload/"+fileName,
      url: "https://8953pmloz0.execute-api.us-east-1.amazonaws.com/dev/upload/"+fileName,
      type: "PUT",
      data: file,
      processData: false,
      cache: false,
      dataType: 'xml',
      beforeSend: function(xhr){
        $('#x-success-msg').text('')
        xhr.setRequestHeader('Content-Type', fileType);
        xhr.setRequestHeader('x-api-key', 'UPpQWQNa8Q6mYWT2pHSg7aAjhqldY1vC1f6EWduq'); // Not safe but the HW doesn't ask for any secure way to do this
      },
      error: function(res) {console.log(res)},
      success: function(res) { 
        $('#x-success-msg').text('File uploaded successfully!')
      }
    });

  });
});
