from django.shortcuts import render, get_object_or_404


from .models import ProgrammingLanguage


def language(request, language):
    """
    The point of entry for a logged in user.
    Shows the available active projects for the user, and allows him
    to create one.
    Shows the pending invites to other projects.
    Shows very critical information about available projects.
    """
    context = {
        'language': get_object_or_404(ProgrammingLanguage, slug=language),
    }
    return render(request, 'project/dashboard.html', context)
