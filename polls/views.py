from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Using generic views is a powerful way to abstract away simplect concepts in
# this case that is ListView (display a list of objects) and DetailView (display
# detail page for particular object. Each generic view needs attr "model" to
# know which model it acts on and then expects the URL to be called "pk" for
# the primary key value.

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return render(request, 'polls/index.html', context)

# Above the templates were provided with the context var latest_question_list.
# for generic.DetailView (arg to DetailView and ResultsView) question var is
# provided automatically because we're using the Django model Question. In
# contrast generic.ListView automatically generates the context var
# 'question_list'. To override this we provide the attr. context_object_name
# and specify the var 'latest_question_list'for the 'polls/index.html' templ to
# use. I assume that the def get_queryset(self): method is a default method
# that can be implemented to control the data the context_obect gets.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})

class DetailView(generic.DetailView):
    model = Question
    # my defauly DetailView generic view uses a template called <app_name>/
    # <model_name>_detail.html. Setting the template_name attr. tells Django
    # to use a specific template name instead of auto-generated default template
    template_name = 'polls/detail.html'

#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dict like objects that lets you access submitted
        # data by key name. request.GET is also a method.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse() helps avoid URL hardcoding, its given the name of thre view,
        # we want to pass control to and the variable portion of the URL that
        # points to that view,
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
