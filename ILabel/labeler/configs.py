# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 10:39:08 2018
config parameters in U-net
@author: yang
"""

import os

#########################
#   General Settings    #
#########################

# name of current experiment / output folder
# experiment_name = 'example_experiment'
experiment_name = 'example_experiment'

# input and output directory paths
raw_data_dir =  './data_Mid100/' # data_epi_all/ data_endo_all/ data_mid_myo/data_Mid100
pp_data_dir = os.path.join(raw_data_dir, 'preprocessed_data')
exp_dir= os.path.join(raw_data_dir, experiment_name) #change raw_data_dir to desired output folder
test_dir = os.path.join(exp_dir, 'test_files')
plot_dir = os.path.join(exp_dir, 'plots')

# data dimensions
dim = 3     # [2,3] train a 2D or 3D U-Net architecture.
n_channels = 1
n_classes = 2

# seed for cross validation splits
seed = 12345
# direction of the test set
# exp_path = './exp_path/'
# number of cpu used for mu'train', 'test'lti-threaded batch generation
n_workers = 10

# training configs
n_cv_splits = 5
n_epochs = 180
learning_rate = 10**(-3)

# the loss function to be used: either one of 'cross_entropy', 'weighted_cross_entropy', or 'dice_coefficient'
loss_name = 'dice_coefficient'

#taken from preprocessing.py . weights are 1 minus averaged class occurrence averaged over patients in the training set
class_weights = [0.394, 0.988]

# class names for monitoring plot. 
# additional FG (foreground) class is the average of the two foreground classes and monitored as selection criterion.
class_dict = {0:'nonheart', 1:'heart', 2:'FG'}

# data augmentation configs
da_kwargs={
'do_elastic_deform': True,
'alpha':(0., 1500.),
'sigma':(30., 50.),
'do_rotation':True,
'angle_z': (0., 2*3.14),
'do_scale':True,
'scale':(0.7, 1.3),
'random_crop':True,
}

#########################
#     2D   UNET        #
#########################

# settings specific to 2D UNet training.
if dim == 2:

    n_features_root = 32
    pre_crop_size = (32, 32)   #patch size before random_crop
    patch_size = (32, 32) # patch size after random_crop
    network_input_shape = [None, patch_size[0], patch_size[1], n_channels]
    network_output_shape = [None, patch_size[0], patch_size[1], n_classes]

    n_train_batches = 40
    n_val_batches = 10
    batch_size= 20
    da_kwargs['angle_x'] = (0, 2*3.14)
    da_kwargs['angle_y'] = (0, 2*3.14)

    # allowed shift from the patch center during random crop
    da_kwargs['rand_crop_dist'] = (pre_crop_size[0] / 2. - 5, pre_crop_size[1] / 2. - 5)

#########################
#        3D UNET        #
#########################

# settings specific to 3D UNet training.
if dim == 3:

    n_features_root = 12
    pre_crop_size = (32, 32, 20)  # patch size before random_crop randomly crops a tensor to a given size
    patch_size = (32, 32, 16) # patch size after random_crop
    network_input_shape = [None, patch_size[2], patch_size[0], patch_size[1], n_channels]
    network_output_shape = [None, patch_size[2], patch_size[0], patch_size[1], n_classes]

    n_train_batches = 20
    n_val_batches = 5
    batch_size = 8
    da_kwargs['angle_x'] = (0, 0.05)    # only allow for slight tilt along x and y axis.
    da_kwargs['angle_y'] = (0, 0.05)

    # allowed shift from the patch center during random crop
    da_kwargs['rand_crop_dist'] = (pre_crop_size[0] / 2. - 5, pre_crop_size[1] / 2. - 5, pre_crop_size[2] / 2. - 2)