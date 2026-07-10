from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry, TopicMember, Notification
from .forms import TopicForm, EntryForm, TopicMemberForm, CommentForm

from django.db.models import Q
from django.db.models import Count, Max

def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def dashboard(request):

    topics = Topic.objects.filter(
        Q(owner=request.user) |
        Q(topicmember__user=request.user)
    ).distinct()

    topic_count = topics.count()

    entry_count = Entry.objects.filter(
        author=request.user
    ).count()

    member_count = TopicMember.objects.filter(
    topic__in=topics
    ).values('user').distinct().count()


    most_active_topic = topics.annotate(
        entries_total=Count('entry')
    ).order_by('-entries_total').first()


    context = {
        'topic_count': topic_count,
        'entry_count': entry_count,
        'member_count': member_count,
        'most_active_topic': most_active_topic,
    }

    return render(
        request,
        'learning_logs/dashboard.html',
        context
    )

'''
@login_required
def topics(request):
    #topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    topics = Topic.objects.filter(
    Q(owner=request.user) |
    Q(topicmember__user=request.user)
    ).distinct().annotate(
    entry_count=Count('entry'),
    member_count=Count('topicmember')
    ).order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
'''

@login_required
def topics(request):
    sort = request.GET.get('sort', 'date')
    search = request.GET.get('search', '')

    topics = Topic.objects.filter(
        Q(owner=request.user) |
        Q(topicmember__user=request.user)
    ).distinct()

    if search:
        topics = topics.filter(
            text__icontains=search
        )

    topics = topics.annotate(
        entry_count=Count('entry'),
        member_count=Count('topicmember')
    )

    if sort == 'members':
        topics = topics.order_by('-member_count')
    elif sort == 'entries':
        topics = topics.order_by('-entry_count')
    else:
        topics = topics.order_by('-date_added')

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if (
    topic.owner != request.user and
    not TopicMember.objects.filter(
        topic=topic,
        user=request.user
    ).exists()
    ):
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    can_edit = (
    topic.owner == request.user or
    TopicMember.objects.filter(
        topic=topic,
        user=request.user,
        permission='edit'
    ).exists()
    )
    context = {'topic': topic,'entries': entries,'can_edit': can_edit}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def entry_detail(request, entry_id):

    entry = Entry.objects.get(id=entry_id)

    topic = entry.topic

    if (
        topic.owner != request.user and
        not TopicMember.objects.filter(
            topic=topic,
            user=request.user
        ).exists()
    ):
        raise Http404


    comments = entry.comment_set.order_by(
        '-date_added'
    )


    context = {
        'entry': entry,
        'comments': comments,
    }


    return render(
        request,
        'learning_logs/entry_detail.html',
        context
    )

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def add_member(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = TopicMemberForm()
    else:
        form = TopicMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.topic = topic
            member.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {
        'topic': topic,
        'form': form
    }

    return render(
        request,
        'learning_logs/add_member.html',
        context
    )

'''
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    context = {'topic': topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)
'''

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    can_edit = (
        topic.owner == request.user or
        TopicMember.objects.filter(
            topic=topic,
            user=request.user,
            permission='edit'
        ).exists()
    )

    if not can_edit:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    context = {'topic': topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

'''
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

'''

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    can_edit = (
        topic.owner == request.user or
        TopicMember.objects.filter(
            topic=topic,
            user=request.user,
            permission='edit'
        ).exists()
    )

    if not can_edit:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.author = request.user
            new_entry.save()

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def remove_member(request, topic_id, member_id):
    topic = Topic.objects.get(id=topic_id)

    # Alleen eigenaar mag leden verwijderen
    if topic.owner != request.user:
        raise Http404

    member = TopicMember.objects.get(
        id=member_id,
        topic=topic
    )

    member.delete()

    return redirect(
        'learning_logs:topic',
        topic_id=topic.id
    )

@login_required
def add_comment(request, entry_id):

    entry = Entry.objects.get(id=entry_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.author = request.user
            comment.save()
            if comment.entry.author != request.user:
                Notification.objects.create(
                    user=comment.entry.author,
                    entry=entry,
                    message=f"{request.user.username} reacted to your entry",
                    is_read=False
                )
                                
            return redirect(
                'learning_logs:topic',
                topic_id=entry.topic.id
            )

    else:
        form = CommentForm()

    context = {
        'entry': entry,
        'form': form
    }

    return render(
        request,
        'learning_logs/add_comment.html',
        context
    )

@login_required
def notifications(request):

    notifications = request.user.notification_set.order_by(
        '-created_at'
    )

    context = {
        'notifications': notifications
    }

    return render(
        request,
        'learning_logs/notifications.html',
        context
    )

@login_required
def index(request):

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    context = {
        'unread_notifications': unread_notifications,
    }

    return render(
        request,
        'learning_logs/index.html',
        context
    )