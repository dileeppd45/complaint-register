from compliant import views
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login1', views.login1, name='login1'),

    path('logout', views.logout, name='logout'),
    path('AdminHomePage', views.AdminHomePage, name='AdminHomePage'),
    path('DepartmentHome', views.DepartmentHome, name='DepartmentHome'),
    path('Addcategory', views.Addcategory, name='Addcategory'),
path('ViewFeedbackAdmin', views.ViewFeedbackAdmin, name='ViewFeedbackAdmin'),
path('ViewFeedbackNltkAdmin', views.ViewFeedbackNltkAdmin, name='ViewFeedbackNltkAdmin'),
path('admin_reply_feedback', views.admin_reply_feedback, name='admin_reply_feedback'),
path('check_feedback/<int:id>', views.check_feedback, name='check_feedback'),
    path('viewCategory', views.viewCategory, name='viewCategory'),
    path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('editCategory/<int:id>', views.editCategory, name='editCategory'),
    path('updatecategory/<int:id>', views.updatecategory, name='updatecategory'),
    path('AddDepartment/<int:id>', views.AddDepartment, name='AddDepartment'),
    path('viewDepartment/<int:id>', views.viewDepartment, name='viewDepartment'),
    path('assignpincode/<int:id>/<str:sid>', views.assignpincode, name='assignpincode'),
    path('ViewPincode/<int:id>', views.ViewPincode, name='ViewPincode'),
    path('editpincode/<int:id>', views.editpincode, name='editpincode'),
    path('updatepincode/<int:id>', views.updatepincode, name='updatepincode'),
    path('deletepincode/<int:id>', views.deletepincode, name='deletepincode'),
    path('editDepartment/<int:id>', views.editDepartment, name='editDepartment'),
    path('updateDepartment/<int:id>', views.updateDepartment, name='updateDepartment'),
    path('deletedepart/<int:id>', views.deletedepart, name='deletedepart'),
    path('viewCategory_cmp', views.viewCategory_cmp, name='viewCategory_cmp'),
    path('DepartmentComplaints/<int:id>', views.DepartmentComplaints, name='DepartmentComplaints'),
    path('DepaComps/<int:id>/<str:sid>', views.DepaComps, name='DepaComps'),
    path('Viewchats/<int:id>', views.Viewchats, name='Viewchats'),
    path('Count', views.Count, name='Count'),
    path('view_graph', views.view_graph, name='view_graph'),
    path('CountCmp/<int:id>', views.CountCmp, name='CountCmp'),
    path('DepNOtify', views.DepNOtify, name='DepNOtify'),
    path('View_Department_N/<int:id>', views.View_Department_N, name='View_Department_N'),
    path('admin_reply_query/<int:id>', views.admin_reply_query, name='admin_reply_query'),
    path('admin_reply_query_action', views.admin_reply_query_action, name='admin_reply_query_action'),
    path('branch_graphs', views.branch_graphs, name='branch_graphs'),
    path('admin_view_querry', views.admin_view_querry, name='admin_view_querry'),
    path('linkSendNotification/<int:id>', views.linkSendNotification, name='linkSendNotification'),
    path('SendNotification', views.SendNotification, name='SendNotification'),
    path('ViewNotification', views.ViewNotification, name='ViewNotification'),
    path('searchusercompliant', views.searchusercompliant, name='searchusercompliant'),
    path('AddStaff', views.AddStaff, name='AddStaff'),
    path('ViewStaff', views.ViewStaff, name='ViewStaff'),
    path('DeleStaff/<str:sid>', views.DeleStaff, name='DeleStaff'),
    path('Viewdepacmplaint', views.Viewdepacmplaint, name='Viewdepacmplaint'),
    path('ReplyComplaint/<int:id>', views.ReplyComplaint, name='ReplyComplaint'),
    path('Compliantbasedondate', views.Compliantbasedondate, name='Compliantbasedondate'),
    path('Department_Com_Date/<str:sid>', views.Department_Com_Date, name='Department_Com_Date'),
    path('DepartChat/<int:id>', views.DepartChat, name='DepartChat'),
    path('Pincodesearch', views.Pincodesearch, name='Pincodesearch'),
    path('ViewNotificationD', views.ViewNotificationD, name='ViewNotificationD'),
    path('User', views.User, name='User'),
    path('ViewMoreChat/<int:id>', views.ViewMoreChat, name='ViewMoreChat'),
    path('viewimage', views.viewimage, name='viewimage'),
    path('deleteimage/<int:id>', views.deleteimage, name='deleteimage'),
    path('replycomplaintaction', views.replycomplaintaction, name='replycomplaintaction'),


 ]