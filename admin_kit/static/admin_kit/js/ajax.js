(function ($) {

    function InitializeSelect(element, data) {
        var child = element.children();
        var values = {};
        if(element.attr('data-ajax-value') != undefined) {
            var data_values = element.attr('data-ajax-value').split(',')
            for(var i in data_values) {
                if(data_values[i]) {
                    values[data_values[i]] = true;
                }
            }
        }
        if(child.val() == '') {
            element.empty();
            for(var i in data) {
                var clonedChild = child.clone();
                clonedChild.text(data[i][0]);
                clonedChild.attr('value', data[i][1]);
                if(values[data[i][1]] == true) {
                    clonedChild.attr('selected', 'selected');
                }
                element.append(clonedChild);
            }
        }
    }

    function InitializeAdminKit(element) {
        if(element.attr('data-ajax-source') != undefined) {
            var target_url = '/admin_kit/ajax/' + element.attr('data-ajax-source');
            $.ajax({
                method: 'get',
                url: target_url,
                dataType: 'json',
                success: function(data) {
                    if(element.hasClass('admin-kit-select')) {
                        InitializeSelect(element, data);
                    }
                }
            });
        }
    }

    $(document).ready(function() {
        $('.admin-kit').each(function() {
            InitializeAdminKit($(this));
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
        });
    })
})(django.jQuery);

function getSuffixName(ele) {
    var name = ele.name;
    if(name == undefined) {
        return name;
    }
    var name_splits = name.split('-');
    return name_splits[name_splits.length - 1];
}