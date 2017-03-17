# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 21:42:51 2016

@author: picturio
"""

    
import os
import numpy as np
import matplotlib.pyplot as plt

from cntk.blocks import default_options
#from cntk.device import gpu, set_default_device
from cntk.ops import cross_entropy_with_softmax, classification_error, relu, input_variable, softmax, combine, times, element_times, AVG_POOLING
from cntk.layers import Convolution, MaxPooling, AveragePooling, Dropout, BatchNormalization, Dense
from cntk.models import Sequential, LayerStack
from cntk.io import MinibatchSource, ImageDeserializer, StreamDef, StreamDefs
from cntk.initializer import glorot_uniform, he_normal
from cntk import Trainer
from cntk.learner import momentum_sgd, learning_rate_schedule, UnitType, momentum_as_time_constant_schedule
from cntk.utils import *


# model dimensions
image_height = 32
image_width  = 32
num_channels = 3
num_classes  = 70
dataDir='d://Projects//data//PRAKTIKER//'


def convolution_bn(input, filter_size, num_filters, strides=(1,1), init=he_normal(), activation=relu):
    if activation is None:
        activation = lambda x: x
        
    r = Convolution(filter_size, num_filters, strides=strides, init=init, activation=None, pad=True, bias=False)(input)
    r = BatchNormalization(map_rank=1)(r)
    r = activation(r)
    
    return r

def resnet_basic(input, num_filters):
    c1 = convolution_bn(input, (3,3), num_filters)
    c2 = convolution_bn(c1, (3,3), num_filters, activation=None)
    p  = c2 + input
    return relu(p)

def resnet_basic_inc(input, num_filters):
    c1 = convolution_bn(input, (3,3), num_filters, strides=(2,2))
    c2 = convolution_bn(c1, (3,3), num_filters, activation=None)

    s = convolution_bn(input, (1,1), num_filters, strides=(2,2), activation=None)
    
    p = c2 + s
    return relu(p)

def resnet_basic_stack(input, num_filters, num_stack):
    assert (num_stack > 0)
    
    r = input
    for _ in range(num_stack):
        r = resnet_basic(r, num_filters)
    return r

def create_basic_model(input, out_dims):
    
    net = Convolution((5,5), 64, init=glorot_uniform(), activation=relu, pad=True)(input)
    net = MaxPooling((3,3), strides=(2,2))(net)

    net = Convolution((5,5), 64, init=glorot_uniform(), activation=relu, pad=True)(net)
    net = MaxPooling((3,3), strides=(2,2))(net)

    net = Convolution((5,5), 128, init=glorot_uniform(), activation=relu, pad=True)(net)
    net = MaxPooling((3,3), strides=(2,2))(net)
    
    net = Dense(128, init=glorot_uniform())(net)
    net = Dense(out_dims, init=glorot_uniform(), activation=None)(net)
    
    return net
 
def create_basic_model_with_batch_normalization(input, out_dims):

    with default_options(activation=relu):
        model = Sequential([
            LayerStack(3, lambda i: [
                Convolution((5,5), [32,32,64][i], init=glorot_uniform(), pad=True),
                BatchNormalization(map_rank=1),
                MaxPooling((3,3), strides=(2,2))
            ]),
            Dense(64, init=glorot_uniform()),
            BatchNormalization(map_rank=1),
            Dense(out_dims, init=glorot_uniform(), activation=None)
        ])

    return model(input)
    
def create_vgg9_model(input, out_dims):
    with default_options(activation=relu):
        model = Sequential([
            LayerStack(3, lambda i: [
                Convolution((3,3), [64,64,96,128][i], init=glorot_uniform(), pad=True),
                Convolution((3,3), [64,64,96,128][i], init=glorot_uniform(), pad=True),
                MaxPooling((3,3), strides=(2,2))
            ]),
            LayerStack(2, lambda : [
                Dense(1024, init=glorot_uniform())
            ]),
            Dropout(0.5),
            Dense(out_dims, init=glorot_uniform(), activation=None)
        ])
        
    return model(input)
    
def create_resnet_model(input, out_dims):
    conv = convolution_bn(input, (3,3), 16)
    r1_1 = resnet_basic_stack(conv, 16, 3)

    r2_1 = resnet_basic_inc(r1_1, 32)
    r2_2 = resnet_basic_stack(r2_1, 32, 2)

    r3_1 = resnet_basic_inc(r2_2, 64)
    r3_2 = resnet_basic_stack(r3_1, 64, 2)

    # Global average pooling
    dropout = Dropout(0.5)(r3_2)
    pool = AveragePooling(filter_shape=(8,8), strides=(1,1))(dropout)    
    net = Dense(out_dims, init=he_normal(), activation=None)(pool)
    
    return net  
    

#
# Define the reader for both training and evaluation action.
#
def create_reader(map_file, mean_file, train):
  
    # transformation pipeline for the features has jitter/crop only when training
    transforms = []
    if train:
        transforms += [
            ImageDeserializer.crop(crop_type='Random', ratio=0.8, jitter_type='uniRatio') # train uses jitter
        ]
    transforms += [
        ImageDeserializer.scale(width=image_width, height=image_height, channels=num_channels, interpolations='linear'),
        ImageDeserializer.mean(mean_file)
    ]
    # deserializer
    return MinibatchSource(ImageDeserializer(map_file, StreamDefs(
        features = StreamDef(field='image', transforms=transforms), # first column in map file is referred to as 'image'
        labels   = StreamDef(field='label', shape=num_classes)      # and second as 'label'
    )))
    
#
# Train and evaluate the network.
#
def train_and_evaluate(reader_train, reader_test, max_epochs, model_func):
    # Input variables denoting the features and label data
    input_var = input_variable((num_channels, image_height, image_width))
    label_var = input_variable((num_classes))

    # Normalize the input
    feature_scale = 1.0 / 256.0
    input_var_norm = element_times(feature_scale, input_var)
    
    # apply model to input
    z = model_func(input_var_norm, out_dims=num_classes)

    #
    # Training action
    #

    # loss and metric
    ce = cross_entropy_with_softmax(z, label_var)
    pe = classification_error(z, label_var)

    # training config
    epoch_size     = 20292
    minibatch_size = 32

    # Set training parameters
    lr_per_minibatch       = learning_rate_schedule([0.01]*10 + [0.003]*10 + [0.001],  UnitType.minibatch, epoch_size)
    momentum_time_constant = momentum_as_time_constant_schedule(-minibatch_size/np.log(0.9))
    l2_reg_weight          = 0.001
    
    # trainer object
    learner     = momentum_sgd(z.parameters, 
                               lr = lr_per_minibatch, momentum = momentum_time_constant, 
                               l2_regularization_weight=l2_reg_weight)
    trainer     = Trainer(z, ce, pe, [learner])

    # define mapping from reader streams to network inputs
    input_map = {
        input_var: reader_train.streams.features,
        label_var: reader_train.streams.labels
    }

    log_number_of_parameters(z) ; print()
    progress_printer = ProgressPrinter(tag='Training')

    # perform model training
    batch_index = 0
    plot_data = {'batchindex':[], 'loss':[], 'error':[]}
    for epoch in range(max_epochs):       # loop over epochs
        sample_count = 0
        while sample_count < epoch_size:  # loop over minibatches in the epoch
            data = reader_train.next_minibatch(min(minibatch_size, epoch_size - sample_count), input_map=input_map) # fetch minibatch.
            trainer.train_minibatch(data)                                   # update model with it

            sample_count += data[label_var].num_samples                     # count samples processed so far
            
            # For visualization...            
            plot_data['batchindex'].append(batch_index)
            plot_data['loss'].append(trainer.previous_minibatch_loss_average)
            plot_data['error'].append(trainer.previous_minibatch_evaluation_average)
            
            progress_printer.update_with_trainer(trainer, with_metric=True) # log progress
            batch_index += 1
        progress_printer.epoch_summary(with_metric=True)
        
    #
    # Evaluation action
    #
    epoch_size     = 8665
    minibatch_size = 16

    # process minibatches and evaluate the model
    metric_numer    = 0
    metric_denom    = 0
    sample_count    = 0
    minibatch_index = 0

    while sample_count < epoch_size:
        current_minibatch = min(minibatch_size, epoch_size - sample_count)

        # Fetch next test min batch.
        data = reader_test.next_minibatch(current_minibatch, input_map=input_map)

        # minibatch data to be trained with
        metric_numer += trainer.test_minibatch(data) * current_minibatch
        metric_denom += current_minibatch

        # Keep track of the number of samples processed so far.
        sample_count += data[label_var].num_samples
        minibatch_index += 1

    print("")
    print("Final Results: Minibatch[1-{}]: errs = {:0.1f}% * {}".format(minibatch_index+1, (metric_numer*100.0)/metric_denom, metric_denom))
    print("")
    
    # Visualize training result:
    window_width            = 32
    loss_cumsum             = np.cumsum(np.insert(plot_data['loss'], 0, 0)) 
    error_cumsum            = np.cumsum(np.insert(plot_data['error'], 0, 0)) 

    # Moving average.
    plot_data['batchindex'] = np.insert(plot_data['batchindex'], 0, 0)[window_width:]
    plot_data['avg_loss']   = (loss_cumsum[window_width:] - loss_cumsum[:-window_width]) / window_width
    plot_data['avg_error']  = (error_cumsum[window_width:] - error_cumsum[:-window_width]) / window_width
    
    plt.figure(1)
    plt.subplot(211)
    plt.plot(plot_data["batchindex"], plot_data["avg_loss"], 'b--')
    plt.xlabel('Minibatch number')
    plt.ylabel('Loss')
    plt.title('Minibatch run vs. Training loss ')
    
    plt.show()

    plt.subplot(212)
    plt.plot(plot_data["batchindex"], plot_data["avg_error"], 'r--')
    plt.xlabel('Minibatch number')
    plt.ylabel('Label Prediction Error')
    plt.title('Minibatch run vs. Label Prediction Error ')
    plt.show()
    
    return softmax(z)
    
reader_train = create_reader(os.path.join(dataDir, 'train_map.txt'), os.path.join(dataDir, 'PRAKTIKER_mean.xml'), True)
reader_test  = create_reader(os.path.join(dataDir, 'test_map.txt'), os.path.join(dataDir, 'PRAKTIKER_mean.xml'), False)

#pred = train_and_evaluate(reader_train, reader_test, max_epochs=10, model_func=create_basic_model)

#pred_vgg  = train_and_evaluate(reader_train, reader_test, max_epochs=50, model_func=create_vgg9_model)

pred_resnet = train_and_evaluate(reader_train, reader_test, max_epochs=25, model_func=create_resnet_model)

#pred_batch= train_and_evaluate(reader_train, reader_test, max_epochs=10, model_func=create_basic_model_with_batch_normalization)