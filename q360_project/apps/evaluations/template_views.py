"""
Template-based views for evaluations app.
Complete implementation for all evaluation-related pages.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .models import (
    EvaluationCampaign, Question, QuestionCategory,
    EvaluationAssignment, Response, EvaluationResult, CampaignQuestion
)
from .forms import (
    EvaluationCampaignForm, QuestionForm, QuestionCategoryForm,
    ResponseForm, BulkAssignmentForm, CampaignQuestionForm
)
from apps.accounts.models import User


# ==================== Campaign Views ====================

class CampaignListView(LoginRequiredMixin, ListView):
    """List all evaluation campaigns."""
    model = EvaluationCampaign
    template_name = 'evaluations/campaign_list.html'
    context_object_name = 'campaigns'
    paginate_by = 10

    def get_queryset(self):
        queryset = EvaluationCampaign.objects.all()

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_campaigns'] = EvaluationCampaign.objects.count()
        context['active_campaigns'] = EvaluationCampaign.objects.filter(status='active').count()
        context['draft_campaigns'] = EvaluationCampaign.objects.filter(status='draft').count()
        return context


@method_decorator(cache_page(300), name='dispatch')  # 5 minutes cache
@method_decorator(vary_on_cookie, name='dispatch')  # Vary by user session
class CampaignDetailView(LoginRequiredMixin, DetailView):
    """View campaign details."""
    model = EvaluationCampaign
    template_name = 'evaluations/campaign_detail.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.object

        # Statistics
        context['total_assignments'] = campaign.assignments.count()
        context['completed_assignments'] = campaign.assignments.filter(status='completed').count()
        context['pending_assignments'] = campaign.assignments.filter(status='pending').count()
        context['completion_rate'] = campaign.get_completion_rate()

        # Questions
        context['total_questions'] = campaign.campaign_questions.count()

        # Recent assignments
        context['recent_assignments'] = campaign.assignments.select_related(
            'evaluator', 'evaluatee'
        ).order_by('-created_at')[:10]

        return context


class CampaignCreateView(LoginRequiredMixin, CreateView):
    """Create new evaluation campaign."""
    model = EvaluationCampaign
    form_class = EvaluationCampaignForm
    template_name = 'evaluations/campaign_form.html'
    success_url = reverse_lazy('evaluations:campaign-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Kampaniya uğurla yaradıldı.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Yeni Kampaniya'
        context['button_text'] = 'Yarat'
        return context


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing campaign."""
    model = EvaluationCampaign
    form_class = EvaluationCampaignForm
    template_name = 'evaluations/campaign_form.html'
    success_url = reverse_lazy('evaluations:campaign-list')

    def form_valid(self, form):
        messages.success(self.request, 'Kampaniya yeniləndi.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Kampaniyanı Redaktə Et'
        context['button_text'] = 'Yenilə'
        return context


@login_required
def campaign_activate(request, pk):
    """Activate a campaign."""
    campaign = get_object_or_404(EvaluationCampaign, pk=pk)

    if not request.user.is_admin():
        messages.error(request, 'Bu əməliyyatı yerinə yetirmək icazəniz yoxdur.')
        return redirect('evaluations:campaign-detail', pk=pk)

    campaign.status = 'active'
    campaign.save()
    messages.success(request, f'{campaign.title} kampaniyası aktivləşdirildi.')

    return redirect('evaluations:campaign-detail', pk=pk)


@login_required
def campaign_complete(request, pk):
    """Complete a campaign."""
    campaign = get_object_or_404(EvaluationCampaign, pk=pk)

    if not request.user.is_admin():
        messages.error(request, 'Bu əməliyyatı yerinə yetirmək icazəniz yoxdur.')
        return redirect('evaluations:campaign-detail', pk=pk)

    campaign.status = 'completed'
    campaign.save()
    messages.success(request, f'{campaign.title} kampaniyası tamamlandı.')

    return redirect('evaluations:campaign-detail', pk=pk)


@login_required
def campaign_questions_assign(request, campaign_pk):
    """Assign questions to a campaign."""
    campaign = get_object_or_404(EvaluationCampaign, pk=campaign_pk)

    if not request.user.is_admin():
        messages.error(request, 'Bu əməliyyatı yerinə yetirmək icazəniz yoxdur.')
        return redirect('evaluations:campaign-detail', pk=campaign_pk)

    if request.method == 'POST':
        form = CampaignQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            order = form.cleaned_data['order']

            # Check if question is already assigned
            if CampaignQuestion.objects.filter(campaign=campaign, question=question).exists():
                messages.error(request, 'Bu sual artıq kampaniyaya əlavə edilib.')
            else:
                # Create campaign question assignment
                CampaignQuestion.objects.create(
                    campaign=campaign,
                    question=question,
                    order=order
                )
                messages.success(request, f'Sual kampaniyaya əlavə edildi.')

            return redirect('evaluations:campaign-questions', campaign_pk=campaign_pk)
    else:
        form = CampaignQuestionForm()

    # Get all active questions grouped by category
    categories = QuestionCategory.objects.filter(is_active=True).prefetch_related('questions')

    # Get currently assigned questions with their order
    assigned_questions = CampaignQuestion.objects.filter(
        campaign=campaign
    ).select_related('question', 'question__category').order_by('order')

    context = {
        'campaign': campaign,
        'form': form,
        'categories': categories,
        'assigned_questions': assigned_questions,
    }

    return render(request, 'evaluations/campaign_questions_form.html', context)


# ==================== Assignment Views ====================

@login_required
def my_assignments(request):
    """View user's evaluation assignments."""
    user = request.user

    # Get assignments
    pending = EvaluationAssignment.objects.filter(
        evaluator=user,
        status__in=['pending', 'in_progress']
    ).select_related('campaign', 'evaluatee')

    completed = EvaluationAssignment.objects.filter(
        evaluator=user,
        status='completed'
    ).select_related('campaign', 'evaluatee')

    context = {
        'pending_assignments': pending,
        'completed_assignments': completed,
        'total_pending': pending.count(),
        'total_completed': completed.count(),
    }

    return render(request, 'evaluations/my_assignments.html', context)


@login_required
def assignment_detail(request, pk):
    """View assignment details and fill evaluation form."""
    assignment = get_object_or_404(
        EvaluationAssignment.objects.select_related('campaign', 'evaluator', 'evaluatee'),
        pk=pk
    )

    # Check permission
    if assignment.evaluator != request.user and not request.user.is_admin():
        messages.error(request, 'Bu qiymətləndirməyə giriş icazəniz yoxdur.')
        return redirect('evaluations:my-assignments')

    # Get questions for this campaign
    campaign_questions = CampaignQuestion.objects.filter(
        campaign=assignment.campaign
    ).select_related('question', 'question__category').order_by('order')

    questions = [cq.question for cq in campaign_questions]

    # Get existing responses
    existing_responses = {
        r.question_id: r for r in Response.objects.filter(assignment=assignment)
    }

    if request.method == 'POST':
        # Process form submission
        all_valid = True

        for question in questions:
            response = existing_responses.get(question.id)
            if not response:
                response = Response(assignment=assignment, question=question)

            # Get form data based on question type
            if question.question_type == 'scale':
                score = request.POST.get(f'question_{question.id}_score')
                if score:
                    response.score = int(score)
                elif question.is_required:
                    all_valid = False
                    messages.error(request, f'Sual "{question.text[:50]}..." cavablandırılmalıdır.')

            elif question.question_type == 'boolean':
                bool_answer = request.POST.get(f'question_{question.id}_boolean')
                if bool_answer is not None:
                    response.boolean_answer = bool_answer == 'true'
                elif question.is_required:
                    all_valid = False
                    messages.error(request, f'Sual "{question.text[:50]}..." cavablandırılmalıdır.')

            elif question.question_type == 'text':
                text_answer = request.POST.get(f'question_{question.id}_text')
                if text_answer:
                    response.text_answer = text_answer
                elif question.is_required:
                    all_valid = False
                    messages.error(request, f'Sual "{question.text[:50]}..." cavablandırılmalıdır.')

            # Get comment
            comment = request.POST.get(f'question_{question.id}_comment')
            if comment:
                response.comment = comment

            if all_valid or not question.is_required:
                response.save()

        if all_valid:
            # Mark assignment as completed
            assignment.status = 'completed'
            assignment.completed_at = timezone.now()
            assignment.save()

            messages.success(request, 'Qiymətləndirmə uğurla təqdim edildi!')
            return redirect('evaluations:my-assignments')

    # Calculate progress
    total_questions = len(questions)
    answered_questions = len(existing_responses)
    progress = (answered_questions / total_questions * 100) if total_questions > 0 else 0

    context = {
        'assignment': assignment,
        'questions': questions,
        'existing_responses': existing_responses,
        'progress': round(progress),
        'total_questions': total_questions,
        'answered_questions': answered_questions,
    }

    return render(request, 'evaluations/assignment_form.html', context)


@login_required
def assignment_save_draft(request, pk):
    """Save assignment as draft (AJAX)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    assignment = get_object_or_404(EvaluationAssignment, pk=pk)

    if assignment.evaluator != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    assignment.status = 'in_progress'
    if not assignment.started_at:
        assignment.started_at = timezone.now()
    assignment.save()

    return JsonResponse({'success': True, 'message': 'Qaralama saxlanıldı'})


@login_required
def assignment_cancel(request, pk):
    """Cancel an evaluation assignment."""
    if request.method != 'POST':
        messages.error(request, 'Yanlış sorğu.')
        return redirect('evaluations:my-assignments')

    assignment = get_object_or_404(EvaluationAssignment, pk=pk)

    # Check permission - only admin or campaign creator can cancel
    if not (request.user.is_admin() or assignment.campaign.created_by == request.user):
        messages.error(request, 'Bu tapşırığı ləğv etmək icazəniz yoxdur.')
        return redirect('evaluations:my-assignments')

    # Check if assignment can be cancelled
    if assignment.status == 'completed':
        messages.error(request, 'Tamamlanmış tapşırıq ləğv edilə bilməz.')
        return redirect('evaluations:campaign-detail', pk=assignment.campaign.pk)

    # Delete assignment and all related responses
    Response.objects.filter(assignment=assignment).delete()
    assignment.delete()

    messages.success(request, 'Tapşırıq ləğv edildi.')
    return redirect('evaluations:campaign-detail', pk=assignment.campaign.pk)


class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an evaluation assignment (CBV approach)."""
    model = EvaluationAssignment
    success_url = reverse_lazy('evaluations:my-assignments')

    def dispatch(self, request, *args, **kwargs):
        """Check permissions before processing."""
        assignment = self.get_object()

        # Check permission - only admin or campaign creator can delete
        if not (request.user.is_admin() or assignment.campaign.created_by == request.user):
            messages.error(request, 'Bu tapşırığı silmək icazəniz yoxdur.')
            return redirect('evaluations:my-assignments')

        # Check if assignment can be deleted
        if assignment.status == 'completed':
            messages.error(request, 'Tamamlanmış tapşırıq silinə bilməz.')
            return redirect('evaluations:campaign-detail', pk=assignment.campaign.pk)

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Override delete to also delete related responses."""
        assignment = self.get_object()
        campaign_pk = assignment.campaign.pk

        # Delete all related responses
        Response.objects.filter(assignment=assignment).delete()

        messages.success(request, 'Tapşırıq silindi.')
        self.success_url = reverse_lazy('evaluations:campaign-detail', kwargs={'pk': campaign_pk})

        return super().delete(request, *args, **kwargs)


@login_required
def campaign_question_delete(request, pk):
    """Delete a question from campaign."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    if not request.user.is_admin():
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    campaign_question = get_object_or_404(CampaignQuestion, pk=pk)
    campaign_question.delete()

    messages.success(request, 'Sual kampaniyadan silindi.')
    return JsonResponse({'success': True, 'message': 'Sual silindi'})


# ==================== Question Management ====================

class QuestionListView(LoginRequiredMixin, ListView):
    """List all questions."""
    model = Question
    template_name = 'evaluations/question_list.html'
    context_object_name = 'questions'
    paginate_by = 20

    def get_queryset(self):
        queryset = Question.objects.select_related('category').filter(is_active=True)

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)

        return queryset.order_by('category', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = QuestionCategory.objects.filter(is_active=True)
        context['total_questions'] = Question.objects.filter(is_active=True).count()
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """Create new question."""
    model = Question
    form_class = QuestionForm
    template_name = 'evaluations/question_form.html'
    success_url = reverse_lazy('evaluations:question-list')

    def form_valid(self, form):
        messages.success(self.request, 'Sual yaradıldı.')
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing question."""
    model = Question
    form_class = QuestionForm
    template_name = 'evaluations/question_form.html'
    success_url = reverse_lazy('evaluations:question-list')

    def form_valid(self, form):
        messages.success(self.request, 'Sual yeniləndi.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


@login_required
def question_delete(request, pk):
    """Delete (deactivate) a question."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    if not request.user.is_admin():
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    question = get_object_or_404(Question, pk=pk)
    question.is_active = False
    question.save()

    messages.success(request, f'Sual "{question.text[:50]}..." deaktiv edildi.')
    return JsonResponse({'success': True, 'message': 'Sual silindi'})


class QuestionCategoryListView(LoginRequiredMixin, ListView):
    """List question categories."""
    model = QuestionCategory
    template_name = 'evaluations/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return QuestionCategory.objects.annotate(
            question_count=Count('questions')
        ).filter(is_active=True)


@login_required
def category_create(request):
    """Create new question category."""
    if not request.user.is_admin():
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    order = request.POST.get('order', 0)

    if not name:
        return JsonResponse({'success': False, 'error': 'Kateqoriya adı tələb olunur'})

    try:
        category = QuestionCategory.objects.create(
            name=name,
            description=description,
            order=int(order) if order else 0
        )
        messages.success(request, f'"{name}" kateqoriyası yaradıldı.')
        return JsonResponse({
            'success': True,
            'message': 'Kateqoriya yaradıldı',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'order': category.order
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def category_update(request, pk):
    """Update question category."""
    if not request.user.is_admin():
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    category = get_object_or_404(QuestionCategory, pk=pk)

    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    order = request.POST.get('order', category.order)

    if not name:
        return JsonResponse({'success': False, 'error': 'Kateqoriya adı tələb olunur'})

    try:
        category.name = name
        category.description = description
        category.order = int(order) if order else 0
        category.save()

        messages.success(request, f'"{name}" kateqoriyası yeniləndi.')
        return JsonResponse({
            'success': True,
            'message': 'Kateqoriya yeniləndi',
            'category': {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'order': category.order
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def category_delete(request, pk):
    """Delete (deactivate) a question category."""
    if not request.user.is_admin():
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    category = get_object_or_404(QuestionCategory, pk=pk)

    # Check if category has active questions
    active_questions_count = category.questions.filter(is_active=True).count()

    if active_questions_count > 0:
        return JsonResponse({
            'success': False,
            'error': f'Bu kateqoriyada {active_questions_count} aktiv sual var. Əvvəlcə sualları silməlisiniz.'
        })

    # Soft delete
    category.is_active = False
    category.save()

    messages.success(request, f'"{category.name}" kateqoriyası silindi.')
    return JsonResponse({'success': True, 'message': 'Kateqoriya silindi'})


# ==================== Results Views ====================

@login_required
def evaluation_results(request, campaign_pk):
    """View evaluation results for a campaign."""
    campaign = get_object_or_404(EvaluationCampaign, pk=campaign_pk)

    # Check permission
    if not request.user.is_admin() and campaign.created_by != request.user:
        messages.error(request, 'Bu hesabata baxmaq icazəniz yoxdur.')
        return redirect('evaluations:campaign-list')

    # Get results
    results = EvaluationResult.objects.filter(
        campaign=campaign
    ).select_related('evaluatee').order_by('-overall_score')

    # Statistics
    total_evaluatees = results.count()
    avg_score = results.aggregate(Avg('overall_score'))['overall_score__avg']

    context = {
        'campaign': campaign,
        'results': results,
        'total_evaluatees': total_evaluatees,
        'avg_score': avg_score,
    }

    return render(request, 'evaluations/results.html', context)


@login_required
def individual_result(request, result_pk):
    """View individual evaluation result."""
    result = get_object_or_404(
        EvaluationResult.objects.select_related('campaign', 'evaluatee'),
        pk=result_pk
    )

    # Check permission
    if not (request.user.is_admin() or
            result.evaluatee == request.user or
            result.campaign.created_by == request.user):
        messages.error(request, 'Bu hesabata baxmaq icazəniz yoxdur.')
        return redirect('dashboard')

    # Get detailed responses
    assignments = EvaluationAssignment.objects.filter(
        campaign=result.campaign,
        evaluatee=result.evaluatee,
        status='completed'
    ).select_related('evaluator')

    # Category scores
    category_scores = {}
    for assignment in assignments:
        responses = Response.objects.filter(
            assignment=assignment,
            score__isnull=False
        ).select_related('question__category')

        for response in responses:
            category = response.question.category.name
            if category not in category_scores:
                category_scores[category] = {
                    'self': [],
                    'supervisor': [],
                    'peer': [],
                    'subordinate': []
                }

            category_scores[category][assignment.relationship].append(response.score)

    # Calculate averages
    chart_data = {
        'categories': [],
        'self': [],
        'supervisor': [],
        'peer': [],
        'subordinate': [],
        'average': []
    }

    for category, scores in category_scores.items():
        chart_data['categories'].append(category)

        for rel_type in ['self', 'supervisor', 'peer', 'subordinate']:
            if scores[rel_type]:
                avg = sum(scores[rel_type]) / len(scores[rel_type])
                chart_data[rel_type].append(round(avg, 2))
            else:
                chart_data[rel_type].append(0)

        # Overall average for this category
        all_scores = []
        for rel_scores in scores.values():
            all_scores.extend(rel_scores)
        if all_scores:
            chart_data['average'].append(round(sum(all_scores) / len(all_scores), 2))
        else:
            chart_data['average'].append(0)

    context = {
        'result': result,
        'assignments': assignments,
        'chart_data': chart_data,
    }

    return render(request, 'evaluations/individual_result.html', context)


# ==================== Bulk Operations ====================

@login_required
def bulk_assign(request):
    """Bulk create evaluation assignments."""
    if not request.user.is_admin():
        messages.error(request, 'Bu əməliyyatı yerinə yetirmək icazəniz yoxdur.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = BulkAssignmentForm(request.POST)
        if form.is_valid():
            campaign = form.cleaned_data['campaign']
            include_self = form.cleaned_data['include_self_evaluation']
            include_supervisor = form.cleaned_data['include_supervisor']
            include_peers = form.cleaned_data['include_peers']
            include_subordinates = form.cleaned_data['include_subordinates']

            created_count = 0
            users = User.objects.filter(is_active=True)

            for user in users:
                # Self evaluation
                if include_self:
                    EvaluationAssignment.objects.get_or_create(
                        campaign=campaign,
                        evaluator=user,
                        evaluatee=user,
                        defaults={'relationship': 'self'}
                    )
                    created_count += 1

                # Supervisor evaluation
                if include_supervisor and user.supervisor:
                    EvaluationAssignment.objects.get_or_create(
                        campaign=campaign,
                        evaluator=user.supervisor,
                        evaluatee=user,
                        defaults={'relationship': 'supervisor'}
                    )
                    created_count += 1

                # Peer evaluations
                if include_peers and user.department:
                    peers = User.objects.filter(
                        department=user.department,
                        is_active=True
                    ).exclude(id=user.id)[:3]  # Limit to 3 peers

                    for peer in peers:
                        EvaluationAssignment.objects.get_or_create(
                            campaign=campaign,
                            evaluator=peer,
                            evaluatee=user,
                            defaults={'relationship': 'peer'}
                        )
                        created_count += 1

                # Subordinate evaluations
                if include_subordinates:
                    subordinates = user.get_subordinates()[:5]  # Limit to 5

                    for sub in subordinates:
                        EvaluationAssignment.objects.get_or_create(
                            campaign=campaign,
                            evaluator=sub,
                            evaluatee=user,
                            defaults={'relationship': 'subordinate'}
                        )
                        created_count += 1

            messages.success(request, f'{created_count} tapşırıq yaradıldı.')
            return redirect('evaluations:campaign-detail', pk=campaign.pk)
    else:
        form = BulkAssignmentForm()

    # Get departments for filter
    from apps.departments.models import Department
    departments = Department.objects.filter(is_active=True).order_by('name')

    context = {
        'form': form,
        'page_title': 'Toplu Tapşırıq Yaratma',
        'departments': departments
    }

    return render(request, 'evaluations/bulk_assign.html', context)


@login_required
def filter_users_by_department(request):
    """AJAX endpoint to filter users by department."""
    if not request.user.is_admin():
        return JsonResponse({'success': False, 'error': 'Permission denied'})

    department_id = request.GET.get('department_id')
    role = request.GET.get('role')

    # Base queryset
    users = User.objects.filter(is_active=True)

    # Filter by department
    if department_id:
        users = users.filter(department_id=department_id)

    # Filter by role
    if role:
        if role == 'admin':
            users = users.filter(role='admin')
        elif role == 'manager':
            users = users.filter(role='manager')
        elif role == 'employee':
            users = users.filter(role='employee')

    # Prepare response data
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name(),
            'email': user.email,
            'department': user.department.name if user.department else '',
            'role': user.role
        })

    return JsonResponse({
        'success': True,
        'users': user_list,
        'count': len(user_list)
    })
