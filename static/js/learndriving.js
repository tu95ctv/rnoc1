$(document).ready(function() {

$(this).on('click', '.show-form-modal,select#id_chon_loai_de_quan_ly,.edit-entry-btn-on-table,form#model-manager input[type=submit],.show-modal-form-link,a.show-modal-form-link_allow_edit,a.searchtable_header_sort,.search-botton,.search-manager-botton', form_table_handle)


function form_table_handle(e, intended_for, abitrary_url) {
        class_value = $(this).attr("class")
        loai_ajax = "normal"
        is_no_show_return_form = false
        is_both_table = "both form and table"
        form_table_template = "normal form template"
        hieu_ung_sau_load_form_va_table = "khong hieu ung"
        closest_wrapper = $(this).closest('div.form-table-wrapper')
        id_closest_wrapper = closest_wrapper.attr('id') // no importaince
        console.log('id_closest_wrapper',id_closest_wrapper)
        table_name = '' // table_name dung de xac dinh table , sau khi submit form o modal se hien thi o day, trong truong hop force_allow_edit thi table_name attr se bi xoa 
        if (intended_for == 'intended_for_autocomplete') {
            is_both_table = "both form and table"
            closest_wrapper = $('#form-table-of-tram-info')
            id_closest_wrapper = 'form-table-of-tram-info'
            url = abitrary_url
            type = "GET"
            data = {}
            if (name_attr_global!='subject') {
            hieu_ung_sau_load_form_va_table ='active tram-form-toogle-li'}
            
        }
        else if (intended_for =='intended_for_manager_autocomplete' ){
            is_both_table = "both form and table"
            closest_wrapper = wrapper_attr_global
            url = abitrary_url
            type = "GET"
            data = {}
        } 
        else if (class_value.indexOf('search-botton') > -1){
        var query;
        query = $('#text-search-input').val();
        console.log('####query',query)
        url = "/omckv2/modelmanager/TramForm/new/"
        url = updateURLParameter(url, 'query_main_search_by_button', query)
        is_both_table = 'table only'
        type = "GET"
        data = {}
        hieu_ung_sau_load_form_va_table ='active tram-table-toogle-li'
    }
    else if (class_value.indexOf('search-manager-botton') > -1){
        var query;
        wrapper_attr_global = $(e.target).closest('.form-table-wrapper')
        query = wrapper_attr_global.find('#text-search-input').val().split('3G_');
        console.log('####query',query)
        url = wrapper_attr_global.find('form').attr('action')
        console.log ('####url',url)

        url = updateURLParameter(url, 'query_main_search_by_manager_button', query)
    
        is_both_table = 'table only'
        type = "GET"
        data = {}
    }

        else if (class_value.indexOf('searchtable_header_sort') > -1) {
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
            hieu_ung_sau_load_form_va_table = "show search box"
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
                //tram_id_for_same_ntp de xac dinh table list
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
                            if (id_closest_wrapper=='form-table-of-tram-info') {
                                obj = $('#tram-table')
                            }
                            else {
                            obj = closest_wrapper.children('.table-manager') }
                            assign_and_fadeoutfadein(obj, tabledata)

                        } else if (is_both_table == "both form and table") {
                            formdata = $(data).find('.form-manager_r').html()
                            if (id_closest_wrapper=='form-table-of-tram-info') {
                                obj = $('#tram-form')
                            }
                            else {
                            obj = closest_wrapper.find('.form-manager') }
                            
                            assign_and_fadeoutfadein(obj, formdata) 
           

                            tabledata = $(data).find('.table-manager_r').html()
                            if (id_closest_wrapper=='form-table-of-tram-info') {
                                obj = $('#tram-table')
                            }
                            else {
                            obj = closest_wrapper.children('.table-manager') }
                            assign_and_fadeoutfadein(obj, tabledata)
                            if (intended_for=='intended_for_autocomplete') {
                               table2data = $(data).find('.table-manager_r2').html()
                                obj = $('#mll-form-table-wrapper .table-manager')
                                assign_and_fadeoutfadein(obj, table2data)
                            }
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
                else if (hieu_ung_sau_load_form_va_table == "show search box"){
                    $('#manager #search-manager-group').show()
                }
                else if(hieu_ung_sau_load_form_va_table == 'active tram-form-toogle-li'){
/*
                $('#tram-form-toogle-li').attr("class","active")
                $('#tram-table-toogle-li').attr("class","")
                
                active_elements = $('#form-table-of-tram-info').find('.active')
                console.log('@@@@@ active_elements',active_elements.attr('id'))
                active_elements.removeClass('active')
                $('#tram-table').addClass('active')
                */
                $('#tram-form-toogle-li a').trigger('click')
                //$('#tram-table-toogle-li a').tab('show')
                }

                else if(hieu_ung_sau_load_form_va_table == 'active tram-table-toogle-li'){

                $('#tram-table-toogle-li a').trigger('click')
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
                    if (name_attr_global=="specific_problem_m2m") {
                        this.value = ui.item['label'] + '**'
                    }
                    else {
                    if (ui.item['desc'] == "chưa có sdt" || !ui.item['desc']) {
                        this.value = ui.item['label']
                    } else {
                        this.value = ui.item['label'] + "-" + ui.item['desc'];
                    }
                }//else
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

                    form_table_handle(event, 'intended_for_autocomplete', '/omckv2/modelmanager/TramForm/' + ui.item.id + '/?tramid=' + ui.item.id)
                    return false // return thuoc ve select :
                }

            }) //close autocompltete
    });

    
    $(this).on("focus", ".autocomplete_search_manager", function() {
        $(this).autocomplete({
                create: function() {

                    $(this).data('ui-autocomplete')._renderItem = function(ul, item) {
                        return $(' <li class="abc" ' + 'thietbi="' + item.label + '">')
                            .append("<a>" + '<b>' + item.label + '</b>' + "<br>" + '<span class="std">' + item.desc + '</span>' + "</a>")
                            .appendTo(ul);
                    }
                },
                focus: function(event, ui) {

                    event.preventDefault(); // Prevent the default focus behavior.
                    return false;

                },
                search: function(e, ui) {
                    name_attr_global = $(e.target).attr("name") //name_attr_global de phan biet cai search o top of page or at mllfilter
                    wrapper_attr_global = $(e.target).closest('.form-table-wrapper')
                    model_attr_global = wrapper_attr_global.find('form').attr('action')
                    patt = /\/(\w*?)Form\//i
                    res = patt.exec(model_attr_global)
                    console.log('model_attr_global',res[1])
                    model_attr_global = res[1]
                    //console.log('model_attr_global',model_attr_global)


                },
                source: function(request, response) {

                    console.log('name_attr_global', name_attr_global)
                    var query = extractLast(request.term)
                    $.get('/omckv2/autocomplete/', {
                        query: query,
                        name_attr: name_attr_global,
                        model_attr_global:model_attr_global
                    }, function(data) {
                        response(data['key_for_list_of_item_dict'])
                            //response(projects)
                    })
                },
                select: function(event, ui) {
                    this.value = ui.item['label']
                    form_table_handle(event, 'intended_for_manager_autocomplete', '/omckv2/modelmanager/'+ model_attr_global +'Form/' + ui.item.id + '/?tramid=' + ui.item.id)
                    return false // return thuoc ve select :
                }

            }) //close autocompltete
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
        form = $(this).closest('form')
        var data = form.serialize()
        if (form.find('#id_ntpServerIpAddressPrimary').val()=='' || form.find('#id_ntpServerIpAddress1').val()==''){
            alert('kiem tra lai may cai o trong kia')
            return false
        }
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




    

    $(this).on("click", ".btnEdit", function() {
        var array_td_need_edit = [] //array la chua nhung index cua td can edit
        var par = $(this).parent().parent();
        wrapper_table = $(this).closest('table')
        table_class = wrapper_table.attr("class") //tr
        if (table_class.indexOf('history-table') > -1) {
            array_td_need_edit = [ 4]
        } else if (table_class.indexOf('doi_tac-table') > -1) {
            array_td_need_edit = [1, 2, 3, 4, 5, 6]
        }
        this_rows = par.children('td')
        var total = this_rows.length;
        this_rows.each(function(i, v) {
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
        table = $(this).closest('.table-manager')
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
                table.html(data)
                //$('#history_search').html(data);
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
        table_div = $(this).closest('.table-manager')
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
                        table_div.html(data);
                    });

                return false; //url = '/omckv2/edit_history_search/',
            }
        }

    });


    $('.datetimepicker').datetimepicker({
        format: DT_FORMAT,
    });


    

    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

   
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
var model_attr_global
var name_attr_global
var wrapper_attr_global
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


//$(function() {
    //PNotify.prototype.options.styling = "bootstrap3";
    //new PNotify({
        //title: 'Regular Notice',
        //text: 'Hello! Have a good day!'
    //});
//