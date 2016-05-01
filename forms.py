from django import forms
from .models import Review


# ##############################################################################
#                                                                    REVIEW FORM
# ##############################################################################
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # The associated model for this form

        # The only fields we need for this form, are the fields that the user
        # needs to insert manually (the rating, and the comment).
        # The other information:
        #   - author:    Is retrieved from the person that is logged in
        #   - pub_date:  Auto-generated using datetime.now()
        #   - item:      Retreived from the page that is requested.
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'cols': 40, 'rows': 15})
        }
