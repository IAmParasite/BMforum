from comments.models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ReportForm
from django.contrib import messages
 
@require_POST
def report(request, post_pk):
    post = get_object_or_404(Comment, pk=post_pk)
    form = ReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        print(report)
        report.post = post
        report.name = request.user
        report.save()
        post.save()
        context = {
            'post': post,
            'form': form,
        }
        messages.add_message(request, messages.SUCCESS, '举报成功！', extra_tags='success')
        #return redirect(post)
        return render(request, 'reports/preview.html', context=context)
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '举报发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'reports/preview.html', context=context)
