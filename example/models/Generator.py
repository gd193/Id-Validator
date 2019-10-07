from django.db import models
import datetime
import random
from .forbidden_words import swear_words
from django.utils import timezone

class id_generator(models.Manager):
    symbols = 'QWERTZUIOPASDFGHJKLYXCVBNM'

    def __Komb_create(self):
        """
        :return: the Kombination for the new id as string
        """

        Komb_string = ''
        Komb_string += self.tag
        if ( self.add_current_year == 'True' ):
            Komb_string += datetime.datetime.now(tz=timezone.utc).strftime(self.current_year_style)
        Komb_string += self.spaceing

        Komb_let = ''
        cleared = False
        while (cleared == False):
            for i in range(0,self.n_letters):
                j = random.randint(0, len(self.symbols) - 1)
                Komb_let += self.symbols[j]
            cleared = True
            sw_set = swear_words.objects.all()
            for word in sw_set:
                if (str(word) in Komb_let):
                    cleared = False
                    
        Komb_string += Komb_let

        for i in range (0,self.n_numbers):
            j = random.randint(0, 9)
            Komb_string += str(j)

        return Komb_string






    def create_new_id(self,tag='ha',add_current_year='True', current_year_style='%y', spaceing='_',n_letters=3,n_numbers=3):
        """
        :param tag: Give the tag of the service the id is provided for
        :param add_current_year: add the current date to the service tag passed as string
        :param current_year_style: give the style the current year should be added, valid inputs are in the datetime doc
        :param spaceing: give the desired spacing symbol as string
        :param n_letters: number of letters in the id, min: 2
        :param n_numbers: number of numbers in the id, min: 1
        :return: create new id in the database and return the id as string
        """

        if n_letters<2:
            return (False, 'Requires n_letter to be int with n_letter>2, ' + str(n_letters) + ' was given')
        if n_numbers<1:
            return (False, 'Requires n_numbers to be int with n_numbers>1, ' + str(n_numbers) + ' was given')

        self.tag = tag
        self.add_current_year = add_current_year
        self.current_year_style = current_year_style

        try:
            datetime.datetime.now(tz=timezone.utc).strftime(current_year_style)
        except:
            return(False, 'Requires valid current_year_style, ' + str(current_year_style)+
                    ' was given. Correct styles here: https://www.programiz.com/python-programming/datetime/strftime')

        if (datetime.datetime.now(tz=timezone.utc).strftime(current_year_style) == current_year_style):
            return (False, 'Requires valid current_year_style, ' + str(current_year_style)+
                    ' was given. Correct styles here: https://www.programiz.com/python-programming/datetime/strftime')

        self.spaceing = spaceing
        self.n_letters = n_letters
        self.n_numbers = n_numbers
        counting_index=0

        validated = False
        Komb = ''

        while (validated == False):
            Komb = self.__Komb_create()
            if (counting_index>1000):
                break
            if (id.objects.filter(Kombination__exact = Komb).count() == 0):
                validated = True
            counting_index+=1


        if (validated == True):
            new_id = self.create (Kombination = Komb, Validated = False)
            return (True,new_id)
        else:
            return (False, 'Could not find a new id with the given arguments.')


class id(models.Model):
    Kombination = models.CharField(max_length = 100)
    Validated = models.BooleanField(default=False)
    creation_time = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc))

    objects = id_generator()

    def __str__(self):
        return self.Kombination
