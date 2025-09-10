from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Board, Topic, Post
from .forms import NewTopicForm, NewPostForm
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .utils import paginate_queryset, increment_view_count
# from django.http import JsonResponse

# # FBV
# def board_list(request):
#     """Display list of all boards with pagination"""
#     boards = Board.objects.annotate(
#         total_posts=Count('topics__posts'),
#         total_topics=Count('topics'),
#         ).all().order_by('id')
    
#     # Add pagination
#     boards = paginate_queryset(request, boards, 10)  # Show 10 boards per page

#     # return render(request, "boards/board_list.html", {"boards": boards})
    
#     # Prepare data for JSON response
#     data = {
#         "results": [
#             {
#                 "pk": board.pk,
#                 "title": board.title,
#                 "content": board.content,
#                 "total_posts": board.total_posts,
#                 "total_topics": board.total_topics,
#             }
#             for board in boards
#         ],
#         "num_pages": boards.paginator.num_pages,
#         "current_page": boards.number,
#     }
#     return JsonResponse(data)

# CBV
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/board_list.html'
    paginate_by = 10
    ordering = ['id']
    
    def get_queryset(self):
        return Board.objects.annotate(
            total_posts=Count('topics__posts'),
            total_topics=Count('topics'),
        ).all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def board_detail(request, board_id):
    """Display board details with topics list and pagination"""
    board = get_object_or_404(Board, id=board_id)
    
    # Get sorting parameter
    sort_param = request.GET.get('sort', 'newest')
    
    # Get all topics for this board
    topics = board.topics.select_related('created_by').prefetch_related('posts').all()
    
    # Apply sorting based on parameter
    if sort_param == 'oldest':
        topics = topics.order_by('created_at')
    else:  # default to 'newest'
        topics = topics.order_by('-created_at')
        
    # Paginate topics using utility function
    topics = paginate_queryset(request, topics, 20)
        
    return render(request, "boards/board_detail.html", {
        "board": board,
        "topics": topics,
        "sort_param": sort_param,  # Pass current sort parameter to template
    })
        
@login_required
def new_topic(request, board_id):
    """Create a new topic in the specified board"""
    board = get_object_or_404(Board, id=board_id)
    
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    topic = form.save(commit=False)
                    topic.board = board
                    topic.created_by = request.user
                    topic.save()
                    
                    messages.success(request, f"Topic '{topic.title}' created successfully!")
                    return redirect('topic_detail', board_id=board.id, topic_id=topic.id)
                    
            except Exception:
                messages.error(request, "Error creating topic. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewTopicForm()
    
    # Get recent topics for display with pagination
    topics_list = board.topics.select_related('created_by').all().order_by('-created_at')
    
    # Paginate topics
    topics = paginate_queryset(request, topics_list, 10)

    return render(request, "boards/new_topic.html", {
        "board": board,
        "topics": topics,
        "form": form
    })

def topic_detail(request, board_id, topic_id):
    """Display topic details with posts and handle new post creation"""
    topic = get_object_or_404(
        Topic.objects.select_related('board', 'created_by'),
        pk=topic_id,
        board__pk=board_id,
    )
    
    # Use utility function to increment view count
    increment_view_count(request, Topic, topic.id, 'view_topic')
    topic.refresh_from_db()

    posts = topic.posts.select_related('created_by').all().order_by('created_at')
    
    # Paginate posts using utility function
    posts = paginate_queryset(request, posts, 20)
    
    # Handle new post creation
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to post.")
            return redirect('login')
            
        form = NewPostForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    post = form.save(commit=False)
                    post.topic = topic
                    post.created_by = request.user
                    post.save()
                    
                    messages.success(request, "Post added successfully!")
                    return redirect('topic_detail', board_id=board_id, topic_id=topic_id)
                    
            except Exception:
                messages.error(request, "Error creating post. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewPostForm()
    
    return render(request, "boards/topic_detail.html", {
        "topic": topic,
        "posts": posts,
        "form": form
    })

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'boards/post_edit.html'
    context_object_name = 'post'
    
    def test_func(self):
        post = self.get_object()
        return post.created_by == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You can only edit your own posts.")
        return super().handle_no_permission()
    
    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('topic_detail', kwargs={
            'board_id': post.topic.board.id,
            'topic_id': post.topic.id
        })
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)