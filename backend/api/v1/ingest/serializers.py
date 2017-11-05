import os
from rest_framework import serializers
from django.contrib.auth.models import User

from apps.media.models import MediaToCreator, MediaCreatorRole, Media, MediaCreator, License
from apps.media.utils.dtrange import range_from_partial_date
from apps.sets.models import Node
from apps.archive.tasks import archive
from apps.archive.operations.hash import generate_hash
from apps.archive.models import ArchiveFile

from psycopg2.extras import DateTimeTZRange


class MediaLicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = [
            'id',
            'name'
        ]


class MediaCreatorRoleSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    def get_name(self, mcr):
        return str(mcr)

    class Meta:
        model = MediaCreatorRole
        fields = ['id', 'name']


class MediaCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaToCreator
        fields = ['role', 'creator']


class IncomingHyperlink(serializers.HyperlinkedRelatedField):

    pass



class CreateMediaSerializer(serializers.Serializer):

    ingestion_id = serializers.CharField(max_length=500)

    year = serializers.IntegerField(min_value=1950, max_value=2050)
    month = serializers.IntegerField(min_value=1, max_value=12, required=False)
    day = serializers.IntegerField(min_value=1, max_value=31, required=False)
    timestamp = serializers.DateTimeField(required=False)

    creators = serializers.PrimaryKeyRelatedField(queryset=MediaCreator.objects.all(), many=True)
    license = serializers.PrimaryKeyRelatedField(queryset=License.objects.all())

    def validate_ingestion_identifier(self, value):
        if not os.path.exists(value):
            raise serializers.ValidationError('The file {} does not seem to exist.'.format(value))

        if not os.path.isfile(value):
            raise serializers.ValidationError('The path {} does not point to a file.'.format(value))

        if not os.access(value, os.R_OK):
            raise serializers.ValidationError('The file at {} is not readable.'.format(value))

        hash = generate_hash(value)
        try:
            af = ArchiveFile.objects.get(hash=hash)
        except ArchiveFile.DoesNotExist:
            return value
        else:
            raise serializers.ValidationError('''
                The same file already exists in the archive. 
                The associated media id is {}'''.format(af.media_set.get().pk))

    def validate_dates(self, data):
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')

        timestamp = data.get('timestamp')

        if day and not  month:
            raise serializers.ValidationError('Cannot have a day without a month')

        if any([year, month, day]) and timestamp:
            raise serializers.ValidationError('Can not use timestamp and any of year, month, day together.')

        if any([year, month, day]):
            start, end = range_from_partial_date(year, month, day)

            if start > end:
                raise serializers.ValidationError('Start can not be before end of timerange.')

    def validate(self, data):
        # self.validate_ingestion_identifier(data.get('ingestion_id'))
        self.validate_dates(data)
        return data


class SimpleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['pk', 'creators', 'license', 'creation_date']


class HAVTargetField(serializers.HyperlinkedRelatedField):
    view_name = 'api:v1:hav_browser:hav_set'
    queryset = Node.objects.all()


class BatchMediaSerializer(serializers.Serializer):

    target = HAVTargetField()

    entries = CreateMediaSerializer(many=True)

    def create(self, validated_data):
        target = validated_data['target']
        user = self.context['user']

        raw_entry_data = self.data
        raw_entries = raw_entry_data.pop('entries', [])

        tasks = []

        for media_data in raw_entries:
            media_data.update(raw_entry_data)
            media_data.update({
                'user': user.pk,
                'target': target.pk
            })

            # queue the task
            task = archive.delay(media_data)
            # collect task ids
            tasks.append(task.id)

        return tasks



class IngestSerializer(CreateMediaSerializer):

    target = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, vd):
        # construct date time range
        dt_range = range_from_partial_date(vd.get('year'), vd.get('month'), vd.get('day'))

        # actually create the media object
        media = Media.objects.create(
                    creation_date=DateTimeTZRange(lower=dt_range[0], upper=dt_range[1]),
                    license=vd.get('license'),
                    set=vd.target,
                    created_by=vd.user
                )

        # save m2m
        for creator in vd['creators']:
            MediaToCreator.objects.create(
                creator=creator,
                media=media
            )

        return SimpleMediaSerializer(media)




class IngestSourcesSerializer(serializers.ListField):
    child = serializers.CharField()


class PrepareIngestSerializer(serializers.Serializer):

    target = HAVTargetField()

    assets = IngestSourcesSerializer()