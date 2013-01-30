from django.contrib import admin

from checkin.models import *

def approve_request(modeladmin, request, queryset):
    for payment_request in queryset:
        payment_request.approve()
approve_request.short_description = "Approve selected requests"

def reject_request(modeladmin, request, queryset):
    for payment_request in queryset:
        payment_request.reject()
reject_request.short_description = "Reject selected requests"
    
class PaymentApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'date')
    actions = [approve_request, reject_request]
    def get_actions(self, request):
        actions = super(PaymentApprovalRequestAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
           del actions['delete_selected']
        return actions
        
admin.site.register(ClimberProfile)
admin.site.register(CaveOpening)
admin.site.register(PaymentApprovalRequest, PaymentApprovalRequestAdmin)
