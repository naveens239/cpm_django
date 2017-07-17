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