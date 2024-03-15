$("#add_face").submit(function (e) {
    e.preventDefault();
    var formData = new FormData(this);
  
    // Add additional form data if needed...
  
    $.ajax({
      method: "POST",
      url: window.location.href,
      data: formData,
      contentType: false,
      processData: false,
      success: function (data) {
        toastr["success"]("تم إضافة المستخدم بنجاح", "عملية ناجحة");
        // Handle success actions if needed...
      },
      error: function (error_data) {
        toastr["error"](error_data.responseText, "خطأ!");
        // Handle error actions if needed...
      },
    });
  });
  