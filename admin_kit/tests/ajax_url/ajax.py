from admin_kit import ajax
import admin_kit

class TestGenresAjax(ajax.Ajax):
    def run(self, request):
        GENRES = (
            ('thriller', 'thriller'),
            ('philosophy', 'philosophy')
        )
        return GENRES

admin_kit.site.register('test-genres', TestGenresAjax)