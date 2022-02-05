import json
from hashlib import sha256

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from documents.forms import DocumentForm
from documents.models import Document


def add_document(request):
    context = {'form': DocumentForm()}
    return render(request, 'add_document.html', context)


def save_document(request):
    print("Form submitted")
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            # Check if nonce and hash are correct
            hash256 = sha256((str(form.cleaned_data['nonce']) + form.cleaned_data['data']).encode()).hexdigest()
            if hash256 != form.cleaned_data['hash']:
                form.add_error("hash", "Invalid hash")
                return render(request, 'add_document.html', {'form': form})
            doc = form.save(commit=False)
            try:
                last_doc = Document.objects.latest('id')
                doc.prev = last_doc.hash
            except ObjectDoesNotExist:
                doc.prev = '0000000000000000000000000000000000000000000000000000000000000000'
            user = request.user
            doc.user = user
            doc.save()
    return redirect('/add/document')


@csrf_exempt
def mine(request):
    form_data = json.loads(request.body)
    doc = form_data['data']
    hash256 = ''
    nonce = 0
    for x in range(100000):
        hash256 = sha256((str(x) + doc).encode()).hexdigest()
        if hash256[0:2] == '00':
            nonce = x
            break
    if hash256[0:2] != '00':
        print("Error, hash not valid. " + hash256)
    data = {
        'nonce': nonce,
        'hash': hash256,
        "data": doc
    }
    return JsonResponse(data)


def view_documents(request):
    context = {'docs': Document.objects.all()}
    for doc in context['docs']:
        hash256 = sha256((str(doc.nonce) + doc.data).encode()).hexdigest()
        if hash256 == doc.hash:
            doc.valid = True
        else:
            doc.valid = False

    return render(request, 'documentlist.html', context)


def view_document(request, did):
    doc = get_object_or_404(Document, pk=did)
    hash256 = sha256((str(doc.nonce) + doc.data).encode()).hexdigest()
    if hash256 == doc.hash:
        doc.valid = True
    else:
        doc.valid = False
    context = {'doc': doc}
    return render(request, "document.html", context)
