# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required


@login_required()
def image_create(request):
    if request.method == 'POST':
        # form é enviado
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # dados do form é valido
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # define o usuário atual ao item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Imagem adicionada com sucesso!')

            # redireciona ao detail view do novo item criado
            return redirect(new_item.get_absolute_url())
    else:
        # constroi o form com os dados fornecidos pelo bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})


@ajax_required
@login_required()
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status:': 'ko'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required()
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # se a pagina não é um inteiro retorna a primeira pagina
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # se a requisição é AJAX e a página está fora do intervalo, retorna uma página vazia
            return HttpResponse('')
        # se a página está fora do intervalo, retorna a última página de resultados
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})