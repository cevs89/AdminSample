from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, CreateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from crud_base.models import KnowledgeBase
from .forms import PostFormKnowledgeBase
from django.contrib import messages


def DeleteRecordView(request, id):
    try:
        query_set = KnowledgeBase.objects.get(pk=id)
    except KnowledgeBase.DoesNotExist:
        return JsonResponse(
            {"msg": "No existe el registro que desea eliminar"}, status=400)

    query_set.delete()
    return JsonResponse(
        {"msg": "El registro de borro de manera correcta"}, status=200)


class ListKnowledgeView(ListView):
    model = KnowledgeBase
    template_name = "list_know.html"

    def get_queryset(self):
        queryset = super(ListKnowledgeView, self).get_queryset()
        return queryset


class CreatetKnowledgeView(CreateView):
    template_name = "knowledge.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = PostFormKnowledgeBase
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = PostFormKnowledgeBase(request.POST, request.FILES)
        context['form'] = form

        if form.is_valid():
            post = form.save(commit=False)
            post.status = 0
            post.parent_id = 1
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo de manera correcta')
        else:
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('list_know'))


class EditKnowledgeView(View):
    template_name = "knowledge.html"

    def get(self, request, *args, **kwargs):
        context = {}
        get_id = kwargs['id']
        object_get = get_object_or_404(KnowledgeBase, pk=get_id)
        context['form'] = PostFormKnowledgeBase(instance=object_get)
        context['get_id'] = get_id
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        get_id = request.POST.get('get_id')
        object_post = get_object_or_404(KnowledgeBase, pk=get_id)

        form = PostFormKnowledgeBase(
            request.POST, request.FILES, instance=object_post)
        context['form'] = form
        context['get_id'] = get_id

        if form.is_valid():
            post = form.save(commit=False)
            post.status = 0
            post.parent_id = 1
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Se Edito de manera correcta')
        else:
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('list_know'))
