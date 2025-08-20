from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db import transaction, models
from .models import Board, Topic, Post
from .forms import NewTopicForm, NewPostForm
import logging

# logging setup
logger = logging.getLogger(__name__)

def board_list(request):
    """Display list of all boards with pagination"""
    try:
        boards = Board.objects.prefetch_related('topics__posts').all().order_by('id')
        
        # Add pagination
        paginator = Paginator(boards, 10)  # Show 10 boards per page
        page = request.GET.get('page')
        
        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
            boards = paginator.page(1)
        except EmptyPage:
            boards = paginator.page(paginator.num_pages)
            
        return render(request, "boards/board_list.html", {"boards": boards})
    
    except Exception as e:
        logger.error(f"Error loading boards: {e}")
        messages.error(request, "Error loading boards. Please try again.")
        return render(request, "boards/board_list.html", {"boards": []})

def board_detail(request, board_id):
    """Display board details with topics list and pagination"""
    try:
        board = get_object_or_404(Board, id=board_id)
        topics = board.topics.select_related('created_by').prefetch_related('posts').all().order_by('-created_at')
        
        # Add pagination for topics
        paginator = Paginator(topics, 20)  # Show 20 topics per page
        page = request.GET.get('page')
        
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
            
        return render(request, "boards/board_detail.html", {
            "board": board,
            "topics": topics
        })
    
    except Http404:
        messages.error(request, "Board not found.")
        return redirect('board_list')
    except Exception as e:
        logger.error(f"Error loading board {board_id}: {e}")
        messages.error(request, "Error loading board. Please try again.")
        return redirect('board_list')

@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def new_topic(request, board_id):
    """Create a new topic in the specified board"""
    try:
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
                        
                except Exception as e:
                    logger.error(f"Error creating topic: {e}")
                    messages.error(request, "Error creating topic. Please try again.")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = NewTopicForm()
        
        # Get recent topics for display
        topics = board.topics.select_related('created_by').all().order_by('-created_at')[:10]
        
        return render(request, "boards/new_topic.html", {
            "board": board,
            "topics": topics,
            "form": form
        })
    
    except Http404:
        messages.error(request, "Board not found.")
        return redirect('board_list')
    except Exception as e:
        logger.error(f"Error in new_topic view for board {board_id}: {e}")
        messages.error(request, "Error loading page. Please try again.")
        return redirect('board_list')

@csrf_protect
@require_http_methods(["GET", "POST"])
def topic_detail(request, board_id, topic_id):
    """Display topic details with posts and handle new post creation"""
    try:
        topic = get_object_or_404(
            Topic.objects.select_related('board', 'created_by'), 
            id=topic_id, 
            board_id=board_id
        )
        
        posts = topic.posts.select_related('created_by').all().order_by('created_at')
        
        # Add pagination for posts
        paginator = Paginator(posts, 20)  # Show 20 posts per page
        page = request.GET.get('page')
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
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
                        
                except Exception as e:
                    logger.error(f"Error creating post: {e}")
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
    
    except Http404:
        messages.error(request, "Topic not found.")
        return redirect('board_detail', board_id=board_id)
    except Exception as e:
        logger.error(f"Error loading topic {topic_id}: {e}")
        messages.error(request, "Error loading topic. Please try again.")
        return redirect('board_detail', board_id=board_id)