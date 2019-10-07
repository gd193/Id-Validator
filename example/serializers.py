from rest_framework import serializers
from .models.Generator import id
from .models.forbidden_words import swear_words
import datetime

class id_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = id
        fields = [ 'Kombination','Validated',]

        extra_kwargs = {'Kombination': {'required': False},
                        'Validated':{'read_only':True},}

    def create(self, validated_data):
        arguments = ['ha', 'True', "%y", '_', 3, 3]  # default arguments for create new id

        if self.context['request'].query_params.get('tag', ''):
            sw_set = swear_words.objects.all()
            for words in sw_set:
                if str(words) in self.context['request'].query_params.get('tag',''):
                    raise serializers.ValidationError('The given tag contained inadequate language')
            arguments[0] = self.context['request'].query_params.get('tag', '')

        if self.context['request'].query_params.get('add_current_year', ''):
            acy = self.context['request'].query_params.get('add_current_year', '')
            if (acy == 'True' or acy == 'False'):
                arguments[1] = acy
            else:
                raise serializers.ValidationError('add_current_year must be True or False, ' + acy +' was given.')

        if self.context['request'].query_params.get('current_year_style', ''):
            arguments[2] = self.context['request'].query_params.get('current_year_style', '')

        if self.context['request'].query_params.get('spacing', ''):
            arguments[3] = self.context['request'].query_params.get('spacing', '')

        if self.context['request'].query_params.get('n_letters', ''):
            n_letters = self.context['request'].query_params.get('n_letters', '')
            try:
                arguments[4] = int(n_letters)
            except:
                raise serializers.ValidationError('Need Valid Integer as n_letters, got ' + n_letters)

        if self.context['request'].query_params.get('n_numbers', ''):
            n_numbers = self.context['request'].query_params.get('n_numbers','')
            try:
                arguments[5] = int(n_numbers)
            except:
                raise serializers.ValidationError('Need valid integer as n_numbers, got '+ n_numbers)


        (success, response_str) = id.objects.create_new_id(*arguments)
        if success:
            return response_str
        else:
            raise serializers.ValidationError(response_str)



    def update(self, validated_data):

        current_time = datetime.datetime.now(datetime.timezone.utc)
        unvalidated_set = id.objects.filter(Validated='False')
        expiring_duration = datetime.timedelta(hours=1)

        for ID in unvalidated_set:
            dt = current_time - ID.creation_time
            if dt > expiring_duration:
                ID.delete()

        updating_Komb = validated_data.get('Kombination')
        updating_id = id.objects.filter(Kombination = updating_Komb)

        if updating_id:
            updating_id = updating_id[0]
            updating_id.Validated = True
            updating_id.save()
            return updating_id

        else:
            raise serializers.ValidationError('The given Id '+updating_Komb+' does not exist.')








