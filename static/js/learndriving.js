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



    /*
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
        if (clicked_button == "Cancle") {
            data = {}
            type = 'GET'
        }
        url = url + '?which-button=' + clicked_button
        $.ajax({
            type: type,
            url: url,
            data: data, // serializes the form's elements.
            error: function(request, status, error) {
                if (error == 'FORBIDDEN') { //403
                    alert('ban ko co quyen tao mll, chi co truc ca moi duoc,', request.responseText)
                } else if (error == 'BAD REQUEST') {
                    $('.filter-mll-div').html(request.responseText);
                } else {
                    new PNotify({
                        title: 'Oh No!',
                        text: request.responseText,
                        type: 'error'
                    });
                }
            },
            success: function(data) {
                //     
                formhtml = $(data).find('div#form-area').html()
                $('.filter-mll-div').html(formhtml); // show response from the php script.
                tabelhtml = $(data).find('div#table-area').html()
                $('#danh-sach-mll').html(tabelhtml);
                assign_and_fadeoutfadein($('#danh-sach-mll'), tabelhtml)

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

            if (mll_id != 'submit-id-cancel') {

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

*/
    //command................

    $('.search-botton').click(function(e) {


        var query;
        query = $('#text-search-input').val().split('3G_').join('');
        $.get('/omckv2/tram_table/', {
            query: query
        }, function(data) {
            $('#form-table-of-tram-info .table-manager').html(data);
        });
        $.get('/omckv2/search_history/', function(data) {
            $('#history_search').html(data);
        });

    });


    var counter = 0;
    $(this).on('click', 'table.cm-table > tbody >tr >td.selection>input[type=checkbox] ', function() {
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
                    console.log('found.index', found.index, 'found', found, '\nreg.lastIndex', reg.lastIndex)
                    matches_tram_attribute_sets.push(found[1]);
                    reg.lastIndex = found.index + 1;
                }
                $.each(matches_tram_attribute_sets, function(index, tram_attribute) {
                    value = tram_row.find('td.' + tram_attribute.split(" ").join("_")).html()
                    value = value.replace(/^ERI_3G_/g, '')
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
        }); //confirm box and function

        return false
    }); //on and function



    $(this).on('click', '.link_to_download_scipt', function() {
        console.log('button ok')
        var data = $(this).closest('form').serialize()
        site_id = $('#form-table-of-tram-info').find('input#id_id').val()
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

    function updateURLParameter(url, param, paramVal) {
        var newAdditionalURL = "";
        var tempArray = url.split("?");
        var baseURL = tempArray[0];
        var additionalURL = tempArray[1];
        var temp = "";
        if (additionalURL) {
            tempArray = additionalURL.split("&");
            for (i = 0; i < tempArray.length; i++) {
                if (tempArray[i].split('=')[0] != param) {
                    newAdditionalURL += temp + tempArray[i];
                    temp = "&";
                }
            }
        }

        var rows_txt = temp + "" + param + "=" + paramVal;
        return baseURL + "?" + newAdditionalURL + rows_txt;
    }

    function toggleDesAsc(additionalURL) {
        var newAdditionalURL = "";
        tempArray = additionalURL.split("&");
        for (i = 0; i < tempArray.length; i++) {
            key = tempArray[i].split('=')[0]

            if (key != 'sort') {
                newAdditionalURL += "&" + tempArray[i];
            } else {
                paraValue = tempArray[i].split('=')[1]
                if (paraValue.indexOf('-') > -1) {
                    console.log('paraValue co - la', paraValue)
                    paraValue = paraValue.replace('-', '')
                } else {
                    paraValue = '-' + paraValue
                }
                newAdditionalURL += "&" + key + '=' + paraValue;
            }
        }
        return newAdditionalURL
    }




    function form_table_handle(e, intended_for, abitrary_url) {
        class_value = $(this).attr("class")
        loai_ajax = "normal"
        is_no_show_return_form = false
        is_both_table = "both form and table"
        form_table_template = "normal form template"
        hieu_ung_sau_load_form_va_table = "khong hieu ung"
        closest_wrapper = $(this).closest('div.form-table-wrapper')
        id_closest_wrapper = closest_wrapper.attr('id') // no importaince
        table_name = '' // table_name dung de xac dinh table , sau khi submit form o modal se hien thi o day, trong truong hop force_allow_edit thi table_name attr se bi xoa 
        if (intended_for == 'intended_for_autocomplete') {
            is_both_table = "both form and table"
            closest_wrapper = $('#form-table-of-tram-info')
            url = abitrary_url
            type = "GET"
            data = {}
        } else if (class_value.indexOf('searchtable_header_sort') > -1) {
            is_both_table = 'table only'
            url = $(this).attr('href')
            if (id_closest_wrapper=='same-ntp-table'){
                tram_id = $('#form-table-of-tram-info').find('#id_id').val()
                console.log('tram_id',tram_id)
                url = updateURLParameter(url, 'tram_id', tram_id)
                console.log('url',url)
            }
            type = "GET"
            data = {}
        } else if (class_value.indexOf('edit-entry-btn-on-table') > -1) {
            url = closest_wrapper.find('form#model-manager').attr('action')
            entry_id = $(this).attr('id')
            url = url.replace(/\/\w+\/$/g, '/' + entry_id + '/')
            console.log('url', url)
            is_both_table = "form only"
            hieu_ung_sau_load_form_va_table = "edit-entry"
            type = "GET"
            data = {}

        } else if (class_value.indexOf('manager-form-select') > -1) {
            url = $('#id_chon_loai_de_quan_ly option:selected').val()
            url = $(this).val() //url = new va method = get
            type = "GET"
            data = {}
        } else if (class_value.indexOf('show-modal-form-link') > -1) {
            url = $(this).attr("href") ///omckv2/show-modal-form-link/ThietBiForm/1/
            form_table_template = 'form on modal'
            table_name = $(this).closest('table').attr('name')
            $('#modal-on-mll-table').attr('table_name', table_name)
            type = "GET"
            data = {}
            is_both_table = "form only"
            if (class_value.indexOf('add-comment') > -1) {
                mll_id = $(this).closest("tr").find('td.id').html()
                url = updateURLParameter(url, 'selected_instance_mll', mll_id)
            } else if (class_value.indexOf('force_allow_edit') > -1) {
                url = updateURLParameter(url, 'is_allow_edit', 'True')
                $('#modal-on-mll-table').removeAttr('table_name')
            } else if (class_value.indexOf('downloadscript') > -1) {
                is_both_table = "both form and table"
                tram_id = $(this).closest('form').find('input[name=id]').val()
                console.log('tram_id', tram_id)
                url = updateURLParameter(url, 'tram_id_for_same_ntp', tram_id)
                hieu_ung_sau_load_form_va_table = 'add class overflow for table'
                console.log('!@#$!@#$1')
            }
        } else if (class_value.indexOf('cancel-btn') > -1) { //cancle buton duoc nhan.
            url = $(this).closest('form').attr("action").replace(/\/\d+\//g, '/new/')
            type = "GET"
            data = {}

        } else if (class_value.indexOf('loc-btn') > -1) {
            url = $(this).closest('form').attr("action") + '?loc=true'
            type = "GET"
            data = $(this).closest('form').serialize()

        } else if (class_value.indexOf('submit-btn') > -1) {
            
            is_get_table_request_get_parameter = false
            url = $(this).closest('form').attr("action")
            if ($(this).val() == 'EDIT'){
            var  retVal=''
            while(retVal=='' ) {
            retVal = prompt("please give the reason", "");
            
            
            }
            if (retVal ==null) {
                console.log('cancel')
                return false
            }
        }
            
            if (id_closest_wrapper == "manager-modal") {
                if (class_value.indexOf('edit-ntp') > -1) {
                    is_both_table = "both form and table"
                    form_table_template = "normal form template"
                    is_get_table_request_get_parameter = true
                    if (class_value.indexOf('update_all_same_vlan_sites') > -1 ){
                        url = updateURLParameter(url,'update_all_same_vlan_sites','yes')
                    } else {
                        url = updateURLParameter(url,'update_all_same_vlan_sites','no')
                    }
                } else {
                    table_name = $('#modal-on-mll-table').attr('table_name')
                    if (table_name) {
                        is_get_table_request_get_parameter = true
                        closest_wrapper = $('table[name=' + table_name + ']').closest('div.form-table-wrapper')
                    } else {// day la truong hop config ca
                        is_both_table = "form only"
                        is_get_table_request_get_parameter = false
                        is_no_show_return_form = true
                    }
                    hieu_ung_sau_load_form_va_table = "hide modal"
                }
            } else {// submit trong normal form
                is_get_table_request_get_parameter = true
            }
        	  
        	
            //get context cua table 
            if (($(this).val() == 'EDIT' || $(this).val() =='Update to db') && is_both_table != 'form only' && is_get_table_request_get_parameter) {
                

                get_parameter_toggle = ''
                desc_th = closest_wrapper.find('th.desc')
                if (desc_th.length == 0) {
                    asc_th = closest_wrapper.find('th.asc')
                    if (asc_th.length == 0) {
                        href = closest_wrapper.find('.searchtable_header_sort').attr('href')
                    } else {
                        console.log('asc')
                        href = asc_th.find('.searchtable_header_sort').attr('href')
                    }

                } else {
                    console.log('desc')
                    href = desc_th.find('.searchtable_header_sort').attr('href')
                }
                get_question_mark = href.indexOf('?')
                get_parameter = href.substring(get_question_mark + 1)
                get_parameter_toggle = toggleDesAsc(get_parameter)
                console.log('##1', get_parameter)
                console.log('##2', get_parameter_toggle)
                if (url.indexOf('?') > -1) {
                    url = url + get_parameter_toggle
                } else {
                    url = url + '?' + get_parameter_toggle.replace('&', '')
                }
                if (retVal) {
                    url = updateURLParameter(url,'edit_reason',retVal)
                } 

                console.log('##after add edit_reason', url)
            }

            if (table_name) {
                url = updateURLParameter(url, 'table_name', table_name)
            }
            type = "POST"
            data = $(this).closest('form').serialize()

        } else {
            console.log('not yet handle ')
            return false
        }

        url = updateURLParameter(url, 'form-table-template', form_table_template)
        url = updateURLParameter(url, 'which-form-or-table', is_both_table)


        $.ajax({
            type: type,
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {

                switch (form_table_template) {
                    case "normal form template":
                        if (is_both_table == "form only" & !is_no_show_return_form) {
                            formdata = $(data).find('.form-manager_r').html()
                            obj = closest_wrapper.children('.form-manager')
                            assign_and_fadeoutfadein(obj, formdata)
                        } else if (is_both_table == 'table only' || table_name) { //||table_name la truong hop submit modal form chi load lai phai table(gui di yeu cau xu ly form va table, nhung chi muon hien thi table thoi) 
                            tabledata = $(data).find('.table-manager_r').html()
                            obj = closest_wrapper.children('.table-manager')
                            assign_and_fadeoutfadein(obj, tabledata)

                        } else if (is_both_table == "both form and table") {
                            formdata = $(data).find('.form-manager_r').html()
                            obj = closest_wrapper.children('.form-manager')
                            assign_and_fadeoutfadein(obj, formdata)

                            tabledata = $(data).find('.table-manager_r').html()
                            obj = closest_wrapper.children('.table-manager')
                            assign_and_fadeoutfadein(obj, tabledata)
                        }
                        break;
                    case 'form on modal': // chi xay ra trong truong hop click vao link show-modal
                        {
                            formdata = $(data).find('.wrapper-modal').html()
                            $("#modal-on-mll-table").html(formdata)
                            $("#modal-on-mll-table").modal()
                        }
                        break;
                }

                // danh cho hieu ung
                if (hieu_ung_sau_load_form_va_table == 'edit-entry') {
                    var navigationFn = {
                        goToSection: function(id) {
                            $('html, body').animate({
                                scrollTop: $(id).offset().top
                            }, 0);
                        }
                    }
                    navigationFn.goToSection('#' + id_closest_wrapper + ' ' + '.form-manager');
                    return false
                } else if (hieu_ung_sau_load_form_va_table == "hide modal") {
                    $("#modal-on-mll-table").modal("hide")
                } else if (hieu_ung_sau_load_form_va_table == 'add class overflow for table') {
                    console.log('!@#$!@#$2')
                    new_attr = $('#manager-modal').find('.table-manager').attr('class') + ' overflow'
                    $('#manager-modal').find('.table-manager').attr('class', new_attr)
                }

            },
            error: function(request, status, error) {
                if (error == 'FORBIDDEN') { //403
                    alert(request.responseText);
                } else if (error == 'BAD REQUEST') {

                    formdata = $(request.responseText).find('.form-manager_r').html()
                    closest_wrapper.find('.form-manager').html(formdata);
                }

            }

        });
        return false; //ajax thi phai co cai nay. khong thi , gia su click link thi 
    }

    $(this).on('click', '.show-form-modal,select#id_chon_loai_de_quan_ly,.edit-entry-btn-on-table,form#model-manager input[type=submit],.show-modal-form-link,a.show-modal-form-link_allow_edit,a.searchtable_header_sort', form_table_handle)

    $(this).on('submit', '.form-manager', function() {
        return false
    })


    //IMPORTANCE
    //GET FORM
    /*

            $(this).on('click', 'ul.dropdown-menu > li#add-comment,ul.comment-ul > li > a.edit-commnent', function() {
            class_atag = $(this).attr("class")
            that = this
            mll_id = $(this).closest("tr").find('td.id').html()
            url = '/omckv2/handelCommentForMLLForm/'
            comment_id = $(this).attr("comment_id")
            if (!comment_id) {
            comment_id = 'new'
                }
            data = {}
            url = url + comment_id + '/'
            action = url
            url = action + '?selected_instance_mll=' + mll_id //add



            $.get(url, data, function(data) {
                $("#modal-on-mll-table").html(data)
                $("#modal-on-mll-table").find('form#add-comment-form-id').attr('action', action)
                copy_row(that)
                $("#modal-on-mll-table").modal();
            })

            return false;
        })



     // chi con dung cho form commenformllform
        $(this).on('submit', '#add-comment-form-id', function() {
            var clicked_button = $("input[type=submit][clicked=true]").attr("value")
            console.log('clicked_button', clicked_button)
            var url = $(this).attr('action')
            var classname = $(this).attr("class")
            
            if (clicked_button == "ADD NEW") {
                url = url.replace(/\/\d+\//g, '/new/')
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
                    } else if (error == 'BAD REQUEST') { //400 required form, validation form
                        $("#modal-on-mll-table").html(request.responseText)
                        $("#modal-on-mll-table").find('form#add-comment-form-id').attr('action', url)
                    }
                }

            });
            //}
            return false;
        })
    */


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
        var trow = $(this).parent().parent(); //tr
        history_search_id = trow.find('td.id').html()

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

        firstrow.find('td').each(function(i, v) {
            if (array_td_need_edit.indexOf(i) > -1) {
                row.append("<td><input type='text' id='" + $(this).attr("class") + "'/></td>");
            }
        })

        row.append("<img src='media/images/disk.png' class='btnSave'/>");
        firstrow.before(row);
        //$(row).prependTo(tbody);

    })


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
                            //http://stackoverflow.com/questions/314636/how-do-you-select-a-particular-option-in-a-select-element-in-jquery
                        string_to_item = 'select option:contains("' + ui.item.thiet_bi + '") '
                        $('#div_id_thiet_bi').find(string_to_item).attr('selected', 'selected')
                    }

                    form_table_handle(event, 'intended_for_autocomplete', '/omckv2/modelmanager/Table3gForm/' + ui.item.id + '/?table3gid=' + ui.item.id)

                    /*
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
                        */
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

    $('.mySelect2').select2({
        width: '100%'
    });



}); //END READY DOCUMENT




$(document).on('click', "input[type=submit]", function() {
    $("input[type=submit]").removeAttr("clicked");
    $(this).attr("clicked", "true");
});
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
    $('#id_thao_tac_lien_quan,.mySelect2').select2({
        width: '100%'
    });
    $('.selectmultiple').select2({
        width: '100%'
    })

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
    if (datahtml) {

        jqueryobject.fadeOut(300);
        jqueryobject.html(datahtml).fadeIn(300);
    }
};


$(function() {
    PNotify.prototype.options.styling = "bootstrap3";
    new PNotify({
        title: 'Regular Notice',
        text: 'Hello! Have a good day!'
    });
});