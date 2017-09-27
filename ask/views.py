from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.shortcuts import resolve_url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ask.forms import LoginForm, SignupForm, QuestionForm, SettingsForm, AnswerForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from ask.models import Question, Answer, Tag, Profile, Like, LikeAnswer


def hello(request):
    body = 'Hello, World! By Django\n'

    body += 'GET parameters:\n'
    body += parse(request.GET)

    body += 'POST parameters:\n'
    body += parse(request.POST)

    return HttpResponse(body, content_type="text/plain")


def parse(params):
    result = ''
    for key, val in params.iteritems():
        result += key + '=' + val + '\n'
    return result


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 10)

    page = request.GET.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    paginator_variables = {
        'page_range': paginator.page_range,
        'next_page': paginator.num_pages,
        'prev_page': 1,
    }
    if objects_page.has_previous():
        paginator_variables['prev_page'] = objects_page.previous_page_number
    if objects_page.has_next():
        paginator_variables['next_page'] = objects_page.next_page_number

    return objects_page, paginator_variables


def get_popular_tags():
    top_tags = Tag.objects.all()
    top_tags = top_tags[:5]
    return top_tags


def get_best_members():
    best_members = Profile.objects.all()
    best_members = best_members[:5]
    return best_members


def new(request):
    _questions = Question.objects.new_questions()
    top_tags = get_popular_tags()
    best_members = get_best_members()

    questions, paginator = paginate(_questions, request)

    context = {
        'questions': questions,
        'top_tags': top_tags,
        'best_members': best_members,
        'paginator': paginator,
    }

    return render(request, 'index.html', context)


def hot(request):

    _questions = Question.objects.hot_questions()
    top_tags = get_popular_tags()
    best_members = get_best_members()

    questions, paginator = paginate(_questions, request)

    context = {
        'questions': questions,
        'top_tags': top_tags,
        'best_members': best_members,
        'paginator': paginator,
    }

    return render(request, 'hot.html', context)


def tag(request, **kwargs):
    _tag = kwargs['tag']
    top_tags = get_popular_tags()
    best_members = get_best_members()
    _questions = Question.objects.has_tag(_tag)
    if not _questions:
        raise Http404()
    questions, paginator = paginate(_questions, request)

    context = {
        'questions': questions,
        'top_tags': top_tags,
        'best_members': best_members,
        'paginator': paginator,
        'tag': _tag,
    }

    return render(request, 'tag.html', context)


def question(request, **kwargs):
    qid = kwargs['qid']

    if qid is None:
        raise Http404()

    _question = Question.objects.get(pk=qid)

    _answers = Answer.objects.filter(question_id=qid)

    top_tags = get_popular_tags()
    best_members = get_best_members()

    answers, paginator = paginate(_answers, request)

    if request.method == 'POST':
        if not request.user.is_authenticated():
            response = redirect('login')
            response['Location'] += '?next=' + qid
            return response

        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = qid
            answer.author = Profile.objects.get(user=request.user)
            answer.save()

            anchor = '#' + str(answer.pk)
            url = resolve_url('question', _question.pk)
            return redirect(url + anchor)
        else:
            form = AnswerForm()
    else:
        form = AnswerForm()

    context = {
        'question': _question,
        'top_tags': top_tags,
        'best_members': best_members,
        'paginator': paginator,
        'answers': answers,
        'form': form
    }

    return render(request, 'question.html', context)


def login(request):
    if request.user.is_authenticated():
        return redirect('new-questions')

    top_tags = get_popular_tags()
    best_members = get_best_members()

    cont = request.GET.get('next', 'new-questions')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        user = auth.authenticate(username=request.POST['login'],
                                 password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect(cont)
        else:
            form.add_error(None, "Incorrect login/password")
    else:
        form = LoginForm()

    context = {
        'top_tags': top_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)

    cont = request.GET.get('next')
    if cont is None:
        return redirect('new-questions')

    return redirect(cont)


def signup(request):
    top_tags = get_popular_tags()
    best_members = get_best_members()

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect('new-questions')

    else:
        form = SignupForm()
    context = {
        'top_tags': top_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'signup.html', context)

@login_required
def ask(request):
    top_tags = get_popular_tags()
    best_members = get_best_members()

    if request.method == 'POST':
        form = QuestionForm(request.user, request.POST)

        if form.is_valid():
            form.clean_tags_names()
            _question = form.save()
            return redirect('question', _question.pk)
    else:
        form = QuestionForm(request.user)
    context = {
        'top_tags': top_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'ask.html', context)


@login_required()
def settings(request):
    top_tags = get_popular_tags()
    best_members = get_best_members()

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES or None)

        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm(initial={'login': request.user.username,
                                     'email': request.user.email,
                                     'nickname': request.user.first_name})
    context = {
        'top_tags': top_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'settings.html', context)

@login_required
def rate_question(request):
    if request.method == 'GET':
        q_id = request.GET['question_id']
        like_type = request.GET['type']

    try:
        like = Like.objects.get(question_id=int(q_id), author_id=request.user.pk)
    except Like.DoesNotExist:
        like = None

    if like is not None:
        return

    if like_type == 'like':
        value = 1
    else:
        value = -1

    rating = 0
    if q_id:
        question = Question.objects.get(pk=int(q_id))
        if question:
            rating = question.rating + value
            question.rating = rating
            question.save()
            Like.objects.create(value=value, question_id=q_id, author_id=request.user.pk)
    return HttpResponse(rating)


@login_required
def rate_answer(request):
    if request.method == 'GET':
        ans_id = request.GET['answer_id']
        like_type = request.GET['type']

    try:
        like = LikeAnswer.objects.get(answer_id=int(ans_id), author_id=request.user.pk)
    except LikeAnswer.DoesNotExist:
        like = None

    if like is not None:
        return

    rating = 0

    if like_type == 'like':
        value = 1
    else:
        value = -1

    if ans_id:
        answer = Answer.objects.get(pk=int(ans_id))
        if answer:
            rating = answer.rating + value
            answer.rating = rating
            answer.save()
            LikeAnswer.objects.create(value=value, answer_id=ans_id, author_id=request.user.pk)
    return HttpResponse(rating)


@login_required
def mark_answer(request):
    if request.method == 'GET':
        ans_id = request.GET['answer_id']
        state = request.GET['state']

    try:
        answer = Answer.objects.get(pk=int(ans_id))
    except Answer.DoesNotExist:
        return

    if answer.question.author_id == request.user.pk:
        if state == 'true':
            answer.is_correct = True
        else:
            answer.is_correct = False
        answer.save()
        print answer
        return HttpResponse()
