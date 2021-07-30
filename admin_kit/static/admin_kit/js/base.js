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
        isMultiSelect = (element.attr('multiple') != undefined)
        for(var i in data) {
            if (isMultiSelect && data[i][1] == "") {
                continue
            }
            var eligibleForPreSelect = false
             // This is to make sure we do pre selection of default values only in case of first time loading.
            if (data[i][1] == defaultValue && initials['initial'] == true) {
                eligibleForPreSelect = true
            }
            var newOption = new Option(data[i][0], data[i][1], (initials===true || initials[data[i][1]] === true || eligibleForPreSelect === true), (initials===true || initials[data[i][1]] === true || eligibleForPreSelect === true));
            element.append(newOption);
        }
    }


    function ajaxSource(element, source) {
        var target_url = window.AdminKitConfig.appName + '/ajax/' + source + '/';
        $.ajax({
            method: 'get',
            url: target_url,
            success: function(data) {
                noDefaultSelectionAvailable = InitializeSelect(element, data);
                $("#"+element.get(0).id).select2({placeholder: 'Select One', allowClear: true})
            }
        });
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
        ajaxSourceAttr = element.kitAttr('ajax-source')
        if (ajaxSourceAttr != undefined && ajaxSourceAttr.startsWith("__")) {
            ajaxSource(element,  element.kitAttr('ajax-source'));
        }
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
    function triggerOnSelect(sources, sourceMap) {
             splitSources = sources.split(",")
             queryString = ""
             for (i=0; i< splitSources.length; i++) {
                 element = $(splitSources[i])
                 value = element.val()
                 if(!element.hasClass('dirty') && !value && element.kitAttr('init-value')) {
                     value = element.kitAttr('init-value');
                     if(element.attr('multiple') === 'multiple') {
                         value = sourceMap[element.get(0).id].split(',');
                     }
                     if (element.kitAttr('default_value') != undefined) {
                        value = element.kitAttr('default_value')
                     }
                 }
                 if (element.get(0) != undefined) {
                     elementQueryField = $("#"+element.get(0).id).kitAttr('default_name')
                     if (queryString == "") {
                         queryString = elementQueryField + "="+ value
                     } else {
                         queryString = queryString+ "&" + elementQueryField + "="+ value
                     }
                 }
             }
             for (i=0; i< sourceMap[sources] .length; i++) {
                 targetID = sourceMap[sources][i]
                 target = $("#"+targetID).kitAttr('ajax-source-in-multi-dep')
                 if (target == undefined) {
                     target = $("#"+targetID).kitAttr('ajax-source')
                 }
                 var target_url = window.AdminKitConfig.appName + '/ajax/' + target + '?'+queryString;
                 console.log(target_url)
                 (function(target_url, targetID){
                     $.ajax({
                         method: 'get',
                         url: target_url,
                         success: function(data) {
                             noDefaultSelection = SetSelectField($("#"+targetID), data, getInitialValues($("#"+targetID)));
                             $("#"+targetID).select2({placeholder: 'Select One', allowClear: true})
                         }
                     });
                 })(target_url, targetID)
             }
    }

    function getDependencies(root) {
        sourceMap = {}
        root.each(function() {
                element = $(this)
                elementSource = element.kitAttr('ajax-source')
//                If element starts with __ then it is a hashed source. hence no processing required.
                    if(elementSource && !elementSource.startsWith("__")) {
                        elementSourceMap = {}
                        splitElementSource = elementSource.split(",")
                        for(i=0; i< splitElementSource.length; i++) {
                            elementSourceMap[splitElementSource[i]] = true
                        }
                        element.select2({allowClear: true})
                        targets = ""

                        // For every dependent element, find its parents
                        $('.admin-kit').each(function() {
                            if($(this).kitAttr('ajax-target') != undefined) {
                                 splitTarget = $(this).kitAttr('ajax-target').split(",")
                                 for(i =0; i< splitTarget.length; i++) {
                                     if(splitTarget[i] in elementSourceMap) {
                                        if($(this).get(0).id.includes("__prefix__")) {
                                            continue
                                        }
                                        if(targets == "") {
                                            targets = targets + "#"+ $(this).get(0).id
                                        } else {
                                            targets = targets + ",#"+ $(this).get(0).id
                                        }
                                     }
                                 }
                            }
                        });
                        if(!$(this).get(0).id.includes("__prefix__")) {
                            if (targets in sourceMap) {
                                sourceMap[targets].push(element.get(0).id)
                            } else {
                                sourceMap[targets] = [element.get(0).id]
                            }
                        }
                }
        });
        return sourceMap
    }

    function addListenerForDependencies(sourceMap) {
        for (var sources in sourceMap) {
            splitSources = sources.split(",")
            allSourcesHasDefaultValue = true
            for (i=0; i< splitSources.length; i++) {
                 element = $(splitSources[i])
                 value = element.val()
                 if(!element.hasClass('dirty') && !value && element.kitAttr('init-value')) {
                     value = element.kitAttr('init-value');
                     if(element.attr('multiple') === 'multiple') {
                         value = sourceMap[element.get(0).id].split(',');
                     }
                 }
                 if (element.kitAttr('default_value') != undefined) {
                    value = element.kitAttr('default_value')
                 }

                 if (value == 'initial' || value == "" || value == undefined) {
                    allSourcesHasDefaultValue = false
                 }
             }
             if (allSourcesHasDefaultValue) {
                triggerOnSelect(sources, sourceMap)
             }
            (function(sources) {
                $(sources).on("select2:select", function(e) {
                    triggerOnSelect(sources, sourceMap)
                });
                $(sources).on("select2:unselect", function(e) {
                    triggerOnSelect(sources, sourceMap)
                });
                $(sources).on("change", function(e) {
                    triggerOnSelect(sources, sourceMap)
                });
            })(sources)
        }
    }

    $(document).ready(function() {

        sourceMap = getDependencies($('.admin-kit'))
        addListenerForDependencies(sourceMap)
        $('.admin-kit').each(function() {
            InitializeAdminKit($(this),[]);
            if (!$(this).get(0).id.includes("__prefix") && $('#check_'+$(this).get(0).id).length) {
                (function(sourceID, targetID){
                    $(sourceID).change(function() {
                        if($(sourceID).is(':checked')){
                            $("#"+ targetID+" > option").prop("selected", "selected");
                            $("#"+ targetID).trigger("change");
                        } else {
                            $("#"+ targetID).val('').trigger("change");
                        }
                    })
                })('#check_'+$(this).get(0).id, $(this).get(0).id)
            }

        });
        // If there are no ajax sources without dependency, there won't be any empty key in sourceMap
        if("" in sourceMap) {
            // Process all elements who doesnt have an ajax target but need to be dynamically loaded
            for(i=0; i< sourceMap[""].length; i++) {
                element = $("#"+sourceMap[""][i])
                ajaxSource(element, element.kitAttr('ajax-source'));
            }
        }

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
                    $(this).select2().select2({placeholder: 'Select One', allowClear: true});
                    InitializeAdminKit($(this),[]);
                    if (!$(this).get(0).id.includes("__prefix") && $('#check_'+$(this).get(0).id).length) {
                        (function(sourceID, targetID){
                            $(sourceID).change(function() {
                                if($(sourceID).is(':checked')){
                                    $("#"+ targetID+" > option").prop("selected", "selected");
                                    $("#"+ targetID).trigger("change");
                                } else {
                                    $("#"+ targetID).val('').trigger("change");
                                }
                            })
                        })('#check_'+$(this).get(0).id, $(this).get(0).id)
                    }
                })
                sourceMap = getDependencies(row.find('.admin-kit'))
                addListenerForDependencies(sourceMap)
                // If there are no ajax sources without dependency, there won't be any empty key in sourceMap
                if("" in sourceMap) {
                     // Process all elements who doesnt have an ajax target but need to be dynamically loaded
                    for(i=0; i< sourceMap[""].length; i++) {
                        element = $("#"+sourceMap[""][i])
                        ajaxSource(element, element.kitAttr('ajax-source'));
                    }
                }
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
