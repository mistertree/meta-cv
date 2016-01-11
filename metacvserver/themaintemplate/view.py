from importlib import import_module

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.template import Context
from django.template.loader import get_template
from django.conf import settings

from cv.models import Hashtag
from themaintemplate.forms import NameCaptchaForm

class TheMainTemplateView(TemplateView, FormMixin):
    """Serves themaintemplate.html and make sure it has the needed variables in
       context"""
    form_class = NameCaptchaForm
    template_name = "themaintemplate/themaintemplate.html"
    MODULES = ["video", "cv"]

    def get_form_kwargs(self, *args, **kwargs):
        dict_kwargs = super(TheMainTemplateView, self).get_form_kwargs(*args, 
            **kwargs)
        dict_kwargs['session'] = self.request.session
        return dict_kwargs

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        """Get HTML from the modules, and adds the module name to the context
           The main template then adds the css file 'module_name/style.scss'
           and the dart file 'module_name/{module_name}_bootstrap.scss'
           """
        ctx = super(TheMainTemplateView, self).get_context_data(*args, **kwargs) 
        ctx['html'] = dict()
        ctx['sass'] = list()
        ctx['dart'] = list()
        ctx['name'] = "{firstname} {surname}".format(
            firstname = settings.FIRST_NAME, surname=settings.SURNAME)

        if self.request.method == "POST" and self.get_form().is_valid():
            ctx['mail'] = settings.PUBLIC_EMAIL
        
        for module_name in TheMainTemplateView.MODULES:
            module = import_module("{module}.views".format(module=module_name)) 

            ctx['html'][module_name] = module.TheMainTemplateHTMLGenerator(
                self.kwargs).generate_html()

            def add_to_context(context_dict, filename):
                ctx[context_dict].append(filename.format(
                    module_name = module_name))
            add_to_context('sass', '{module_name}/style.scss')
            add_to_context('dart', '{module_name}/{module_name}_bootstrap.dart')

        return ctx

def switch_ajax(ajax_classbasedview):
    """Returns a view.
       This view will pass the request to another view. It chooses this view by
       checking if the request is done by an ajax client."""
    def view(request, *args, **kwargs):
        view = None
        if request.is_ajax():
            view = ajax_classbasedview.as_view()
        else:
            view = TheMainTemplateView.as_view()
        return view(request, *args, **kwargs)
    return view
