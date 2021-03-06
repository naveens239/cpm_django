from rest_framework import serializers
from cpm.models import Project, Schedule, Material, OrderStatus, Prototype, ScheduleComment, MaterialComment, VendorList,OrderPriority,ReadCommentTrack

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Schedule
		fields = '__all__'		
		depth = 1

class MaterialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Material
		fields='__all__'
		depth = 1

class PrioritySerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderPriority
		fields='__all__'

class StatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderStatus
		fields='__all__'

class PrototypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Prototype
		fields='__all__'

class ScheduleCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScheduleComment
		fields='__all__'

class MaterialCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaterialComment
		fields='__all__'

class VendorListSerializer(serializers.ModelSerializer):
	class Meta:
		model = VendorList
		fields='__all__'

class TrackCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = ReadCommentTrack
		fields='__all__'
