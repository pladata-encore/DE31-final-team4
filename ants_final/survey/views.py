from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import SurveyQuestion

def index(request):
    latest_question_list = SurveyQuestion.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'survey/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(SurveyQuestion, pk=question_id)
    return render(request, 'survey/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(SurveyQuestion, pk=question_id)
    try:
        selected_choice = question.surveyresponse_set.get(pk=request.POST['choice'])
    except (KeyError, SurveyResponse.DoesNotExist):
        return render(request, 'survey/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('survey:results', args=(question.id,)))
