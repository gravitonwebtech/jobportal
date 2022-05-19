from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from pyparsing import empty

from accounts.forms import EmployerProfileUpdateForm
from accounts.models import FullDetailEmployer, User
from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm
from jobsapp.models import Applicant, Job
from tags.models import Tag
from django.shortcuts import redirect, render



class DashboardView(ListView):
    model = Job
    # template_name = "jobs/employer/dashboard.html"
    template_name = "dash/dashboardEmp.html"
    context_object_name = "jobs"
    
    # for the form cretion in the dashboard
    form_class = CreateJobForm
    extra_context = {"title": "Post New Job"}
    success_url = reverse_lazy("jobs:employer-dashboard")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy("accounts:login")
        if self.request.user.is_authenticated and self.request.user.role != "employer":
            return reverse_lazy("accounts:login")
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        data=[]
        s=FullDetailEmployer.objects.filter(employerData=self.request.user)
        if s.exists():
            print("exist")
            context["checkUserDetails"]=True
        else:
            context["checkUserDetails"]=None
            print("not exist")
        count=0 
        value=Job.objects.filter(user_id=self.request.user.id).count()
        data.append(value)
        context['PostJobCount']=data
        context["x"] =FullDetailEmployer.objects.filter(employerData_id=self.request.user)
        print("@@@in emplopyer table printing the user full details ",self.request.user.password)
        print(context['PostJobCount'])
        context["userData"] = User.objects.get(email=self.request.user)
        print('checking the user context' ,self.request.user.role)
        context['PostJobCount1']=Job.objects.filter(user_id=self.request.user.id)
        print("checking jobPosted count",context['PostJobCount'])
        context["applicant"]=Applicant.objects.filter(comment="x.id")
        print("helloworld")
        if context["applicant"].exists():
            applicantIs=True
        else:
            applicantIs=None
        context["applicantIs"]=applicantIs
        for x in context['PostJobCount1']:
            if Applicant.objects.filter(job=x.id).exists():
                count=count+1
                x=Applicant.objects.filter(job=x.id)
                context["applicant"]=context["applicant"].union(x)
        # print("this is the count value ",context["applicant"])
        context["applicant"]=context["applicant"][0:3]
        print("!!@contect value need to check",type(context["applicant"]))
        print("helloword second time")
        if context["applicant"] is not empty:
            context["isApplicant"]=True
            print("value is going inseid ")
        else:
            context["isApplicant"]=None
        context['applicantCount']=count
        print("hellowrod third time ")
        context["job"]=Job.objects.filter(user_id=self.request.user.id).distinct()[0:10]
        context["viewProfile"]=FullDetailEmployer.objects.filter(employerData=self.request.user)
        print("view profile ",context["viewProfile"])
        if context["viewProfile"].exists():
            context["viewProfileVar"]=True
        else:
            context["viewProfileVar"]=None
        print(context['job'])
        print("hellowrld fourth time")
        context["tags"] = Tag.objects.all()
        print(type(context['PostJobCount']))
        context["allApplicant"] = Applicant.objects.filter(job__user_id=self.request.user.id).order_by("id")
        print("chekcing all applicant",context["allApplicant"])
        return context
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def get_queryset(self,**kwargs):
        context = {}
        data=[]
        count=0 
        value=Job.objects.filter(user_id=self.request.user.id).count()
        # context['PostJobCount']=[context['PostJobCount']]
        data.append(value)
        context['PostJobCount']=data
        print(context['PostJobCount'])
        context['PostJobCount1']=Job.objects.filter(user_id=self.request.user.id)
        print("checking jobPosted count",context['PostJobCount'])
        context["applicant"]=Applicant.objects.filter(comment="x.id")
        for x in context['PostJobCount1']:
            if Applicant.objects.filter(job=x.id).exists():
                count=count+1
                x=Applicant.objects.filter(job=x.id)
                context["applicant"]=context["applicant"].union(x)
        # print("this is the count value ",context["applicant"])
        context["applicant"]=context["applicant"][0:3]
        context['applicantCount']=count
        context["job"]=Job.objects.all().distinct()[0:10]
        print(context['job'])
        print(type(context['PostJobCount']))
        context["allApplicant"] = Applicant.objects.filter(job__user_id=self.request.user.id).order_by("id")
        print("chekcing all applicant",context["allApplicant"])
        # if "status" in self.request.GET and len(self.request.GET.get("status")) > 0:
        #     self.queryset = self.queryset.filter(status=int(self.request.GET.get("status"))
        # print("context",context)
        return context


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = "jobs/employer/applicants.html"
    context_object_name = "applicants"
    paginate_by = 6

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs["job_id"]).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = Job.objects.get(id=self.kwargs["job_id"])
        return context


class JobCreateView(CreateView):
    template_name = "dash/dashboardEmp.html"
    form_class = CreateJobForm
    extra_context = {"title": "Post New Job"}
    success_url = reverse_lazy("jobs:employer-dashboard")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy("accounts:login")
        if self.request.user.is_authenticated and self.request.user.role != "employer":
            return reverse_lazy("accounts:login")
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class JobUpdateView(UpdateView):
    template_name = "jobs/update.html"
    form_class = CreateJobForm
    extra_context = {"title": "Edit Job"}
    slug_field = "id"
    slug_url_kwarg = "id"
    success_url = reverse_lazy("jobs:employer-dashboard")
    context_object_name = "job"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Job updated successfully")
        return super(JobUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ApplicantsListView(ListView):
    model = Applicant
    template_name = "jobs/employer/all-applicants.html"
    context_object_name = "applicants"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        # return self.model.objects.filter(job__user_id=self.request.user.id)
        self.queryset = self.model.objects.filter(job__user_id=self.request.user.id).order_by("id")
        if "status" in self.request.GET and len(self.request.GET.get("status")) > 0:
            self.queryset = self.queryset.filter(status=int(self.request.GET.get("status")))
        return self.queryset


@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def filled(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        job.filled = True
        job.save()
    except IntegrityError as e:
        return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))
    return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class AppliedApplicantView(DetailView):
    model = Applicant
    template_name = "jobs/employer/applied-applicant-view.html"
    context_object_name = "applicant"
    slug_field = "id"
    slug_url_kwarg = "applicant_id"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.select_related("job").filter(job_id=self.kwargs["job_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class SendResponseView(UpdateView):
    model = Applicant
    http_method_names = ["post"]
    pk_url_kwarg = "applicant_id"
    fields = ("status", "comment")

    def get_success_url(self):
        return reverse_lazy(
            "jobs:applied-applicant-view",
            kwargs={"job_id": self.request.POST.get("job_id"), "applicant_id": self.get_object().id},
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != request.POST.get("status"):
            if request.POST.get("status") == "1":
                status = "Pending"
            elif request.POST.get("status") == "2":
                status = "Accepted"
            else:
                status = "Rejected"
            messages.success(self.request, "Response was successfully sent")
            # notify_candidate_about_job_status_change.delay(self.object.user.get_full_name(), self.object.user.email, self.object.job.id, self.object.job.title, status)
        else:
            messages.warning(self.request, "Response already sent")
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query" % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class EmployerProfileEditView(UpdateView):
    form_class = EmployerProfileUpdateForm
    context_object_name = "employer"
    template_name = "jobs/employer/edit-profile.html"
    success_url = reverse_lazy("accounts:employer-profile-update")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

def EmployerProfileEdit(request):
    data =FullDetailEmployer.objects.filter(employerData=request.user)
    print("checking that is exist",s)
    if s.exists():
        print("exist")
        context["checkUserDetails"]=True
    else:
        context["checkUserDetails"]=None
    print("employer profile data",data)
    context={"data":data}
    return render(request,"jobs/employer/edit-profile.html",context)