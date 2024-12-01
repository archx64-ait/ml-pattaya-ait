import os
import pickle
from typing import Any

import pandas as pd
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from ECEC.settings import PROJECT_ROOT
from predictor.choices import columns
from predictor.forms import DetectionForm


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.request.GET.get("result")
        try:
            context["result"] = str(result)

        except ValueError:
            context["result"] = 'Not Eligible'

        return context


class PredictFormView(FormView):
    form_class = DetectionForm
    template_name = 'predict.html'
    loaded_model = pickle.load(open(os.path.join(PROJECT_ROOT, "best_model.pkl"), "rb"))

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        data_list = list(cleaned_data.values())
        result = self.predict(data_list)
        return redirect(f"{reverse_lazy('predictor:success')}?result={result}")

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["results"] = getattr(self, "result", None)
        return context

    def predict(self, data):
        data_df = pd.DataFrame([data], columns=columns)
        if self.loaded_model.predict(data_df) == 0:
            predicted_class = 'Not Eligible'
        else:
            predicted_class = 'Eligible'

        return predicted_class
