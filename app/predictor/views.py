import os
import pickle
from typing import Any

import pandas as pd
from django.shortcuts import redirect
# from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from ECEC.settings import PROJECT_ROOT
from predictor.forms import DetectionForm


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        result = self.request.GET.get("result")

        try:
            context["result"] = str(result)

        except ValueError:
            context["result"] = 'Benign'

        return context


class PredictFormView(FormView):
    form_class = DetectionForm
    template_name = 'predict.html'
    loaded_model = pickle.load(open(os.path.join(PROJECT_ROOT, "best_model.pkl"), "rb"))

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        data_list = list(cleaned_data.values())
        # return redirect(f"{reverse_lazy('predictor:success')}?result={data_list}")`
        return self.render_to_response(self.get_context_data(result=data_list))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["results"] = getattr(self, "result", None)
        return context

    def predict(self, data):
        # data_df = pd.DataFrame(data)
        #
        # if self.loaded_model.predict(data_df) == 0:
        #     predicted_class = 'Not Eligible'
        # else:
        #     predicted_class = 'Eligible'

        return data

    # data = pd.DataFrame(data_list,
    #                     columns=['Applicant_Gender', 'Owned_Car', 'Owned_Realty', 'Total_Children', 'Total_Income',
    #                              'Income_Type', 'Education_Type', 'Family_Status', 'Housing_Type',
    #                              'Owned_Mobile_Phone', 'Owned_Work_Phone', 'Owned_Phone', 'Owned_Email',
    #                              'Job_Title', 'Total_Family_Members', 'Applicant_Age', 'Years_of_Working',
    #                              'Total_Bad_Debt', 'Total_Good_Debt'])
    # result = self.predict(data)


    # def form_valid(self, form):
    #     applicant_gender = form.cleaned_data['applicant_gender']
    #     owned_car = form.cleaned_data['owned_car']
    #     total_children = form.cleaned_data['total_children']
    #     total_income = form.cleaned_data['total_income']
    #     income_type = form.cleaned_data['income_type']
    #     education_type = form.cleaned_data['education_type']
    #     family_status = form.cleaned_data['family_status']
    #     housing_type = form.cleaned_data['housing_type']
    #     owned_mobile_phone = form.cleaned_data['owned_mobile_phone']
    #     owned_work_phone = form.cleaned_data['owned_work_phone']
    #     owned_phone = form.cleaned_data['owned_phone']
    #     owned_Email = form.cleaned_data['owned_Email']
    #     job_title = form.cleaned_data['job_title']
    #     total_family_members = form.cleaned_data['total_family_members']
    #     applicant_age = form.cleaned_data['applicant_age']
    #     years_of_working = form.cleaned_data['years_of_working']
    #     total_bad_depth = form.cleaned_data['total_bad_depth']
    #     total_good_depth = form.cleaned_data['total_good_depth']
