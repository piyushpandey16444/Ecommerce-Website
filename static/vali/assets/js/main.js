(function () {
	"use strict";

	var treeviewMenu = $('.app-menu');

	// Toggle Sidebar
	$('[data-toggle="sidebar"]').click(function(event) {
		event.preventDefault();
		$('.app').toggleClass('sidenav-toggled');
	});

	// Activate sidebar treeview toggle
	$("[data-toggle='treeview']").click(function(event) {
		event.preventDefault();
		if(!$(this).parent().hasClass('is-expanded')) {
			//treeviewMenu.find("[data-toggle='treeview']").parent().removeClass('is-expanded');
		}
		$(this).parent().toggleClass('is-expanded');
	});
    // Activate sidebar treeview toggle
	$("[data-toggle='treegroup']").click(function(event) {
		event.preventDefault();
		if(!$(this).parent().hasClass('is-expanded')) {
			//treeviewMenu.find("[data-toggle='treeview']").parent().removeClass('is-expanded');
		}
		$(this).parent().toggleClass('is-expanded');
	});

	// Set initial active toggle
	$("[data-toggle='treeview.'].is-expanded").parent().toggleClass('is-expanded');
//	$("[data-toggle='treegroup.'].is-expanded").parent().toggleClass('is-expanded');

	//Activate bootstrip tooltips
	$("[data-toggle='tooltip']").tooltip();

	// For highlight searched word
	// $("#searchbar").keyup(function () {
	//     var data = this.value.toUpperCase().split(" ");    
	//     $(".table").find("tr").not("tr:first").find("td").each(function (index, elem) {
	//     var $elem = $(elem);
	//         for (var d = 0; d < data.length; ++d) {
	//             // Highlight
	//             if ($elem.text().toUpperCase().indexOf(data[d]) != -1) {
	//                 $elem.addClass('highlighted-td-txt');   
	//             } else {
	//                 $elem.removeClass('highlighted-td-txt');
	//             }
	//         }
	//     })     
	// })
	// End

	$(".dash-link:eq(0)").attr('href', 'http://127.0.0.1:8000/admin/auth/user/');
	$(".dash-link:eq(1)").attr('href', 'http://127.0.0.1:8000/admin/hoitymoppet/product/');
	$(".dash-link:eq(2)").attr('href', 'http://127.0.0.1:8000/admin/generic_links/categories/');
	$(".dash-link:eq(3)").attr('href', 'http://127.0.0.1:8000/admin/enquiry_order/enquiry/');
	$(".dash-link:eq(4)").attr('href', 'http://127.0.0.1:8000/admin/enquiry_order/order/');


	// Code for all aps menu should be on top 19 June 2020 | Devashish

	var li_accounts = $("li.treeview [title='Models in the Accounts application']").parent();
	var li_administration = $("li.treeview [title='Models in the Administration application']").parent();
	var li_authentication = $("li.treeview [title='Models in the Authentication and Authorization application']").parent();
	var li_generic = $("li.treeview [title='Models in the Generic_Links application']").parent();
	var li_hoitymoppet = $("li.treeview [title='Models in the Hoitymoppet application']").parent();

	var li_enquiryorder = $("li.treeview [title='Models in the Enquiry_Order application']").parent();
	var li_des = $("li.treeview [title='Models in the Dynamic Email Settings application']").parent();

	$(".navbar-nav li").click(function(){
        $(".navbar-nav li").css("background","transparent");
        $(this).css("background","#432f98");
    });

	$(".nav-link-accounts").click(function(){
		$(li_accounts).css("display", "block");
		$(li_accounts).addClass("is-expanded");
		// var f_li = $(li_accounts).find('li a.treeview-item').first().text();

		$(li_administration).css("display", "none");
		$(li_authentication).css("display", "none");
		$(li_generic).css("display", "none");
		$(li_hoitymoppet).css("display", "none");
		$(li_enquiryorder).css("display", "none");
		$(li_des).css("display", "none");
	});

	$(".nav-link-administration").click(function(){
		$(li_administration).css("display", "block");
		$(li_administration).addClass("is-expanded");
		// var f_li = $(li_administration).find('li a.treeview-item').first().text();

		$(li_accounts).css("display", "none");
		$(li_authentication).css("display", "none");
		$(li_generic).css("display", "none");
		$(li_hoitymoppet).css("display", "none");
		$(li_enquiryorder).css("display", "none");
		$(li_des).css("display", "none");
	});

	$(".nav-link-authentication").click(function(){
		$(li_authentication).css("display", "block");
		$(li_authentication).addClass("is-expanded");
		// var f_li = $(li_authentication).find('li a.treeview-item').first().text();

		$(li_accounts).css("display", "none");
		$(li_administration).css("display", "none");
		$(li_generic).css("display", "none");
		$(li_hoitymoppet).css("display", "none");
		$(li_enquiryorder).css("display", "none");
		$(li_des).css("display", "none");
	});

	$(".nav-link-generic").click(function(){
		$(li_generic).css("display", "block");
		$(li_generic).addClass("is-expanded");
		// var f_li = $(li_generic).find('li a.treeview-item').first().text();

		$(li_accounts).css("display", "none");
		$(li_administration).css("display", "none");
		$(li_authentication).css("display", "none");
		$(li_hoitymoppet).css("display", "none");
		$(li_enquiryorder).css("display", "none");
		$(li_des).css("display", "none");
	});

	$(".nav-link-hoitymoppet").click(function(){
		$(li_hoitymoppet).css("display", "block");
		$(li_hoitymoppet).addClass("is-expanded");
		// var f_li = $(li_hoitymoppet).find('li a.treeview-item').first().text();

		$(li_accounts).css("display", "none");
		$(li_administration).css("display", "none");
		$(li_generic).css("display", "none");
		$(li_authentication).css("display", "none");
		$(li_enquiryorder).css("display", "none");
		$(li_des).css("display", "none");
	});

	$(".nav-link-enquiryorder").click(function(){
		$(li_enquiryorder).css("display", "block");
		$(li_enquiryorder).addClass("is-expanded");
		// var f_li = $(li_hoitymoppet).find('li a.treeview-item').first().text();

		$(li_accounts).css("display", "none");
		$(li_administration).css("display", "none");
		$(li_generic).css("display", "none");
		$(li_authentication).css("display", "none");
		$(li_hoitymoppet).css("display", "none");
		$(li_des).css("display", "none");
	});





	$(".nav-link-emailsettings").click(function(){
		$(li_des).css("display", "block");
		$(li_des).addClass("is-expanded");
		$(li_enquiryorder).css("display", "none");
		
		// var f_li = $(li_hoitymoppet).find('li a.treeview-item').first().text();

		$(li_accounts).css("display", "none");
		$(li_administration).css("display", "none");
		$(li_generic).css("display", "none");
		$(li_authentication).css("display", "none");
		$(li_hoitymoppet).css("display", "none");
	});


	// let url = $(location).attr('href');
	// console.log("This is current url .....", url);
	
 	var url = window.location.href;
	if (url.search("accounts") >= 0) {
		console.log("This is current url .....1");
	    $(".nav-link-accounts").click();
	}
	else if(url.search("logentry") >= 0){
		$(".nav-link-administration").click();
		console.log("This is current url .....2");
	}
	else if(url.search("auth") >= 0){
		$(".nav-link-authentication").click();
 		console.log("This is current url .....3");
	}
	else if(url.search("generic_links") >= 0){
		console.log("This is current url .....4");
	    $(".nav-link-generic").click();
	}
	else if(url.search("hoitymoppet") >= 0){
		console.log("This is current url .....5");
	    $(".nav-link-hoitymoppet").click();
	}
	else if(url.search("enquiry_order") >= 0){
		console.log("This is current url .....6");
	    $(".nav-link-enquiryorder").click();
	}

	$("#id_slug").prop("readonly", true);

	$(".field-slider_name").addClass("col-md-12");
	$(".field-slider_summary").addClass("col-md-12");
	$(".field-company_details").addClass("col-md-12");
	$(".field-company_summary").addClass("col-md-12");
	$(".field-video_heading").addClass("col-md-12");
	$(".field-video_summary").addClass("col-md-12");
	$(".field-video_details").addClass("col-md-12");
	$(".field-ads_name").addClass("col-md-12");
	$(".field-ads_summary").addClass("col-md-12");
	$(".field-privacypolicy_details").addClass("col-md-12");
	$(".field-disclaimer_details").addClass("col-md-12");
	$(".field-terms_details").addClass("col-md-12");
	$(".field-faq_details").addClass("col-md-12");
	$(".field-customer_feedback").addClass("col-md-12");

	// End

})();