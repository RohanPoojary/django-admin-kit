(function ($) {
    
        $.fn.kitAttr = function(key) {
            var attr = $(this).attr('data-kit-config');
            if(attr != undefined) {
                var attrObj = JSON.parse(attr);
                return attrObj[key];
            }
            return attr;
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
            var values = {};
            if(element.kitAttr('init-value') != undefined && element.kitAttr('init-value') != "") {
                var data_values = element.kitAttr('init-value').split(',')
                for(var i in data_values) {
                    if(data_values[i]) {
                        values[data_values[i]] = true;
                    }
                }
            }
            if(!element.hasClass('dirty') && (element.val() == null || element.val() == '')) {
                SetSelectField(element, data, values);
            }
        }
    
        function SetSelectField(element, data, initials) {
            var child = element.children().eq(0).clone();
            element.empty();
            if(!data || data.length == 0) {
                element.append(child);
            }
            for(var i in data) {
                var clonedChild = child.clone();
                // clonedChild.removeClass('hidden');
                clonedChild.text(data[i][0]);
                clonedChild.attr('value', data[i][1]);
                if(initials===true || initials[data[i][1]] === true) {
                    clonedChild.attr('selected', 'selected');
                } else {
                    clonedChild.attr('selected', null);
                }
                element.append(clonedChild);
            }
        }
    
        function ajaxSource(element, source, query) {
            var target_url = '{{app}}/ajax/' + source + '/';
            $.ajax({
                method: 'get',
                url: target_url,
                data: {
                    q: query
                },
                success: function(data) {
                    InitializeSelect(element, data);
                }
            });
        }
    
        function ajaxTarget(element, target) {
            var targetElement;
            if(target.indexOf(':') >= 0) {
                targetElement = target.slice(target.indexOf(':') + 1);
                target = target.slice(0, target.indexOf(':'))
            }
            var target_url = '{{app}}/ajax/' + target + '/';
            var value = element.val();
    
            if(!element.hasClass('dirty') && !value && element.kitAttr('init-value'))
                value = element.kitAttr('init-value').split(',');
    
            $.ajax({
                method: 'get',
                url: target_url,
                data: {
                    q: value
                },
                success: function(data) {
                    var parentModule = element.parents('.module').eq(0);
    
                    if(targetElement != undefined) {
                        var parentId = parentModule.parent().attr('id');
                        var targetId = parentId + '-' + targetElement;
                        var elements = parentModule.find('#id_' + targetId);
                        elements.val(data);
                    } else {
                        var elements = parentModule.kitFind({
                            'ajax-source': target,
                            'ajax-subscribe': true
                        });
                        for(var i = 0; i < elements.length; i++) {
                            SetSelectField(elements.eq(i), data, true);
                        }
                    }
                }
            });
        }
    
        function InitializeAdminKit(element, data, update) {
            if(element.hasClass('admin-kit-select')) {
                if(update != true)
                    InitializeSelect(element, data);
                ProcessAdminKit(element, data)
            }
        }
    
        function ProcessAdminKit(element, query) {
            if(element.kitAttr('ajax-source') != undefined) {
                ajaxSource(element,  element.kitAttr('ajax-source'), '');
            }
            if(element.kitAttr('ajax-target') != undefined) {
                ajaxTarget(element,  element.kitAttr('ajax-target'), query);
            }
        }
    
        function AdminKitReady(element) {
            InitializeAdminKit(element,[], true);
            element.on('change', function() {
                $(this).addClass('dirty');
                ProcessAdminKit(element, element.val());
            });
        }
    
        $(document).ready(function() {
    
            $('.admin-kit').each(function() {
                AdminKitReady($(this));
            });
    
            {% if duplicate %}
            $(".module").each(function() {
                var addBtn = $(this).children('.add-row');
                var addDup = addBtn.clone();
    
                var link = addDup.children('a');
    
                link.text('Add a duplicate');
    
                link.click(function(e) {
                    e.preventDefault();
    
                    addDup.parent().attr('data-duplicate', true);
                    addBtn.children('a').click();
                    e.stopImmediatePropagation();
                    return false;
                });
    
                $(this).append(addDup);
            });
            {% endif %}

            $(document).on("formset:added", function(event, $row, formsetName) {
    
                var parent = $row.parents('.module');
                
                {% if duplicate %}
                if(parent.attr('data-duplicate')) {
                    duplicateRow($row, $row.prev());
    
                    parent.attr('data-duplicate', null);
    
                    var children = $row.find('.add-row');
                    var prev_children = $row.prev().find('.add-row');
    
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
                {% endif %}
    
                $row.find('.admin-kit').each(function() {
                    AdminKitReady($(this));
                });
            });
        });
    
        function duplicateRow($row, $prev, cur_id, prev_id) {
            var curr_inputs = $row.find(":input");
            var prev_inputs = $prev.find(":input");
            
            var prevValues = {};
    
            if(cur_id == undefined) {
                cur_id = $row.attr("id");
            }
    
            if(prev_id == undefined) {
                prev_id = $prev.attr("id");
            }
        
            for(var i = 0; i < prev_inputs.length ; i++){
                var prevName = getSuffixName(prev_inputs.eq(i), prev_id);
                if(prevName)
                    prevValues[prevName] = prev_inputs.eq(i).val();
            }
        
            for(var i = 0; i < curr_inputs.length ; i++){
                var currName = getSuffixName(curr_inputs.eq(i), cur_id);
                if(currName)
                    curr_inputs.eq(i).val(prevValues[currName]);
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
    
        var suffix = name.split('-');
        var suffix_name = suffix[suffix.length - 1];
    
        output = name.replace(suf_id + '-', '');
    
        if(suffix_name.toLowerCase() != suffix_name)
            return undefined
    
        return output
    
    }