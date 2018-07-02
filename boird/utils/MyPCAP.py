#! /usr/bin/python2.7
# -*- coding: utf-8 -*-


"""
Created on 2017-5-24


@module: MyPCAP
@used: .pcap capture and analysis
"""

import scapy


dpkt  = sniff(iface = "wlp7s0", count = 100)
