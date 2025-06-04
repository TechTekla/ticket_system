from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import User
from .forms import UserForm

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user-list')

class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user-list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user-list')
