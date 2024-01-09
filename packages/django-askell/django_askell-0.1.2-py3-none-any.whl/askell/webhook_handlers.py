from django.utils import timezone


def payment_created(request, event, data):
    from .models import Payment
    if event == 'payment.created':
        payment_data = {key: data[key] for key in Payment.KEYS_TO_COPY}
        payment_data['user'] = request.user
        uuid = data.pop('uuid')
        Payment.objects.get_or_create(uuid=uuid, defaults=payment_data)
    return True

def payment_changed(request, event, data):
    from .models import Payment
    if event == 'payment.changed':
        payment = Payment.objects.get(uuid=data['uuid'])
        for attr, val in data.items():
            setattr(payment, attr, val)
        if data['state'] == 'settled':
            payment.settled = True
            payment.settled_at = timezone.now()
        payment.save()
    return True