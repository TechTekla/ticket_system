from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Department, Client, Ticket, TicketResponse
from .serializers import (
    DepartmentSerializer,
    ClientSerializer,
    TicketSerializer,
    TicketResponseSerializer
)

# Standard permission for authenticated users
class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Custom permission to only allow authenticated users to create/update/delete.
    Allows read-only access for unauthenticated users.
    """
    pass

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows departments to be viewed or edited.
    """
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Only authenticated users can modify

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('name')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tickets to be viewed or edited.
    Users can only see tickets they created, are assigned to, or tickets from clients
    associated with their department (if applicable, though not explicitly modeled here).
    Admins can see all tickets.
    """
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    # Only authenticated users can create/update/delete tickets.
    # For read operations, we'll filter based on user.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned tickets to a given user,
        by filtering against `created_by` or `assigned_to` or if the user is a superuser.
        """
        user = self.request.user
        if user.is_superuser:
            return Ticket.objects.all().order_by('-created_at')
        
        # Non-superusers can see tickets they created or are assigned to
        return Ticket.objects.filter(
            created_by=user
        ).union(
            Ticket.objects.filter(assigned_to=user)
        ).order_by('-created_at')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resolve(self, request, pk=None):
        """
        Custom action to mark a ticket as 'Resolved'.
        """
        ticket = self.get_object()
        if ticket.status == 'Resolved':
            return Response({'detail': 'Ticket is already resolved.'}, status=status.HTTP_200_OK)
        
        ticket.status = 'Resolved'
        ticket.save()
        return Response({'detail': f'Ticket {ticket.id} marked as Resolved.', 'status': ticket.status})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def close(self, request, pk=None):
        """
        Custom action to mark a ticket as 'Closed'.
        """
        ticket = self.get_object()
        if ticket.status == 'Closed':
            return Response({'detail': 'Ticket is already closed.'}, status=status.HTTP_200_OK)

        ticket.status = 'Closed'
        ticket.save()
        return Response({'detail': f'Ticket {ticket.id} marked as Closed.', 'status': ticket.status})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def expired_tickets(self, request):
        """
        Returns a list of tickets marked as expired.
        """
        # This assumes 'is_expired' is set by a separate process (e.g., a cron job or management command)
        # For demonstration, we'll just filter by the field.
        expired_tickets = Ticket.objects.filter(is_expired=True).order_by('-created_at')
        serializer = self.get_serializer(expired_tickets, many=True)
        return Response(serializer.data)


class TicketResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ticket responses to be viewed or edited.
    Users can only see responses for tickets they have access to or responses they made.
    """
    queryset = TicketResponse.objects.all().order_by('-created_at')
    serializer_class = TicketResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restricts the returned responses to those associated with tickets
        the user has access to, or responses made by the user.
        """
        user = self.request.user
        if user.is_superuser:
            return TicketResponse.objects.all().order_by('-created_at')
        
        # Get tickets the user has access to (created or assigned)
        accessible_tickets = Ticket.objects.filter(
            created_by=user
        ).union(
            Ticket.objects.filter(assigned_to=user)
        ).values_list('id', flat=True) # Get just the IDs

        # Return responses for those tickets OR responses made by the user
        return TicketResponse.objects.filter(
            ticket__id__in=list(accessible_tickets)
        ).union(
            TicketResponse.objects.filter(responded_by=user)
        ).order_by('-created_at')