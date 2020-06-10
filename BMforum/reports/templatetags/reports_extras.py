from django import template
from ..forms import ReportForm
 
register = template.Library()
 
 
@register.inclusion_tag('reports/inclusions/_form.html', takes_context=True)
def show_report_form(context, post, form=None):
    if form is None:
        form = ReportForm()
    return {
        'form': form,
        'post': post,
    }