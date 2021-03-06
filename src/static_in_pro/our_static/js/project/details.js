$(window).scroll(function() {
  sessionStorage.scrollTop = $(this).scrollTop();
});

$(document).ready(function() {
  if (sessionStorage.scrollTop != "undefined") {
    $(window).scrollTop(sessionStorage.scrollTop);
  }
});
function populate_sub_category(category, sub_category){

        selected_category = category;
        console.log('category is',selected_category);
        request_url = '/get_sub_category/' + selected_category + '/';
        console.log(request_url);
        $('#edit-modal-ele-subcategory').empty();
        
        $.ajax({
            url: request_url,
            contentType: "application/json",
            dataType: "json",
            success: function(response){
                //response = jQuery.parseJSON(response)
                console.log('data received on click');
                
                $.each(response, function(index, value){
                   console.log('in here');
                   $('#edit-modal-ele-subcategory').append($('<option>').text(value).attr('value', value));
                    //$('#id_sub_category_choice').append(
                         //$('<option></option>').val(index).html(text)
                         //$("#results").html("<p>$_POST contained: " + res + "</p>");
                     //);
                });
                $("#edit-modal-ele-subcategory").val(sub_category).find("option[value="+"'" + sub_category+"'" +"]").attr('selected', true);
               
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
   
}
function populate_vendor(vendor){

  
        console.log('vendor is',vendor);
        request_url = '/get_vendors/';
        console.log(request_url);
        $('#edit-modal-ele-vendor').empty();
        
        $.ajax({
            url: request_url,
            contentType: "application/json",
            dataType: "json",
            success: function(response){
                //response = jQuery.parseJSON(response)
                console.log(response);
                console.log('data received on click');
                
                $.each(response, function(index, value){
                   console.log('in here');
                   $('#edit-modal-ele-vendor').append($('<option>').text(value).attr('value', value));
                    //$('#id_sub_category_choice').append(
                         //$('<option></option>').val(index).html(text)
                         //$("#results").html("<p>$_POST contained: " + res + "</p>");
                     //);
                });
                $("#edit-modal-ele-vendor").val(vendor).find("option[value="+"'" + vendor+"'" +"]").attr('selected', true);
               
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
   
}
// // refresh chart with new data
	function refresh_task_chart(data) {
		var xAxisData = []
		var chartData = []
		for (var i = 0; i < data.length; i++) {
			xAxisData[i] = data[i].task_name;
			var d = [];
			d.push(data[i].assigned_to.name);
			d.push(Date.parse(data[i].start_date));
			d.push(Date.parse(data[i].end_date));
			chartData[i] = d;
		}

		console.log(chartData);

		$('#task_chart').highcharts({
        chart: {
            type: 'columnrange',
            inverted: true
        },

        title: {
            text: 'Scheduled Tasks'
        },

        xAxis: {
            categories: xAxisData
        },

        yAxis: {
             type: 'datetime',
             dateTimeLabelFormats: { // don't display the dummy year
                month: '%e. %b',
                year:'%y'
            },
            title: { text: '' }
            
        },

        tooltip: {
        	formatter: function() {
              return ''       + Highcharts.dateFormat('%e %b\'%y', new Date(this.point.low))
                     + ' - '  + Highcharts.dateFormat('%e %b\'%y', new Date(this.point.high));
          }
        },

        plotOptions: {
            columnrange: {
                dataLabels: {
                    enabled: true,
                    inside: true,
                    align: 'center',
                    formatter: function() {
                    	if (this.y === this.point.low) {
                      	return '' + this.point.name;
                      } else {
                      	return 'Hello';
                      }
                    }
                    
                }
           }
        }, 
         

        legend: { enabled: false },

        series: [{ name: '', data: chartData }]
	});
	}


// refresh the corresponding task data in that table
	function refresh_task_table(data) {
		var tbody = $("<tbody></tbody>")

		for (var i = 0; i < data.length; i++) {
			var col_id = $("<td class=\"row-ele-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
			var col_task = $("<td></td>").text(data[i].task_name.toString());
			var col_assigned = $("<td></td>").text(data[i].assigned_to.name.toString());
			var col_start = $("<td></td>").text((new Date(data[i].start_date)).toDateString());
			var col_end = $("<td></td>").text((new Date(data[i].end_date)).toDateString());
      var col_commnt_butn = $('<td><button class=" btn btn-primary btn-xs comment_task" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
			var col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_task" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button></td>');
			var col_del_butn = $('<td><button  class="btn btn-danger btn-xs delete_task" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button></td>');

			var row = $("<tr></tr>").append(col_id, col_task, col_assigned, col_start, col_end, col_commnt_butn,col_edit_butn, col_del_butn);

			tbody = tbody.append(row);
		}


		$('#taskTableBody').html(tbody.html());
		$('button.delete_task').on('click',function(){
      		$("#deleteTaskModal").modal("show");
          	$("#delete-modal-header-ele-id").val($(this).closest('tr').find('.row-ele-id').text());
       	});
    $('button.comment_task').on('click',function(){
          
            $("#task-comment-modal-header-ele-id").val($(this).closest('tr').find('.row-ele-id').text());
            var task_id = parseInt($(this).closest('tr').find('.row-ele-id').text());
            $.ajax({
            url:'/api/schedulecomments/',
            data: {
                'schedule_id':task_id,
            },
            success: function(data) {
              console.log(data);
              var commentbody = $("<div></div>")
              for (var i = 0; i < data.length; i++) {
                var col_id = $("<h5 class=\"row-ele-id\" style=\"display:none;\"></h5>").text(data[i].id.toString());
                var sdate = new Date(data[i].commented_on);
                var start_date_str = '' + sdate.getDate() + '/' + (sdate.getMonth()+1) + '/' + sdate.getFullYear() + ' '+ sdate.getHours()+':'+sdate.getMinutes();
                var col_commented_on = $("<b style=\"color:grey;\"></b>").text(start_date_str);
                var filler_1 = $("<span></span>").text(" by ");
                var col_author = $("<span style=\"color:rgb(55, 138, 231);\"></span>").text(data[i].author.toString());
                var filler_2 = $("<span><i></i></span>").text(" : ");
                var col_comment = $("<span style=\"word-wrap: break-word; width:100px; font-family:'Times New Roman';\"></span>").text(data[i].comment.toString());
               
                // var col_end = $("<td></td>").text((new Date(data[i].end_date)).toDateString());
                // var col_commnt_butn = $('<td><button class=" btn btn-primary btn-xs comment_task" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
                // var col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_task" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button></td>');
                // var col_del_butn = $('<td><button  class="btn btn-danger btn-xs delete_task" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button></td>');

                var row = $("<div></div>").append(col_id,col_commented_on,filler_1, col_author,filler_2, col_comment);

                commentbody = commentbody.append(row);
              }
              $('#schedule_comments').html(commentbody.html());
             
           }
      });
           $("#commentTaskModal").modal("show");
      });
    	$('button.update_task').on('click',function(){
      		var task_id = parseInt($(this).closest('tr').find('.row-ele-id').text());

      		$.ajax({
      			url:'/api/schedules/' + task_id,
      			success: function(data) {
      				$('#edit-modal-header-ele-id').val(task_id);
      				$("#edit-modal-ele-task").val(data.task_name);		
      				$("#id_assigned_to").children("option").each(function(){
      					if (parseInt($(this).attr("value")) == data.assigned_to.id) {
      						$(this).attr('selected','');
      					} else {
      						$(this).removeAttr('selected');
      					}
      				});
      				var sdate = new Date(data.start_date);
      				var edate = new Date(data.end_date);
      				
      				var start_date_str = '' + (sdate.getMonth()+1) + '/' + sdate.getDate() + '/' + sdate.getFullYear();
      				var end_date_str = '' + (edate.getMonth()+1) + '/' + edate.getDate() + '/' + edate.getFullYear();

      				$("#edit-modal_start-datepick").val(start_date_str);
      				$("#edit-modal_end-datepick").val(end_date_str);
          			$("#editTaskModal").modal("show");
      			}
      		})
    	});
	}

	var g_task_data = null;
// refresh task of that particular project
	function refresh_task() {
		$.ajax({
			url:'/api/schedules',
			data: {
				'project_id':project_id,
			},
			success: function(data) {
				$(document).ready(function() {
					g_task_data = data;
          console.log(data);
					refresh_task_table(data);
				});
			}
		});			
	}
	refresh_task();
// date picker for start date
	$(function() {
        $( '#edit-modal_start-datepick' ).datepicker();
    });
// date picker for end date
    $(function() {
        $( '#edit-modal_end-datepick' ).datepicker();
    });
//click of the graph button function
    $(function() {
    	$('#id-task-view-chart-btn').on('click', function() {
    		$("#modal-view-chart").modal("show").on('shown.bs.modal', function(){
    			refresh_task_chart(g_task_data);
    		});
    	});
    });

// refresh the corresponding order data in that table
  function refresh_order_table(data,comment_data) {

    var tbody = $("<tbody></tbody>")
    console.log('inside order table itself',data);
    for (var i = 0; i < data.length; i++) {
      //var col_id = $("<td class=\"row-order-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      var col_id = $("<td class=\"row-order-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      var col_date = $("<td  style=\"display:none;\"></td>").text(data[i].added_on.toString());
      var sdate = new Date(data[i].added_on);
      var hours = sdate.getHours();
      var mins = sdate.getMinutes();
      //var ampm = hours >= 12 ? 'pm' : 'am';
      var year=new Date().getFullYear()+'';
      year= year.match(/\d{2}$/)
      var author = data[i].author.toString();
      var start_date_str = '' + sdate.getDate() + '/' + (sdate.getMonth()+1) + '/' + year + ' '+ hours+':'+mins+" "+author;
      var col_disp_date = $("<td style=\"font-size:15px;overflow:hidden;\"></td>").text(start_date_str);
      var col_category = $("<td style=\"font-size:14px;word-wrap:break-word\"></td>").text(data[i].order_category.toString()+"- "+data[i].order_sub_category.toString());
      var col_sub_category = $("<td style=\"font-size:14px;overflow:hidden;white-space:nowrap;\"></td>").text(data[i].order_sub_category.toString());
      var col_order = $("<td style=\"overflow:hidden;word-wrap:break-word;font-size:14px\"></td>").text(data[i].order_item.toString());
      var col_vendor = $("<td style=\"font-size:15px;word-wrap:break-word\"></td>").text(data[i].order_vendor.toString());
      //var col_order_url = $("<td style=\"overflow:hidden;white-space:nowrap\"></td>").text(data[i].order_item_url.toString());
      var url = data[i].order_item_url.toString();
      //var col_order_url = $("<td><a href="+url+">Link</a></td>");
      var lastChar = url.substr(url.length - 1);
      if (lastChar =='/'){
        url = url.substring(0, url.length - 1);
      }
      var col_order_url = $("<td style=\"overflow:hidden;white-space:nowrap\"><a target="+"_blank"+" href="+url+">"+url+"</a></td>");
      var col_quantity = $("<td style=\"font-size:15px;\"></td>").text(data[i].order_quantity.toString());      
      var col_currency = $("<td style=\"font-size:15px;\"></td>").text(data[i].order_currency.toString()); 
      var col_price = $("<td style=\"font-size:15px;\"></td>").text(data[i].order_currency.toString()+data[i].order_unit_price.toString());
      var col_ELT =  $("<td style=\"font-size:15px;\"></td>").text(data[i].est_lead_time.toString()); 
      var col_priority =  $("<td style=\"font-size:15px;\"></td>").text(data[i].order_priority.name.toString()); 
      var status = data[i].order_status.name.toString();

      if (staff_status === true && status === "Not Approved"){
          //alert('here in approve');
          var col_status_butn =   $('<td class=\"row-order-status-name\"><button style=\"background-color:red;\" class=" btn btn-primary status_app" data-title="approve">Approve</button></td>');
      }
      else if (status === "Not Placed"){
          var col_status_butn =   $('<td class=\"row-order-status-name\"><button style=\"background-color:blue;\" class=" btn btn-primary status_app" data-title="place">Place</button></td>');
      }
      else if (status === "Not Shipped"){
          var col_status_butn =   $('<td class=\"row-order-status-name\"><button style=\"background-color:orange;\" class=" btn btn-primary status_app" data-title="ship">To Ship</button></td>');
      }
      else if (status === "Not Delivered"){
          var col_status_butn =   $('<td class=\"row-order-status-name\"><button style=\"background-color:green;\" class=" btn btn-primary status_app" data-title="deliver">Delivery</button></td>');
      }
      else if (status === "Delivered"){
          var col_status_butn =   $('<td class=\"row-order-status-name\"><button style=\"background-color:violet;padding:4px;\" class=" btn btn-primary status_app" data-title="working">W</button>&nbsp;<button style=\"background-color:grey;padding:4px;\" class=" btn btn-primary status_app" data-title="not working">NW</button></td>');
      }
      else{
          //alert('out of approve');
          var col_status_butn =   $('<td class=\"row-order-status-name\"></td>').text(status);
      }
      var col_hsn =  $("<td style=\"overflow:hidden;word-wrap:break-word;font-size:14px\"></td>").text(data[i].order_hsn.toString()); 
      var col_track_btn =  $('<td><button class=" btn btn-primary track_courier" data-title="Track" data-toggle="modal">Track</button></td>');
      var col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_order" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button>&nbsp;<button  class="btn btn-danger btn-xs delete_order" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button>&nbsp;<button class=" btn btn-primary btn-xs comment_order" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
      var comm_id = $("<td class=\"row-new-comment-id\" style=\"display:none;\"></td>").text((0).toString());
      //console.log(comment_data)
      //alert('hereeeeeeee',typeof(comment_data));
      for (var j = 0; j < comment_data.length; j++) {
        //console.log(comment_data[j]);
        var eid = comment_data[j].id.toString();
        if (comment_data[j].order_id == data[i].id && comment_data[j].read_flag=='N'){
          console.log(data[i].id, comment_data[j].read_flag);
          col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_order" data-title="Edit" data-toggle="modal">\
            <i class="fa fa-pencil fa-lg"></i></button>&nbsp;<button  class="btn btn-danger btn-xs delete_order" data-title="Delete" data-toggle="modal">\
            <i class="fa fa-trash fa-lg"></i></button>&nbsp;<button class=" btn btn-primary btn-xs comment_order" data-title="Comment" data-toggle="modal">\
            <i class="edit-comment ' +eid+' fa fa-envelope fa-lg" style="color:yellow" text="*"></i></button></td>');
            comm_id = $("<td class=\"row-new-comment-id\" style=\"display:none;\"></td>").text(eid);
          //alert('yipeeeee its yellow');
          break;
         }
         else{
          col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_order" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button>&nbsp;<button  class="btn btn-danger btn-xs delete_order" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button>&nbsp;<button class=" btn btn-primary btn-xs comment_order" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
          comm_id = $("<td class=\"row-new-comment-id\" style=\"display:none;\"></td>").text(eid);
         }
      };
      //var col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_order" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button>&nbsp;<button  class="btn btn-danger btn-xs delete_order" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button>&nbsp;<button class=" btn btn-primary btn-xs comment_order" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
      
      var row = $("<tr></tr>").append(col_id,col_date,col_disp_date,col_category,col_order,col_vendor,col_order_url,col_quantity,
                                      col_price,col_ELT,col_priority,col_hsn,col_status_butn,col_track_btn,col_edit_butn,comm_id);
      tbody = tbody.append(row);
    }

    $('#orderTableBody').html(tbody.html());
   
    $('#orderTable').DataTable({
        bJQueryUI: true,        
        dom: 'Bfrtip',
        autoWidth: false,
        scrollX:true,
        columns: [
         { width: '0%'},
         { width: '0%'},
         { width: '6%' },
         { width: '7%' },
         { width: '18%' },
         { width: '8%' },
         { width: '5%' },
         { width: '5%' },
         { width: '9%' },
         { width: '5%' },
         { width: '7%' },
         { width: '5%' },
         { width: '7%' },
         { width: '7%' },
         { width: '11%' },
         { width: '0%'}
      ],
        buttons: [
       {
           extend: 'pdf',
           footer: true,
           exportOptions: {
                columns: [2,3,4,5,6,7,8,11]
            }
       },
       {
           extend: 'csv',
           footer: false,
           exportOptions: {
                columns: [0,2,3,4,5,6,7,8,11]
            }
          
       },
       {
           extend: 'excel',
           footer: false,
           exportOptions: {
                columns: [0,2,3,4,5,6,7,8,11]
            }
       }         
    ],  
    // rowReorder: {
    //         selector: 'td:nth-child(5)'
    //     },
    //     responsive: true,
        // buttons: [
        //       'copy', 'excel', 'pdf', 'print'
        //   ],
        order: [[1,'desc']]
    });
document.getElementById('estimate-price').value = "";

  var priceFired = function () {
 var table = $('#orderTable').DataTable();
 var net_total = table.column(8).data();
    var TotalValue = 0;
    $.each( net_total, function( key, index ) {
       if(index.charAt(0)=='R'){
            index = index.slice( 2 );
            TotalValue += parseFloat(index);
            //alert(index);
       };
        $("#estimate-price").val(parseInt(TotalValue));
}); 
};
$(document).ready(function() {
  priceFired();
});

var eventFired = function ( type ) {
//$("#estimate-price").val(0);
var table = $('#orderTable').DataTable();
var filtered = table.rows( { filter : 'applied'} ).data();

//var net_total = table.column(8).data();
var TotalValue = 0;
for(var key in filtered){
  if (typeof(filtered[key][8]) === 'string'){
    var price = filtered[key][8];
    if(price.charAt(0)==='R'){
          price = price.slice( 2 );
          TotalValue += parseFloat(price);
          //alert(TotalValue);
   };
 };
};
 
 $("#estimate-price").val(TotalValue);
};

 $('#orderTable').on( 'search.dt', function () {
   var value = $('.dataTables_filter input').val();
   //var table = $('#orderTable').DataTable();
   if (value.length < 2 ){
    priceFired();
    return;
};
   eventFired( 'Search' ); 
 }).DataTable();
 


    // to enhance order delete on all pages.
     $('#orderTable').on('click','button.delete_order',function(){
    // $('button.delete_order').on('click',function(){
          var status = $(this).closest('tr').find('.row-order-status-name').text();
          console.log(status);
          //if ($(this).closest('tr').find('.row-order-status-id').text() > 100)
            
          if (status === "Place"  || status === "Not Approved" || status === "Approve")
            $("#deleteOrderModal").modal("show");
          else
            $("#deleteErrorOrderModal").modal("show");
            $("#delete-modal-header-ele-order-id").val($(this).closest('tr').find('.row-order-id').text());
            //$("#delete-modal-ele-status-id").val($(this).closest('tr').find('.row-order-status-id').text());

        });
     $('#orderTable').on('click','button.track_courier',function(){
          $("#order-track-modal-header-ele-id").val($(this).closest('tr').find('.row-order-id').text());
          var order_id = parseInt($(this).closest('tr').find('.row-order-id').text());
          console.log(order_id);
          console.log('tracking.....');
          $("#trackOrderModal").modal("show");
     });
     function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

     $('#orderTable').on('click','button.status_app',function(){
          $("#order-status-modal-header-ele-id").val($(this).closest('tr').find('.row-order-id').text());
          var order_id = parseInt($(this).closest('tr').find('.row-order-id').text());
          console.log(order_id);
          
          //var status = $(this).closest('tr').find('.row-order-status-name').text();
          var status = $(this).attr("data-title");
          console.log('status.....'+status +" "+project_id+" "+$(this).attr("data-title"));
          var data = {"status":status,"order_id":order_id,"project_id":project_id,"csrfmiddlewaretoken": csrftoken };
          console.log(data);
          $.post("/projectdetails/"+project_name+"/", data,  function(data) {document.location.reload();});
          //$("#trackOrderModal").modal("show");

     });

     $('#orderTable').on('click','button.comment_order',function(){
     //$('button.comment_order').on('click',function(){
            //var csrftoken = getCookie('csrftoken');
            $("#order-comment-modal-header-ele-id").val($(this).closest('tr').find('.row-order-id').text());
            var order_id = parseInt($(this).closest('tr').find('.row-order-id').text());
            console.log(order_id);
            var comm_id = parseInt($(this).closest('tr').find('.row-new-comment-id').text());
            console.log(comm_id);
            $.ajax({
            url:'/api/commentrack/',
            type: 'PUT',
            data: {
                'id':comm_id,'order_id':order_id,'read_flag':'Y','project_id':project_id, 'user_name':user
            },
            dataType: "json",
            crossDomain:false,
            beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function() {
               console.log('success');
               $("."+comm_id).removeAttr("style");
               $("."+comm_id).removeClass("fa-envelope");
               $("."+comm_id).addClass("fa-comment");
               $("."+comm_id).val("");
            }});
            //var data ={'id':comm_id,'order_id':order_id,'read_flag':'Y','project_id':project_id, 'user_name':user};
            //$.post("/api/commentrack/", data,  function(data) {document.location.reload();});

            $.ajax({
            url:'/api/ordercomments/',
            data: {
                'order_id':order_id,
            },
            success: function(data) {
              console.log(data);
              var commentbody = $("<div></div>")
              for (var i = 0; i < data.length; i++) {
                var col_id = $("<h5 class=\"row-ele-id\" style=\"display:none;\"></h5>").text(data[i].id.toString());
                var sdate = new Date(data[i].commented_on);
                var start_date_str = '' + sdate.getDate() + '/' + (sdate.getMonth()+1) + '/' + sdate.getFullYear() + ' '+ sdate.getHours()+':'+sdate.getMinutes();
                var col_commented_on = $("<b style=\"color:grey;\"></b>").text(start_date_str);
                var filler_1 = $("<span></span>").text(" by ");
                var col_author = $("<span style=\"color:rgb(55, 138, 231);\"></span>").text(data[i].author.toString());
                var filler_2 = $("<span><i></i></span>").text(" : ");
                var col_comment = $("<span style=\"word-wrap: break-word; width:100px; font-family:'Times New Roman';\"></span>").text(data[i].comment.toString());
               
                // var col_end = $("<td></td>").text((new Date(data[i].end_date)).toDateString());
                // var col_commnt_butn = $('<td><button class=" btn btn-primary btn-xs comment_task" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
                // var col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_task" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button></td>');
                // var col_del_butn = $('<td><button  class="btn btn-danger btn-xs delete_task" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button></td>');

                var row = $("<div></div>").append(col_id,col_commented_on,filler_1, col_author,filler_2, col_comment);

                commentbody = commentbody.append(row);
              }
              $('#order_comments').html(commentbody.html());
             
           }
      });
           $("#commentOrderModal").modal("show");
      });
    $('#orderTable').on('click','button.show_status',function(){ 
    //$('button.show_status').on('click',function(){
           // var all_order_status = "{{ order_status_data}}";
           // alert(all_order_status);
          // for (i = 0; i < all_order_status.length; i++) {
          //     alert(all_order_status[i].name +" " +all_order_status[i].status_id +"<br>");
          // }
          //$("#orderStatusModal").modal("show");
            $("#modal-order-status-id").text($(this).closest('tr').find('.row-order-status-id').text());
            var status = $(this).closest('tr').find('.row-order-status-id').text();
            //alert(status);
            var content=$("<div></div>")

            var status_arr= []
            $.ajax({
              url:'/api/status',
              success:function(data){
                for(i = 0; i < data.length; i++){
                  status_arr.push([data[i].status_id,data[i].name])

                }
              
                status_arr.sort()
                //alert(status_arr)
                for(i = 0; i < status_arr.length; i++){
                  if (status==status_arr[i][0]){
                      var status_row = $("<h4 class=\"text-align-center\"style=\"color:green;display:inline-block;padding:10px 20px;\"></h4>").text(status_arr[i][1].toString());
                      
                  }
                  else if(status < status_arr[i][0]){
                      var status_row = $("<h4 class=\"text-align-center\"style=\"color:red;display:inline-block;padding:20px;\"></h4>").text(status_arr[i][1].toString());
                  }
                  else if(status > status_arr[i][0]){
                      var status_row = $("<h4 class=\"text-align-center\"style=\"color:green;display:inline-block;padding:20px;\"></h4>").text(status_arr[i][1].toString());
                  }
                  var gap = status_row;
                  if (i < status_arr.length-1){
                  var gap = status_row.append($("<h4 style=\"color:blue;display:inline-block;padding:5px;\"><i class=\"fa fa-long-arrow-right fa-lg\"></i></h4>"));
                  }
                  content = content.append(gap);

              }
           
            $('#orderStatusBodyModal').html(content.html());
                $("#orderStatusModal").modal("show");
              }
          })
        });
    $('#orderTable').on('click','button.update_order',function(){
    //$('button.update_order').on('click',function(){
          var order_id = parseInt($(this).closest('tr').find('.row-order-id').text());
          //var status = parseInt($(this).closest('tr').find('.row-status-id').text());
          $.ajax({
            url:'/api/materials/' + order_id,
            success: function(data) {
              
              var status_id = data.order_status.status_id;
              var item = data.order_item;    
              var category = data.order_category;    
              var subcategory = data.order_sub_category;    
              var quantity = data.order_quantity;    
              var currency = data.order_currency; 
              var price = data.order_unit_price; 
              var vendor = data.order_vendor; 
              var url = data.order_item_url;
              var priority_id = data.order_priority.priority_id;
              var hsn = data.order_hsn;
              
              var elt = data.est_lead_time;
              var est_lead_num = elt.slice(0,1);
              var est_lead_day = elt.slice(1,2);

             
               
              console.log('before call', data.order_category);
              populate_sub_category(category, subcategory); 
              populate_vendor(vendor);
              //if (data.order_status.status_id > 100)
              //fetch_category(data.order_category);
              if (data.order_status.name === "Not Approved" || data.order_status.name === "Not Placed" ){
                 document.getElementById("edit-modal-header-ele-order-id").value = order_id;
                 document.getElementById("edit-modal-ele-status").value = status_id;
                 document.getElementById("edit-modal-ele-item").value = item;
                 document.getElementById("edit-modal-ele-category").value = category;
                 document.getElementById("edit-modal-ele-subcategory").value = subcategory;
                 document.getElementById("edit-modal-ele-quantity").value = quantity;
                 document.getElementById("edit-modal-ele-currency").value = currency;
                 document.getElementById("edit-modal-ele-price").value = price;
                 document.getElementById("edit-modal-ele-vendor").value = vendor;
                 document.getElementById("edit-modal-ele-url").value = url;
                 document.getElementById("edit-modal-ele-priority").value = priority_id;
                 document.getElementById("edit-modal-ele-hsn").value = hsn;
                 document.getElementById("edit-modal-ele-num").value = est_lead_num;
                 document.getElementById("edit-modal-ele-day").value = est_lead_day;

                 $("#editOrderModal").modal("show");
               }
              else if (data.order_status.name === "Not Working" || data.order_status.name === "Working"){
                 document.getElementById("status-modal-header-ele-order-id").value = order_id;
                 document.getElementById("status-modal-ele-status").value = status_id;
                 document.getElementById("status-modal-ele-item").value = item;
                 document.getElementById("status-modal-ele-category").value = category;
                 document.getElementById("status-modal-ele-subcategory").value = subcategory;
                 document.getElementById("status-modal-ele-quantity").value = quantity;
                 document.getElementById("status-modal-ele-currency").value = currency;
                 document.getElementById("status-modal-ele-price").value = price;
                 document.getElementById("status-modal-ele-vendor").value = vendor;
                 document.getElementById("status-modal-ele-url").value = url;
                 document.getElementById("status-modal-ele-priority").value = priority_id;
                 document.getElementById("status-modal-ele-hsn").value = hsn;
                 document.getElementById("status-modal-ele-num").value = est_lead_num;
                 document.getElementById("status-modal-ele-day").value = est_lead_day;
                 $("#editStatusModal").modal("show");
               }
              else 
                 $("#editErrorOrderModal").modal("show");

            }
          })
      });
  }
  var g_order_data = null;
// refresh order of that particular project
  function refresh_order() {
    $.ajax({
      url:'/api/materials',
      data: {
        'project_id':project_id,
      },

      success: function(data) {  
        g_order_data = data;
        $.ajax({
            url:'/api/commentrack',
            data: {
              'project_id':project_id,
            },

            success: function(data) {  
              comment_data = data;
              refresh_order_table(g_order_data,comment_data);
            }
      });     
       
      }
    });     
  }
     refresh_order();

  $('button.delete_image').on('click',function(){
     var imageId = $(this).data('id'); 
     $('#deleteImageModal').modal("show");
     $("#delete-modal-header-ele-image-id").val($(this).data('id'));
     
   });
  
  function fetch_category(){
        $('#orderTable').on('click','button.update_order',function(){

        request_url = '/get_category/';
        console.log(request_url);
        $('#edit-modal-ele-category').empty();
        
        $.ajax({
            url: request_url,
            contentType: "application/json",
            dataType: "json",
            success: function(response){
                //response = jQuery.parseJSON(response)
                console.log('cat data received');
                
                $.each(response, function(index, value){
                   console.log('in here');
                   $('#edit-modal-ele-category').append($('<option>').text(value).attr('value', value));
                });     
                //$("#edit-modal-ele-category select").val(category);  
               
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
  fetch_category();

  

  function fetch_sub_category(){
    $('#id_order_category, #edit-modal-ele-category').on('change', function() {
        selected_category = $(this).val();
        request_url = '/get_sub_category/' + selected_category + '/';
        console.log(request_url);
        $('#id_order_sub_category').empty();
        $('#edit-modal-ele-subcategory').empty();
        
        $.ajax({
            url: request_url,
            contentType: "application/json",
            dataType: "json",
            success: function(response){
                //response = jQuery.parseJSON(response)
                console.log('data received');
                
                $.each(response, function(index, value){
                   console.log('in here');
                   $('#id_order_sub_category').append($('<option>').text(value).attr('value', value));
                   $('#edit-modal-ele-subcategory').append($('<option>').text(value).attr('value', value));
                    //$('#id_sub_category_choice').append(
                         //$('<option></option>').val(index).html(text)
                         //$("#results").html("<p>$_POST contained: " + res + "</p>");
                     //);
                });
               
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
