from time import time

import jwt
from marketing.settings import *

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from main.models import *


class MobilnikPaymentService(object):
    class Payload(object):

        AUDIENCE = 'mobilnik.kg'
        TYPE = 'acquiring.mobilnik.kg/api/v1'

        def __init__(self):
            self.expiration = None
            self.issued_at = None
            self.request = dict()

        def set_issued_at(self, issued_at):
            self.issued_at = issued_at

        def set_expiration(self, exp):
            self.expiration = exp

        def add_property(self, field_name, field_value):
            self.request[field_name] = field_value

        def add_product(self, name, price):
            product = {
                'name': name,
                'price': price
            }
            if 'products' not in self.request:
                self.request['products'] = list()

            self.request['products'].append(product)

        def create_payload(self, seller_id):
            return {
                'iss': seller_id,
                'aud': self.AUDIENCE,
                'typ': self.TYPE,
                'exp': self.expiration,
                'iat': self.issued_at,
                'request': self.request
            }

    def __init__(self, config):
        self.seller_id = config['seller_id']
        self.seller_secret_key = config['seller_secret_key']

    def generate_token(self, description, seller_data, products, is_test_payment):
        payload = self.Payload()
        payload.set_issued_at(issued_at=int(time()))
        payload.set_expiration(exp=int(time()) + 3600)
        payload.add_property(field_name='currencyCode', field_value='KGS')
        payload.add_property(field_name='description', field_value=description)
        payload.add_property(field_name='sellerData', field_value=seller_data)

        total_sum = 0

        for item in products:
            payload.add_product(name=item['name'], price=item['price'])
            total_sum += float(item['price'])

        payload.add_property(field_name='totalSum', field_value=total_sum)
        payload.add_property(field_name='test', field_value=is_test_payment)

        token = payload.create_payload(seller_id=self.seller_id)

        return jwt.encode(token, self.seller_secret_key)

    def get_payload_for_payment(self, post_body):
        return jwt.decode(post_body, self.seller_secret_key, audience=self.Payload.AUDIENCE)


class MobilnikPayEvent(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MobilnikPayEvent, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        transaction = TransactionKeys.objects.get(id=request.POST.get('transaction_id'))
        mobilnik = MobilnikPaymentService({'seller_id': SELLER_ID,
                                           'seller_secret_key': SELLER_SECRET})
        token = mobilnik.generate_token(transaction.handler.first_name,
                                        {'transaction_id': transaction.pk, 'user_id': request.user.pk},
                                        [{'name': transaction.handler.first_name, 'price': transaction.product.price1}],
                                        False)

        return JsonResponse(dict(token=token.decode('utf-8'), seller_id=SELLER_ID))


def mobilnik_response(request):
    data = request.body.decode('utf-8')
    mobilnik = MobilnikPaymentService({'seller_id': SELLER_ID,
                                       'seller_secret_key': SELLER_SECRET})
    decode_response = mobilnik.get_payload_for_payment(data)

    request_info = decode_response['request']['sellerData']

    response_info = decode_response['response']
    transaction = TransactionKeys.objects.get(pk=request_info['transaction_id'])
    transaction.confirm_as_admin()
    return HttpResponse(response_info['orderId'], status=200)
