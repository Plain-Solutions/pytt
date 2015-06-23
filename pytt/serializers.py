from pytt.models import *
from rest_framework import serializers


class TRSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeReference
        fields = ('sequence', 'begin', 'end')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name', 'tag', 'dtype')


class TagDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('tag', )


class DepartmentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('info', )


class FullGroupSerializer(serializers.ModelSerializer):
    department = TagDepartmentSerializer()
    class Meta:
        model = Group
        fields = ('department', 'name', 'gform', 'gtype')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'gform', 'gtype')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name', 'ssu_id')


class DayTimeParitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DayTimeParity
        fields = ('day', 'time', 'parity')


class SubgroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Subgroup
        fields = ('name', 'location', 'teacher', 'activity')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', 'begin_date', 'end_date')


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ('message', )


class CellSerializer(serializers.ModelSerializer):
    dtp = DayTimeParitySerializer()
    subject = SubjectSerializer()
    subgroup = SubgroupSerializer()

    class Meta:
        model = Cell
        fields = ('dtp', 'subject', 'subgroup')


class TeacherSubgroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subgroup
        fields = ('name', 'location', 'activity')


class TeacherCellSerializer(serializers.ModelSerializer):
    group = FullGroupSerializer()
    dtp = DayTimeParitySerializer()
    subject = SubjectSerializer()
    subgroup = TeacherSubgroupSerializer()

    class Meta:
        model = Cell
        fields = ('group', 'dtp', 'subject', 'subgroup')


class FullPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParityReference
        fields = ('begin_day', 'end_day', 'is_even')


class PRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParityReference
        fields = ('is_even', )
