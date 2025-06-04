
from rest_framework import serializers
from .models import Department, Client, Ticket, TicketResponse
from django.contrib.auth.models import User

# Serializer for the User model (read-only for related fields)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['username', 'email', 'first_name', 'last_name'] # Prevent direct modification via these serializers

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__' # Includes 'id', 'name', 'code'

class ClientSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Client
        fields = '__all__' # Includes 'id', 'name', 'contact_person', 'email', 'phone_number', 'department'
        # If you want to allow setting department by ID, 'department' should be in fields.
        # If you want to show department details, you can nest the DepartmentSerializer.
        # Example of nesting:
        # department = DepartmentSerializer(read_only=True)

class TicketSerializer(serializers.ModelSerializer):
    # Display related object details instead of just IDs
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'subject', 'description', 'priority', 'status', 'created_at',
            'updated_at', 'is_expired',
            'created_by', 'created_by_username', # Include 'created_by' for writing, 'created_by_username' for reading
            'assigned_to', 'assigned_to_username',
            'client', 'client_name'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_expired', 'created_by'] # created_by is set automatically

    def create(self, validated_data):
        # Automatically set `created_by` to the current authenticated user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TicketResponseSerializer(serializers.ModelSerializer):
    # Display related object details instead of just IDs
    ticket_subject = serializers.CharField(source='ticket.subject', read_only=True)
    responded_by_username = serializers.CharField(source='responded_by.username', read_only=True)

    class Meta:
        model = TicketResponse
        fields = [
            'id', 'ticket', 'ticket_subject', 'response_text', 'responded_by',
            'responded_by_username', 'created_at', 'status'
        ]
        read_only_fields = ['created_at', 'responded_by'] # responded_by is set automatically

    def create(self, validated_data):
        # Automatically set `responded_by` to the current authenticated user
        validated_data['responded_by'] = self.context['request'].user
        return super().create(validated_data)