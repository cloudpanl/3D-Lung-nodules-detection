# -*- coding: utf-8 -*-
"""
Created on 2018/12/19 11:00

# 建立一个起始的预训练，该预训练以之前训练好的n-net为初始节点node and fix，并封装了topk等部分参数，第2阶段就在该预训练基础上做精调
"""
import torch
import numpy as np
import argparse
from importlib import import_module
parser = argparse.ArgumentParser(description='network surgery')
parser.add_argument('--model1', '-m1', metavar='MODEL', default='base',
                    help='model')
parser.add_argument('--model2', '-m2', metavar='MODEL', default='base',
                    help='model')
parser.add_argument('--resume', default='', type=str, metavar='PATH',
                    help='path to latest checkpoint (default: none)')
# args = parser.parse_args(['--model1','net_detector_3','--model2','net_classifier_3','--resume','../detector/results/res18-20170419-153425/020.ckpt'])
args = parser.parse_args()

nodmodel = import_module(args.model1)
config1, nod_net, loss, get_pbb = nodmodel.get_model()
checkpoint = torch.load(args.resume)
state_dict = checkpoint['state_dict']
nod_net.load_state_dict(state_dict)

casemodel = import_module(args.model2)

config2 = casemodel.config
args.lr_stage2 = config2['lr_stage']
args.lr_preset2 = config2['lr']
topk = config2['topk']
case_net = casemodel.CaseNet(topk = topk,nodulenet=nod_net)
new_state_dict = case_net.state_dict()
torch.save({'state_dict': new_state_dict,'epoch':0},'results/start.ckpt')
