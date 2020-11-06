import admin_kit

class TestEmpty(admin_kit.ajax.Ajax):
    unique = True
    response_type = 'text'

class TestAjax(admin_kit.ajax.Ajax):
    def run(self, request, **kwargs):
        output = (
            ('book1', '1'),
            ('book2', '2')
        )
        return output

admin_kit.site.register('testajax', TestAjax)
admin_kit.site.register('empty', TestEmpty)

