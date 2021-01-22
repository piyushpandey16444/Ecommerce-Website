;(function($){
    "use strict";

    // disableEvent function called on page load
    disableEvent();
    addnewAddress();
    addnewChild();

    // calculation();
    // updateCart();

	// Disable events
    function disableEvent(){
        
        // All buttons controls
        $(".cancel_form").css("display","none");
        $('.btn_form').prop('disabled', true);
        $('.btn_form').css('opacity', '.5');
        
        // Profile controls
        $('.user_fname').prop('disabled', true);
        $('.user_lname').prop('disabled', true);
        $('.gender').prop('disabled', true);
        $('.user_emailid').prop('disabled', true);
        $('.user_mobileno').prop('disabled', true);
        
        // Aadhar card controls
        $('.aadharcard_name').prop('disabled', true);
        $('.aadharcard_number').prop('disabled', true);
        
        // Pan card controls
        $('.pancard_name').prop('disabled', true);
        $('.pancard_number').prop('disabled', true);
        
        // Change password controls
        $('.old_password').prop('disabled', true);
        $('.new_password').prop('disabled', true);
        $('.confirm_password').prop('disabled', true);
    };

    // Enable events
    function enableButton(){
        
        // All buttons controls
        $(".cancel_form").css("display","inline-block");
        $('.btn_form').prop('disabled', false);
        $('.btn_form').css('opacity', '100');
        
        // Profile controls
        $('.user_fname').prop('disabled', false);
        $('.user_lname').prop('disabled', false);
        $('.gender').prop('disabled', false);
        $('.user_emailid').prop('disabled', false);
        $('.user_mobileno').prop('disabled', false);
        
        // Aadhar card controls
        $('.aadharcard_name').prop('disabled', false);
        $('.aadharcard_number').prop('disabled', false);
        
        // Pan card controls
        $('.pancard_name').prop('disabled', false);
        $('.pancard_number').prop('disabled', false);
        
        // Change password controls
        $('.old_password').prop('disabled', false);
        $('.new_password').prop('disabled', false);
        $('.confirm_password').prop('disabled', false);
    };

    function addnewAddress(){
        $('.add_new_address_box').css('display','none');
    };

    function addnewChild(){
        $('.add_new_child_box').css('display','none');
    };

    function addnewChild(){
        $('.add_new_child_box').css('display','none');
    };

    $(".update_form_container").css("display","none");

    $(".edit_form").click(function(){
        $(".edit_form").css("display","none");
        $(".update_form_container").css("display","block");
        enableButton();
    });

    $(".cancel_form").click(function(){
        $(".edit_form").css("display","block");
        $(".update_form_container").css("display","none");
        disableEvent();
    });

    $(".add_new_address_btn").click(function(){
        $('.add_new_address_box').css('display','block');
        $('.add_new_address_btn').css('display','none');
    });

    $(".add_new_child_btn").click(function(){
        $('.add_new_child_box').css('display','block');
        $('.add_new_child_btn').css('display','none');
    });

    $(".edit_address_btn").click(function(){
        var fid = $(this).attr('id');
        var ebtn = $(this).css('display','none');
        $('#form'+fid).css('display','block');
        var target = $(this).parent().next().css('display', 'none');
    });

    // function updateCart(){
    //     var sum = 0;
    //     $(".total-col").each(function(){
    //         var value = $(this).text();
    //         if(!isNaN(value) && value.length != 0) {
    //             sum += parseFloat(value);
    //         }
    //     });
    //     console.log("Total add value is ........", sum);
    //     document.getElementById('total-payable').innerHTML = sum;
    //     document.getElementById('cart-subtotal').innerHTML = sum;
    // };

    // function calculation(){
    //     $(".cartitems").click(function(){
    //         var cid = event.currentTarget.id;
    //         var inpval = $(this).find(".form-control").val();
    //         var pcol = $(this).find(".price-col").text();
    //         var totalsum = inpval * pcol
    //         document.getElementById('a'+cid).innerHTML = totalsum;
    //         updateCart();
    //     });
    // };

})(jQuery)