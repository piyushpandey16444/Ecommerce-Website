(function () {
    $('[data-toggle="sidebar"]').click(function(event) {
        if ($('.object-tools').hasClass('object-tools-mr')){
            $('.object-tools').animate({'margin-right': '3%'});
        }else{
            $('.object-tools').animate({'margin-right': '16%'});
        }
        $('.object-tools').toggleClass('object-tools-mr');
    });
    if ($('.vali-multicheckbox').length > 0){
        //handle permission's help text , hide <p>
        $('.related-widget-wrapper').parent().addClass('col').removeClass('col-7').next().hide();
        // ul
        $('.vali-multicheckbox').each(function(){
            // if the label's text is seprate appname | modelname | permission
            var is_perm_label = false;
            var inputs = {};
            // li
            $(this).children().each(function(){
                var lbl = $(this).find('label');
                if (lbl.length > 0){
                    var txts = lbl.text().trim().split('|');
                    // app | model | permission
                    if (txts.length  == 3){
                        is_perm_label = true;
                        var appname = txts[0].trim();
                        var modelname = txts[1].trim();
                        var permission = txts[2].trim();
                        var perm_html = '<div class="animated-checkbox"><label>'+lbl.find('input').prop('outerHTML')+'<span class="label-text">'+permission+'</span></label></div>';
                        if (appname in inputs){
                            if (modelname in inputs[appname]){
                                inputs[appname][modelname].push(perm_html);
                            }else{
                                inputs[appname][modelname] = [perm_html];
                            }
                        }else{
                            inputs[appname] = {};
                            inputs[appname][modelname] = [perm_html];
                        }
                    }
                }
            });
            if (is_perm_label){
                // rebuild lines appname | model | permissions for add change delete
                var html = "";
                for (var key in inputs) {
                    html += '<li class="list-group-item list-group-item-action"><div class="row"><span class="col-2">'
                    +key+'</span><div class="col">';
                    var counter = 0;
                    for (var mkey in inputs[key]){
                        if (counter == Object.keys(inputs[key]).length -1){
                            html += '<div class="row px-0"><span class="col-2">'+mkey+'</span>';
                        }else{
                            html += '<div class="row px-0 line-head mr-1 mb-1"><span class="col-2">'+mkey+'</span>';
                        }
                        inputs[key][mkey].sort();
                        for (var inputkey in inputs[key][mkey]){
                            html += '<div class="col">'+ inputs[key][mkey][inputkey]+'</div>';
                        }
                        html += '</div>';
                        counter += 1;
                    }
                    html += '</div></div></li>';
                }
                $(this).children().remove();
                $(this).html(html);
            }else{
                $(this).children().addClass('list-group-item');
                // $(this).children().css('background','red');

                var bgcolor0 = $("li.list-group-item label[for=id_color_0]").text().trim();
                var bgcolor1 = $("li.list-group-item label[for=id_color_1]").text().trim();
                var bgcolor2 = $("li.list-group-item label[for=id_color_2]").text().trim();
                var bgcolor3 = $("li.list-group-item label[for=id_color_3]").text().trim();
                var bgcolor4 = $("li.list-group-item label[for=id_color_4]").text().trim();
                var bgcolor5 = $("li.list-group-item label[for=id_color_5]").text().trim();
                var bgcolor6 = $("li.list-group-item label[for=id_color_6]").text().trim();
                var bgcolor7 = $("li.list-group-item label[for=id_color_7]").text().trim();
                var bgcolor8 = $("li.list-group-item label[for=id_color_8]").text().trim();
                var bgcolor9 = $("li.list-group-item label[for=id_color_9]").text().trim();
                var bgcolor10 = $("li.list-group-item label[for=id_color_10]").text().trim();
                var bgcolor11 = $("li.list-group-item label[for=id_color_11]").text().trim();
                var bgcolor12 = $("li.list-group-item label[for=id_color_12]").text().trim();
                var bgcolor13 = $("li.list-group-item label[for=id_color_13]").text().trim();
                var bgcolor14 = $("li.list-group-item label[for=id_color_14]").text().trim();
                var bgcolor15 = $("li.list-group-item label[for=id_color_15]").text().trim();
                var bgcolor16 = $("li.list-group-item label[for=id_color_16]").text().trim();
                var bgcolor17 = $("li.list-group-item label[for=id_color_17]").text().trim();
                var bgcolor18 = $("li.list-group-item label[for=id_color_18]").text().trim();
                var bgcolor19 = $("li.list-group-item label[for=id_color_19]").text().trim();
                var bgcolor20 = $("li.list-group-item label[for=id_color_20]").text().trim();


                if($("ul#id_color .list-group-item:eq(0) input").attr("id") == "id_color_0"){
                    $("li.list-group-item label[for=id_color_0]").css('background', bgcolor0);
                    $("li.list-group-item label[for=id_color_0]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(1) input").attr("id") == "id_color_1"){
                    $("li.list-group-item label[for=id_color_1]").css('background', bgcolor1);
                    $("li.list-group-item label[for=id_color_1]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(2) input").attr("id") == "id_color_2"){
                    $("li.list-group-item label[for=id_color_2]").css('background', bgcolor2);
                    $("li.list-group-item label[for=id_color_2]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(3) input").attr("id") == "id_color_3"){
                    $("li.list-group-item label[for=id_color_3]").css('background', bgcolor3);
                    $("li.list-group-item label[for=id_color_3]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(4) input").attr("id") == "id_color_4"){
                    $("li.list-group-item label[for=id_color_4]").css('background', bgcolor4);
                    $("li.list-group-item label[for=id_color_4]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(5) input").attr("id") == "id_color_5"){
                    $("li.list-group-item label[for=id_color_5]").css('background', bgcolor5);
                    $("li.list-group-item label[for=id_color_5]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(6) input").attr("id") == "id_color_6"){
                    $("li.list-group-item label[for=id_color_6]").css('background', bgcolor6);
                    $("li.list-group-item label[for=id_color_6]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(7) input").attr("id") == "id_color_7"){
                    $("li.list-group-item label[for=id_color_7]").css('background', bgcolor7);
                    $("li.list-group-item label[for=id_color_7]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(8) input").attr("id") == "id_color_8"){
                    $("li.list-group-item label[for=id_color_8]").css('background', bgcolor8);
                    $("li.list-group-item label[for=id_color_8]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(9) input").attr("id") == "id_color_9"){
                    $("li.list-group-item label[for=id_color_9]").css('background', bgcolor9);
                    $("li.list-group-item label[for=id_color_9]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(10) input").attr("id") == "id_color_10"){
                    $("li.list-group-item label[for=id_color_10]").css('background', bgcolor10);
                    $("li.list-group-item label[for=id_color_10]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(11) input").attr("id") == "id_color_11"){
                    $("li.list-group-item label[for=id_color_11]").css('background', bgcolor11);
                    $("li.list-group-item label[for=id_color_11]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(12) input").attr("id") == "id_color_12"){
                    $("li.list-group-item label[for=id_color_12]").css('background', bgcolor12);
                    $("li.list-group-item label[for=id_color_12]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(13) input").attr("id") == "id_color_13"){
                    $("li.list-group-item label[for=id_color_13]").css('background', bgcolor13);
                    $("li.list-group-item label[for=id_color_13]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(14) input").attr("id") == "id_color_14"){
                    $("li.list-group-item label[for=id_color_14]").css('background', bgcolor14);
                    $("li.list-group-item label[for=id_color_14]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(15) input").attr("id") == "id_color_15"){
                    $("li.list-group-item label[for=id_color_15]").css('background', bgcolor15);
                    $("li.list-group-item label[for=id_color_15]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(16) input").attr("id") == "id_color_16"){
                    $("li.list-group-item label[for=id_color_16]").css('background', bgcolor16);
                    $("li.list-group-item label[for=id_color_16]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(17) input").attr("id") == "id_color_17"){
                    $("li.list-group-item label[for=id_color_17]").css('background', bgcolor17);
                    $("li.list-group-item label[for=id_color_17]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(18) input").attr("id") == "id_color_18"){
                    $("li.list-group-item label[for=id_color_18]").css('background', bgcolor18);
                    $("li.list-group-item label[for=id_color_18]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(19) input").attr("id") == "id_color_19"){
                    $("li.list-group-item label[for=id_color_19]").css('background', bgcolor19);
                    $("li.list-group-item label[for=id_color_19]").addClass('dynamic-color-bg');
                }

                if($("ul#id_color .list-group-item:eq(20) input").attr("id") == "id_color_20"){
                    $("li.list-group-item label[for=id_color_20]").css('background', bgcolor20);
                    $("li.list-group-item label[for=id_color_20]").addClass('dynamic-color-bg');
                }

                // $(this).children().css('background', bgcolor);

            }
        });
    }
})();