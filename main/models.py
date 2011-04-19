from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from hubarcode.ean13 import EAN13Encoder
from hubarcode.code128 import Code128Encoder
from settings import MEDIA_ROOT
from PIL import Image


def make_upload_path(instance, filename):
    #raise IOError(instance.id)
    return u"products/%s" % filename
    
#def make_barcode_path(instance, filename):
#    return u"barcodes/%d/%s" % (instance.product.id, filename)



# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=200)
    image = models.ImageField(upload_to=make_upload_path, blank=True, max_length=200)
    price = models.DecimalField(decimal_places=4, max_digits=19, null=True, blank=True)
    quantity = models.IntegerField(max_length=10, blank=True, default=1)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    expire_date = models.DateField(blank=True)

    barcode_EAN13 = models.CharField(max_length=12, blank=True, null=True)
    barcode_EAN128 = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name
    
#    def save(self, *args, **kwargs):
#
#        if self.barcode_EAN13:
#            encoder = EAN13Encoder(self.barcode_EAN13)
#
#
#        super(Product, self).save(*args, **kwargs)


#
##            raise IOError(type(self.barcode_EAN13))
##            code = self.barcode_EAN13
##            raise IOError(type(int(code)))
#            encoder = EAN13Encoder(str(self.barcode_EAN13))
#            path = MEDIA_ROOT + '/barcodes/%s' % 'ean13-for' + str(self.id) + '.png'
#            encoder.save(path)
#            image = Image.open(path)
#            my_barcode = MyBarcode(
#                product = self,
#                barcode = 'barcodes/%s' % 'ean13-for' + str(self.id) + '.png'
#            )
#            my_barcode.save()




class MyBarcode(models.Model):
    product = models.ForeignKey(Product)
    barcode = models.ImageField(upload_to='/barcodes/', max_length=200, blank=True)

    def __unicode__(self):
        return "my_barcode for" + self.product.name


@receiver(post_save, sender=Product)
def my_handler(sender, **kwargs):
    #raise IOError(kwargs)
    instance = kwargs.get('instance')
#    raise IOError(instance)
    if instance.barcode_EAN13:
        encoder = EAN13Encoder(instance.barcode_EAN13)
        encoder.save(MEDIA_ROOT + '/barcodes/' + 'ean13-' + str(instance.id) + '.png')
        b = MyBarcode(
            product = instance,
            barcode = '/barcodes/' + 'ean13-' + str(instance.id) + '.png'
        )
        b.save()
    if instance.barcode_EAN128:
        encoder = Code128Encoder(instance.barcode_EAN128)
        encoder.save(MEDIA_ROOT + '/barcodes/' + 'ean128-' + str(instance.id) + '.png')
        b = MyBarcode(
            product = instance,
            barcode = '/barcodes/' + 'ean128-' + str(instance.id) + '.png'
        )
        b.save()


