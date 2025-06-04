from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from django.contrib import messages
from django.utils import timezone

@login_required
def submit_ticket(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        description = request.POST['description']
        priority = request.POST['priority']
        department = request.POST['department']

        Ticket.objects.create(
            subject=subject,
            description=description,
            priority=priority,
            department=department,
            client=request.user,
        )
        messages.success(request, 'Ticket submitted successfully.')
        return redirect('ticket_list')
    return render(request, 'submit_ticket.html')


@login_required
def ticket_list(request):
    if request.user.is_staff:  # or add role check
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(client=request.user)
    return render(request, 'ticket_list.html', {'tickets': tickets})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})


@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.status = request.POST['status']
        ticket.resolve_date = timezone.now() if ticket.status == 'Resolved' else None
        ticket.save()
        messages.success(request, 'Ticket updated.')
        return redirect('ticket_detail', ticket_id=ticket.id)
    return render(request, 'ticket_update.html', {'ticket': ticket})
