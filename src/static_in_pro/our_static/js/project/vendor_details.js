

  function refresh_vendor_table_view(data) {

    var tbody = $("<tbody></tbody>")
    console.log('inside vendor view table itself');
    console.log(data);
    
    for (var i = 0; i < data.length; i++) {

      //var col_id = $("<td class=\"row-order-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      var col_id = $("<td class=\"row-vendor-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      if (data[i].vendor_name !=null){
      var vendor_name = $("<td style=\"font-size:15px\"></td>").text(data[i].vendor_name.toString());}
      else { var vendor_name = $("<td style=\"font-size:15px\"></td>").text("".toString());}

      if (data[i].address != null){
      var address = $("<td style=\"font-size:15px\"></td>").text(data[i].address.toString());}
      else{var address = $("<td style=\"font-size:15px\"></td>").text("".toString()); }

      console.log('check one');
      if (data[i].GSTIN != null){
      var GSTIN = $("<td style=\"font-size:15px\"></td>").text(data[i].GSTIN.toString());}
      else{var GSTIN = $("<td style=\"font-size:15px\"></td>").text("".toString()); }

      if (data[i].contact_person  !=null){
      var contact_person = $("<td style=\"font-size:15px\"></td>").text(data[i].contact_person.toString());}
      else{ var contact_person = $("<td style=\"font-size:15px\"></td>").text("".toString()); }

      if (data[i].contact_num !=null){
      var contact_num = $("<td style=\"font-size:15px\"></td>").text(data[i].contact_num.toString());}
      else{ var contact_num = $("<td style=\"font-size:15px\"></td>").text("".toString()); }

      if (data[i].website !=null && data[i].website != ""){
      var url = data[i].website.toString();
     
      var lastChar = url.substr(url.length - 1);
      if (lastChar ==='/'){
        url = url.substring(0, url.length - 1);}
      var website = $("<td style=\"overflow:hidden;white-space:nowrap;font-size:15px\"><a target="+"_blank"+" href="+url+">"+"URL"+"</a></td>");}
      else{ var website = $("<td style=\"font-size:15px\"></td>").text("".toString()); }

      var col_status =   $('<td><button class=" btn btn-primary btn-xs update_vendor" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button>&nbsp;<button  class="btn btn-danger btn-xs delete_vendor" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button>&nbsp;</button></td>');
      var row = $("<tr></tr>").append(col_id,vendor_name,address,GSTIN,contact_person,contact_num,website,col_status);
      tbody = tbody.append(row);
    }
    console.log('out of loop');
      // $('tr').sort(function(a,b){
      //    return new Date($(a).find('col_date').val()).getTime() < new Date($(b).find('input').val()).getTime() 
      // }).appendTo(tbody)
    console.log(tbody);
    $('#viewVendorBody').html(tbody.html());
   
    $('#viewVendor').DataTable({
        bJQueryUI: true,        
        dom: 'Bfrtip',
        buttons: [
              'copy', 'excel', 'pdf', 'print'
          ],
        order: [[1,'desc']]
    });
    

    $('#viewVendor').on('click','button.update_vendor',function(){
    //$('button.update_order').on('click',function(){
          var vendor_id = parseInt($(this).closest('tr').find('.row-vendor-id').text());
          //var status = parseInt($(this).closest('tr').find('.row-status-id').text());
          $.ajax({
            url:'/api/vendor/' + vendor_id,
            success: function(data) {
              $('#edit-vendor-id').val(vendor_id);
              $("#edit-vendor-name").val(data.vendor_name);
              $("#edit-vendor-address").val(data.address);    
              $("#edit-vendor-GSTIN").val(data.GSTIN);    
              $("#edit-contact-person").val(data.contact_person);    
              $("#edit-contact-num").val(data.contact_num);    
              $("#edit-vendor-website").val(data.website); 
              
            }
          })
          $("#editVendorModal").modal("show");
      });

     $('#viewVendor').on('click','button.delete_vendor',function(){
        $("#deleteVendorModal").modal("show");
        $("#delete-vendor-id").val($(this).closest('tr').find('.row-vendor-id').text());
  });
    
  }

  g_view_vendor_data = null;
 function refresh_vendor_view() {
    console.log('in function');
    $.ajax({
      url:'/api/vendor',
      success: function(data) {  
        console.log('successs---vendor data');
        g_view_vendor_data = data;
        refresh_vendor_table_view(data);
      }
    });     
  }
  refresh_vendor_view();