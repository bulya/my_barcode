# Create your views here.
import os
import zbar

from django.core.files.base import ContentFile

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template.context import RequestContext
from main.forms import MyScanner
from main.models import Product
from settings import MEDIA_ROOT
from PIL import Image
from django.core.files.storage import default_storage

c = {}


def home(request):
    products = Product.objects.all()
    c['products'] = products
    return render_to_response('main.html', c, context_instance=RequestContext(request))

def details(request, id):
    c['product'] = Product.objects.filter(pk=id)[0]
    return render_to_response('details.html', c, context_instance=RequestContext(request))

def scan(request):
    c['error_message'] = False
    c['form'] = MyScanner()

    if request.method == 'POST':


        bar_code_from_post = request.FILES.get('bar_code')
        path = default_storage.save('temp/temp.png', ContentFile(bar_code_from_post.read()))
        tmp_file = os.path.join(MEDIA_ROOT, path)

        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')

        pil = Image.open(MEDIA_ROOT + '/temp/temp.png').convert('L')
        width, height = pil.size
        raw = pil.tostring()

        image = zbar.Image(width, height, 'Y800', raw)
        scanner.scan(image)

        for symbol in image:
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data[:-1]
            pr_ean13 = Product.objects.filter(barcode_EAN13__contains=symbol.data[:-1])
            if pr_ean13:
                return HttpResponseRedirect('/product/' + str(pr_ean13[0].id))

            pr_ean128 = Product.objects.filter(barcode_EAN128__contains=symbol.data[:-1])
            if pr_ean128:
                return HttpResponseRedirect('/product/' + str(pr_ean128[0].id))

            no_result = True
            break


        c['error_message'] = True
        if os.path.exists(MEDIA_ROOT + '/temp/temp.png'):
            os.remove(MEDIA_ROOT + '/temp/temp.png')

    return render_to_response('scan.html', c, context_instance=RequestContext(request))