# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from google.appengine.api import users
from nankin.models import Jot, Vote, Meta, Comment, Page
from nankin import utils
from appengine_django.auth.models import User
from GChartWrapper import HorizontalBarStack
RECENT_POST_SIZE = 5

def index(request):  
    try:
        page = int(request.GET['page'])
    except:
        page = 1  
    jots = Jot.all().order('-when').fetch(utils.PAGE_SIZE, utils.PAGE_SIZE * (page - 1))
    return list(request, jots)
    
    
    
def list(request, jots):
    try:
        page = int(request.GET['page'])
    except:
        page = 1  
    paginator = utils.createPaginator(page=page)
    for jot in jots:
        if jot.tags and jot.tags[0] != 'photo':
            jot.what = utils.strip_tags(jot.what)[:200] + "..."
    recent_posts = Jot.all().order('-when').fetch(RECENT_POST_SIZE, 0)
    recent_comments = Comment.all().order('-when').fetch(RECENT_POST_SIZE, 0)
    read_most = Jot.all().order('-read_num').fetch(RECENT_POST_SIZE, 0)
    return render_to_response('index.html', {'jots':jots, 'paginator':paginator,
                                             'recent_posts':recent_posts, 'recent_comments':recent_comments,
                                             'read_most':read_most},
                                             context_instance=RequestContext(request))
    

def about(request):
    about = Jot.all().filter('tags =', 'about').get()
    if about:
        return view(request, about.key())
    else:
        raise Http404

def login(request):
    return HttpResponseRedirect(users.create_login_url(request.GET.get('next', '') or request.GET.get('continue', '/')))

def logout(request):
    return HttpResponseRedirect(users.create_logout_url('/'))

def news(request):
    recent_posts = Jot.all().order('-when').fetch(RECENT_POST_SIZE, 0)
    recent_comments = Comment.all().order('-when').fetch(RECENT_POST_SIZE, 0)
    read_most = Jot.all().order('-read_num').fetch(RECENT_POST_SIZE, 0)
    return render_to_response('news.html', {'recent_posts':recent_posts, 'recent_comments':recent_comments, 'read_most':read_most}, context_instance=RequestContext(request))

"""
    转向发布页面
"""
@login_required
def publish(request):
    mode = request.GET.get('mode', None)
    return render_to_response('publish.html', {'mode':mode}, context_instance=RequestContext(request))

@login_required
def delete(request, key):
    user = users.get_current_user()
    type = request.GET.get('type')
    if type == 'comment':
        try:
            model = Comment.get(key)
        except Exception, e:
            raise Http404
    else:
        try:
            model = Jot.get(key)
        except Exception, e:
            raise Http404
    if not (model.who.user == user):
        return HttpResponseRedirect('/')
    model.remove()
    return HttpResponseRedirect('/')

@login_required
def comment(request, key):
    what = request.POST.get('what', None)
    #google user
    user = users.get_current_user()
    #django user
    user = User.all().filter('user = ', user).get()
    try:
        jot = Jot.get(key)
    except Exception, e:
        raise Http404
    comment = Comment(who=user, what=what, refer=jot)
    comment.create()
    return HttpResponseRedirect('/view/' + key + '/')

def view(request, key):
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    paginator = utils.createPaginator(page)
    
    try:
        jot = Jot.get(key)
        jot.read_num += 1
        jot.put()
    except Exception, e:
        raise Http404
    comments = Comment.all().filter('refer =', jot).order('when').fetch(utils.PAGE_SIZE, utils.PAGE_SIZE * (page - 1))

    return render_to_response('view.html', {'entry':jot, 'comments':comments}, context_instance=RequestContext(request))

@login_required
def edit(request, key):
    mode = request.GET.get('mode', None)
    user = users.get_current_user()
    try:
        jot = Jot.get(key)
    except Exception, e:
        raise Httindexp404
    if not (jot.who.user == user):
        return HttpResponseRedirect('/')
    return render_to_response('publish.html', {'jot':jot, 'mode':mode}, context_instance=RequestContext(request))
    
@login_required
def post(request):
    title = request.POST.get('title', None)
    what = request.POST.get('what', None)
    user = users.get_current_user()
    #django user
    user = User.all().filter('user = ', user).get()
    tags = request.POST.get('tags', None)
    tags = tags.split(",")
    edit_key = request.POST.get('edit-key', None)
    if title and what:
        if edit_key:
            jot = Jot.get(edit_key)
            jot.title = title
            jot.what = what
            jot.tags = tags
            jot.put()
        else:
            jot = Jot(title=title, what=what, tags=tags, who=user)
            jot.create()
    return HttpResponseRedirect("/")

def vote(request):
    choice = request.GET.get('choice', None)
    id = request.GET.get('id', None)
    who = users.get_current_user()
    if not who:
        who = users.User(email=User.all().get().email)

    jot = Jot.get(id)
    meta = Meta.get()
    
    if choice == 'y':
        jot.like = jot.like + 1
        if jot.like > meta.max_like:
            meta.max_like = jot.like
    elif choice == 'n':
        jot.unlike = jot.unlike + 1
        if jot.unlike > meta.max_unlike:
            meta.max_unlike = jot.unlike
    meta.save()
    unlike = standard_ratio(meta.max_unlike, 0, jot.unlike)
    like = standard_ratio(meta.max_like, 0, jot.like)
    vote = Vote(who=who, jot=jot)
    jot.save()
    vote.put()
    return render_to_response('vote_stat.html', {'jot':{'like':like, 'unlike':unlike}}, context_instance=RequestContext(request))

def view_by_tag(request, tag):
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    jots = Jot.all().filter('tags = ', tag).order('-when').fetch(utils.PAGE_SIZE, utils.PAGE_SIZE * (page - 1))
    return list(request, jots)

def page(request, path):
    returned_page = Page.all().filter("path = ", path).get();
    if not returned_page:
        returned_page = Page(path=path)
    return render_to_response('page.html', {'page':returned_page}, context_instance=RequestContext(request))

@login_required
def publish_page(request, path):
    return render_to_response('publish_page.html', {'path':path}, context_instance=RequestContext(request))

@login_required
def create_page(request):
    path = request.POST.get('path',None)
    name = request.POST.get('name', None)
    what = request.POST.get('what', None)
    who = users.get_current_user()
    #django user
    who = User.all().filter('user = ', who).get()
    edit_key = request.POST.get('edit-key', None)
    if path and name and what:
        page = Page(path=path,name=name,who=who,what=what)
        page.save()
        return HttpResponseRedirect('/page/'+path+'/')
    return HttpResponseRedirect('/')
"""
    Google Friend Connection
"""
def friend_connect(request, template):
    return render_to_response(template, context_instance=RequestContext(request))

def page_not_found(request):
    return render_to_response('404.html', context_instance=RequestContext(request))

def draw_vote_stat(data):
    G = HorizontalBarStack(data, encoding='text')
    G.fill('bg', 'lg', 'ffffff')
    G.color('4d89f9')
    G.bar(10)
    G.size(100, 29)
    for i in range(len(data)):
        G.marker('t' + str(data[i]), 'black', 0, i, 11)
    #for day in :
    return G.img()