g_view_mat_data = null;
 function refresh_view() {
    console.log('in function');
    $.ajax({
      url:'/api/materials',
      success: function(data) {  
        console.log('successs');
        g_view_mat_data = data;
        refresh_view_table(data);
      }
    });     
  }
  refresh_view();

  function refresh_view_table(data) {

    var tbody = $("<tbody></tbody>")
    console.log('inside view table itself');
    console.log(data);
    
    for (var i = 0; i < data.length; i++) {
      //var col_id = $("<td class=\"row-order-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      var col_id = $("<td class=\"row-order-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      var col_date = $("<td  style=\"display:none;\"></td>").text(data[i].added_on.toString());
      var project_name = $("<td style=\"font-size:15px\"></td>").text(data[i].project_name.name.toString());
      var sdate = new Date(data[i].added_on);
      var hours = sdate.getHours();
      var mins = sdate.getMinutes();
      var year = sdate.getFullYear()+'';
      year= year.match(/\d{2}$/)
      var author = data[i].author.toString();
      var start_date_str = '' + sdate.getDate() + '/' + (sdate.getMonth()+1) + '/' + year + '\n'+ hours+':'+mins+"\n"+author;
      var col_disp_date = $("<td style=\"font-size:15px;white-space:pre\"></td>").text(start_date_str);
      var col_category = $("<td style=\"font-size:15px\"></td>").text(data[i].order_category.toString()+"- "+data[i].order_sub_category.toString());
      var col_order = $("<td style=\"overflow:hidden;white-space:nowrap;font-size:15px\"></td>").text(data[i].order_item.toString());
      var col_vendor = $("<td></td>").text(data[i].order_vendor.toString());
      var url = data[i].order_item_url.toString();
      var col_order_url = $("<td style=\"overflow:hidden;white-space:nowrap\"><a target="+"_blank"+" href="+url+">"+"URL"+"</a></td>");
      var col_quantity = $("<td></td>").text(data[i].order_quantity.toString());      
      var col_currency = $("<td></td>").text(data[i].order_currency.toString()); 
      var col_price = $("<td></td>").text(data[i].order_currency.toString()+data[i].order_unit_price.toString());
      var col_ELT = $("<td></td>").text(data[i].est_lead_time.toString()); 
      var col_status =   $('<td class=\"row-order-status-name\"></td>').text(data[i].order_status.name.toString());
      var row = $("<tr></tr>").append(col_id,col_date,col_disp_date,project_name,col_category,col_order,col_vendor,col_order_url,col_quantity,
                                      col_price,col_ELT,col_status);
      tbody = tbody.append(row);
    }
    
      // $('tr').sort(function(a,b){
      //    return new Date($(a).find('col_date').val()).getTime() < new Date($(b).find('input').val()).getTime() 
      // }).appendTo(tbody)

    $('#viewTableBody').html(tbody.html());
   
    $('#viewTable').DataTable({
        bJQueryUI: true,        
        dom: 'Bfrtip',
        buttons: [
              'copy', 'excel', 'pdf', 'print'
          ],
        order: [[1,'desc']]
    });
   
    
  }

  function hide_fields(){
    console.log('hide/show fields');
      $('#div_id_category_choice').on('change', function() {
        console.log('inside change');
        if($('#id_category_choice').val() == "Others"){
          $('#id_category').css('display','inline');
          $('#div_id_category .control-label').css('display','inline');
        }
        else{
          $('#id_category').css('display','none');
          $('#div_id_category .control-label').css('display','none');
        }
      });

      $('#div_id_sub_category_choice').on('change', function() {
        if($('#id_sub_category_choice').val() == "Others"){
          $('#id_sub_category').css('display','inline');
          $('#div_id_sub_category .control-label').css('display','inline');
        }
        else{
          $('#id_sub_category').css('display','none');
          $('#div_id_sub_category .control-label').css('display','none');

        }
      });
  }
  hide_fields();
function fetch_sub_category(){
    $('#div_id_category_choice').on('change', function() {
        selected_category = $('#id_category_choice').val();
        request_url = '/get_sub_category/' + selected_category + '/';
        console.log(request_url);
        $('#id_sub_category_choice').empty();
        
        $.ajax({
            url: request_url,
            contentType: "application/json",
            dataType: "json",
            success: function(response){
                //response = jQuery.parseJSON(response)
                console.log('data received');
                
                $.each(response, function(index, value){
                   console.log('in here');
                   $('#id_sub_category_choice').append($('<option>').text(value).attr('value', value));
                    //$('#id_sub_category_choice').append(
                         //$('<option></option>').val(index).html(text)
                         //$("#results").html("<p>$_POST contained: " + res + "</p>");
                     //);
                });
                $('#id_sub_category_choice').append($('<option>').text('Others').attr('value', 'Others'));
            },
           error: function (jqXHR, exception) {
        var msg = '';
        if (jqXHR.status === 0) {
            msg = 'Not connect.\n Verify Network.';
        } else if (jqXHR.status == 404) {
            msg = 'Requested page not found. [404]';
        } else if (jqXHR.status == 500) {
            msg = 'Internal Server Error [500].';
        } else if (exception === 'parsererror') {
            msg = 'Requested JSON parse failed.';
        } else if (exception === 'timeout') {
            msg = 'Time out error.';
        } else if (exception === 'abort') {
            msg = 'Ajax request aborted.';
        } else {
            msg = 'Uncaught Error.\n' + jqXHR.responseText;
        }
        console.log(msg);
    }, 
        });
        return false;
    });
}
fetch_sub_category();