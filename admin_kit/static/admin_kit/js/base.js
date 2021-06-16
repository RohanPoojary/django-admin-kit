    $.fn.kitAttr = function(key, value) {
        var attr = $(this).attr('data-kit-config');
        if(attr == undefined)
            return attr;
        var attrObj = JSON.parse(attr);
        if(value == undefined)
            return attrObj[key];
        attrObj[key] = value;
        $(this).attr('data-kit-config', JSON.stringify(attrObj));
    };
    $.fn.kitFind = function(config) {
        return this.find('.admin-kit').filter(function() {
            for(var key in config) {
                if($(this).kitAttr(key) != config[key])
                    return false;
            }
            return true;
        });
    };

    function InitializeSelect(element, data) {
        var values = getInitialValues(element);
        if(!element.hasClass('dirty') && (element.val() == null || element.val() == '')) {
            SetSelectField(element, data, values);
        }
    }

    <!-- SetSelectField sets the options for a select field. Initials will be pre selected and data will be populated as options    -->
    function SetSelectField(element, data, initials) {
        var child = element.children().eq(0).clone();
        element.empty();
        <!--   This is to make sure that the default selection works when specified in model field witj some value -->
        defaultValue = element.kitAttr('default_value')
        for(var i in data) {
            var eligibleForPreSelect = false
            if (data[i][1] == defaultValue) {
                eligibleForPreSelect = true
            }
            var newOption = new Option(data[i][0], data[i][1], (initials===true || initials[data[i][1]] === true || eligibleForPreSelect === true), (initials===true || initials[data[i][1]] === true || eligibleForPreSelect === true));
            element.append(newOption);
        }
    }


    function ajaxSource(element, source, query) {
        var target_url = window.AdminKitConfig.appName + '/ajax/' + source + '/';
        $.ajax({
            method: 'get',
            url: target_url,
            data: {
                q: query
            },
            success: function(data) {
                InitializeSelect(element, data);
                $("#"+element.get(0).id).select2({placeholder: 'Select One'})
            }
        });
    }

    function ajaxTarget(element, target) {
        var target_array = target.split(',');

        target_array.forEach(function (target) {

            var targetElement;

            if(target.indexOf(':') >= 0) {
                targetElement = target.slice(target.indexOf(':') + 1);
                target = target.slice(0, target.indexOf(':'))
            }

            var is_global = target[0] === "#";

            if (is_global) {
                target = target.slice(1);
            }

            var target_url = window.AdminKitConfig.appName + '/ajax/' + target + '/';
            var value = element.val();
            if(!element.hasClass('dirty') && !value && element.kitAttr('init-value')) {
                value = element.kitAttr('init-value');
                if(element.attr('multiple') === 'multiple') {
                    value = value.split(',');
                }
            }

            var parentModule = element.parents('.module').eq(0);

            var elements = [];

            if(targetElement != undefined) {
                var parentId = parentModule.parent().attr('id');
                var targetId = parentId + '-' + targetElement;
                elements = parentModule.find('#id_' + targetId);

            } else {
                if(is_global) {

                    elements = $("body").kitFind({
                        'ajax-source': "#"+target,
                        'ajax-subscribe': true
                    });
                } else {

                    elements = parentModule.kitFind({
                        'ajax-source': target,
                        'ajax-subscribe': true
                    });
                }
            }

            for(var i = 0; i < elements.length; i++) {
                elements.eq(i).addClass('admin-kit-ready');
            }


            $.ajax({
                method: 'get',
                url: target_url,
                data: {
                    q: value
                },
                success: function(data) {

                    if(targetElement != undefined) {
                        elements.val(data);
                    } else {
                        for(var i = 0; i < elements.length; i++) {
                            SetSelectField(elements.eq(i), data, getInitialValues(elements.eq(i)));
                            $("#"+elements.eq(i).get(0).id).select2({placeholder: 'Select One'})
                        }
                    }
                }
            });
        })
    }

    function InitializeAdminKit(element, data) {
        if(element.hasClass('admin-kit-select') && !element.hasClass('admin-kit-ready')) {
            ProcessAdminKit(element, data, true);
            element.addClass('admin-kit-ready');
        }
    }

    function ProcessAdminKit(element, query, update_once) {

        if (update_once === true && element.hasClass('admin-kit-ready')) {
            return
        }
        if(element.kitAttr('ajax-source') != undefined) {
            ajaxSource(element,  element.kitAttr('ajax-source'), '');
        }

        if(element.kitAttr('ajax-target') != undefined) {
            ajaxTarget(element,  element.kitAttr('ajax-target'), query);
        }
    }

    function AdminKitReady(element) {
        InitializeAdminKit(element,[]);
        element.on('change', function (e) {
            $(this).addClass('dirty');
            ProcessAdminKit(element, element.val(), false);
        });

    }

    function getInitialValues(element) {
        values = {}
        if(element.kitAttr('init-value') != undefined && element.kitAttr('init-value') != "") {
            var data_values = element.kitAttr('init-value').split(',')
            for(var i in data_values) {
                if(data_values[i]) {
                    values[data_values[i]] = true;
                }
            }
        }
        return values
    }

    $(document).ready(function() {

        $('.admin-kit').each(function() {
            AdminKitReady($(this));
        });

        <!--   Select2 is not compatible with Django Jquery. And FormSet Added and Duplicate is not compatible with Normal JQuery. Hence forming a club of both      -->
        (function (djangoJQuery) {

            djangoJQuery.fn.kitVal = function() {
                var value = djangoJQuery(this).val();
                if(value != undefined && djangoJQuery(this).attr('multiple') != undefined) {
                    value = djangoJQuery(this).val().join();
                }
                return value
            };

            djangoJQuery.fn.kitAttr = function(key, value) {
                var attr = djangoJQuery(this).attr('data-kit-config');
                if(attr == undefined)
                    return attr;
                var attrObj = JSON.parse(attr);
                if(value == undefined)
                    return attrObj[key];
                attrObj[key] = value;
                djangoJQuery(this).attr('data-kit-config', JSON.stringify(attrObj));
            };

            djangoJQuery.fn.kitFind = function(config) {
                return this.find('.admin-kit').filter(function() {
                    for(var key in config) {
                        if(djangoJQuery(this).kitAttr(key) != config[key])
                            return false;
                    }
                    return true;
                });
            };
            if(window.AdminKitConfig.duplicate){
                djangoJQuery(".module").each(function() {
                    var addBtn = djangoJQuery(this).children('.add-row');
                    var addDup = addBtn.clone();
                    var link = addDup.children('a');
                    link.text('Add a Duplicate');
                    link.click(function(e) {
                        e.preventDefault();
                        addDup.parent().attr('data-duplicate', true);
                        addBtn.children('a').click();
                        e.stopImmediatePropagation();
                        return false;
                    });
                    djangoJQuery(this).append(addDup);
                });
            }
            djangoJQuery(document).on('formset:added', function(event, row, formsetName) {
            var parent = row.parents('.module');

            if(window.AdminKitConfig.duplicate) {
                if(parent.attr('data-duplicate')) {
                    duplicateRow(row, row.prev());

                    parent.attr('data-duplicate', null);

                    var children = row.find('.add-row');
                    var prev_children = row.prev().find('.add-row');

                    for(var i = 0; i < children.length; i++) {
                        var prev_module = prev_children.eq(i).parents('.module').eq(0);
                        var curr_module = children.eq(i).parents('.module').eq(0);

                        var total_forms_elem = prev_module.children('input[name$=TOTAL_FORMS]');

                        for(var j = 0; j <  total_forms_elem.val(); j++) {
                            children.eq(i).find('a').click();
                        }

                        var cur_id = curr_module.children('input[name$=TOTAL_FORMS]').attr('id').replace('-TOTAL_FORMS', '');
                        var prev_id = prev_module.children('input[name$=TOTAL_FORMS]').attr('id').replace('-TOTAL_FORMS', '');

                        duplicateRow(curr_module, prev_module, cur_id, prev_id);
                    }
                }
            }

            <!--     Django FormSet Added is not compatible with Select2. Hence we need to remove select2 and reinitialize again -->
            row.find('.admin-kit').each(function() {
                $(this).parent().find("span").remove()
                $(this).select2().select2({placeholder: 'Select One'});
                AdminKitReady($(this));
                })
            });

            function duplicateRow(row, prev, cur_id, prev_id) {
                var curr_inputs = row.find(":input");
                var prev_inputs = prev.find(":input");

                var prevEleInd = {};

                if(cur_id == undefined) {
                    cur_id = row.attr("id");
                }

                if(prev_id == undefined) {
                    prev_id = prev.attr("id");
                }

                for(var i = 0; i < prev_inputs.length ; i++){
                    var prevName = getSuffixName(prev_inputs.eq(i), prev_id);
                    if(prevName)
                        prevEleInd[prevName] = i;
                }

                for(var i = 0; i < curr_inputs.length ; i++){
                    var currName = getSuffixName(curr_inputs.eq(i), cur_id);
                    if(currName) {
                        var prevElement = prev_inputs.eq(prevEleInd[currName]);
                        curr_inputs.eq(i).val(prevElement.val());
                        if(prevElement.hasClass('admin-kit')) {
                            curr_inputs.eq(i).kitAttr('init-value', prevElement.kitVal());
                        }
                    }
                }
            }
        })(django.jQuery);

        function getSuffixName(ele, suf_id) {
            var name = ele.attr('name');
            for(var i = 0; i < ele.parents('.module').length - 1; i++) {
                name = name.replace(/-\d+/, '')
            }

            if(name == undefined || name.indexOf('__prefix__') >= 0) {
                return undefined;
            }

            if(ele.attr('type') == 'hidden')
                return undefined;

            output = name.replace(suf_id + '-', '');

            return output

        }
    });