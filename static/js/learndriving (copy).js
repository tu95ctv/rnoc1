//abc
$(document).ready(function() {
    //.show-form-modal
    $(this).on('click', 'a.manager-a-form-select-link,select#id_chon_loai_de_quan_ly,.edit-entry-btn-on-table,form#model-manager input[type=submit],.show-modal-form-link,a.show-modal-form-link_allow_edit,a.searchtable_header_sort,.search-botton,.search-manager-botton', form_table_handle)


    function form_table_handle(e, intended_for, abitrary_url, sort_field) {

        class_value = $(this).attr("class")
        loai_ajax = "normal"
        is_no_show_return_form = false
            //is_both_table = "both form and table"
        is_table = true
        is_form = true
        form_table_template = "normal form template" //'form on modal'
        hieu_ung_sau_load_form_va_table = "khong hieu ung"
        closest_wrapper = $(this).closest('div.form-table-wrapper')
        id_closest_wrapper = closest_wrapper.attr('id') // no importaince
        console.log('id_closest_wrapper', id_closest_wrapper)
        var table_object
        console.log('@@@@@@@@@table_object', table_object)
            //table_name = '' // table_name dung de xac dinh table , sau khi submit form o modal se hien thi o day, trong truong hop force_allow_edit thi table_name attr se bi xoa 
        if (intended_for == 'intended_for_autocomplete') {
            //is_both_table = "both form and table"
            is_table = true
            is_form = true
            closest_wrapper = $('#form-table-of-tram-info')
            id_closest_wrapper = 'form-table-of-tram-info'
            url = abitrary_url
            type = "GET"
            data = {}

            console.log("$('input#id_khong_search_tu_dong').prop('checked')", $('input#id_khong_search_tu_dong').prop('checked'))
            if ($('input#id_khong_search_tu_dong').prop('checked')) {
                url = updateURLParameter(url, 'search_tu_dong_table_mll', 'no')
            } else {
                url = updateURLParameter(url, 'search_tu_dong_table_mll', 'yes')
            }

            if (name_attr_global != 'object') {

                hieu_ung_sau_load_form_va_table = 'active tram-form-toogle-li'
            }
            console.log('sort_field', sort_field)
            if (sort_field == 'SN1' || sort_field == 'SN2') {
                hieu_ung_sau_load_form_va_table = 'active thong-tin-tram toogle'
            } else if (sort_field == '3G') {
                hieu_ung_sau_load_form_va_table = 'active thong-tin-3g toogle'
            } else if (sort_field == '2G') {
                hieu_ung_sau_load_form_va_table = 'active thong-tin-2g toogle'
            } else if (sort_field == '4G') {
                hieu_ung_sau_load_form_va_table = 'active thong-tin-4g toogle'
            }

        } else if (intended_for == 'intended_for_manager_autocomplete') {
            is_both_table = "both form and table"
            is_table = true
            is_form = true
            closest_wrapper = wrapper_attr_global
            url = abitrary_url
            type = "GET"
            data = {}
        } else if (class_value.indexOf('search-botton') > -1) {
            var query;
            query = $('#text-search-input').val();
            url = "/omckv2/modelmanager/TramForm/new/"
            url = updateURLParameter(url, 'query_main_search_by_button', query)
            is_both_table = 'table only'
            type = "GET"
            data = {}
            hieu_ung_sau_load_form_va_table = 'active tram-table-toogle-li'
            if (id_closest_wrapper = 'form-table-of-tram-info_dang_le_ra') {
                closest_wrapper = $('#form-table-of-tram-info')
                id_closest_wrapper = closest_wrapper.attr('id') // no importaince
            }
        } else if (class_value.indexOf('search-manager-botton') > -1) {
            var query;
            wrapper_attr_global = $(e.target).closest('.form-table-wrapper')
            query = wrapper_attr_global.find('#text-search-input').val().split('3G_');
            url = wrapper_attr_global.find('form').attr('action')
            url = updateURLParameter(url, 'query_main_search_by_button', query)

            is_both_table = 'table only'
            type = "GET"
            data = {}
        } else if (class_value.indexOf('searchtable_header_sort') > -1) {
            is_table = true
            is_form = false
            is_both_table = 'table only'
            url = $(this).attr('href')
            if (id_closest_wrapper == 'edit-history-wrapper-div') {
                console.log('$(this)', $(this).attr('class'))
                closest_i_want = $(this).closest('div#form-table-of-tram-info')
                console.log('closest_i_want', closest_i_want)
                console.log('0closest_i_want', closest_i_want.attr('id'))
                if (closest_i_want.attr('id')!='form-table-of-tram-info') {
                    closest_i_want = $(this).closest('div#mll-form-table-wrapper')
                    console.log('2closest_i_want', closest_i_want)
                    if (closest_i_want.attr('id')!='mll-form-table-wrapper') {
                        return false
                    } else {
                        console.log('3closest_i_want', closest_i_want.attr('id'))
                        url = updateURLParameter(url, 'model_name', 'Mll')
                        tram_id = closest_i_want.find('#id_id').val()
                        console.log('tram_id', tram_id)
                    }
                } else {
                    url = updateURLParameter(url, 'model_name', 'Tram')
                    tram_id = $('#form-table-of-tram-info').find('#id_id').val()
                    console.log('tram_id', tram_id)
                }
                url = updateURLParameter(url, 'edited_object_id', tram_id)
                url  = removeParam ('tramid',url)
                //url = url.replace(/&?tramid=([^&]$|[^&]*?&)/i, "")
                console.log('###########url new', url)
            }
            type = "GET"
            data = {}
        } else if (class_value.indexOf('edit-entry-btn-on-table') > -1) {
            is_both_table = "form only"
            is_table = false
            is_form = true
            url = closest_wrapper.find('form#model-manager').attr('action')
            entry_id = $(this).attr('id')
            url = url.replace(/\/\w+\/$/g, '/' + entry_id + '/')
            console.log('url', url)

            if (id_closest_wrapper == 'form-table-of-tram-info') {
                hieu_ung_sau_load_form_va_table = 'active tram-form-toogle-li'
            } else {
                hieu_ung_sau_load_form_va_table = "edit-entry"

            }
            type = "GET"
            data = {}


        } else if (class_value.indexOf('manager-form-select') > -1) {
            is_table = true
            is_form = true
                //url = $('#id_chon_loai_de_quan_ly option:selected').val()
            url = $(this).val() //url = new va method = get
            type = "GET"
            data = {}
            hieu_ung_sau_load_form_va_table = "show search box"

            /*
             var editor = CKEDITOR.instances['id_ghi_chu'];
    if (editor) { //alert('instance exists');
        editor.destroy(true); 
        //alert('destroyed'); 
    }
    CKEDITOR.replace('id_ghi_chu');
    */

        } else if (class_value.indexOf('manager-a-form-select-link') > -1) {
            is_table = true
            is_form = true
            url = $(this).attr('href')
            console.log('@@@@@@@@@@ndt', url)
            type = "GET"
            data = {}
            hieu_ung_sau_load_form_va_table = "show search box 2"

        } else if (class_value.indexOf('show-modal-form-link') > -1) {
            is_table = false
            url = $(this).attr("href") ///omckv2/show-modal-form-link/ThietBiForm/1/
            form_table_template = 'form on modal'
            table_name = $(this).closest('table').attr('name')
            if (table_name) {
                $('#modal-on-mll-table').attr('table_name', table_name)
            } else {
                $('#modal-on-mll-table').removeAttr('table_name')
            }
            type = "GET"
            data = {}

            if (class_value.indexOf('add-comment') > -1 || class_value.indexOf('Nhan-Tin-UngCuu') > -1) {
                mll_id = $(this).closest("tr").find('td.id').html()
                url = updateURLParameter(url, 'selected_instance_mll', mll_id)
            } else if (class_value.indexOf('force_allow_edit') > -1) {
                url = updateURLParameter(url, 'force_allow_edit', 'True')
                $('#modal-on-mll-table').removeAttr('table_name')
            } else if (class_value.indexOf('downloadscript') > -1) {
                //is_both_table = "both form and table"
                is_table = true
                tram_id = $(this).closest('form').find('input[name=id]').val()
                console.log('tram_id', tram_id)
                url = updateURLParameter(url, 'tram_id_for_same_ntp', tram_id)
                    //tram_id_for_same_ntp de xac dinh table list
                hieu_ung_sau_load_form_va_table = 'add class overflow for table'
                console.log('!@#$!@#$1')
            }
        } else if (class_value.indexOf('cancel-btn') > -1) { //cancle buton duoc nhan.
            is_table = true
            is_form = true
            url = $(this).closest('form').attr("action").replace(/\/\d+\//g, '/new/')
            type = "GET"
            data = {}

        } else if (class_value.indexOf('loc-btn') > -1) {
            is_table = true
            is_form = true
            url = $(this).closest('form').attr("action") + '?loc=true'
            type = "GET"
            data = $(this).closest('form').serialize()

        } else if (class_value.indexOf('submit-btn') > -1) { // ca truong hop add and edit
            url = $(this).closest('form').attr("action")
            if ($(this).val() == 'EDIT' || $(this).val() == 'Update to db') {
                var retVal = ''
                while (retVal == '') {
                    retVal = prompt("please give the reason", "");

                }
                if (retVal == null) {
                    return false
                }
            }

            if (id_closest_wrapper == "manager-modal") {

                table_name = $('#modal-on-mll-table').attr('table_name')
                console.log('table_name##############333', table_name)
                    //khi submit
                if (table_name) { // mac du add new commnent hay la edit trang_thai, hay thiet bi thi cung phai is_get_table_request_get_parameter = true
                    is_get_table_request_get_parameter = true
                    table_object = $('table[name=' + table_name + ']').closest('div.table-manager')
                    url = updateURLParameter(url, 'table_name', table_name)
                        //url = updateURLParameter(url, 'khong_show_2_nut_cancel_va_loc', 'yes')
                    is_both_table = "both form and table"
                    is_table = true
                    is_form = true
                    if (url.indexOf('CommentForm') > -1 && $(this).val() == 'ADD NEW') {
                        hieu_ung_sau_load_form_va_table = "change style for add comment to edit comment"
                            //console.log('@@@@@@@@ADFASDFASDFDFDSFD')
                    }
                } else {

                    if (class_value.indexOf('edit-ntp') > -1) {
                        is_get_table_request_get_parameter = true
                        is_both_table = "both form and table"
                        is_table = true
                        is_form = true
                        url = updateURLParameter(url, 'update_all_same_vlan_sites', 'no')
                        url = removeParam('update_all_same_vlan_sites',url)
                        console.log('@@@@@@@@@@@@@@@ editntp',url)
                    } else if (class_value.indexOf('update_all_same_vlan_sites') > -1) {
                        url = updateURLParameter(url, 'update_all_same_vlan_sites', 'yes')
                        is_get_table_request_get_parameter = true
                        is_both_table = "both form and table"
                        is_table = true
                        is_form = true
                     
                    } else { // truong hop config ca
                        //is_both_table = "form only"

                        is_table = false
                        is_form = true
                        is_get_table_request_get_parameter = false
                            //is_no_show_return_form = true
                            //hieu_ung_sau_load_form_va_table = "hide modal"
                        hieu_ung_sau_load_form_va_table = "update ca truc info"
                    }
                }


            } else { // submit trong normal form
                is_table = true
                is_form = true
                url = $(this).closest('form').attr("action")

                if ($(this).val() == 'EDIT') {
                    is_get_table_request_get_parameter = true
                } else {
                    is_get_table_request_get_parameter = false
                }
            }


            //get context cua table 
            if (is_get_table_request_get_parameter) {

                get_parameter_toggle = ''
                var table_contain_div
                if (table_object) {
                    table_contain_div = table_object
                } else {
                    if (id_closest_wrapper == 'form-table-of-tram-info') {
                                table_contain_div = $('#tram-table')

                    } else {
                                table_contain_div = closest_wrapper
                            }
                    

                }
                console.log('table_contain_div',table_contain_div.attr('class'))
                desc_th = table_contain_div.find('th.desc:first')
                if (desc_th.length == 0) {
                    asc_th = table_contain_div.find('th.asc:first')
                    if (asc_th.length == 0) {
                        href = table_contain_div.find('.searchtable_header_sort:first').attr('href')
                        console.log('khong co asc hoac desc o table')
                    } else {
                        href = asc_th.find('.searchtable_header_sort').attr('href')
                        console.log('co asc class o table',asc_th.length,asc_th.attr('class'))
                    }

                } else {
                    console.log('co desc class o table',desc_th.length,desc_th.attr('class'),desc_th,desc_th.outerHTML)
                    href = desc_th.find('a').attr('href')
                }
                get_question_mark = href.indexOf('?')
                get_parameter = href.substring(get_question_mark + 1)
                console.log('FFFFFFFFFFFFFFhref',href)
                console.log('FFFFFFFFFFFFFFget_parameter',get_parameter)
                get_parameter_toggle = toggleDesAsc(get_parameter)
                console.log('@@@@@@@get_parameter_toggle', get_parameter_toggle)
                if (url.indexOf('?') > -1) {
                    url = url + get_parameter_toggle
                } else {
                    url = url + '?' + get_parameter_toggle.replace('&', '')
                    console.log('@@@@@@@url', url)
                }
                if (retVal) {
                    url = updateURLParameter(url, 'edit_reason', retVal)
                }

                console.log('##after add edit_reason', url)

                if (!table_object) {
                    url  = removeParam ('table_name',url)
                    //url = url.replace(/&?table_name=([^&]$|[^&]*)/i, "")
                    console.log('url new', url)

                    //url2 = url.replace(/&khong_show_2_nut_cancel_va_loc=([^&]$|[^&]*)/i, "")
                    //console.log('url 2',url2)
                }

            }


            type = "POST"
            for (instance in CKEDITOR.instances) {
                CKEDITOR.instances[instance].updateElement();
            }
            data = $(this).closest('form').serialize()

        } else {
            console.log('not yet handle ')
            return false
        }

        url = updateURLParameter(url, 'form-table-template', form_table_template)
        url = updateURLParameter(url, 'is_form', is_form)
        url = updateURLParameter(url, 'is_table', is_table)
            //url = updateURLParameter(url, 'which-form-or-table', is_both_table)
        if (id_closest_wrapper == 'mll-form-table-wrapper') {
            loc_cas = $('select[name="loc-ca"]').val()
            if (loc_cas) {
                newpara = loc_cas.join("d4");

            } else {
                newpara = "None"


            }
            url = updateURLParameter(url, 'loc-ca', newpara)
        }


        $.ajax({
            type: type,
            url: url,
            data: data, // serializes the form's elements.
            success: function(data) {

                switch (form_table_template) {
                    case "normal form template":

                        if (is_form & !is_no_show_return_form) {
                            formdata = $(data).find('.form-manager_r').html()
                            if (id_closest_wrapper == 'form-table-of-tram-info') {
                                obj = $('#tram-form')

                            } else {
                                obj = closest_wrapper.children('.form-manager')
                            }
                            assign_and_fadeoutfadein(obj, formdata)
                            show_map_from_longlat()
                        }

                        if (is_table) { //||table_name la truong hop submit modal form chi load lai phai table(gui di yeu cau xu ly form va table, nhung chi muon hien thi table thoi) 
                            tabledata = $(data).find('.table-manager_r').html()
                            if (id_closest_wrapper == 'form-table-of-tram-info') {
                                obj = $('#tram-table')
                            } else if (table_object) {
                                obj = table_object
                            } else {
                                obj = closest_wrapper.children('.table-manager')
                            }
                            assign_and_fadeoutfadein(obj, tabledata)
                            if (intended_for == 'intended_for_autocomplete' && !$('input#id_khong_search_tu_dong').prop('checked')) {
                                table2data = $(data).find('.table-manager_r2').html()
                                obj = $('div#mll-form-table-wrapper > div.table-manager')
                                assign_and_fadeoutfadein(obj, table2data)

                            }
                        }

                        /*else if (is_both_table == "both form and table") {
                            console.log('url', url)
                            formdata = $(data).find('.form-manager_r').html()
                            if (id_closest_wrapper == 'form-table-of-tram-info') {
                                obj = $('#tram-form')

                            } else {
                                obj = closest_wrapper.children('.form-manager')
                            }

                            assign_and_fadeoutfadein(obj, formdata)
                            show_map_from_longlat()
                            tabledata = $(data).find('.table-manager_r').html()


                            if (id_closest_wrapper == 'form-table-of-tram-info') {
                                obj = $('#tram-table')
                            } else if (table_object) {
                                obj = table_object
                            } else {
                                obj = closest_wrapper.children('.table-manager')
                            }
                            assign_and_fadeoutfadein(obj, tabledata)
                            
                        }*/
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
                } else if (hieu_ung_sau_load_form_va_table == "show search box") {
                    $('#manager #search-manager-group').show()
                } else if (hieu_ung_sau_load_form_va_table == "show search box 2") {
                    $('#manager #search-manager-group').show()
                    $("#dropdown-toggle-manager").dropdown("toggle");
                } else if (hieu_ung_sau_load_form_va_table == 'active tram-form-toogle-li') {

                    $('#tram-form-toogle-li a').trigger('click')

                } else if (hieu_ung_sau_load_form_va_table == 'active tram-table-toogle-li') {

                    $('#tram-table-toogle-li a').trigger('click')
                } else if (hieu_ung_sau_load_form_va_table == 'active thong-tin-tram toogle') {
                    $('#tram-form-toogle-li a').trigger('click')
                    $('a[href="#thong-tin-tram"]').trigger('click')
                } else if (hieu_ung_sau_load_form_va_table == 'active thong-tin-3g toogle') {
                    $('#tram-form-toogle-li a').trigger('click')
                    $('a[href="#thong-tin-3g"]').trigger('click')
                } else if (hieu_ung_sau_load_form_va_table == 'active thong-tin-2g toogle') {
                    $('#tram-form-toogle-li a').trigger('click')
                    $('a[href="#thong-tin-2g"]').trigger('click')
                } else if (hieu_ung_sau_load_form_va_table == 'active thong-tin-4g toogle') {
                    $('#tram-form-toogle-li a').trigger('click')
                    $('a[href="#thong-tin-4g"]').trigger('click')

                } else if (hieu_ung_sau_load_form_va_table == "update ca truc info") {
                    ca_moi_chon = closest_wrapper.find('select#id_ca_truc option:selected').html()
                    console.log('@@@@ca_moi_chon', ca_moi_chon)
                    $('span#ca-dang-truc').html('Ca ' + ca_moi_chon)
                } else if (hieu_ung_sau_load_form_va_table == "change style for add comment to edit comment") {
                    dtuong = $('#modal-on-mll-table h4.add-comment-modal-title')
                    console.log('@@@@@@@@@@@', dtuong.attr('class'))
                    dtuong.css("background-color", "#ec971f")
                        //dtuong.attr('style',"background-color:#ec971f")
                }

            },
            error: function(request, status, error) {
                if (error == 'FORBIDDEN') { //403
                    console.log(request.responseText)
                    data = $(request.responseText).find('#info_for_alert_box').html()
                    alert(data);
                } else if (error == 'BAD REQUEST') {
                    formdata = $(request.responseText).find('.form-manager_r').html()
                    closest_wrapper.find('.form-manager').html(formdata);

                }

            }

        });
        return false; //ajax thi phai co cai nay. khong thi , gia su click link thi 
    }
    $(this).on('click', '#submit-id-copy-tin-nhan', function() {
        //copyToClipboard($('#id_noi_dung_tin_nhan'))
        copyToClipboard(document.getElementById("id_noi_dung_tin_nhan"));
        return false
    })

    function copyToClipboard(elem) {
        // create hidden text element, if it doesn't already exist
        var targetId = "_hiddenCopyText_";
        var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
        var origSelectionStart, origSelectionEnd;
        if (isInput) {
            // can just use the original source element for the selection and copy
            target = elem;
            origSelectionStart = elem.selectionStart;
            origSelectionEnd = elem.selectionEnd;
        } else {
            // must use a temporary form element for the selection and copy
            target = document.getElementById(targetId);
            if (!target) {
                var target = document.createElement("textarea");
                target.style.position = "absolute";
                target.style.left = "-9999px";
                target.style.top = "0";
                target.id = targetId;
                document.body.appendChild(target);
            }
            target.textContent = elem.textContent;
        }
        // select the content
        var currentFocus = document.activeElement;
        target.focus();
        target.setSelectionRange(0, target.value.length);

        // copy the selection
        var succeed;
        try {
            succeed = document.execCommand("copy");
        } catch (e) {
            succeed = false;
        }
        // restore original focus
        if (currentFocus && typeof currentFocus.focus === "function") {
            currentFocus.focus();
        }

        if (isInput) {
            // restore prior selection
            elem.setSelectionRange(origSelectionStart, origSelectionEnd);
        } else {
            // clear temporary content
            target.textContent = "";
        }
        return succeed;
    }

    var obj_autocomplete = {
        create: function() {

            $(this).data('ui-autocomplete')._renderItem = function(ul, item) {
                return $(' <li class="abc" ' + 'thietbi="' + item.label + '">')
                    .append("<a>" + '<b>' + item.label + '</b>' + "<br>" + '<span class="std">' + item.desc + '</span>' + "</a>")
                    .appendTo(ul);
            }
        },

        search: function(e, ui) {
            console.log('dang search')
            showloading = false
            name_attr_global = $(e.target).attr("name")

        },

        source: function(request, response) {

            console.log('name_attr_global', name_attr_global)
            query = request.term
            $.get('/omckv2/autocomplete/', {
                query: query,
                name_attr: name_attr_global
            }, function(data) {

                return_data = data['key_for_list_of_item_dict']


                if (name_attr_global == "doi_tac" || name_attr_global == "nguyen_nhan" || name_attr_global == "du_an" || name_attr_global == "su_co" || name_attr_global == "thiet_bi" || name_attr_global == "trang_thai")

                {
                    if (data['dau_hieu_co_add']) {
                        $('#div_id_' + name_attr_global + ' .glyphicon-plus').show()
                    } else {
                        $('#div_id_' + name_attr_global + ' .glyphicon-plus').hide()
                    }
                } else if (name_attr_global == "thao_tac_lien_quan")

                {
                    is_curent_add = data['curent_add']
                    number_dau_hieu_co_add = data['dau_hieu_co_add'] //0,1,2
                    if (number_dau_hieu_co_add) {
                        document.styleSheets[0].addRule('#div_id_' + name_attr_global + ' .glyphicon-plus:before', 'content: "+ ' + number_dau_hieu_co_add + '"');
                        $('#div_id_' + name_attr_global + ' .glyphicon-plus').show()
                    } else {
                        $('#div_id_' + name_attr_global + ' .glyphicon-plus').hide()
                    }
                }

                response(return_data)
            })
        },
        select: function(event, ui) {
            if (name_attr_global == "specific_problem_m2m") {
                this.value = ui.item['label'] + '**'
            } else if (name_attr_global == "doi_tac") {
                $('#div_id_' + name_attr_global + ' .glyphicon-plus').hide()
                if (ui.item['desc'] == "chưa có sdt" || !ui.item['desc']) {
                    this.value = ui.item['label']
                } else {
                    this.value = ui.item['label'] + "-" + ui.item['desc'];
                }
            } else if (name_attr_global == 'thao_tac_lien_quan') {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item['label']);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(", ");
                x = number_dau_hieu_co_add - is_curent_add
                if (x) {
                    document.styleSheets[0].addRule('#div_id_' + name_attr_global + ' .glyphicon-plus:before', 'content: "+ ' + x + '"');
                    $('#div_id_' + name_attr_global + ' .glyphicon-plus').show()
                } else {
                    $('#div_id_' + name_attr_global + ' .glyphicon-plus').hide()
                }

            } else {
                if (name_attr_global == 'nguyen_nhan' || name_attr_global == 'du_an' || name_attr_global == 'su_co' || name_attr_global == "thiet_bi" || name_attr_global == "trang_thai") {

                    $('#div_id_' + name_attr_global + ' .glyphicon-plus').hide()
                }

                this.value = ui.item['label']
            }
            return false
        }

    }

    $(this).on("focus", ".autocomplete", function() {
        if (!$(this).data("autocomplete"))

        {
            $(this).autocomplete(obj_autocomplete)
        }
    });

    $(this).on('click', ".autocomplete", function() {
        value = $(this).val()
        if (value.length === 0) {
            value = 'tatca'

        }
        $(this).autocomplete("search", value)

    });
    $(this).on("keyup", ".autocomplete", function() {
        if ($(this).val().length === 0) {
            $('#div_id_' + name_attr_global + ' .glyphicon-plus').hide()
        }
    });


    // $('.autocomplete').autocomplete(obj_autocomplete) //close autocompltete




    $(this).on("focus", ".autocomplete_search_tram", function() {
        $(this).autocomplete({
                create: function() {
                    $(this).data('ui-autocomplete')._renderItem = function(ul, item) {
                        return $('<li>').append(
                                $('<div>').append('<b>' + '<span class="greencolor">' + item.sort_field + ":</span>" + '<span class="">' + item.label + '</span>' + '</b>')
                                .append('<div class="table-type-wrapper">'

                                    +
                                    '<div  class="wrapper-a-tr"><div class="wrapper-dt-autocomplete" >' + '<span class="tram_field_name">SN1: </span>' + '<span class="chontram" type-tram = "SN1" type-thiet-bi = "2G&3G">' + item.sn1 + '</span>' + '</div>' + '<div class="wrapper-dt-autocomplete" >' + '<span class="tram_field_name">SN2: </span>' + '<span class="chontram" type-tram = "SN2" type-thiet-bi = "2G&3G">' + item.sn2 + '</span>' + '</div></div>' +
                                    '<div class="wrapper-a-tr"><div class="wrapper-dt-autocomplete" >' + '<span class="tram_field_name">3G: </span>' + '<span class="chontram" type-tram = "3G" type-thiet-bi = "' + item.s3g_thietbi + '">' + item.s3g + '</span>' + '</div>' + '<div class="wrapper-dt-autocomplete" >' + '<span class="tram_field_name">2G: </span>' + '<span class="chontram" type-tram = "2G" type-thiet-bi  = "' + item.s2g_thietbi + '">' + item.s2g + '</span>' + '</div></div>' +
                                    '<div class="wrapper-a-tr"><div class="wrapper-dt-autocomplete" >' + '<span class="tram_field_name">4G: </span>' + '<span class="chontram" type-tram = "4G" type-thiet-bi = "' + item.s4g_thietbi + '">' + item.s4g + '</span>' + '</div></div>' +
                                    '</div>'))
                            .appendTo(ul)


                    }
                },
                focus: function(event, ui) {

                    event.preventDefault(); // Prevent the default focus behavior.
                    return false;

                },
                search: function(e, ui) {
                    showloading = false
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
                        return_data = data['key_for_list_of_item_dict']
                        response(return_data)

                    })
                },
                select: function(event, ui) {

                    if ($(event.toElement).attr('class') == 'chontram') {
                        sort_field = $(event.toElement).attr('type-tram')
                        thiet_bi = $(event.toElement).attr('type-thiet-bi')
                        value_select = event.toElement.innerText

                    } else {
                        sort_field = ui.item.sort_field
                        value_select = ui.item['label']
                        thiet_bi = ui.item.thiet_bi
                    }




                    if (name_attr_global == "object") {
                        var terms = split(this.value);
                        // remove the current input
                        terms.pop();
                        // add the selected item
                        terms.push(value_select);
                        // add placeholder to get the comma-and-space at the end
                        terms.push("");
                        this.value = terms.join(", ");
                    } else {
                        this.value = value_select; //this.value tuc la gia tri hien thi trong input text
                    }


                    if (name_attr_global == "object") {
                        $('#id_site_name').val(ui.item.site_name_1)
                            //http://stackoverflow.com/questions/314636/how-do-you-select-a-particular-option-in-a-select-element-in-jquery
                        string_to_item = 'select option:contains("' + thiet_bi + '") '
                        $('#div_id_thiet_bi').find(string_to_item).attr('selected', 'selected')
                    }

                    form_table_handle(event, 'intended_for_autocomplete', '/omckv2/modelmanager/TramForm/' + ui.item.id + '/?tramid=' + ui.item.id, sort_field)

                    return false // return thuoc ve select :
                }

            }) //close autocompltete
    });


    $(this).on("focus", ".autocomplete_search_manager", function(e) {
        $(this).autocomplete({
                create: function() {
                    console.log('khi nang', $(e.target).attr('class').split(' ').indexOf('autocomplete_search_manager'))

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
                    console.log('model_attr_global', res[1])
                    model_attr_global = res[1]
                        //console.log('model_attr_global',model_attr_global)


                },
                source: function(request, response) {

                    console.log('name_attr_global', name_attr_global)
                    var query = extractLast(request.term)
                    $.get('/omckv2/autocomplete/', {
                        query: query,
                        name_attr: name_attr_global,
                        model_attr_global: model_attr_global
                    }, function(data) {
                        response(data['key_for_list_of_item_dict'])
                            //response(projects)
                    })
                },
                select: function(event, ui) {
                    this.value = ui.item['label']
                    form_table_handle(event, 'intended_for_manager_autocomplete', '/omckv2/modelmanager/' + model_attr_global + 'Form/' + ui.item.id + '/?tramid=' + ui.item.id)

                    return false // return thuoc ve select :
                }

            }) //close autocompltete
    });




    var counter = 0;
    $(this).on('click', 'table.lenh-table > tbody >tr >td.selection>input[type=checkbox] ', function() {
        chosing_row_id = $(this).closest("tr").find('td.id').html()
        console.log('chosing_row_id', chosing_row_id, $(this).is(':checked'))
        is_check = !$(this).is(':checked')
        if (false) { /* bo chon 1 row*/
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
            $(this).prop("checked", true)
            counter = counter + 1

            var newrowcopy = $('<tr>');


            $(this).closest("tr").children().each(function(i, v) {
                if (!$(this).hasClass("selection") && i < 6) { /*BO CHON NHUNG CAI SELECTION*/
                    var thishtml = $(this).prop('outerHTML') //cu
                    newrowcopy.append(thishtml)

                }
            });

            comment = $(this).closest('tr').find('td.command').html()

            var reg = /\[(thamso.*?)\]/g;
            var matches_thamso_attribute_sets = []
            var found
            while (found = reg.exec(comment)) {
                console.log('found.index', found.index, 'found', found, '\nreg.lastIndex', reg.lastIndex)
                matches_thamso_attribute_sets.push(found[1]);
                reg.lastIndex = found.index + 1;

            }


            newtd = $('<td>')
            $.each(matches_thamso_attribute_sets, function(index, thamso_name) {
                newtd.append($('<p>').html(thamso_name))
                newtd.append($('<input/>').attr({
                    type: 'text',
                    id: thamso_name
                }))

            })
            if (comment.indexOf('[TG]') > -1) {
                newtd.append($('<p>').html('chon TG 1800'))
                newtd.append($('<input/>').attr({
                    type: 'checkbox',
                    class: "chon-TG-1800"
                }))
            }
            newtd.append('<div><input type="button" class="ibtnDel"  value="Delete"><input type="button" class="move up"  value="Up"><input type="button" class="move down"  value="Down"></div></td>')
            newrowcopy.append(newtd);

            /*
            th.add($('th').append('delete'))
            var thead = $('thead')
            thead.append($('tr').append(th))
            */
            /*
            var tbody = $('tbody')
            tbody.append(newRow)
            var table = $('table')
            table.append(tbody)
            */
            $("table#myTable>tbody").append(newrowcopy)
            choosed_command_array_global.push(chosing_row_id)
            console.log(choosed_command_array_global)
        }

    });



    $("table#myTable").on("click", ".ibtnDel", function(event) {
        is_ton_tai_them_1_tr_id = false
        tr_id = $(this).closest("tr").find('td.id').html()
        $(this).closest("tr").remove();

        $("table#myTable").find('tbody tr td.id').each(function() {
            if (this.html() == tr_id) {
                is_ton_tai_them_1_tr_id = true
            }

        })
        if (!is_ton_tai_them_1_tr_id) {
            $('table.lenh-table').find('tr td  input[value =' + tr_id + ']').attr('checked', false)
            counter -= 1
        }
    });




    $(this).on('click', '.generate-command', function() {
        var command_set_many_tram = "";
        $('.tram-table > tbody > tr').each(function() {
            var command_set_one_tram = "";
            var tram_row = $(this)


            $('#myTable > tbody > tr').each(function() {
                tr = $(this)
                var one_command = $(this).find('td.command').html();
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
                    console.log('tram_attribute 2', tram_attribute)
                    if (tram_attribute == 'Site ID 3G') {
                        value = value.replace(/^ERI_3G_/g, '')
                    } else if (tram_attribute == 'Site ID 2G') {
                        console.log('i want see............')
                        value = value.replace(/^SRN_2G_/g, '')
                    } else if (tram_attribute.indexOf('thamso') > -1) {
                        value = tr.find('input#' + tram_attribute).val()
                    } else if (tram_attribute == 'TG') {

                        is_check = tr.find('input.chon-TG-1800')
                        console.log('i want seeaaaaaaaaaaaaaaaaa', is_check)
                        is_check = is_check.is(":checked")
                        if (is_check) {
                            console.log('i want seeaaaaaaaaaaaaaaaaa2222222222', is_check)
                            value = tram_row.find('td.' + 'TG_1800').html()
                        }
                    }
                    one_command = one_command.replace('[' + tram_attribute + ']', value)
                });
                command_set_one_tram += one_command + '\n\n\n'
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

    $(this).on('click', 'table#myTable tbody tr td input.move', function() {
        var row = $(this).closest('tr');
        console.log('rowwwwwwwwwwwwww', row)
        if ($(this).hasClass('up'))
            row.prev().before(row);
        else
            row.next().after(row);
    });

    $(this).on('click', '.link_to_download_scipt', function() {
        console.log('button ok')
        form = $(this).closest('form')
        var data = form.serialize()
        if (form.find('#id_ntpServerIpAddressPrimary').val() == '' || form.find('#id_ntpServerIpAddress1').val() == '') {
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
            array_td_need_edit = [4]
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


    $(this).on('click', 'a[href="#location"]', function() {
        console.log('okkkkkkkkkkkkkkkkkk')
        googlemap1_html = $('#bando-wrapper').html()
        $('#wrapper-ban-do').html(googlemap1_html)
        $('#wrapper-ban-do #googleMap').attr('new', 'khac-di').css("width", "600px").css("height", "456px")
    })


    $('.datetimepicker').datetimepicker({
        format: DT_FORMAT,
    });


    $('.datetimepicker_only_date').datetimepicker({
        viewMode: 'days',
        format: DATE_FORMAT,
    });

    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }
    /* 
       
     $('.selectmultiple').select2({
         width: '100%'
     }) */
    //$(".tablemll").colResizable();

    $('.mySelect2').select2({
        width: '100%'
    });
    $('.selectmultiple').select2({
        width: '100%'
    })

    $('#modal-on-mll-table').on('hidden.bs.modal', function(e) {
        // do something...
        $(this).empty()
    })


    $(this).on('click', '#replace-carrier-return', function() {

        value = $('#mll-form-table-wrapper #id_specific_problem_m2m').val().replace('\n', '')
        console.log('iloveyuou', value)
        $('#mll-form-table-wrapper #id_specific_problem_m2m').val(value)
    })

/*    
array = ['.history-table','#mll-table-id']
$(array).each(function(i,v){    
$(v).find('tbody tr:first td').each(function(){
    console.log(v,$(this).attr('class'),$(this).width())
})
$(v).find('thead tr:first th').each(function(){
    console.log(v,'thead',$(this).attr('class'),$(this).width())
})
})
var newTbl = $('#mll-table-id').clone();

        // remove table header from original table
newTbl.find('tbody').remove();  
$('#table-manager_phu').html(newTbl)
//scrolify($('.tablemll'), 560); // 160 is height    
//$('.table-manager #mll-table-id').find('thead').remove();  

$('.table-manager #mll-table-id').find('thead tr th').each(function(){
     $(this).html('')
 })
*/
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

    $('.datetimepicker_only_date').datetimepicker({
        viewMode: 'days',
        format: DATE_FORMAT,
    });
    $('.mySelect2').select2({
        width: '100%'
    });
    $('.selectmultiple').select2({
        width: '100%'
    })

});
$(function() {
    $(".comboboxd4").combobox();

});
showloading = true
$(document).on("ajaxStart", function() {
    if (showloading == true) {
        $("#loading").show();
    }
    showloading = true


}).on("ajaxComplete", function() {
    /*
    var editor = CKEDITOR.instances['id_ghi_chu'];
    if (editor) { editor.destroy(true); 
    CKEDITOR.replace('id_ghi_chu');}
    */
    $("#loading").hide();

});

$("#loading").hide();

var choosed_command_array_global = []
$('#submit-id-command-cancel').hide()
var model_attr_global
var name_attr_global
var wrapper_attr_global
var DT_FORMAT = 'HH:mm DD/MM/YYYY'
var DATE_FORMAT = 'DD/MM/YYYY'

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

/*
var myCenter //= new google.maps.LatLng(10.77749,106.68157)
function map_init() {
  var mapProp = {
    center:myCenter,
    zoom:15,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);

  var marker=new google.maps.Marker({
  position:myCenter,
  });

marker.setMap(map);

}
google.maps.event.addDomListener(window, 'load', map_init);

*/


function map_init2(myCenter) {
    var mapProp = {
        center: myCenter,
        zoom: 15,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("googleMap1"), mapProp);

    var marker = new google.maps.Marker({
        position: myCenter,
    });

    marker.setMap(map);

}
google.maps.event.addDomListener(window, 'load', map_init2);


function show_map_from_longlat() {

    long = parseFloat($('#id_Long_3G').val().replace(',', '.'));
    lat = parseFloat($('#id_Lat_3G').val().replace(',', '.'));
    //LatLng = lat + "," + long;
    try {
        myCenter = new google.maps.LatLng(lat, long);
        //map_init()
        map_init2(myCenter)
    } catch (err) {}
}

function removeParam(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

/*
 function scrolify(tblAsJQueryObject, height){
        var oTbl = tblAsJQueryObject;

        // for very large tables you can remove the four lines below
        // and wrap the table with <div> in the mark-up and assign
        // height and overflow property  
        var oTblDiv = $("<div/>");
        oTblDiv.css('height', height);
        oTblDiv.css('overflow','scroll');               
        oTbl.wrap(oTblDiv);

        // save original width
        oTbl.attr("data-item-original-width", oTbl.width());
        oTbl.find('thead tr th').each(function(){
            $(this).attr("data-item-original-width",$(this).width());
        }); 
        oTbl.find('tbody tr:eq(0) td').each(function(){
            $(this).attr("data-item-original-width",$(this).width());
        });                 


        // clone the original table
        var newTbl = oTbl.clone();

        // remove table header from original table
        oTbl.find('thead tr').remove();                 
        // remove table body from new table
        newTbl.find('tbody tr').remove();   

        oTbl.parent().parent().prepend(newTbl);
        newTbl.wrap("<div/>");

        // replace ORIGINAL COLUMN width                
        newTbl.width(newTbl.attr('data-item-original-width'));
        newTbl.find('thead tr th').each(function(){
            $(this).width($(this).attr("data-item-original-width"));
        });     
        oTbl.width(oTbl.attr('data-item-original-width'));      
        oTbl.find('tbody tr:eq(0) td').each(function(){
            $(this).width($(this).attr("data-item-original-width"));
        });                 
    }
*/
//$(function() {
//PNotify.prototype.options.styling = "bootstrap3";
//new PNotify({
//title: 'Regular Notice',
//text: 'Hello! Have a good day!'
//});
//

/*
$(function(){
    $(".wrapper1").scroll(function(){
        $(".wrapper2")
            .scrollLeft($(".wrapper1").scrollLeft());
    });
    $(".wrapper2").scroll(function(){
        $(".wrapper1")
            .scrollLeft($(".wrapper2").scrollLeft());
    });
});

*/
// Change the selector if needed
/*
var $table = $('table.scroll'),
    $bodyCells = $table.find('tbody tr:first').children(),
    colWidth;

// Adjust the width of thead cells when window resizes
$(window).resize(function() {
    // Get the tbody columns width array
    colWidth = $bodyCells.map(function() {
        console.log($(this).attr('class'),$(this).width())
        return $(this).width();
    }).get();
    
    // Set the width of thead columns
    $table.find('thead tr').children().each(function(i, v) {
        console.log($(v).attr('class'),i,colWidth[i])
        $(v).width(colWidth[i]);
    });    
}).resize(); // Trigger resize handler
*/

//$('table.tablemll').fixedHeaderTable({ footer: false, cloneHeadToFoot: true, fixedColumn: false });