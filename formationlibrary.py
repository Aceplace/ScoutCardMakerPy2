from formation import get_default_variation
from exceptions import LibraryException
import copy
import pickle
import re

class FormationLibrary:
    def __init__(self):
        self.formations = {}

    def add_formation_to_library(self, formation_name, formation):
        if not formation_name:
            raise LibraryException(
                'Empty formation name not allowed.')

        formation_words = formation_name.upper().split()

        if any(direction in formation_words for direction in ['LT', 'LEFT', 'RT', 'RIGHT']):
            raise LibraryException('Don\'t include a direction with formation name (direction is implicitly to the right.')

        formation_name = ' '.join(formation_words)

        formation_to_save = copy.deepcopy(formation)

        self.formations[formation_name] = formation_to_save

    def does_formation_exist(self, formation_name):
        return formation_name in self.formations

    def delete_formation_from_library(self, formation_name):
        formation_name = ' '.join(formation_name.upper().split())

        try:
            del self.formations[formation_name]
        except KeyError:
            raise LibraryException(f'{formation_to_delete} not in formations.')

    def save_library(self, filename):
        try:
            with open(filename, 'wb') as file_object:
                pickle.dump(self.formations, file_object)
        except IOError as e:
            raise LibraryException(str(e))

    def load_library(self, filename):
        try:
            with open(filename, 'rb') as file_object:
                formations = pickle.load(file_object)
                self.formations = formations
        except IOError as e:
            raise LibraryException(str(e))

    def get_formation(self, formation_name):
        try:
            formation = copy.deepcopy(self.formations[formation_name])
        except KeyError:
            raise LibraryException(f'{formation_name} not in formations.')

        return formation

    def get_composite_formation_variation(self, formation_name, hash):
        if not self.formations:
            raise LibraryException('Formation Library Empty')

        formation_name = ' '.join(formation_name.strip().upper().split())

        # Find which direction is going
        reg_ex = re.compile(r'(RT|LT|RIGHT|LEFT)')
        matches = reg_ex.findall(formation_name)
        if len(matches)  != 1:
            raise LibraryException('Can\'t determine if going Lt or Rt from formation name: ' + formation_name)
        else:
            direction = 'RT' if matches[0] == 'RT' or matches[0] == 'RIGHT' else 'LT'

        # determine mof, field, boundary type
        if hash == 'm':
            variation_type = 'mof'
        elif (hash == 'r' and  direction == 'RT') or (hash == 'L' and direction == 'LT'):
            variation_type = 'boundary'
        else:
            variation_type = 'field'

        formation_name = reg_ex.sub('', formation_name)
        formation_words = formation_name.split()
        first_index = 0
        last_index = len(formation_words) - 1

        #Pro trips c gun
        formation_variation = get_default_variation(variation_type)
        still_looking_for_match = False
        while first_index <= last_index:
            sub_formation_name = ' '.join(formation_words[first_index:last_index + 1])
            if sub_formation_name in self.formations:
                formation_variation.override_player_positions(
                    self.formations[sub_formation_name].variations[variation_type],
                    self.formations[sub_formation_name].affected_player_tags
                )
                first_index = last_index + 1
                last_index = len(formation_words) - 1
                still_looking_for_match = False
            else:
                still_looking_for_match = True
                last_index -= 1

        if still_looking_for_match:
            raise LibraryException(sub_formation_name + ' doesn\'t exist in library. Create it.')


        #check that all sub_formations exist and create a composite variation from them
        """sub_formation_name = ''
        formation_variation = get_default_variation(variation_type)
        for word in formation_words:
            sub_formation_name = word if sub_formation_name == '' else sub_formation_name + ' ' + word
            if sub_formation_name in self.formations:
                formation_variation.override_player_positions(
                    self.formations[sub_formation_name].variations[variation_type],
                    self.formations[sub_formation_name].affected_player_tags
                )
                sub_formation_name = ''

        if sub_formation_name != '':
            raise LibraryException(sub_formation_name + ' doesn\'t exist in library. Create it.')"""

        if direction == 'LT':
            formation_variation.flip()

        return formation_variation

    def get_sorted_formation_names(self):
        return sorted([formation_name for formation_name in self.formations.keys() ])

