
$(document).ready(function() {

/*
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


*/

    $(this).on("submit", "#amll-form", function() {
        var clicked_button = $("input[type=submit][clicked=true]").attr("value");
        if (clicked_button == "Filter") {
            console.log(' trong ham Filter')
            var url = "/omckv2/mll_filter/"; // the script where you handle the form input.
            var type = 'GET';
        } else {
            var url = "/omckv2/luu_mll_form/"; // the script where you handle the form input.
            var type = 'POST'
        }
        var data = $(this).serialize() 
        if (clicked_button=="Cancle"){
           data={} 
           type = 'GET'
        }
        url = url + '?which-button=' + clicked_button
        $.ajax({
            type: type,
            url: url,
            data: data, // serializes the form's elements.
            error: function(request, status, error) {
                if (error == 'FORBIDDEN') { //403
                    alert('ban ko co quyen tao mll, chi co truc ca moi duoc,',error.responseText)
                } else if (error == 'BAD REQUEST') {
                    $('.filter-mll-div').html(request.responseText);
                    /*
                 $('.datetimepicker').datetimepicker({
                format: DT_FORMAT,
            });
                $('.comboboxd4').combobox()
*/
                } else {
                    new PNotify({
                        title: 'Oh No!',
                        text: request.responseText,
                        type: 'error'
                    });
                }

                /*
                new PNotify({
    title: 'Oh No!',
    text: request.responseText,
    type: 'error'
});
*/
            },
            success: function(data) {
                //     
                formhtml = $(data).find('div#form-area').html()
                $('.filter-mll-div').html(formhtml); // show response from the php script.
                //assign_and_fadeoutfadein($('.filter-mll-div'),formhtml)
                /*
                if (clicked_button == "Edit MLL initial") {
                    $('.first-comment').hide()
                }
                */
                tabelhtml = $(data).find('div#table-area').html()
                $('#danh-sach-mll').html(tabelhtml);
                assign_and_fadeoutfadein($('#danh-sach-mll'), tabelhtml)
                    /*
                $('.datetimepicker').datetimepicker({
                format: DT_FORMAT,
            });
                $('.comboboxd4').combobox()
                */
                    /*
                    new PNotify({
                        title: ' Success',
                        text: 'Ban vua luu 1 entry vao database!',
                        type: 'success'
                    });
                    */
            }

        }); //ajax curly close
        return false; // avoid to execute the actual submit of the form.
    });



    $(this).on('click', '.edit-mll-bnt', function() {
        mll_id = $(this).attr("id");
        if (!mll_id) {
            mll_id = 'Cancel'
        }
        $.get('/omckv2/mll_form/', {
            mll_id: mll_id
        }, function(data) {
            $('.filter-mll-div').html(data);
            /*
            $('.datetimepicker').datetimepicker({
                format: DT_FORMAT,
            });
            $('.comboboxd4').combobox()
            */
            if (mll_id != 'submit-id-cancel') {
                //$('.first-comment').hide()
                /*$('.first-comment').find("input, textarea,select").each(function(index) {
                $(this).attr("readonly","readonly")
            });*/
            }
        });
        var navigationFn = {
            goToSection: function(id) {
                $('html, body').animate({
                    scrollTop: $(id).offset().top
                }, 0);
            }
        }
        navigationFn.goToSection('#amll-form');
        return false

    });


//command................
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
   
       $('#search-lenh').on('keyup', function() {
        var query;
        query = $(this).val();
        $.get('/omckv2/lenh-suggestion/', {
            query: query
        }, function(data) {
            $('.lenh-table-div').html(data);

            $('table.cm-table > tbody>tr>td.id').each(function() {
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
        var command_set_many_tram = "";
        $('.tram-table > tbody > tr').each(function() {
            var command_set_one_tram = "";
            var tram_row = $(this)
            $('#myTable > tbody > tr > td.command').each(function() {
                var one_command = $(this).html();
                var reg = /\[(.+?)\]/g;
                var matches_tram_attribute_sets = []
                var found
                while (found = reg.exec(one_command)) {
                    console.log('found.index', found.index, 'found',found, '\nreg.lastIndex', reg.lastIndex)
                    matches_tram_attribute_sets.push(found[1]);
                    reg.lastIndex = found.index + 1;
                }
                $.each(matches_tram_attribute_sets, function(index, tram_attribute) {
                    value = tram_row.find('td.' + tram_attribute.split(" ").join("_")).html()
                    value = value.replace(/^ERI_3G_/g,'')
                    one_command = one_command.replace('[' + tram_attribute + ']', value)
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

        bootbox.confirm("Are you sure?", function(result) {
            if (result == true) {
                $.get('/omckv2/delete_mll/', {
                    query: id
                }, function(data) {
                    $('#danh-sach-mll').html(data);
                });


            };
            /*Example.show("Confirm result: " + result);*/
        }); //confirm box and function
        /*
             
                if (confirm("Are you sure?"))  {
                $.get('/omckv2/delete-mll/', {
                    query: id
                }, function(data) {
                    $('#danh-sach-mll').html(data);
                });
            };

        */

        return false
    }); //on and function


    /*
     $('.modal-ok-btn').on('click', function() {
        confirm_press_ok  = true;
        });

*/

    /*

        $('.modal-ok-btn').on('click', function() {
            $.get('/omckv2/delete-mll/', {
                query: id
            }, function(data) {
                $('#danh-sach-mll').html(data);
            });
            $("#myModal").modal("hide");
        });

    */



    //Config Ca modal



    $('.thong-tin-tram').on('click', 'button.download-script', function() {
        site_id = $('.thong-tin-tram').attr('site_id')
        $("#config_ca_modal").find('.modal-title').html("Download Scrip")
        $.get('/omckv2/load_form_config_ca/', {
            loai_form: 'NTP',
            site_id: site_id
        }, function(data) {
            // $("#config_ca_modal").find('.').html(data)
            $("#config_ca_modal").find('.modal-body').html(data)
            $("#config_ca_modal").find('.modal-body').attr('loai_form', 'NTP')
            $("#config_ca_modal").modal();
        });


        return false;
    });

    $(this).on('click', 'button.link_to_download_scipt', function() {
        console.log('button ok')
        var data = $(this).closest('form').serialize()
        site_id = $('.thong-tin-tram').attr("site_id")
        var win = window.open('/omckv2/download_script_ntp/' + '?site_id=' + site_id + '&' + data);
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

    $(this).on('click', 'a.call-modal', function() {

        $("#config_ca_modal").find('.modal-title').html("CONFIG CA")
        $("#config_ca_modal").find('h4').css('background-color', '#337ab7')
        $.get('/omckv2/load_form_config_ca/', {
            loai_form: 'config_ca'
        }, function(data) {
            $("#config_ca_modal").find('.modal-body').html(data)
        })

        $("#config_ca_modal").find('.modal-body').attr('loai_form', 'config_ca')
        $("#config_ca_modal").modal();
        return false;
    })

    $(this).on('click', 'a#config_ca_filter_mll_table', function() {
        url = $(this).attr("ajax-url")
        $.get(url, {}, function(data) {
            $("#config_ca_filter_mll_table_modal").html(data)
        })
        $("#config_ca_filter_mll_table_modal").modal();

        return false;
    })

    $(this).on('submit', 'form#config_ca_filter_mll_table', function() {
        //url = $(this).attr("action")
        var data = $(this).serialize()
        $.ajax({
            type: "POST",
            url: '/omckv2/config_ca_filter_mll_table/',
            data: data, // serializes the form's elements.
            success: function(data) {
                new PNotify({
                    title: ' Success',
                    text: 'ok',
                    type: 'success'
                });
                $("#config_ca_filter_mll_table_modal").modal("hide");
            },
            error: function(request, status, error) {
                alert(request.responseText);
            }

        });
        return false;
    })
    $(this).on('submit', '#config_ca_modal form', function() {
        console.log('config_ca_form')
        var url = "/omckv2/config_ca/"; // the script where you handle the form input.
        loai_form = $(this).closest('.modal-body').attr('loai_form')
        site_id = $('.thong-tin-tram').attr('site_id')
        var data = $(this).serialize() + '&loai_form=' + loai_form + '&site_id=' + site_id


        if (loai_form != 'NTP') {
            $.ajax({
                type: "POST",
                url: url,
                data: data, // serializes the form's elements.
                success: function(data) {
                    $('a#ca_truc_a').html(data)
                    $("#config_ca_modal").modal("hide");
                },
                error: function(request, status, error) {
                    alert(request.responseText);
                }

            });
        } else if (loai_form == 'NTP') {
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
                },
                error: function(request, status, error) {
                    alert(request.responseText);
                }

            });
        }
        //}

    })

    function copy_row(this_obj) {
        tableHtml = $(this_obj).closest("table").prop('outerHTML')
        var rownum = $(this_obj).closest("tr").prevAll("tr").length + 1
        doituong = $(tableHtml)
        doituong.find('tbody > tr').not(':nth-child(' + rownum + ')').remove()
            //$('th:lt(10):gt(5),th:last-child', doituong).remove()
            //$('td:lt(10):gt(5),td:last-child', doituong).remove()

        $('th:lt(15):gt(5)', doituong).remove()
        $('td:lt(15):gt(5)', doituong).remove()

        $('a', doituong).contents().unwrap();
        doituong.attr("class", "table table-bordered")
        doituong.find('th').each(function() {
            $(this).attr("class", "")
        })
        content = doituong.prop('outerHTML')
        $("#modal-on-mll-table").find('div.table-div').html(content)
    }


    $(this).on('click', 'ul.dropdown-menu > li#add-comment,ul.comment-ul > li > a.edit-commnent, .handlemodal', function() {
        class_atag = $(this).attr("class")
        that = this
        try {
            rs = class_atag.indexOf('handlemodal')
        } catch (e) {
            rs = -1 // 'add new comment'
        }
        if (rs > -1) { // i.e if handlemodal in url
            get_form_url = $(this).attr("href")
            url = get_form_url
            data = {}
            action = url
        } 
        else { //i.e handelCommentForMLLForm
            mll_id = $(this).closest("tr").find('td.id').html()
            
            url = '/omckv2/handelCommentForMLLForm/'
            comment_id = $(this).attr("comment_id")
            if (!comment_id) {
                comment_id = 'new'
            }

            data = { }
            url = url + comment_id + '/'
            action = url
            url = action + '?selected_instance_mll=' + mll_id //add 

        }

        // Luu y ve van de Asynchronation
        //myform = $("#modal-on-mll-table").find('form#add-comment-form-id')
        $.get(url, data, function(data) {
            $("#modal-on-mll-table").html(data)
            //$("#modal-on-mll-table").find('form#add-comment-form-id').attr('selected_instance_mll', mll_id).attr('comment_id', comment_id)
            $("#modal-on-mll-table").find('form#add-comment-form-id').attr('action', action)
            if (rs == -1){
            copy_row(that)
        }
            $("#modal-on-mll-table").modal();
        })

        return false;
    })


    /* 
    $('#danh-sach-mll').on('click', 'ul.comment-ul > li > a.edit-commnent111', function() {
        selected_instance_mll = $(this).closest("tr").find('td.id').html();
        copy_row(this)
        comment_id = $(this).attr("comment_id")
        console.log('comment_id', comment_id)
        myform = $("#modal-on-mll-table").find('form#add-comment-form-id')
        $.get('/omckv2/load_edit_comment/', {
            comment_id: comment_id
        }, function(data) {
            myform.html(data)
            $('.datetimepicker-comment').datetimepicker({
                format: DT_FORMAT
            }) 
            $('.comboboxd4').combobox()
            $('#id_thao_tac_lien_quan').select2();
            $("#modal-on-mll-table form").find('button').html("EDIT").attr("class", "btn btn-warning addcomment-ok-btn")

        })
        id = $(this).closest("tr").find('td.id').html();
        myform.attr('selected_instance_mll', selected_instance_mll).attr('add_or_edit', "edit").attr('comment_id', comment_id)
        $("#modal-on-mll-table h4.modal-title").html("Edit comment")
        $("#modal-on-mll-table ").find('h4').css('background-color', '#ec971f')
        $("#modal-on-mll-table").modal();
        return false;
    });
click vao edit comment*/
    $(this).on('submit', '#add-comment-form-id', function() {
        //selected_instance_mll = $(this).attr('selected_instance_mll')
        //comment_id = $(this).attr('comment_id')
        //var url = "/omckv2/add_comment/"; // the script where you handle the form input.
        var clicked_button = $("input[type=submit][clicked=true]").attr("value")
        console.log('clicked_button',clicked_button)
        var url = $(this).attr('action')
        if (clicked_button=="ADD NEW") {
            url = url.replace(/\/\d+\//g,'/new/')
            console.log(url)
        }
        
        console.log('url in form submit', url)
        var data = $(this).serialize()
            //data += "&selected_instance_mll=" + encodeURIComponent(selected_instance_mll)
        $.ajax({
            type: "POST",
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {
                $("#modal-on-mll-table").modal("hide");
                $('#danh-sach-mll').html(data); // show response from the php script.
            },
            error: function(request, status, error) {
                console.log('status', error)
                if (error == 'FORBIDDEN') { //403
                    alert(request.responseText);
                } 
                else if (error == 'BAD REQUEST') {//400 required form, validation form
                    $("#modal-on-mll-table").html(request.responseText)
                    $("#modal-on-mll-table").find('form#add-comment-form-id').attr('action', url)
                }
            }

        });
        //}
        return false;
    })
/*
    $(this).on('click', 'a.edit-contact', function() {
        id = $(this).attr("id")
        $.get('/omckv2/get_contact_form/', {
            id: id
        }, function(data) {
            var thisform = $('#myModal-edit-doitac form')
            thisform.attr('id_doi_tac', id).attr('actionfake', '/omckv2/get_contact_form/')
            thisform.find('#form-contain').html(data)
        })
        $("#myModal-edit-doitac").find('.modal-title').html("EDIT DOI TAC")
        $("#myModal-edit-doitac").modal();
        return false;
    })

    $(this).on('submit', '#myModal-edit-doitac form', function() {

        var id = $(this).attr('id_doi_tac');
        console.log('id', id)
        var url = $(this).attr("actionfake"); // the script where you handle the form input.
        var data = $(this).serialize()
        data += '&id=' + id;
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


    
*/

    /*
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
    */

    $(this).on('click', 'a.searchtable_header_sort', function() {
        var this_linkable_table_part_link = $(this)
        var url = $(this).attr('href')
        var onclick = $(this).attr('onclick')

        if (url.indexOf("tram_table") > 0)

        {
            if (onclick != "return false") { //return true hoac == undefine
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




        } else if (url.indexOf("doitac_table_sort") > 0) {
            if (onclick != "return false") {
                $.get(url, function(data) {
                    this_linkable_table_part_link.closest(".table-div").html(data);
                });

                return false;
            }
        }
    });


    $(this).on("click", ".btnEdit", function() {
        var array_td_need_edit = [] //array la chua nhung index cua td can edit
        var par = $(this).parent().parent();
        wrapper_table = $(this).closest('table')
        table_class = wrapper_table.attr("class") //tr
        if (table_class.indexOf('history-table') > -1) {
            array_td_need_edit = [2, 3, 4]
        } else if (table_class.indexOf('doi_tac-table') > -1) {
            array_td_need_edit = [1, 2, 3, 4, 5, 6]
        }
        this_row = par.children('td')
        var total = this_row.length;
        this_row.each(function(i, v) {
            this_html = $(this).text()
            this_html = ((this_html == "—") ? "" : this_html)
            if (array_td_need_edit.indexOf(i) > -1) {
                $(this).html("<input type='text' id='" + $(this).attr("class") + "' value='" + this_html + "'/>");
            } else if (i == total - 1) {
                $(this).html("<img src='media/images/disk.png' class='btnSave'/>");
            }
        })

    });
    $(this).on("click", ".btnSave", function() {
        wrapper_table = $(this).closest('table')
        table_class = wrapper_table.attr("class")
        table_div = $(this).closest('div.table-div')
        url = wrapper_table.attr("table-action")
        var trow = $(this).parent().parent(); //tr
        history_search_id = trow.find('td.id').html()
        var row = {
            action: "edit"
        };
        row.history_search_id = history_search_id
        trow.find('input,select,textarea').each(function() {
            row[$(this).attr('id')] = $(this).val();
        });
        if (table_class.indexOf('history-table') > 0) {
            //url = '/omckv2/edit_history_search/',
            $.get(url, row, function(data) {
                $('#history_search').html(data);
            });
        } else if (table_class.indexOf('doi_tac-table') > 0) {

            $.get(url, row, function(data) {
                console.log(data);

                $('#table-doitac').html(data);
            });
        }

    });

    $(this).on("click", ".btnDelete", function() {

        wrapper_table = $(this).closest('table')
        table_class = wrapper_table.attr("class")
        url = wrapper_table.attr("table-action")
            //console.log('table_class',table_class,'url',url)
        var trow = $(this).parent().parent(); //tr
        history_search_id = trow.find('td.id').html()
            /*
         $.get( url,{"action":"delete","history_search_id":history_search_id}, function(data) {
            $('#history_search').html(data);
        });
    */
            //$('.modal-ok-btn').attr("deleteId",history_search_id)
        if (table_class.indexOf('history-table')) {
            $("#myModal").find('div#id-deleted-object').html("Doi tuong xoa co id " + history_search_id)
                //$("#myModal").modal();
            if (confirm("Are you sure?")) {
                $.get(url, {
                        "action": "delete",
                        "history_search_id": history_search_id
                    },
                    function(data) {
                        $('#history_search').html(data);
                    });
                //$("#myModal").modal("hide");

                return false; //url = '/omckv2/edit_history_search/',
            }
        }

    });
    $(this).on('click', '.addrow', function() {
            a = $(this).parent()
            tbody = a.find('tbody')
            firstrow = tbody.find('tr:first')
            total = firstrow.find('td').length
            console.log('tbody', a)
            array_td_need_edit = [1, 2, 3, 4, 5, 6]
            row = $('<tr><td class="id">')
                /*
                for (i=1;i<total-1;i++){
                    if (array_td_need_edit.indexOf(i)> -1){
                    row.append('<td><input type="text"/></td>');}
                    else {
                        row.append('<td></td>')
                    }
                  
                }
                */
            firstrow.find('td').each(function(i, v) {
                if (array_td_need_edit.indexOf(i) > -1) {
                    row.append("<td><input type='text' id='" + $(this).attr("class") + "'/></td>");
                }
            })

            row.append("<img src='media/images/disk.png' class='btnSave'/>");
            firstrow.before(row);
            //$(row).prependTo(tbody);

        })
        /*
    $(this).on("click", ".btnDelete", function() {
        var par = $(this).parent().parent(); //tr
        par.remove();

    });
*/

    $('.datetimepicker').datetimepicker({
        format: DT_FORMAT,
    });


    $(this).on("focus", ".autocomplete", function() {
        $(this).autocomplete({
                create: function() {

                    $(this).data('ui-autocomplete')._renderItem = function(ul, item) {
                        return $(' <li class="abc" ' + 'thietbi="' + item.label + '">')
                            .append("<a>" + '<b>' + item.label + '</b>' + "<br>" + '<span class="std">' + item.desc + '</span>' + "</a>")
                            .appendTo(ul);
                    }
                },
                search: function(e, ui) {
                    name_attr_global = $(e.target).attr("name")

                },
                source: function(request, response) {
                    console.log('name_attr_global', name_attr_global)
                    var query = request.term
                    $.get('/omckv2/autocomplete/', {
                        query: query,
                        name_attr: name_attr_global
                    }, function(data) {
                        response(data['key_for_list_of_item_dict'])

                    })
                },
                select: function(event, ui) {
                    if (ui.item['desc'] == "chưa có sdt" || !ui.item['desc']) {
                        this.value = ui.item['label']
                    } else {
                        this.value = ui.item['label'] + "-" + ui.item['desc'];
                    }

                    return false
                }

            }) //close autocompltete


    });



    $(this).on("focus", ".autocomplete_search_tram", function() {
        $(this).autocomplete({
                create: function() {
                    $(this).data('ui-autocomplete')._renderItem = function(ul, item) {
                        /*
                        return $(' <li class="abc" ' + 'thietbi="' + item.label + '">')
                            .append("<a>" + '<b>' + '<span class="greencolor">' + item.sort_field + "-</span>" 
                                + item.label + '</b>' + "<br>" + '<span class="std">' + item.desc + '</span>' + 
                                "<br>" + '<span class="std">' + item.desc2 + '</span>' + "</a>")
                            .appendTo(ul);
                        */
                        return $('<li>').append(
                                $('<a>').append('<b>' + '<span class="greencolor">' + item.sort_field + "-</span>" + item.label + '</b>')
                                .append("<br>" + '<span class="std">' + item.desc + '</span>' +
                                    "<br>" + '<span class="std">' + item.desc2 + '</span>'))
                            .appendTo(ul)

                    }
                },
                focus: function(event, ui) {

                    event.preventDefault(); // Prevent the default focus behavior.
                    return false;

                },
                search: function(e, ui) {
                    name_attr_global = $(e.target).attr("name") //name_attr_global de phan biet cai search o top of page or at mllfilter
                    console.log('name_attr_global', name_attr_global)

                    //console.log("ui in search", ui)
                    //console.log(e.target)
                },
                source: function(request, response) {

                    console.log('name_attr_global', name_attr_global)
                    var query = extractLast(request.term)
                    $.get('/omckv2/autocomplete/', {
                        query: query,
                        name_attr: name_attr_global
                    }, function(data) {
                        response(data['key_for_list_of_item_dict'])
                            //response(projects)
                    })
                },
                select: function(event, ui) {
                    if (name_attr_global == "subject") {
                        var terms = split(this.value);
                        // remove the current input
                        terms.pop();
                        // add the selected item
                        terms.push(ui.item.value);
                        // add placeholder to get the comma-and-space at the end
                        terms.push("");
                        this.value = terms.join(", ");
                    } else {
                        this.value = ui.item['label']; //this.value tuc la gia tri hien thi trong input text
                    }
                    if (name_attr_global == "subject") {
                        $('#id_site_name').val(ui.item.site_name_1)
                        $('#id_thiet_bi').val(ui.item.thiet_bi)
                    }

                    $.get('/omckv2/detail_tram_compact_with_search_table/', {
                        id: ui.item.id,
                        query: ui.item.label
                    }, function(data) {
                        formhtml = $(data).find('div#form-area').html()
                        tabelhtml = $(data).find('div#table-area').html()
                        $('.thong-tin-tram').fadeOut(300);
                        $('.thong-tin-tram').html(formhtml).fadeIn(300);
                        $('.thong-tin-tram').attr('site_id', ui.item.id)
                        assign_and_fadeoutfadein($('.danh-sach-tram-tim-kiem'), tabelhtml)
                            //$('.danh-sach-tram-tim-kiem').html(tabelhtml);
                    });

                    return false // return thuoc ve select :
                }

            }) //close autocompltete
    });

    $(this).on('submit', 'form#detail_tram', function() {
        var val = $('.thong-tin-tram').attr('site_id')
        var data = $(this).serialize() + '&' + 'site_id=' + val
        var url = $(this).attr('action') ///omckv2/edit_site/
        $.ajax({
            type: "POST",
            url: url,
            val: val,
            data: data, // serializes the form's elements.
            success: function(data) {
                $('.thong-tin-tram').fadeOut(300);
                $('.thong-tin-tram').html(data).fadeIn(300);
                //$('.thong-tin-tram').find('form').attr('site_id',val)
            }
        });

        return false;
    });

    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

    $(".autocomplete_search_tram1")
        // don't navigate away from the field on tab when selecting an item
        .bind("keydown", function(event) {
            if (event.keyCode === $.ui.keyCode.TAB &&
                $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
        })
        .autocomplete({
            minLength: 0,
            search: function(e, ui) {
                name_attr_global = $(e.target).attr("name") //name_attr_global de phan biet cai search o top of page or at mllfilter
                console.log('name_attr_global', name_attr_global)
                    //console.log("ui in search", ui)
                    //console.log(e.target)
            },
            source: function(request, response) {

                console.log('name_attr_global', name_attr_global)
                var query = extractLast(request.term)
                $.get('/omckv2/autocomplete/', {
                    query: query,
                    name_attr: name_attr_global
                }, function(data) {
                    response(data['key_for_list_of_item_dict'])
                        //response(projects)
                })
            },
            focus: function() {
                // prevent value inserted on focus
                return false;
            },
            select: function(event, ui) {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(", ");
                return false;
            }
        });
    //consume_alert();
    $('.selectmultiple').select2()
        //$(".tablemll").colResizable();


    $(this).on('click', "input[type=submit]", function() {
        $("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
        $(this).attr("clicked", "true");
    });



}); //END READY DOCUMENT

//var $loading = $('#loadingDiv').hide();
$(document).ajaxComplete(function(event, xhr, settings) {

    $('.datetimepicker-comment').datetimepicker({
        format: DT_FORMAT
    });

    $('.comboboxd4').combobox()
        /*
            $('.comboboxd4').select2({
  placeholder: "Select a state",
  allowClear: true
});
*/
    $('.datetimepicker').datetimepicker({
        format: DT_FORMAT,
    });

    $('.datetimepicker').datetimepicker({
        format: DT_FORMAT,
    });
     $('#id_thao_tac_lien_quan').select2({
                width: '100%'
            });
});
$(function() {
    $(".comboboxd4").combobox();

});

$(document).on("ajaxStart", function() {
    $("#loading").show();
}).on("ajaxComplete", function() {
    $("#loading").hide();
});

$("#loading").hide();

var choosed_command_array_global = []
$('#submit-id-command-cancel').hide()

var name_attr_global
var DT_FORMAT = 'HH:mm DD/MM/YYYY'
    /*
    function consume_alert() {
        if (_alert) return;
        _alert = window.alert;
        window.alert = function(message) {
            new PNotify({
                title: 'Alert',
                text: message
            });
        };
    }
    */
PNotify.prototype.options.delay ? (function() {
    PNotify.prototype.options.delay = 1500;

}()) : (alert('Timer is already at zero.'))


function test() {
    console.log('toi dang test')
}

test(1);

(function($) {
    $.widget("custom.combobox", {
        _create: function() {
            this.wrapper = $("<span>")
                .addClass("custom-combobox")
                .insertAfter(this.element);

            this.element.hide();
            this._createAutocomplete();
            this._createShowAllButton();
        },

        _createAutocomplete: function() {
            var selected = this.element.children(":selected"),
                value = selected.val() ? selected.text() : "";

            this.input = $("<input>")
                .appendTo(this.wrapper)
                .val(value)
                .attr("title", "")
                .addClass("custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left")
                .autocomplete({
                    delay: 0,
                    minLength: 0,
                    source: $.proxy(this, "_source")
                })
                .tooltip({
                    tooltipClass: "ui-state-highlight"
                });

            this._on(this.input, {
                autocompleteselect: function(event, ui) {
                    ui.item.option.selected = true;
                    this._trigger("select", event, {
                        item: ui.item.option
                    });
                },

                autocompletechange: "_removeIfInvalid"
            });
        },

        _createShowAllButton: function() {
            var input = this.input,
                wasOpen = false;

            $("<a>")
                .attr("tabIndex", -1)
                .attr("title", "Show All Items")
                .tooltip()
                .appendTo(this.wrapper)
                .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                })
                .removeClass("ui-corner-all")
                .addClass("custom-combobox-toggle ui-corner-right")
                .mousedown(function() {
                    wasOpen = input.autocomplete("widget").is(":visible");
                })
                .click(function() {
                    input.focus();

                    // Close if already visible
                    if (wasOpen) {
                        return;
                    }

                    // Pass empty string as value to search for, displaying all results
                    input.autocomplete("search", "");
                });
        },

        _source: function(request, response) {
            var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
            response(this.element.children("option").map(function() {
                var text = $(this).text();
                if (this.value && (!request.term || matcher.test(text)))
                    return {
                        label: text,
                        value: text,
                        option: this
                    };
            }));
        },

        _removeIfInvalid: function(event, ui) {

            // Selected an item, nothing to do
            if (ui.item) {
                return;
            }

            // Search for a match (case-insensitive)
            var value = this.input.val(),
                valueLowerCase = value.toLowerCase(),
                valid = false;
            this.element.children("option").each(function() {
                if ($(this).text().toLowerCase() === valueLowerCase) {
                    this.selected = valid = true;
                    return false;
                }
            });

            // Found a match, nothing to do
            if (valid) {
                return;
            }

            // Remove invalid value
            this.input
                .val("")
                .attr("title", value + " didn't match any item")
                .tooltip("open");
            this.element.val("");
            this._delay(function() {
                this.input.tooltip("close").attr("title", "");
            }, 2500);
            this.input.autocomplete("instance").term = "";
        },

        _destroy: function() {
            this.wrapper.remove();
            this.element.show();
        }
    });
})(jQuery);


// D4 fadeIn fadeOut
function d4fadeOutFadeIn(jqueryobject, datahtml) {

    jqueryobject.fadeOut(300);
    jqueryobject.html(datahtml).fadeIn(300);
    jqueryobject.attr('site_id', ui.item.value)
};

function assign_and_fadeoutfadein(jqueryobject, datahtml) {

    jqueryobject.fadeOut(300);
    jqueryobject.html(datahtml).fadeIn(300);
};