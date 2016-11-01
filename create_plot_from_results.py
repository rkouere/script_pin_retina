import matplotlib.pyplot as plt
import csv
import argparse
import sys
import json
import copy


class Experience:
    'A class representing an experience'
    def __init__(self):
        self.persons = set()

    def get_number_of_persons(self):
        """
        Returns the number of persons who have participated in the experience
        """
        return len(self.persons)

    def set_experiences_from_csv(self, csv_file):
        """
        Generates the experiences from a csv file.
        """
        with open(csv_file, 'r') as csvfile:
            plots = list(csv.reader(csvfile, delimiter=','))
            #getting the person's details
        for row in plots:
            self.add_person(row[0], row[1], row[2], row[3])

        # adding the experiences
        for row in plots:
            self.get_person(row[0]).add_experience(row[4:])

    def generate_array_of_data(self):
        """
        Return the data as an array.
        """
        tmp = []
        for person in self.persons:
            for experience in person.get_experiences():
                tmp.append(person.get_details() + experience)
        return tmp

    def add_person(self, name, age, sex, glasses):
        """
        If not already created, adds a person to the list
        of person having done the experience
        """
        if self._check_person_already_exists(name) is not True:
            self.persons.add(Person(name, age, sex, glasses))

    def print_persons(self):
        """
        Prints the list of people having participated in the experience.
        """
        for person in self.persons:
            person.print_details()

    def _check_person_already_exists(self, name):
        """
        Checks that the name is already used by a person.
        """
        for person in self.persons:
            if person.get_name() == name:
                return True

        return False

    def get_person(self, name):
        """
        Returns an object person if the person exists.
        Return False if not.
        """
        for person in self.persons:
            if person.get_name() == name:
                return person
        else:
            return False

    def normalise_all_times(self):
        """
        For each person, normalise the times.
        """
        for person in self.persons:
            person.normalise_time()


class Person:
    'A person who has participated in the experience'
    def __init__(self, name, age, sex, glasses):
        self.experiences = []
        self.name = name
        self.age = age
        self.sex = sex
        self.glasses = glasses
        self.timing_normalisation_max = 60000
        self.col_id = 7
        self.col_time = 6
        self.col_OK = 4
        self.col_name = 0

    def get_name(self):
        return self.name

    def get_details(self):
        """
        Return the details as an array
        """
        return [self.name, self.age, self.sex, self.glasses]

    def get_experiences(self):
        """
        Returns the experiences
        """
        return self.experiences

    def print_details(self):
        print("{}, {}, {}, {}".format(
            self.name, self.age, self.sex, self.glasses))

    def add_experience(self, data):
        self.experiences.append(data)

    def print_experiences(self):
        for experience in self.experiences:
            print("{}".format(experience))

    def normalise_time(self):
        """
        Goes over each data in the timing and normalise them
        """
        # we set the first value as the min and max
        minimal_value = int(self.experiences[0][2])
        maximal_value = int(self.experiences[0][2])
        # find the minimal and max value
        for experience in self.experiences:
            if int(experience[2]) < minimal_value:
                minimal_value = int(experience[2])
            if int(experience[2]) > maximal_value:
                maximal_value = int(experience[2])

        norme = (maximal_value - minimal_value) / self.timing_normalisation_max
        # we normalise each value
        for experience in self.experiences:
            experience[2] = norme * (int(experience[2]) - minimal_value)


class Plotting:
    def __init__(self):
        self.reduced_dic_to_n_rows = {}
        self.dic_two_rows_averaged = {}
        self.col_id = 7
        self.col_time = 6
        self.col_OK = 4
        self.col_name = 0
        self.name_of_graphe = ""

    def get_name_of_graph(self):
        return self.name_of_graph

    def get_values_time(self, plots):
        """
        Get the values for the time col
        plots : an array of data
        """
        self.name_of_graph = "time"
        self._reduce_dic_to_two_values(plots, self.col_id, self.col_time)
        return self._generate_averaged_value_from_two_row_dic()

    def _generate_averaged_value_from_two_row_dic(self):
        tmp_avg = 0
        for key, values in self.reduced_dic_to_n_rows.items():
            tmp_avg = 0
            for value in values:
                tmp_avg += int(value)
            self.dic_two_rows_averaged[int(key)] = tmp_avg/len(values)
        return self.dic_two_rows_averaged

    def _reduce_dic_to_two_values(self, plots, key_id, value_id):
        """
        Takes the two values needed to draw the plot.
        plots : an array of data
        key_id : the index of the data to use as the key
        value_id : the index of the data to be used as value
        """
        for row in plots:
            if row[key_id] in self.reduced_dic_to_n_rows:
                self.reduced_dic_to_n_rows[row[key_id]].append(row[value_id])
            else:
                self.reduced_dic_to_n_rows[row[key_id]] = [row[value_id]]

    def get_number_of_OK_per_id(self, plots):
        """
        Gets the number of time someone has managed to enter the right pin.
        plots : an array of data
        """
        self.name_of_graph = "number of OK per experience"
        self._reduce_dic_to_two_values(plots, self.col_id, self.col_OK)
        return self._OK_avg()

    def _OK_avg(self):
        """
        Returns the average number of OK.
        """
        tmp_avg = 0
        for key, values in self.reduced_dic_to_n_rows.items():
            tmp_avg = 0
            for value in values:
                if value == "OK":
                    tmp_avg += 1
            self.dic_two_rows_averaged[key] = tmp_avg
        return self.dic_two_rows_averaged

    def get_hall_of_fame(self, plots):
        """
        Prints the results of each participant
        plots : an array of data
        """
        self.name_of_graph = "hall of fame"
        self._reduce_dic_to_two_values(plots, self.col_name, self.col_OK)
        return self._OK_avg()

    def get_time_from_minimum_number_of_good_answers(
            self, plots, per_good_aswrs, number_of_guinea_pigs, max_time):
        """
        Returns a list of experiences which have been answered at least
        percentage_of_good_answers % of the time.
        plots : an array of data
        percentage_of_good_answers : the % of good answer we want to keep
        """

        # get the average number of good answers per experience
        self.get_number_of_OK_per_id(plots)
        ids_of_experiences_to_keep = []
        # go over the experiences and get the ids of the answers > percentage
        for id_of_exp, values in self.dic_two_rows_averaged.items():
            if ((values * 100) / number_of_guinea_pigs) >= per_good_aswrs:
                ids_of_experiences_to_keep.append(id_of_exp)

        # we reset the variables
        self.reduced_dic_to_n_rows = {}
        self.dic_two_rows_averaged = {}
        # we get the average time it took to complete each id
        self.get_values_time(plots)
        # we need a temp file to store the final results
        tmp = {}
        # we just want to keep the values of the experiences above the
        # percentage
        for key, values in self.dic_two_rows_averaged.items():
            if "{}".format(key) in ids_of_experiences_to_keep:
                if values < max_time:
                    tmp[key] = values
        self.name_of_graph = "time with a success rate above "
        self.name_of_graph += "{}% ".format(per_good_aswrs)
        self.name_of_graph += "+ a completion time below {}ms".format(max_time)
        self.dic_two_rows_averaged = copy.deepcopy(tmp)
        print("Number of experiences in the result = " + str(len(self.dic_two_rows_averaged)))
        self.print_n_exp_with_full_success(plots, ids_of_experiences_to_keep)
        #self.print_plot_values_from_id(plots, ids_of_experiences_to_keep)
    
    def print_n_exp_with_full_success(self, plots):
        """
        Prints a table of the n experiences with a 100% success rate, with
        the settings associated with the experiences.
        """
        col_synchrone = 0
        col_angle = 0
        col_shaking = 0
        col_shaking_type = 0
        col_level = 0
        # we reduce the data to a 3 col dictionary
        for row in plots:
            # we only want to use the correct answers
            if row[self.col_OK] == "OK":
                if row[self.col_id] in self.reduced_dic_to_n_rows:
                    self.reduced_dic_to_n_rows[row[self.col_id]][5].append(row[self.col_OK])
                    self.reduced_dic_to_n_rows[row[self.col_id]][6].append(row[self.col_time])
                else:
                    self.reduced_dic_to_n_rows[row[self.col_id]] = [
                            row[col_synchrone],
                            row[col_angle],
                            row[col_shaking],
                            row[col_shaking_type],
                            row[col_level],
                            [row[self.col_OK]],
                            [row[self.col_time]]]
        # we change the number of OK in the dic to a number
        tmp_avg = 0
        for key, values in self.reduced_dic_to_n_rows.items():
            tmp_avg = 0
            for value in values[5]:
                if value == "OK":
                    tmp_avg += 1
            self.reduced_dic_to_n_rows[key][5] = tmp_avg
            print(json.dumps(self.reduced_dic_to_n_rows, indent=1))

    def print_plot_values_from_id(self, plots, ids):
        """
        First gets the settings of each id (goes through each experience in the
        plots and get the first settings... they are always the same)
        Prints the settings of the given ids.
        """
        settings_of_chosen_ids = {}
        for experience in plots:
            #print(json.dumps(experience))
            if "{}".format(experience[self.col_id]) in ids:
                if int(experience[self.col_id]) not in settings_of_chosen_ids:
                    settings_of_chosen_ids[int(
                        experience[self.col_id])] = experience[6:]
        print(json.dumps(settings_of_chosen_ids, indent=1))

    def create_plot(self):
        'Creattes a graph from two values'
        plt.figure(figsize=(24, 18))
        plt.bar(range(len(self.dic_two_rows_averaged)),
                self.dic_two_rows_averaged.values(),
                align='center', width=1)
        plt.xticks(range(len(self.dic_two_rows_averaged)), list(
            self.dic_two_rows_averaged.keys()))
        locs, labels = plt.xticks()
        plt.setp(labels, rotation=90)
        plt.xlabel('experience id')
        plt.ylabel('y')
        plt.title(self.name_of_graph)
        plt.legend()
        plt.show()


# dictionary that will hold the informations about the results
experience = Experience()
plotting = Plotting()


def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__)
    # this is a option which need one extra argument
    argparser.add_argument("--mode",
                           "-m",
                           choices=['time', 'success', "hall_of_fame"],
                           help="Prints the average time/success/hall of fame"+
                           "taken to complete an " +
                                "experiment.")

    argparser.add_argument("--normalisation",
                           "-n",
                           action="store_true",
                           help="Normalise the times of every experiment.")

    argparser.add_argument("--avg_OK_percentage",
                           "-a",
                           nargs='+',
                           help="Prints the time for the experiences with a %"
                           + "of success over what has been passed as"
                           + "a parameter.\n Default : 100, 60000")

    argparser.add_argument("--csv",
                           "-c",
                           required=True,
                           help="the csv file to open")
    
    argparser.add_argument("--table_OK_index_sorted",
                           "-t",
                           nargs='+',
                           help="Prints the list of experiences with "
                           + "the best success rate and sorted according"
                           + "to the time it took to complete it")

    arguments = argparser.parse_args()

    # sets the arguments
    csv_file = arguments.csv
    experience.set_experiences_from_csv(csv_file)
    if arguments.normalisation:
        experience.normalise_all_times()

    plot = experience.generate_array_of_data()
    print(len(plot))
#    plots = get_values_as_json(csv_file)

    if arguments.mode == 'time':
        plotting.get_values_time(plot)
    elif arguments.mode == 'success':
        plotting.get_number_of_OK_per_id(plot)
    elif arguments.mode == 'hall_of_fame':
        plotting.get_hall_of_fame(plot)
    elif arguments.table_OK_index_sorted:
        plotting.print_n_exp_with_full_success(plot)
        return
    elif arguments.avg_OK_percentage:
        plotting.get_time_from_minimum_number_of_good_answers(
            plot, int(arguments.avg_OK_percentage[0]),
            experience.get_number_of_persons(),
            int(arguments.avg_OK_percentage[1]))

    plotting.create_plot()
# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
