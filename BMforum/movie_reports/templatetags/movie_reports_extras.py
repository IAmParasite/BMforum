from django import template
from ..forms import ReportForm
 
register = template.Library()
 
 
@register.inclusion_tag('movie_reports/inclusions/_form.html', takes_context=True)
def show_movie_report_form(context, post, form=None):
    if form is None:
        form = ReportForm()
    return {
        'form': form,
        'post': post,
    }