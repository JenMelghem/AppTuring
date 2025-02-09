from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Question

# Vista para la página de inicio
def index(request):
    return render(request, 'index.html')

# Vista del panel de administración
def admin_panel(request):    
    # Obtén las preguntas pendientes (aún no tienen respuesta)
    pending_questions = Question.objects.filter(response__isnull=True)
    # Obtén las preguntas que ya tienen respuesta
    answered_questions = Question.objects.filter(response__isnull=False)

    return render(request, 'admin.html', {
        'pending_questions': pending_questions,
        'answered_questions': answered_questions
    })

# Vista para que los usuarios envíen preguntas
def submit_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        if question_text:
            # Crea una nueva pregunta sin respuesta
            Question.objects.create(question=question_text)
            return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Vista para que el administrador responda las preguntas    
def answer_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        response = request.POST.get('response')
        is_human = request.POST.get('is_human') == 'true'

        try:
            question = Question.objects.get(id=question_id)
            question.response = response
            question.is_human = is_human
            question.save()
            # Redirigir al usuario a una vista donde pueda votar si fue IA o humano
            return redirect('vote_question', question_id=question.id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Vista para obtener la última respuesta
def get_latest_response(request):
    if request.method == "GET":
        # Recuperar la última pregunta respondida
        question = Question.objects.filter(response__isnull=False).order_by("-created_at").first()
        if question:
            return JsonResponse({
                'question': question.question,
                'response': question.response,
                'is_human': question.is_human
            })
        # Si no hay preguntas respondidas aún
        return JsonResponse({'error': 'No hay respuestas aún'}, status=404)
# views.py

def vote_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return render(request, 'error.html', {'message': 'Pregunta no encontrada'})

    if request.method == 'POST':
        user_vote = request.POST.get('is_human')
        if user_vote == 'true':
            correct = question.is_human
            if correct:
                message = "¡Correcto! La respuesta fue dada por un humano."
            else:
                message = "Incorrecto. La respuesta no fue dada por un humano."
        else:
            correct = not question.is_human
            if correct:
                message = "¡Correcto! La respuesta fue dada por IA."
            else:
                message = "Incorrecto. La respuesta no fue dada por IA."

        return render(request, 'vote_result.html', {'message': message, 'correct': correct})

    return render(request, 'vote_question.html', {'question': question})
