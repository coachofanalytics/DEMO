from django import forms
from marketing.models import Ads,Whatsapp_Groups
from django.utils.translation import gettext_lazy as _


class WhatsappForm(forms.ModelForm):
    class Meta:
        model = Whatsapp_Groups #Whatsapp
        fields = [
                    "category",
                    "type",
                    "group_name",
                    "group_id",
                    "is_active",
                    "is_featured",
        ]
        labels = {
                    "group_name":"Enter Whatsapp Group",
                    "group_id ":"Enter Whatsapp Group id",
                    "type":"ad_type",
        }


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads #Whatsapp
        fields = [
            "ad_title",
            "bulletin",
            "company",
            "short_name",
            "description",
            "company_site",
            "message",
            "meeting_link",
            "video_link",
            "signature",
            "image_name",
            "link",
            "is_active",
            "is_featured",
        ]
        labels = {
                    "image_name":"Select image_name",
                    "description":"What does your company do?",
                    "message":"Describe the ad message to be posted",
}   