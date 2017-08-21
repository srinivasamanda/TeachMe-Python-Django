from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CourseForm, NotesForm, UserForm
from .models import Course, Notes

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_course(request):
    if not request.user.is_authenticated():
        return render(request, 'course/login.html')
    else:
        form = CourseForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.course_logo = request.FILES['course_logo']
            file_type = course.course_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'course': course,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'course/create_course.html', context)
            course.save()
            return render(request, 'course/detail.html', {'course': course})
        context = {
            "form": form,
        }
        return render(request, 'course/create_course.html', context)


def create_notes(request, course_id):
    form = NotesForm(request.POST or None, request.FILES or None)
    course = get_object_or_404(Course, pk=course_id)
    if form.is_valid():
        courses_notes = course.notes_set.all()
        for s in courses_notes:
            if s.chapter_title == form.cleaned_data.get("chapter_title"):
                context = {
                    'course': course,
                    'form': form,
                    'error_message': 'You already added that notes',
                }
                return render(request, 'course/create_notes.html', context)
        notes = form.save(commit=False)
        notes.course = course
        notes.audio_file = request.FILES['audio_file']
        file_type = notes.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'course': course,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'course/create_notes.html', context)

        notes.save()
        return render(request, 'course/detail.html', {'course': course})
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'course/create_notes.html', context)


def delete_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    course.delete()
    courses = Course.objects.filter(user=request.user)
    return render(request, 'course/index.html', {'courses': courses})


def delete_notes(request, course_id, notes_id):
    course = get_object_or_404(Course, pk=course_id)
    notes = Notes.objects.get(pk=notes_id)
    notes.delete()
    return render(request, 'course/detail.html', {'course': course})


def detail(request, course_id):
    if not request.user.is_authenticated():
        return render(request, 'course/login.html')
    else:
        user = request.user
        course = get_object_or_404(Course, pk=course_id)
        return render(request, 'course/detail.html', {'course': course, 'user': user})


def favorite(request, notes_id):
    notes = get_object_or_404(Notes, pk=notes_id)
    try:
        if notes.is_favorite:
            notes.is_favorite = False
        else:
            notes.is_favorite = True
        notes.save()
    except (KeyError, Notes.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    try:
        if course.is_favorite:
            course.is_favorite = False
        else:
            course.is_favorite = True
        course.save()
    except (KeyError, Course.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'course/login.html')
    else:
        courses = Course.objects.filter(user=request.user)
        notes_results = Notes.objects.all()
        query = request.GET.get("q")
        if query:
            courses = courses.filter(
                Q(course_title__icontains=query) |
                Q(author__icontains=query)
            ).distinct()
            notes_results = notes_results.filter(
                Q(chapter_title__icontains=query)
            ).distinct()
            return render(request, 'course/index.html', {
                'courses': courses,
                'notes': notes_results,
            })
        else:
            return render(request, 'course/index.html', {'courses': courses})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'course/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                courses = Course.objects.filter(user=request.user)
                return render(request, 'course/index.html', {'courses': courses})
            else:
                return render(request, 'course/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'course/login.html', {'error_message': 'Invalid login'})
    return render(request, 'course/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                courses = Course.objects.filter(user=request.user)
                return render(request, 'course/index.html', {'courses': courses})
    context = {
        "form": form,
    }
    return render(request, 'course/register.html', context)


def notes(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'course/login.html')
    else:
        try:
            notes_ids = []
            for course in Course.objects.filter(user=request.user):
                for notes in course.notes_set.all():
                    notes_ids.append(notes.pk)
            users_notes = Notes.objects.filter(pk__in=notes_ids)
            if filter_by == 'favorites':
                users_notes = users_notes.filter(is_favorite=True)
        except Course.DoesNotExist:
            users_notes = []
        return render(request, 'course/notes.html', {
            'notes_list': users_notes,
            'filter_by': filter_by,
        })