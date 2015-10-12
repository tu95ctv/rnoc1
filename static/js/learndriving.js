$(":checkbox").attr("autocomplete", "off");
$(document).mouseup(function(e) {
    var container = $(".scrollable");

    if (!container.is(e.target) // if the target of the click isn't the container...
        && container.has(e.target).length === 0) // ... nor a descendant of the container
    {
        container.hide();
    }
});
$(document).keyup(function(e) {
    var container = $(".scrollable");

    if (!container.is(e.target) // if the target of the click isn't the container...
        && container.has(e.target).length === 0) // ... nor a descendant of the container
    {
        container.hide();
    }
});

$(document).ready(function() {
    /*$(".js-example-basic-single").select2();
    $("#e1").select2();*/
    $('.quest_button').click(function() {
        var catid;
        catid = $(this).attr("idquest");
        id = '#' + 'quest' + catid
        val = $(id).html()
        $('#demo').html(val);


    });

    $('#btn-nxt').click(function() {
        current = (parseInt($('#current_quest').attr("value")) + 1).toString();

        $('#current_quest').attr("value", current);
        id = '#' + 'quest' + current;
        val = $(id).html();
        $('#demo').html(val);
    });

    $('#btn-pre').click(function() {
        current = (parseInt($('#current_quest').attr("value")) - 1).toString();

        $('#current_quest').attr("value", current);
        id = '#' + 'quest' + current;
        val = $(id).html();
        $('#demo').html(val);
    });



    $("#myForm").submit(function() {

        var url = "/select_forum/"; // the script where you handle the form input.
        var val = $("input[type=submit][clicked=true]").attr("value")
        console.log(val)
        var data = $("#myForm").serialize() + '&' + 'btn=' + val
        $.ajax({
            type: "POST",
            url: url,
            val: val,
            data: data, // serializes the form's elements.
            success: function(data) {
                $('#thongbao').html(data); // show response from the php script.
            }
        });

        return false; // avoid to execute the actual submit of the form.
    });

    $("#myForm input[type=submit]").click(function() {
        $("input[type=submit]", $(this).parents("#myForm")).removeAttr("clicked");
        $(this).attr("clicked", "true");
    });

    $(".leechform").submit(function() {

        var url = "/leech/"; // the script where you handle the form input.

        $.ajax({
            type: "POST",
            url: url,
            data: $(".leechform").serialize(), // serializes the form's elements.
            success: function(data) {
                $('#thongbao').html(data); // show response from the php script.
            }
        });

        return false; // avoid to execute the actual submit of the form.
    });

    $('#entry').on('submit', '#entryform', function() {



        /*var url = "/edit_entry/"; // the script where you handle the form input.*/
        var url = $(this).attr("action")
        $.ajax({
            type: "POST",
            url: url,
            data: $("#entryform").serialize(), // serializes the form's elements.
            success: function(data) {
                $('#thongbao').html(data); // show response from the php script.
            }
        });

        return false; // avoid to execute the actual submit of the form.
    });




    $('#get-thongbao').click(function() {

        $.get('/get-thongbao/', {
            query: 'a'
        }, function(data) {
            $('#thongbao').html(data);
        });

    });
    $('#importul-btn').click(function() {

        $.get('/importul/', {
            query: 'a'
        }, function(data) {
            $('#thongbao').html(data);
        });

    });
    $('#stop-post').click(function() {

        $.get('/stop-post/', {
            query: 'a'
        }, function(data) {
            $('#thongbao').html(data);
        });

    });




    $('#tao-object').click(function() {

        $.get('/tao_object/', {
            query: 'a'
        }, function(data) {
            $('#thongbao').html(data);
        });

    });

    $('.entry-row').click(function() {
        entry_id = $(this).attr("id");

        $.get('/get_description/', {
            entry_id: entry_id
        }, function(data) {
            $('#entry').html(data);
        });

    });


    $('table.paleblue tbody tr').click(function() {
        entry_id = $(this).children("td.id").html();
        console.log(entry_id)
        $.get('/get_description/', {
            entry_id: entry_id
        }, function(data) {
            $('#entry').html(data);
        });

    });




    $('.filter-mll-div').on('submit', "#amll-form", function() {


        var clicked_button = $("input[type=submit][clicked=true]").attr("value");
        console.log(clicked_button)
        if (clicked_button == "Filter") {
            var url = "/omckv2/mll_filter/"; // the script where you handle the form input.
            var type = 'GET';
        } else if (clicked_button == "Cancle") {

            $(this).find("input[type=text], textarea, [name=id-mll-entry]").val("");
            $(this).find("input[name=mll]").val("Tao MLL");
            return false;
        } else {
            var url = "/omckv2/luu_mll_form/"; // the script where you handle the form input.
            var type = 'POST'
        }
        var data = $(this).serialize()

        $.ajax({
            type: type,
            url: url,
            data: data, // serializes the form's elements.
            error: function(request, status, error) {
                alert(request.responseText);
            },
            success: function(data) {
                $('#danh-sach-mll').html(data); // show response from the php script.
            }

        }); //ajax curly close
        return false; // avoid to execute the actual submit of the form.
    });


    $(".filter-mll-div").on('click', "input[type=submit]", function() {
        $("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
        $(this).attr("clicked", "true");
    });

    $("#danh-sach-mll").on('click', '.edit-mll-bnt', function() {
        console.log('ban dang clik edit-mll-bnt')
        mll_id = $(this).attr("id");

        $.get('/omckv2/edit_mll_entry/', {
            mll_id: mll_id
        }, function(data) {
            $('.filter-mll-div').html(data);
           

            $('.datetimepicker').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',

    });

        });
        var navigationFn = {
            goToSection: function(id) {
                $('html, body').animate({
                    scrollTop: $(id).offset().top
                }, 0);
            }
        }
        navigationFn.goToSection('#mll-filter-add-div');

    });
    $(this).on('click', '#submit-id-command-cancel', function() {
        console.log('ok nhan cancel')
        $('form#command-form').find('textarea,[name=id-command-entry]').val('')
        $('#submit-id-mll').val('Add Command')
        return false;
    });
    $(this).on('click', '.edit-command-bnt', function() {
        console.log('ban dang clik edit-command-bnt')

        mll_id = $(this).attr("id");
        console.log(mll_id)

        $.get('/omckv2/edit_command/', {
            mll_id: mll_id
        }, function(data) {
            $('.command-form').html(data);
            /*$('#command-form').append('<input type="submit" name="mll" value="Cancel" class="btn btn-primary" id="submit-id-mll">')*/
            $('#command-form').append('<div style="display:none"><input type="hidden" value="' + mll_id + '" name="id-command-entry"></div>')
            $('#submit-id-command-cancel').show()

            $('#submit-id-mll').val('Edit command')
        });

        var navigationFn = {
            goToSection: function(id) {
                $('html, body').animate({
                    scrollTop: $(id).offset().top
                }, 0);
            }
        }
        navigationFn.goToSection('.command-form');

    });



    /*text-search-input*/

    /*
    $('#text-search-input').keyup(function() {
        var query;
        query = $(this).val().replace('3G_', '');
        $.get('/omckv2/suggestion/', {
            query: query
        }, function(data) {
            $('.suggestion').html(data);
        });
    });


    $('#text-search-input').click(function() {
        var query;
        query = $(this).val().replace('3G_', '');
        $.get('/omckv2/suggestion/', {
            query: query
        }, function(data) {
            $('.suggestion').html(data);
        });
    });


    
    $('.suggestion').on('click', 'select > option', function(e) {
        console.log('ban dang click');
        var abc = $(e.target).html()
        console.log(abc)
        $('#text-search-input').val(abc)
    });


*/
    $('#text-search-input').keydown(function(e) {
        if (e.keyCode == 13) {

            var query;
            query = $(this).val();
            $.get('/omckv2/tram_table/', {
                query: query
            }, function(data) {
                $('.danh-sach-tram-tim-kiem').html(data);
            });
            $.get('/omckv2/search_history/', function(data) {
                $('#history_search').html(data);
            });
        }
    });
    

    $('.search-botton').click(function(e) {


        var query;
        query = $('#text-search-input').val().split('3G_').join('');
        $.get('/omckv2/tram_table/', {
            query: query
        }, function(data) {
            $('.danh-sach-tram-tim-kiem').html(data);
        });
        $.get('/omckv2/search_history/', function(data) {
            $('#history_search').html(data);
        });

    });

    $('.suggestion').on('click', 'select > option', function(e) {
        console.log('ban dang click');
        var abc = $(e.target).html()
        console.log(abc)
        $('#text-search-input').val(abc)
    });

    $('.suggestion').on('click', '.site-link', function() {
        var query;
        query = $(this).attr("tram");
        type = $(this).attr("type");
        id = $(this).attr("id")
        console.log(id)
        console.log(query);
        $.get('/show_detail_tram/', {
            query: query,
            type: type,
            id:id
        }, function(data) {
            $('.thong-tin-tram').html(data)
        });
        $.get('/omckv2/tram_table/', {
            query: query,
            id:id
        }, function(data) {
            $('.danh-sach-tram-tim-kiem').html(data);
        });

        $.get('/omckv2/search_history/', function(data) {
            $('#history_search').html(data);
        });
    });

    

/*
    $(this).on('keydown', '#text-search-input', function(e) {
        if (e.keyCode == 40) {
            console.log('ban dang nhan phim xuong')
            abc = $("select > option:first-child").val();
            console.log(abc)

            $("select > option:first-child").attr('selected', true)
            $("select").focus();
        }
    });


*/

    /*sugesstion-id_thiet_bi*/
    /*
    $('#sugesstion-id_thiet_bi').on('click', 'select > option', function(e) {
        var abc = $(e.target).html()
        console.log(abc)
        $('#id_thiet_bi_input').val(abc)
        
        $('#id_site_name').val($(this).attr('sitename'))
        $('#id_thiet_bi').val($(this).attr('thietbi'))

    });



    $('.filter-mll-div').on('keyup', '#id_thiet_bi_input', function() {
        var query;
        query = $(this).val();
        $.get('/omckv2/suggestion/', {
            query: query
        }, function(data) {
            $('#sugesstion-id_thiet_bi').html(data);
        });
    });
    $('#id_thiet_bi_input').click(function() {
        var query;
        query = $(this).val();
        $.get('/omckv2/suggestion/', {
            query: query
        }, function(data) {
            $('#sugesstion-id_thiet_bi').html(data);
        });
    });

    


    $(this).on('click', 'div#sugesstion-id_thiet_bi > select > option.site-link', function() {
        var query;
        query = $(this).attr("tram");
        type = $(this).attr("type");

        console.log(query);

        $.get('/show_detail_tram/', {
            query: query,
            type: type
        }, function(data) {
            $('.thong-tin-tram').html(data)
        });
        $.get('/omckv2/tram_table/', {
            query: query
        }, function(data) {
            $('.danh-sach-tram-tim-kiem').html(data);
        });
        $.get('/omckv2/search_history/', function(data) {
            $('#history_search').html(data);
        });
        $('#id_thiet_bi_input').val(query)
    });

*/

    

    /* eND SUGGESTION-ID THIET BI*/
    
/*
    $('#danh-sach-mll').on('click', 'table.tablemll > tbody > tr >td.thiet_bi', function() {
        console.log('ok, b')

        var query;
        query = $(this).html().replace('3G_', '')
        console.log(query);

        $.get('/show_detail_tram/', {
            query: query,
            type: 'all'
        }, function(data) {
            $('.thong-tin-tram').html(data)
        });

        $.get('/omckv2/tram_table/', {
            query: query
        }, function(data) {
            $('.danh-sach-tram-tim-kiem').html(data);
        });

        $.get('/omckv2/search_history/', function(data) {
            $('#history_search').html(data);
        });
    });


*/

    $('#search-lenh').on('keyup', function() {
        var query;
        query = $(this).val();
        $.get('/omckv2/lenh-suggestion/', {
            query: query
        }, function(data) {
            $('.lenh-table-div').html(data);

            $('table.cm-table > tbody>tr>td.id').each(function() {
                console.log('ok')
                var choosed_this = $(this).html()
                if (choosed_command_array_global.indexOf(choosed_this) > -1) {

                    $(this).parent().find('td.selection>input[type=checkbox]').prop('checked', true);
                }
            })

        });
    });



    $('.tram-table-div').on('keydown', '#search-lenh', function(e) {
        if (e.keyCode == 13) {
            var query;
            query = $('#search-lenh').val();
            console.log('ban da nhan enter de tim kiem tram')
            $.get('/omckv2/lenh_table/', {
                query: query
            }, function(data) {

                $(".lenh-table").html(data);
            });
        }
    });



    $(".select").bind("keydown change", function() {
        console.log('ban dan nhan keydown')
    });


    var counter = 0;

    $('.lenh-table-div').on('click', 'table.cm-table > tbody >tr >td.selection>input[type=checkbox] ', function() {
        chosing_row_id = $(this).closest("tr").find('td.id').html()
        console.log('chosing_row_id', chosing_row_id, $(this).is(':checked'))

        if (!$(this).is(':checked')) { /* bo chon 1 row*/
            console.log(chosing_row_id)
            $("table#myTable").find("td.id").filter(function() {
                var id = $(this).html();
                if (id == chosing_row_id) {
                    $(this).parent().remove();
                    var index = choosed_command_array_global.indexOf(id);
                    if (index > -1) {
                        choosed_command_array_global.splice(index, 1);
                    }
                    counter = $('#myTable tr').length - 1;
                    console.log('ban da bo chon 1 row lenh', choosed_command_array_global)
                }
            }) /* close brace for filter function*/

        } /* close if*/
        else {
            counter = counter + 1
            var newrowcopy = "";
            $(this).closest("tr").children().each(function() {
                if (!($(this).hasClass("selection") || $(this).is(':last-child'))) { /*BO CHON NHUNG CAI SELECTION*/
                    var thishtml = $(this).prop('outerHTML')
                    newrowcopy += thishtml
                }
            });
            var newRow = $("<tr>");
            /*newrowcopy = '<td>'+counter + '</td>' +  newrowcopy;*/
            newrowcopy += '<td><input type="button" class="ibtnDel"  value="Delete"></td>';
            newRow.append(newrowcopy);
            if (counter == 1113) alert('het quyen add row')
            $("table#myTable>tbody").append(newRow);
            choosed_command_array_global.push(chosing_row_id)
            console.log(choosed_command_array_global)
        }

    });



    $("table#myTable").on("click", ".ibtnDel", function(event) {

        tr_id = $(this).closest("tr").find('td.id').html()
        $(this).closest("tr").remove();
        $('table.cm-table').find('tr td  input[value =' + tr_id + ']').attr('checked', false)
        counter -= 1
    });




    $(this).on('click', '.generate-command', function() {

        console.log('ban dang click generate-command')

        var command_set_many_tram = "";
        $('.tram-table > tbody > tr').each(function() {
            var command_set_one_tram = "";
            var tram_row = $(this)
            $('#myTable > tbody > tr > td.command').each(function() {

                var one_command = $(this).html();
                var reg = /\[(.+?)\]/g;
                var matches_tram_attribute_sets = [],
                    found;

                while (found = reg.exec(one_command)) {
                    console.log('found.index', found.index, found, '\nreg.lastIndex', reg.lastIndex)
                    matches_tram_attribute_sets.push(found[1]);
                    reg.lastIndex = found.index + 1;
                }
                $.each(matches_tram_attribute_sets, function(index, tram_attribute) {

                    one_command = one_command.replace('[' + tram_attribute + ']', tram_row.find('td.' + tram_attribute.split(" ").join("_")).html())
                });
                command_set_one_tram += one_command + '\n'
            });

            command_set_many_tram += command_set_one_tram + '\n\n'
        });

        $('textarea.command-erea').val(command_set_many_tram);
        console.log(command_set_many_tram)
    });

    var id;
    $(this).on('click', 'ul.dropdown-menu > li.delete ', function() {
        id = $(this).closest("tr").find('td.id').html();
        $("#myModal").modal();
        return false;
    });


    $('.modal-ok-btn').on('click', function() {
        $.get('/omckv2/delete-mll/', {
            query: id
        }, function(data) {
            $('#danh-sach-mll').html(data);
        });
        $("#myModal").modal("hide");
    });




    $(this).on('click', 'ul.dropdown-menu > li#add-comment ', function() {
        console.log('ban dang clik vo li a ');
        id = $(this).closest("tr").find('td.id').html();
        $("#myModal-add-comment").find('form#add-comment-form-id').attr('selected_instance_mll', id).attr('comment_id', "new")

        tableHtml = $(this).closest("table").prop('outerHTML')
        var rownum = $(this).closest("tr").prevAll("tr").length + 1
          
        doituong = $(tableHtml)

        doituong.find('tbody > tr').not(':nth-child(' + rownum + ')').remove()

        $('th:lt(10):gt(5),th:last-child', doituong).remove()
        $('td:lt(10):gt(5),td:last-child', doituong).remove()
        $('a', doituong).contents().unwrap();
        doituong.attr("class", "table table-bordered")
        doituong.find('th').each(function(){
            $(this).attr("class", "")
        })
        content = doituong.prop('outerHTML')
        $("#myModal-add-comment").find('div.table-div').html(content)
        $("#myModal-add-comment").find('.modal-title').html("ADD COMMENT")
        $("#myModal-add-comment").find('button.addcomment-ok-btn').html("ADD COMMENT").attr("class", "btn btn-primary addcomment-ok-btn")
        $("#myModal-add-comment").find('h4').css('background-color', '#337ab7')
        $("#myModal-add-comment").find('textarea,input#id_datetime').val('')
        $('#datetimepicker_comment').datetimepicker({
        format: 'YYYY-MM-DD HH:mm'
    });
        $("#myModal-add-comment").modal();
        
        return false;
    })

    $('.thong-tin-tram').on('click', '.download-script', function() {
        site_id = $('.thong-tin-tram').attr('site_id')
        $("#config_ca_modal").find('.modal-title').html("Download Scrip")
        $("#config_ca_modal").find('button.addcomment-ok-btn').html("download-script").attr("class", "btn btn-primary link_to_download_scipt")
        $.get('/omckv2/load_form_config_ca/',{loai_form:'NTP',site_id:site_id},function(data){
           // $("#config_ca_modal").find('.').html(data)
                $("#config_ca_modal").find('.modal-body').html(data)
                $("#config_ca_modal").find('.modal-body').attr('branch', 'download_script')
                //.append( '<button type="submit" class="btn btn-primary link_to_download_scipt">download-script</button>').
                //append( '<button type="submit" class="btn btn-primary Update to db">Update to db</button>')
                $("#config_ca_modal").modal();
        });

         
        return false;
    });

    $(this).on('click','.link_to_download_scipt',function(){
        console.log('button ok')
        var data = $(this).closest('form').serialize()
        site_id = $('.thong-tin-tram').attr("site_id")
        var win = window.open('/omckv2/download_script_ntp/'+'?site_id=' + site_id+'&'+data );
        if (win) {
            //Browser has allowed it to be opened
            $("#config_ca_modal").modal("hide");
            win.focus();
        } else {
            //Broswer has blocked it
            alert('Please allow popups for this site');
        }
 
        return false

    })
        /*
        var id_3g = $('#id_site_id_3g').val();
        var win = window.open('/omckv2/download-script/' + '?id_3g=' + id_3g, '_blank');
        if (win) {
            //Browser has allowed it to be opened
            win.focus();
        } else {
            //Broswer has blocked it
            alert('Please allow popups for this site');
        }

    });*/
    $(this).on('click', 'a.call-modal', function() {

        $("#config_ca_modal").find('.modal-title').html("CONFIG CA")
        $("#config_ca_modal").find('button.addcomment-ok-btn').html("Submit ca").attr("class", "btn btn-primary addcomment-ok-btn")
        $("#config_ca_modal").find('h4').css('background-color', '#337ab7')
        //$("#config_ca_modal").find('form div#form-contain').html('<input type="radio" name="ca_truc" value="Moto">Moto<br><input type="radio" name="ca_truc" value="Alu">Alu<br><input type="radio" name="ca_truc" value="Huawei">Huawei<br><input type="radio" name="ca_truc" value="HCM">HCM<br>')
        $.get('/omckv2/load_form_config_ca/',{loai_form:'config_ca'},function(data){
            $("#config_ca_modal").find('form div#form-contain').html(data)
        })

        $("#config_ca_modal").find('.modal-body').attr('branch', 'config_ca')

        $("#config_ca_modal").modal();
        return false;
    })


    $(this).on('submit', '#config_ca_modal form', function() {
        console.log('config_ca_form')
        var url = "/omckv2/config_ca/"; // the script where you handle the form input.
        branch = $(this).closest('.modal-body').attr('branch')
        site_id = $('.thong-tin-tram').attr('site_id')
        var data = $(this).serialize() + '&branch=' + branch + '&site_id=' + site_id


        if (branch!='download_script'){
        $.ajax({
            type: "GET",
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {
                $('a#ca_truc_a').html(data)
                $("#config_ca_modal").modal("hide");
            },
            error: function(request, status, error) {
                alert(request.responseText);
            }

        }); }
        else {
            console.log('day la nhanh update script')
            $.ajax({
            type: "POST",
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {
                contain_form = $("#config_ca_modal").find('.modal-body')
                contain_form.fadeOut(300);
                contain_form.html(data)
                contain_form.fadeIn(300);
                //$("#config_ca_modal").modal("hide");
            },
            error: function(request, status, error) {
                alert(request.responseText);
            }

        }); 
        }
        //}
        return false;
    })

    /* click vao edit comment*/
     $('#danh-sach-mll').on('click', 'ul.comment-ul > li > a.edit-commnent', function() {
        selected_instance_mll = $(this).closest("tr").find('td.id').html();
        myform = $("#myModal-add-comment").find('form#add-comment-form-id')
         comment_id= $(this).attr("comment_id")
         console.log('comment_id',comment_id)
         $.get('/omckv2/load_edit_comment/',{comment_id:comment_id},function(data){
            myform.html(data)

         })
        id = $(this).closest("tr").find('td.id').html();
        myform.attr('selected_instance_mll', selected_instance_mll).attr('add_or_edit', "edit").attr('comment_id', comment_id)

        $("#myModal-add-comment").modal();
        return false;


});
        /*
    $('#danh-sach-mll').on('click', 'ul.comment-ul > li > a', function() {
        comment_id = $(this).attr("comment_id")
        id = $(this).closest("tr").find('td.id').html();
        $("#myModal-add-comment").find('form#add-comment-form-id').attr('selected_instance_mll', id).attr('add_or_edit', "edit").attr('comment_id', comment_id)

        comment_contain = $(this).find('span.comment').html()
        datetime = $(this).find('span.comment-time').html()
        comment_contain = comment_contain.replace(/<br>/g, '');
        content = $(this).closest("table").prop('outerHTML')
        var rownum = $(this).closest("tr").prevAll("tr").length + 1
    
        doituong = $(content)

        doituong.find('tbody > tr').not(':nth-child(' + rownum + ')').remove()
     
        $('th:lt(10):gt(5),th:last-child', doituong).remove()
        $('td:lt(10):gt(5),td:last-child', doituong).remove()
        $('a', doituong).contents().unwrap();
        doituong.attr("class", "table table-bordered")
        content = doituong.prop('outerHTML')
        $("#myModal-add-comment").find('div.table-div').html(content)
        $("#myModal-add-comment").find('textarea').val(comment_contain)
        $("#myModal-add-comment").find('input#id_datetime').val(datetime)
        $("#myModal-add-comment").find('.modal-title').html("EDIT COMMENT")
        $("#myModal-add-comment").find('button.addcomment-ok-btn').html("EDIT").attr("class", "btn btn-warning addcomment-ok-btn")
        $("#myModal-add-comment").find('h4').css('background-color', '#ec971f')
        $("#myModal-add-comment").modal();
        return false;
    })
*/

    $(this).on('submit', '#add-comment-form-id', function() {

        selected_instance_mll = $(this).attr('selected_instance_mll')
        console.log('selected_instance_mll',selected_instance_mll)
        add_or_edit = $(this).attr('add_or_edit')
        comment_id = $(this).attr('comment_id')
        console.log(comment_id)
        var url = "/omckv2/add_comment/"; // the script where you handle the form input.
        var data = $(this).serialize()
        data += "&selected_instance_mll=" + encodeURIComponent(selected_instance_mll) + "&comment_id=" + comment_id;

        console.log(data);
        $.ajax({
            type: "POST",
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {
                $("#myModal-add-comment").modal("hide");
                $('#danh-sach-mll').html(data); // show response from the php script.
            },
            error: function(request, status, error) {
                alert(request.responseText);
            }

        });
        //}
        return false;
    })

    $(this).on('click','a.edit-contact',function(){
        id =$(this).attr("id")
            $.get('/omckv2/get_contact_form/',{id:id}, function(data){
                var thisform = $('#myModal-edit-doitac form')
                thisform.attr('id_doi_tac',id).attr('actionfake','/omckv2/get_contact_form/')
                 thisform.find('#form-contain').html(data)
            })
            $("#myModal-edit-doitac").find('.modal-title').html("EDIT DOI TAC")
            $("#myModal-edit-doitac").modal();
            return false;
    })

    $(this).on('submit','#myModal-edit-doitac form', function(){

            var id = $(this).attr('id_doi_tac');
            console.log('id',id)
            var url = $(this).attr("actionfake"); // the script where you handle the form input.
            var data = $(this).serialize() 
            data+= '&id=' +id;
        $.ajax({
            type: "POST",
            url: url,
            data: data, // serializes the form's elements.
            error: function(request, status, error) {
                alert(request.responseText);
            },
            
            success: function(data) {
                $('#myModal-edit-doitac').modal('hide')
             $('#danh-sach-mll').html(data);
             
             
            },
            
        });
        
        return false;


    })


    $('.tram-table-div').on('submit', '#command-form', function() {

        console.log('form da duoc submit');
        var url = "/omckv2/add_command/"; // the script where you handle the form input.
        var data = $(this).serialize()
        $.ajax({
            type: "POST",
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {
                $('.lenh-table-div').html(data); // show response from the php script.
            }
        });

        return false;
    })
    $('.filter-mll-div').on('focus', 'textarea.expand', function() {
        $(this).addClass("expanding")
        $(this).animate({
            height: "160px",
            width: "200px"
        }, 300);
    });
    $('.filter-mll-div').on('blur', 'textarea.expand', function() {
        $(this).animate({
            height: "60px",
            width: "140px"
        }, 300);
        $(this).removeClass("expanding")
    });

    $('.filter-mll-div').on('focus', 'input.expand-input', function() {
        $(this).addClass("expanding-input")
        $(this).animate({
            width: "160px"
        }, 300);
    });
    $('.filter-mll-div').on('blur', 'input.expand-input', function() {
        $(this).animate({
            width: "70px"
        }, 300);
        $(this).removeClass("expanding-input")
    });

    $('.filter-mll-div').on('focus', 'input.expand-input1', function() {
        $(this).addClass("expanding-input1")
        $(this).animate({
            width: "140px"
        }, 300);
    });
    $('.filter-mll-div').on('blur', 'input.expand-input1', function() {
        $(this).animate({
            width: "100px"
        }, 300);
        $(this).removeClass("expanding-input1")
    });


    $(this).on('click', 'a.searchtable_header_sort', function() {
        var url = $(this).attr('href')
        var onclick = $(this).attr('onclick')

        if (url.indexOf("tram_table") > 0)

        {
            if (onclick != "return false") {
                $.get(url, function(data) {
                    $('.danh-sach-tram-tim-kiem').html(data);
                });

                return false;
            }

        } else if (url.indexOf("mll_filter") > 0) {
            if (onclick != "return false") {
                $.get(url, function(data) {
                    $('#danh-sach-mll').html(data);
                });

                return false;
            }

        } else if (url.indexOf("search_history") > 0) {
            if (onclick != "return false") {
                $.get(url, function(data) {
                    $('#history_search').html(data);
                });

                return false;
            }

        }


    });


    $(this).on("click", ".btnEdit", function() {
        var par = $(this).parent().parent(); //tr
        var array = [2, 4]
        par.children('td').each(function(i, v) {
                /*console.log(i,v)*/
                if (array.indexOf(i) > -1) {
                    $(this).html("<input type='text' id='" + $(this).attr("class") + "' value='" + $(this).html() + "'/>");
                } else if (i == 5) {
                    $(this).html("<img src='media/images/disk.png' class='btnSave'/>");
                }
            })
          
    });


    $(this).on("click", ".btnSave", function() {
        var trow = $(this).parent().parent(); //tr
        history_search_id = trow.find('td.id').html()
        var row = {};
        row.history_search_id = history_search_id
        trow.find('input,select,textarea').each(function() {
            row[$(this).attr('id')] = $(this).val();
        });
        console.log(row);
        $.get('/omckv2/edit_history_search/', row, function(data) {
            $('#history_search').html(data);
        });
        var array = [2, 4]
        trow.children().each(function(i, v) {
            /*$(this) = td*/
            if (array.indexOf(i) > -1) {
                $(this).html($(this).children("input[type=text]").val());



            } else if (i == 5) {
                $(this).html("<img src='media/images/delete.png' class='btnDelete'/><img src='media/images/pencil.png' class='btnEdit'/>");
            }

        });

    
    });
    $(this).on("click", ".btnDelete", function() {
        var par = $(this).parent().parent(); //tr
        par.remove();

    });

    $('.datetimepicker').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',

    });


$(this).on("focus", ".autocomplete", function () {
 $(this).autocomplete({
    create: function() {
        
        $(this).data('ui-autocomplete')._renderItem = function( ul, item ) {
      return $(' <li class="abc" ' + 'thietbi="' + item.label +'">')
        .append( "<a>" + '<b>' + item.label + '</b>' + "<br>" +'<span class="std">' + item.desc + '</span>' + "</a>" )
        .appendTo( ul );
    }},
    focus: function (event, ui) {
       if (ui.item['desc'] == "chưa có sdt" || !ui.item['desc']){
                this.value = ui.item['label']}
            else {
                this.value = ui.item['label'] + "-" + ui.item['desc'];}
       event.preventDefault(); // Prevent the default focus behavior.
},     
    search:  function( e, ui ) {
        temp_global_variable= $(e.target).attr("name")
        console.log('temp_global_variable',temp_global_variable)
        console.log("ui in search",ui)
        console.log(e.target)
    },
      source:function( request, response ) {
        //var inputfieldname = $(this).attr("name");

        console.log('temp_global_variable',temp_global_variable)
            var query = request.term
           $.get('/omckv2/get_need_variable/',{query:query,inputfieldname:temp_global_variable}, function(data) {
        response (data['key1'] )
        //response(projects)
        })
      },
        select: function( event, ui ) {
            console.log('ui.item',ui.item)
            //alert( ui.item ?
              //"Selected: " + ui.item['value'] + ", geonameId: " + ui.item['desc'] :
              //"Nothing selected, input was " + this.value );
            if (ui.item['desc'] == "chưa có sdt"|| !ui.item['desc'] ){
                this.value = ui.item['label']}
            else {
                this.value = ui.item['label'] + "-" + ui.item['desc'];}
            
            return false
          }

    })//close autocompltete
 

});


$(this).on("focus", ".autocomplete_search_tram", function () {
 $(this).autocomplete({
    create: function() {
        $(this).data('ui-autocomplete')._renderItem = function( ul, item ) {
      return $(' <li class="abc" ' + 'thietbi="' + item.label +'">')
        .append( "<a>" + '<b>' + '<span class="greencolor">'+item.sort_field +"-</span>" + item.label + '</b>' + "<br>" +'<span class="std">' + item.desc + '</span>' + "<br>" +'<span class="std">' + item.desc2 + '</span>' +"</a>" )
        .appendTo( ul );
    }},
    focus: function (event, ui) {
       
       event.preventDefault(); // Prevent the default focus behavior.
       return false;
       //if (event.keyCode == 40 ||event.keyCode == 38){
       //this.value = ui.item['label'];
       //}
},     
    search:  function( e, ui ) {
        temp_global_variable= $(e.target).attr("name")
        console.log('temp_global_variable',temp_global_variable)
        console.log("ui in search",ui)
        console.log(e.target)
    },
      source:function( request, response ) {
        //var inputfieldname = $(this).attr("name");

        console.log('temp_global_variable',temp_global_variable)
            var query = request.term
           $.get('/omckv2/get_need_variable/',{query:query,inputfieldname:temp_global_variable}, function(data) {
        response (data['key1'] )
        //response(projects)
        })
      },
        select: function( event, ui ) {
            console.log('ui.item',ui.item)
            //alert( ui.item ?
              //"Selected: " + ui.item['value'] + ", geonameId: " + ui.item['desc'] :
              //"Nothing selected, input was " + this.value );
            this.value = ui.item['label'];
            if (temp_global_variable=="subject"){
            $('#id_site_name').val(ui.item.site_name_1)
            $('#id_thiet_bi').val(ui.item.thiet_bi)

        }
            
            $.get('/show_detail_tram/', {
            id:ui.item.value
        }, function(data) {
            $('.thong-tin-tram').fadeOut(300);
            
            $('.thong-tin-tram').html(data).fadeIn(300);
            $('.thong-tin-tram').attr('site_id',ui.item.value)
        });
        $.get('/omckv2/tram_table/', {
            query:ui.item.label,
            id:ui.item.value
        }, function(data) {
            $('.danh-sach-tram-tim-kiem').html(data);
        });

        $.get('/omckv2/search_history/', function(data) {
            $('#history_search').html(data);
        });
            return false
          }

    })//close autocompltete
 

});

$(this).on('submit','.thong-tin-tram form',function(){
    var val = $(this).attr('site_id')
    var data = $(this).serialize() + '&' + 'site_id=' + val
        $.ajax({
            type: "POST",
            url: '/omckv2/edit_site/',
            val: val,
            data: data, // serializes the form's elements.
            success: function(data) {
                $('.thong-tin-tram').fadeOut(300);
                $('.thong-tin-tram').html(data).fadeIn(300);
                $('.thong-tin-tram').find('form').attr('site_id',val)
            }
        });

    return false;
});

}); //END READY DOCUMENT



var $loading = $('#loadingDiv').hide();


var choosed_command_array_global = []
$('#submit-id-command-cancel').hide()

var temp_global_variable