from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import users, Task

# Create your views here.

@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    
    # Check if all tasks are now completed (for confetti message)
    all_tasks = Task.objects.filter(user=request.user)
    total = all_tasks.count()
    completed = all_tasks.filter(completed=True).count()
    
    if total > 0 and completed == total:
        messages.success(request, '🎉 Amazing! All tasks completed! 🎉')
    
    return redirect('tasks')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterView(CreateView):
    model = users
    form_class = RegisterForm
    template_name = 'base/register.html'
    success_url = reverse_lazy('tasks')
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)
    
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/tasks.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user)
        
        # Search functionality
        search_input = self.request.GET.get('search', '')
        if search_input:
            tasks = tasks.filter(
                Q(title__icontains=search_input) | 
                Q(description__icontains=search_input)
            )
        
        # Filter functionality
        filter_by = self.request.GET.get('filter', 'all')
        if filter_by == 'active':
            tasks = tasks.filter(completed=False)
        elif filter_by == 'completed':
            tasks = tasks.filter(completed=True)
        elif filter_by in ['High', 'Medium', 'Low']:
            tasks = tasks.filter(priority=filter_by)
        
        # Calculate progress for the progress bar
        total_count = tasks.count()
        completed_count = tasks.filter(completed=True).count()
        progress_percent = (completed_count / total_count * 100) if total_count > 0 else 0
        
        # Check if all tasks are completed (for confetti message)
        all_completed = (total_count > 0 and completed_count == total_count)
        
        # Show confetti message if all tasks completed
        if all_completed and not self.request.session.get('confetti_shown'):
            messages.success(self.request, '🎉 Congratulations! All tasks completed! 🎉')
            self.request.session['confetti_shown'] = True
        elif not all_completed:
            self.request.session['confetti_shown'] = False
        
        context['tasks'] = tasks
        context['search_input'] = search_input
        context['filter_by'] = filter_by
        context['total_count'] = total_count
        context['completed_count'] = completed_count
        context['progress_percent'] = int(progress_percent)
        context['count'] = tasks.filter(completed=False).count()  # Keep for backward compatibility
        
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'completed']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'priority', 'completed']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_delete.html'

def toggle_theme(request):
    if request.method == 'POST':
        if request.session.get('theme') == 'light':
            request.session['theme'] = 'dark'
        else:
            request.session['theme'] = 'light'
    return redirect(request.META.get('HTTP_REFERER', 'tasks'))