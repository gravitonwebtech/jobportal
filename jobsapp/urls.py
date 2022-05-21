from django.test import testcases
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "jobs"

urlpatterns = [
    path("", HomeView, name="home"),
    path("favorite/", favorite, name="favorite"),
    path("search/", SearchView.as_view(), name="search"),
    path(
        "employer/dashboard/",
        include(
            [
                path("", DashboardView.as_view(), name="employer-dashboard"),
                path(
                    "all-applicants/",
                    ApplicantsListView.as_view(),
                    name="employer-all-applicants",
                ),
                path(
                    "applicants/<int:job_id>/",
                    ApplicantPerJobView.as_view(),
                    name="employer-dashboard-applicants",
                ),
                path(
                    "applied-applicant/<int:job_id>/view/<int:applicant_id>",
                    AppliedApplicantView.as_view(),
                    name="applied-applicant-view",
                ),
                path("mark-filled/<int:job_id>/", filled, name="job-mark-filled"),
                path("send-response/<int:applicant_id>", SendResponseView.as_view(), name="applicant-send-response"),
                path("jobs/create/", JobCreateView.as_view(), name="employer-jobs-create"),
                path("jobs/<int:id>/edit/", JobUpdateView.as_view(), name="employer-jobs-edit"),
            ]
        ),
    ),
    path("employee/",
        include(
            [
                path(
                    "my-applications",
                    EmployeeMyJobsListView.as_view(),
                    name="employee-my-applications",
                ),
                path("favorites", FavoriteListView.as_view(), name="employee-favorites"),
            ]
        ),
    ),
    path("apply-job/<int:job_id>/", ApplyJobView.as_view(), name="apply-job"),
    path("jobs/", JobListView, name="jobs"),
    path("jobs/<int:id>/", JobDetailsView.as_view(), name="jobs-detail"),
    path("test/", HomeView1.as_view(), name="test"),
    path("testCandidate/", testCandidate.as_view(), name="testCandidate"),
    path("member/", member, name="member"),
    path("blog/", blog.as_view(), name="blog"),
    path("contact/", contact.as_view(), name="contact"),
    path("about/", about.as_view(), name="about"),
    path("profile/", profile, name="profile"),
    path("table/", table.as_view(), name="table"),
    path("billing/", billing.as_view(), name="billing"),
    path("changePassword/", changePassword, name="changePassword"),
    path("updateProfile/", EmployerProfileEditView.as_view(), name="updateProfile"),
    path('blogShow/<int:pk>', blogShow, name='blogShow'),
    path('updateEmployer/', updateEmployer, name='updateEmployer'),
    path('changePasswordEmp/', changePasswordEmp, name='changePasswordEmp'),
    path('candidates/', candidates, name='candidates'),
    path('candidatesFull/<int:pk>/', candidatesFull, name='candidatesFull'),
    path('shortValueCompany/<int:pk>', shortValueCompany, name='shortValueCompany'),
    path('shortValueLocation/<int:pk>', shortValueLocation, name='shortValueLocation'),
    path('shortValueTag/<int:pk>', shortValueTag, name='shortValueTag'),
    path("home", Home, name="Home"),
    # path('blog1/', blog, name='blog'),
    path('changePasswordEmp/', changePasswordEmp, name='changePasswordEmp'),
    # path('blog1/', blog, name='blog'),
    path("postjob/", postjob, name="postjob"),
    path("postjobDash/", postjobDash, name="postjobDash"),
    path("viewProfile/", viewProfile, name="viewProfile"),
    path("companyProfile/", companyProfile, name="companyProfile"),
    path("changepassword/", changepassword, name="changepassword"),
    path("QuizAdmin/",QuizAdmin,name="QuizAdmin"),
    path("category/<str:value>",category,name="category"),
    path("terms/",terms,name="terms"),
    path("email/",email,name="email"),
    path("memberplan/",memberplan,name="memberplan"),
    path("forgetPassword/",forgetPassword,name="forgetPassword"),
    path("userPassword/",userPassword ,name="userPassword"),
    path("completeMember/",completeMember,name="completeMember"),
    path("checkout/",checkout,name="checkout"),
    path("privacy/",privacy,name="privacy"),
    path("memberplanPricing/<int:pk>",memberplanPricing,name="memberplanPricing"),
    path("memberplanPricingEmployer",memberplanPricingEmployer,name="memberplanPricingEmployer"),
    path("successUrl/",successUrl,name="successUrl"),
    path("posted_jobs/<int:pk>",home.posted_jobs,name='posted_jobs'),
    path("updateJob/",home.updateJob,name='updateJob'),
    path('accounts/', include('allauth.urls')),
    path('people_applied/<int:pk>',home.ApplicantsApplied,name="people_applied"),
    path('statusChange/<int:pk>/<int:ck>',statusChange,name="statusChange"),
    path('career/',careerAdv ,name="career"),
    path("allCourse",allCourse,name="allCourse"),
    path("trainingCertificates/<int:pk>",trainingCertificates,name="trainingCertificates"),
    path("traninPlacementDetails/<int:pk>",traninPlacementDetails,name="traninPlacementDetails"),
    path("myjobs/",myjobs,name="myjobs"),
    path("memberplanPricingTraining/<int:pk>",memberplanPricingTraining,name="memberplanPricingTraining"),
    path('jobtypes/<int:pk>',jobtypes,name="jobtypes"),
    path('RefundPolicy/',RefundPolicy,name="RefundPolicy"),
    path("viewallPrimum/",viewallPrimum,name="viewallPrimum"),
    path("featuredProfile/",featuredProfile,name="featuredProfile"),
    path("resumeWriting/",resumeWriting,name="resumeWriting"),
    path("careerBooster/",careerBooster,name="careerBooster"),
    path("profileHightligter/",profileHightligter,name="profileHightligter"),
    path("linkdinMakeover/",linkdinMakeover,name="linkdinMakeover"),
    path("mockInterview/",mockInterview,name="mockInterview"),
    path("faqEmp/",faqEmp,name="faqEmp"),
    path("supportEmp/",supportEmp,name="supportEmp"),
    path("supportCandidate/",supportCandidate,name="supportCandidate"),
    path("documentEmp/",documentEmp,name="documentEmp")
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
