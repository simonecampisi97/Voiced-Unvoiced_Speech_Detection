# This Libraray is modified based the work by Milo Spencer-Harper and Oli Blum,
# https://stackoverflow.com/a/37366154/10404826 On top of that, I added support for showing weights (linewidth,
# colors, etc.) Contributor: Jianzheng Liu Contact: jzliu.100@gmail.com
import copy

from matplotlib import pyplot
from math import cos, sin, atan
from time import localtime, strftime
import numpy as np


class Neuron:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, neuron_radius, ax, id=-1, label=None):
        circle = pyplot.Circle((self.x, self.y), radius=neuron_radius, fill=False)
        ax.add_patch(circle)
        ax.text(self.x, self.y - 0.15, str(id), size=10, ha='center')
        if label is not None:
            ax.text(self.x, self.y - 1.5, label, size=8, ha='center', va='top')


class Layer:
    def __init__(self, network, number_of_neurons, number_of_neurons_in_widest_layer):
        self.vertical_distance_between_layers = 8
        self.horizontal_distance_between_neurons = 2
        self.neuron_radius = 0.5
        self.number_of_neurons_in_widest_layer = number_of_neurons_in_widest_layer
        self.previous_layer = self.__get_previous_layer(network)
        self.y = self.__calculate_layer_y_position()
        self.neurons = self.__intialise_neurons(number_of_neurons)

    def __intialise_neurons(self, number_of_neurons):
        neurons = []
        x = self.__calculate_left_margin_so_layer_is_centered(number_of_neurons)
        for iteration in range(number_of_neurons):
            neuron = Neuron(x, self.y)
            neurons.append(neuron)
            x += self.horizontal_distance_between_neurons
        return neurons

    def __calculate_left_margin_so_layer_is_centered(self, number_of_neurons):
        return self.horizontal_distance_between_neurons * (
                self.number_of_neurons_in_widest_layer - number_of_neurons) / 2

    def __calculate_layer_y_position(self):
        if self.previous_layer:
            return self.previous_layer.y + self.vertical_distance_between_layers
        else:
            return 0

    def __get_previous_layer(self, network):
        if len(network.layers) > 0:
            return network.layers[-1]
        else:
            return None

    def __line_between_two_neurons(self, neuron1, neuron2, ax, weight=0.4, textoverlaphandler=None, real_weight=0.4):
        angle = atan((neuron2.x - neuron1.x) / float(neuron2.y - neuron1.y))
        x_adjustment = self.neuron_radius * sin(angle)
        y_adjustment = self.neuron_radius * cos(angle)

        # assign colors to lines depending on the sign of the weight
        color = 'red'
        if weight > 0:
            color = 'green'

        # assign different line_widths to lines depending on the size of the weight
        abs_weight = abs(weight)
        if abs_weight > 0.5:
            linewidth = 4 * abs_weight
        elif abs_weight > 0.8:
            linewidth = 6 * abs_weight
        else:
            linewidth = 2 * abs_weight

        # linewidth = abs_weight * 4

        # draw the weights and adjust the labels of weights to avoid overlapping
        if abs_weight > 0.5:
            # while loop to determine the optimal locaton for text labels to avoid overlapping
            index_step = 2
            num_segments = 10
            txt_x_pos = neuron1.x - x_adjustment + index_step * (
                    neuron2.x - neuron1.x + 2 * x_adjustment) / num_segments
            txt_y_pos = neuron1.y - y_adjustment + index_step * (
                    neuron2.y - neuron1.y + 2 * y_adjustment) / num_segments
            while ((not textoverlaphandler.getspace([txt_x_pos - 0.5, txt_y_pos - 0.5, txt_x_pos + 0.5,
                                                     txt_y_pos + 0.5])) and index_step < num_segments):
                index_step = index_step + 1
                txt_x_pos = neuron1.x - x_adjustment + index_step * (
                        neuron2.x - neuron1.x + 2 * x_adjustment) / num_segments
                txt_y_pos = neuron1.y - y_adjustment + index_step * (
                        neuron2.y - neuron1.y + 2 * y_adjustment) / num_segments

            # print("Label positions: ", "{:.2f}".format(txt_x_pos), "{:.2f}".format(txt_y_pos), "{:3.2f}".format(
            # weight))
            a = ax.text(txt_x_pos, txt_y_pos, "{:3.2f}".format(real_weight), size=8, ha='center')
            a.set_bbox(dict(facecolor='white', alpha=0))
            # print(a.get_bbox_patch().get_height())

        line = pyplot.Line2D((neuron1.x - x_adjustment, neuron2.x + x_adjustment),
                         (neuron1.y - y_adjustment, neuron2.y + y_adjustment), linewidth=linewidth, color=color)
        ax.add_line(line)

    def draw(self, ax, layerType=0, weights=None, textoverlaphandler=None, input_label=None, real_weights=None):
        j = 0  # index for neurons in this layer
        for k, neuron in enumerate(self.neurons):
            i = 0  # index for neurons in previous layer
            neuron_label = input_label[k] if input_label is not None else None
            neuron.draw(self.neuron_radius, ax=ax, id=j + 1, label=neuron_label)
            if self.previous_layer:
                for previous_layer_neuron in self.previous_layer.neurons:
                    self.__line_between_two_neurons(neuron, previous_layer_neuron, ax, weights[i, j],
                                                    textoverlaphandler, real_weight=real_weights[i, j])
                    i = i + 1
            j = j + 1

        # write Text
        x_text = self.number_of_neurons_in_widest_layer * self.horizontal_distance_between_neurons
        if layerType == 0:
            ax.text(x_text, self.y, 'Input Layer', fontsize=12)
        elif layerType == -1:
            ax.text(x_text, self.y, 'Output Layer', fontsize=12)
        else:
            ax.text(x_text, self.y, 'Hidden Layer ' + str(layerType), fontsize=12)


# A class to handle Text Overlapping
# The idea is to first create a grid space, if a grid is already occupied, then
# the grid is not available for text labels.
class TextOverlappingHandler:
    # initialize the class with the width and height of the plot area
    def __init__(self, width, height, grid_size=0.2):
        self.grid_size = grid_size
        self.cells = np.ones((int(np.ceil(width / grid_size)), int(np.ceil(height / grid_size))), dtype=bool)

    # input test_coordinates(bottom left and top right), 
    # getspace will tell you whether a text label can be put in the test coordinates
    def getspace(self, test_coordinates):
        x_left_pos = int(np.floor(test_coordinates[0] / self.grid_size))
        y_botttom_pos = int(np.floor(test_coordinates[1] / self.grid_size))
        x_right_pos = int(np.floor(test_coordinates[2] / self.grid_size))
        y_top_pos = int(np.floor(test_coordinates[3] / self.grid_size))
        if self.cells[x_left_pos, y_botttom_pos] and self.cells[x_left_pos, y_top_pos] \
                and self.cells[x_right_pos, y_top_pos] and self.cells[x_right_pos, y_botttom_pos]:
            for i in range(x_left_pos, x_right_pos):
                for j in range(y_botttom_pos, y_top_pos):
                    self.cells[i, j] = False

            return True
        else:
            return False


class NeuralNetwork:
    def __init__(self, number_of_neurons_in_widest_layer):
        self.number_of_neurons_in_widest_layer = number_of_neurons_in_widest_layer
        self.layers = []
        self.layertype = 0

    def add_layer(self, number_of_neurons):
        layer = Layer(self, number_of_neurons, self.number_of_neurons_in_widest_layer)
        self.layers.append(layer)

    def draw(self, ax, weights_list=None, input_label=None, real_weights_list=None):
        # vertical_distance_between_layers and horizontal_distance_between_neurons are the same with the variables of
        # the same name in layer class
        vertical_distance_between_layers = 6
        horizontal_distance_between_neurons = 2
        overlaphandler = TextOverlappingHandler(
            self.number_of_neurons_in_widest_layer * horizontal_distance_between_neurons,
            len(self.layers) * vertical_distance_between_layers, grid_size=0.2)

        for i in range(len(self.layers)):
            layer = self.layers[i]
            if i == 0:
                layer.draw(ax=ax, layerType=0, input_label=input_label)
            elif i == len(self.layers) - 1:
                layer.draw(ax=ax, layerType=-1, weights=weights_list[i - 1],
                           textoverlaphandler=overlaphandler,
                           real_weights=real_weights_list[i - 1])
            else:
                layer.draw(ax=ax, layerType=i, weights=weights_list[i - 1],
                           textoverlaphandler=overlaphandler,
                           real_weights=real_weights_list[i - 1])

        ax.axis('scaled')
        ax.axis('off')
        ax.set_title('Neural Network architecture', fontsize=15)

        # figureName = 'ANN_' + strftime("%Y%m%d_%H%M%S", localtime()) + '.png'
        # pyplot.savefig(figureName, dpi=300, bbox_inches="tight")
        # pyplot.show()


class DrawNN:
    # para: neural_network is an array of the number of neurons from input layer to output layer, e.g.,
    # a neural network of 5 nerons in the input layer, 10 neurons in the hidden layer 1 and 1 neuron in the output
    # layer is [5, 10, 1] para: weights_list (optional) is the output weights list of a neural network which can be
    # obtained via classifier.coefs_
    def __init__(self, neural_network, weights_list=None, input_label=None):
        self.input_label = input_label
        self.neural_network = neural_network
        self.weights_list = weights_list
        self.weights_list_normalized = self.normalize_weights()

        # if weights_list is none, then create a uniform list to fill the weights_list
        if weights_list is None:
            weights_list = []
            for first, second in zip(neural_network, neural_network[1:]):
                tempArr = np.ones((first, second)) * 0.4
                print(first, second)
                weights_list.append(tempArr)
            self.weights_list = weights_list

    def normalize_weights(self):
        normalized_weights = copy.deepcopy(self.weights_list)

        for layer_id in range(len(normalized_weights)):
            curr_max = np.max(np.abs(np.array(normalized_weights[layer_id])))

            for i in range(len(normalized_weights[layer_id])):
                for j in range(len(normalized_weights[layer_id][i])):
                    normalized_weights[layer_id][i][j] = normalized_weights[layer_id][i][j] / curr_max

        return normalized_weights

    def draw(self, ax):
        widest_layer = max(self.neural_network)
        network = NeuralNetwork(widest_layer)
        for l in self.neural_network:
            network.add_layer(l)
        network.draw(ax, self.weights_list_normalized, self.input_label,
                     self.weights_list)
