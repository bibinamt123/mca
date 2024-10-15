from django.contrib import admin
from .models import Product, Order, DeliveryBoy, Feedback1,Cart,Payment

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image', 'manufacture_date', 'expiry_date', 'quantity')
    list_editable = ('quantity',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'address', 'created_at', 'payment_status')  # Added payment_status field

    # Method to display payment status in the admin panel
    def payment_status(self, obj):
        # Check if the payment exists for the order
        payment = Payment.objects.filter(order=obj).first()
        if payment:
            return payment.status  # Shows the payment status (e.g., 'Pending', 'Success')
        return "Not Paid"  # Default message if no payment is found

    payment_status.short_description = 'Payment Status'



@admin.register(DeliveryBoy)
class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment', 'reply')
    search_fields = ('user__username', 'product__name', 'comment')
    list_filter = ('rating', 'product')

    def save_model(self, request, obj, form, change):
        if 'reply' in form.changed_data:
            # Notify the user via email when the admin replies
            if obj.user and obj.reply:
                subject = f"Reply to your feedback on {obj.product.name}"
                message = f"Dear {obj.user.username},\n\nThank you for your feedback on {obj.product.name}.\n\nAdmin's reply: {obj.reply}\n\nBest regards,\nYour Company Name"
                obj.user.email_user(subject, message)
        super().save_model(request, obj, form, change)

admin.site.register(Feedback1, FeedbackAdmin)
