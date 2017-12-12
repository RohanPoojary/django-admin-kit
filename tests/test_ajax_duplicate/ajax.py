import admin_kit

class GenresAjax(admin_kit.ajax.Ajax):
    unique = True

    def run(self, request):
        query = request.GET.getlist('q[]')
        response = list(zip(query, query))
        return response

class GenresDescriptionAjax(admin_kit.ajax.Ajax):
    response_type = 'text'

    def run(self, request):
        query = request.GET['q']
        if query:
            return 'Description of %s' % str(query)


admin_kit.site.register('genres-desc', GenresDescriptionAjax)
admin_kit.site.register('genres', GenresAjax)
