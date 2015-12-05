from django.db.models import Q
import autocomplete_light
from family.models import Person

class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = Person

    def choices_for_request(self):
        if self.request.user.is_staff:
            q = self.request.GET.get('q', '')
            if q:
                import re
                choices = self.choices.all()
                names=re.findall(r"[\w']+", q, re.UNICODE)
                name1=names[0].strip()
                if len(names) >1:
                    name2=names[1].strip()
                    if len(name2)>0:
                        choices = choices.filter(
                            (Q(first__icontains=name1) & Q(last__icontains=name2)) |
                            (Q(first__icontains=name2) & Q(last__icontains=name1))
                        )
                    else:    
                        choices = choices.filter(Q(first__icontains=name1) | Q(last__icontains=name1) | Q(chinese__icontains=name1))
                else:
                    choices = choices.filter(Q(first__icontains=name1) | Q(last__icontains=name1)  | Q(chinese__icontains=name1))

            return self.order_choices(choices)[0:self.limit_choices]
        else:
            return Person.objects.none()
    
autocomplete_light.register(PersonAutocomplete)
