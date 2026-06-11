from django import forms
from .models import ProviderPost, ServiceProfile


class ServiceProfileForm(forms.ModelForm):
    class Meta:
        model = ServiceProfile
        fields = [
            "profile_image",
            "business_name",
            "phone",
            "email",
            "location",
            "service_type",
            "available_days",
            "available_time",
            "description",
            "hourly_rate",
            "latitude",
            "longitude",
            "website",
            "facebook",
            "instagram",
            "tiktok",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional fields
        for field in ["website", "facebook", "instagram", "tiktok", "latitude", "longitude"]:
            self.fields[field].required = False
        self.fields["profile_image"].required = False

        # Placeholders
        placeholders = {
            "business_name":  "e.g. Ram Electricals",
            "phone":          "e.g. 9800000000",
            "email":          "e.g. you@example.com",
            "location":       "e.g. Kathmandu, Baneshwor",
            "available_days": "e.g. Mon–Fri",
            "available_time": "e.g. 9 AM – 6 PM",
            "description":    "Describe your experience and what you offer…",
            "hourly_rate":    "e.g. 500",
            "latitude":       "e.g. 27.717245",
            "longitude":      "e.g. 85.323960",
            "website":        "https://yourwebsite.com",
            "facebook":       "https://facebook.com/yourpage",
            "instagram":      "https://instagram.com/yourhandle",
            "tiktok":         "https://tiktok.com/@yourhandle",
        }
        for name, placeholder in placeholders.items():
            if name in self.fields:
                self.fields[name].widget.attrs["placeholder"] = placeholder

        # Coord fields: read-friendly number inputs
        for coord in ["latitude", "longitude"]:
            self.fields[coord].widget = forms.NumberInput(attrs={
                "placeholder": placeholders[coord],
                "step": "any",
            })

        # Style the service_type dropdown
        self.fields["service_type"].widget.attrs.update({
            "class": "sp-select"
        })



class ProviderPostForm(forms.ModelForm):
    class Meta:
        model = ProviderPost
        fields = ['title', 'description', 'address', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")

        # Must upload only one
        if image and video:
            raise forms.ValidationError("Upload only ONE: image or video.")

        if not image and not video:
            raise forms.ValidationError("You must upload either image or video.")

        # File size limit 10MB
        if image and image.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Image size must be under 10MB.")

        if video and video.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Video size must be under 10MB.")

        return cleaned_data