(function ($) {

    function InitializeSelect(element, data) {
        var values = {};
        if(element.attr('data-ajax-value') != undefined) {
            var data_values = element.attr('data-ajax-value').split(',')
            for(var i in data_values) {
                if(data_values[i]) {
                    values[data_values[i]] = true;
                }
            }
        }
        if(element.val() == null || element.val() == '') {
            SetSelectField(element, data, values);
        }
    }

    function SetSelectField(element, data, initials) {
        var child = element.children().eq(0).clone();
        element.empty();
        // console.log(element, data);
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
            }
            element.append(clonedChild);
        }
    }

    function ajaxSource(element, source, query) {
        var target_url = '/admin_kit/ajax/' + source + '/';
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
        var target_url = '/admin_kit/ajax/' + target + '/';
        $.ajax({
            method: 'get',
            url: target_url,
            data: {
                q: element.val()
            },
            success: function(data) {
                var parentModule = element.parentsUntil('.module').parent().eq(0);
                if(targetElement != undefined) {
                    var parentId = parentModule.parent().attr('id');
                    var targetId = parentId + '-' + targetElement;
                    var elements = parentModule.find('#id_' + targetId);
                    elements.val(data);
                } else {
                    var elements = parentModule.find('.admin-kit.admin-kit-subscribe[data-ajax-source=' + target + ']');
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
        if(element.attr('data-ajax-source') != undefined) {
            ajaxSource(element,  element.attr('data-ajax-source'), '');
        }
        if(element.attr('data-ajax-target') != undefined) {
            ajaxTarget(element,  element.attr('data-ajax-target'), query);
        }
    }

    function AdminKitReady(element) {
        InitializeAdminKit(element,[], true);
        element.on('change', function() {
            ProcessAdminKit(element, element.val());
        });
    }

    $(document).ready(function() {

        $('.admin-kit').each(function() {
            AdminKitReady($(this));
        });

        $(".js-inline-admin-formset .module").each(function() {
            var addBtn = $(this).children('.add-row');
            var addDup = addBtn.clone();
            addDup.children('a').text('Add a duplicate');
            addDup.on('click', function(e) {
                e.preventDefault();
                addDup.parent().attr('data-duplicate', true);
                addBtn.children('a').click();
                return false;
            });
            $(this).append(addDup);
        });

        $(document).on("formset:added", function(event, $row, formsetName) {
            if($row.parent().attr('data-duplicate')) {
                var curr_inputs = $row.find(":input");
                var prev_inputs = $row.prev().find(":input");
                for(var i = 0, j = 0; i < prev_inputs.length && j < curr_inputs.length;){
                    var prevName = getSuffixName(prev_inputs[i]);
                    var curName = getSuffixName(curr_inputs[j]);
                    if(curName==undefined) {
                        j++;
                        continue
                    }
                    if(prevName != curName) {
                        i++;
                        continue;
                    }
                    
                    $(curr_inputs[j]).val($(prev_inputs[i]).val());
                    i++;
                    j++;
                }
                $row.parent().attr('data-duplicate', null);
            }

            $row.find('.admin-kit').each(function() {
                AdminKitReady($(this));
            });
        });
    });
})(django.jQuery);

function getSuffixName(ele) {
    var name = ele.name;
    if(name == undefined) {
        return name;
    }
    var name_splits = name.split('-');
    return name_splits[name_splits.length - 1];
}