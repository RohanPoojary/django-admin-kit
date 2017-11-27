import admin_kit

class TestAjax(admin_kit.ajax.Ajax):
    def run(self, request):
        output = (
            ('book1', '1'),
            ('book2', '2')
        )
        return output

admin_kit.site.register('testajax', TestAjax)
