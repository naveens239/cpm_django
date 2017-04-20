
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
                var start_date_str = '' + (sdate.getMonth()+1) + '/' + sdate.getDate() + '/' + sdate.getFullYear() + ' '+ sdate.getHours()+':'+sdate.getMinutes();
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
  function refresh_order_table(data) {

    var tbody = $("<tbody></tbody>")
    console.log('inside order table itself');
    for (var i = 0; i < data.length; i++) {
      var col_id = $("<td class=\"row-order-id\" style=\"display:none;\"></td>").text(data[i].id.toString());
      var col_category = $("<td></td>").text(data[i].order_category.toString());
      var col_sub_category = $("<td></td>").text(data[i].order_sub_category.toString());
      var col_order = $("<td></td>").text(data[i].order_item.toString());
      var col_vendor = $("<td></td>").text(data[i].order_vendor.toString());
      var col_order_url = $("<td></td>").text(data[i].order_item_url.toString());
      var col_quantity = $("<td></td>").text(data[i].order_quantity.toString());      
      var col_currency = $("<td></td>").text(data[i].order_currency.toString()); 
      var col_price = $("<td></td>").text(data[i].order_unit_price.toString());
      var col_status = $("<td class=\"row-order-status-id\" style=\"display:none;\"></td>").text(data[i].order_status.status_id.toString());
      var col_status_butn =   $('<td><button class=" btn btn-primary show_status" data-title="Status" data-toggle="modal">Track</button></td>');
      var col_commnt_butn = $('<td><button class=" btn btn-primary btn-xs comment_order" data-title="Comment" data-toggle="modal"><i class="fa fa-comment fa-lg"></i></button></td>');
      var col_edit_butn = $('<td><button class=" btn btn-primary btn-xs update_order" data-title="Edit" data-toggle="modal"><i class="fa fa-pencil fa-lg"></i></button></td>');
      var col_del_butn = $('<td><button  class="btn btn-danger btn-xs delete_order" data-title="Delete" data-toggle="modal"><i class="fa fa-trash fa-lg"></i></button></td>');

      var row = $("<tr></tr>").append(col_id,col_category,col_sub_category,col_order,col_vendor,col_order_url,col_quantity,col_currency,
                                      col_price,col_status,col_status_butn,col_commnt_butn,col_edit_butn,col_del_butn);

      tbody = tbody.append(row);
    }


    $('#orderTableBody').html(tbody.html());
    $('button.delete_order').on('click',function(){
          if ($(this).closest('tr').find('.row-order-status-id').text() > 100)
            $("#deleteErrorOrderModal").modal("show");
          else
            $("#deleteOrderModal").modal("show");
            $("#delete-modal-header-ele-order-id").val($(this).closest('tr').find('.row-order-id').text());
            //$("#delete-modal-ele-status-id").val($(this).closest('tr').find('.row-order-status-id').text());

        });
     $('button.comment_order').on('click',function(){
          
            $("#order-comment-modal-header-ele-id").val($(this).closest('tr').find('.row-order-id').text());
            var order_id = parseInt($(this).closest('tr').find('.row-order-id').text());
            console.log(order_id);
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
                var start_date_str = '' + (sdate.getMonth()+1) + '/' + sdate.getDate() + '/' + sdate.getFullYear() + ' '+ sdate.getHours()+':'+sdate.getMinutes();
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
    $('button.show_status').on('click',function(){
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
    $('button.update_order').on('click',function(){
          var order_id = parseInt($(this).closest('tr').find('.row-order-id').text());
          //var status = parseInt($(this).closest('tr').find('.row-status-id').text());
          $.ajax({
            url:'/api/materials/' + order_id,
            success: function(data) {
              $('#edit-modal-header-ele-order-id').val(order_id);
              $("#edit-modal-ele-status").val(data.order_status.status_id);
              $("#edit-modal-ele-item").val(data.order_item);    
              $("#edit-modal-ele-category").val(data.order_category);    
              $("#edit-modal-ele-subcategory").val(data.order_sub_category);    
              $("#edit-modal-ele-quantity").val(data.order_quantity);    
              $("#edit-modal-ele-currency").val(data.order_currency); 
              $("#edit-modal-ele-price").val(data.order_unit_price); 
              $("#edit-modal-ele-vendor").val(data.order_vendor); 
              $("#edit-modal-ele-url").val(data.order_item_url);  
              if (data.order_status.status_id > 100)
                 $("#editErrorOrderModal").modal("show");
              else 
                 $("#editOrderModal").modal("show");
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
        $(document).ready(function() {
          g_order_data = data;
          refresh_order_table(data);
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

