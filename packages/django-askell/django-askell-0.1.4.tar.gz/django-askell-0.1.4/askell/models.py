import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from .webhooks import register_webhook_handler
from .webhook_handlers import payment_created, payment_updated

user_model = get_user_model()


class Payment(models.Model):

    KEYS_TO_COPY = ['description', 'reference', 'amount', 'currency']

    uuid = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    description = models.CharField(max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    settled_at = models.DateTimeField(blank=True, null=True, editable=False)
    settled = models.BooleanField(default=False)
    reference = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(user_model, blank=True, null=True, on_delete=models.SET_NULL, related_name='payments')

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)
        self.__original_settled = self.settled
   
    def save(self, *args, **kwargs):
        if self.__original_settled != self.settled and self.settled:	
            self.settled_at = timezone.now()
        super().save(*args, **kwargs)

    def as_dict(self):
        return {
            'uuid': self.uuid,
            'description': self.description,
            'created_at': self.created_at,
            'settled_at': self.settled_at,
            'settled': self.settled,
            'reference': self.reference,
            'amount': self.amount,
            'currency': self.currency,
            'user': self.user.id if self.user else None,
        }

register_webhook_handler(payment_created)
register_webhook_handler(payment_updated)

# @register_snippet
# class Subscription(models.Model):
#     user = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.SET_NULL, related_name='subscriptions')
#     reference = models.CharField(max_length=255)
#     active_until = models.DateTimeField(blank=True, null=True)
#     token = models.CharField(max_length=100, blank=True)
#     active = models.BooleanField(default=False)
#     is_on_trial = models.BooleanField(default=False)
#     plan = models.ForeignKey('askell.Plan', to_field='plan_id', on_delete=models.CASCADE, null=True, blank=True)
#     description = models.CharField(max_length=1024, blank=True, null=True)
#     subscription_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    
#     def __str__(self):
#         if self.user:
#             return f"Subscription for {self.user.username} ({self.user.id})"
#         else:
#             return f"Subscription for {self.reference} (no user linked)"

#     panels = [
#         FieldPanel('user'),
#         FieldPanel('reference'),
#         FieldPanel('active_until'),
#         FieldPanel('token'),
#         FieldPanel('active'),
#         FieldPanel('is_on_trial'),
#         FieldPanel('plan'),
#         FieldPanel('description'),
#         FieldPanel('subscription_id'),
#     ]

# @register_snippet
# class Plan(ClusterableModel):
#     name = models.CharField(max_length=512)
#     alternative_name = models.CharField(max_length=512, blank=True, null=True)
#     reference = models.CharField(max_length=512, blank=True, null=True)
#     interval = models.CharField(max_length=50, blank=True, null=True)
#     interval_count = models.IntegerField(blank=True, null=True)
#     amount = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
#     currency = models.CharField(max_length=10, blank=True, null=True)
#     trial_period_days = models.IntegerField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     description_richtext = RichTextField(blank=True, null=True)
#     enabled = models.BooleanField(default=False)
#     private = models.BooleanField(default=False)
#     electronic_only = models.BooleanField(default=True)
#     plan_id = models.PositiveIntegerField(unique=True)
#     offer = models.BooleanField(default=False)
#     offer_code = models.CharField(max_length=255, default='', blank=True)
    
#     panels = [
#         FieldPanel('name'),
#         FieldPanel('description'),
#         FieldPanel('description_richtext'),
#         FieldPanel('interval'),
#         FieldPanel('interval_count'),
#         FieldPanel('amount'),
#         FieldPanel('currency'),
#         FieldPanel('trial_period_days'),
#         FieldPanel('enabled'),
#         FieldPanel('private'),
#         MultiFieldPanel([
#             FieldPanel('offer'),
#             FieldPanel('offer_code'),
#         ], heading="Offer parameters"),
#         FieldPanel('plan_id'),
#         FieldPanel('alternative_name'),
#         FieldPanel('electronic_only'),
#         FieldPanel('reference'),
#         InlinePanel('groups', heading="Groups to assign to users in plan"),
#     ]

#     def __str__(self):
#         return self.name

#     def subscription_groups(self):
#         return ', '.join([g.group.name for g in self.groups.all()])


# @register_snippet
# class PlanGroups(models.Model):

#     plan = ParentalKey(Plan, related_name='groups', on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)

#     panels = [
#          MultiFieldPanel(
#             [
#                 FieldPanel("plan"),
#                 FieldPanel("group"),
#             ],
#             heading="Plan / Group relations",
#         ),
#     ]

#     def __str__(self):
#         return f"{self.plan.name} -> {self.group.name}"

