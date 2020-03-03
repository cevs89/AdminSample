from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, CreateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from recognition.models import RecognitionElement
from recognition.forms import PostFormRecognitionElement, EditFormRecognitionElement
from django.contrib import messages


def DeleteRecognition(request, id):
    try:
        query_set = RecognitionElement.objects.get(pk=id)
    except RecognitionElement.DoesNotExist:
        return JsonResponse(
            {"msg": "No existe el registro que desea eliminar"}, status=400)

    query_set.delete()
    return JsonResponse(
        {"msg": "El registro de borro de manera correcta"}, status=200)


class ListRecognitionView(ListView):
    model = RecognitionElement
    template_name = "list_reconocimiento.html"

    def get_queryset(self):
        queryset = super(ListRecognitionView, self).get_queryset()
        return queryset


class CreatetRecognitionView(CreateView):
    template_name = "reconocimiento.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = PostFormRecognitionElement
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = PostFormRecognitionElement(request.POST, request.FILES)
        context['form'] = form

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo de manera correcta')
        else:
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('list_recon'))


class EditRecognitionView(View):
    template_name = "reconocimiento.html"

    def get(self, request, *args, **kwargs):
        context = {}
        get_id = kwargs['id']
        object_get = get_object_or_404(RecognitionElement, pk=get_id)
        context['form'] = EditFormRecognitionElement(instance=object_get)
        context['get_id'] = get_id
        context['editForm'] = True
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        get_id = request.POST.get('get_id')
        object_post = get_object_or_404(RecognitionElement, pk=get_id)

        form = EditFormRecognitionElement(
            request.POST, request.FILES, instance=object_post)
        context['form'] = form
        context['editForm'] = True
        context['get_id'] = get_id

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Se Edito de manera correcta')
        else:
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('list_recon'))
