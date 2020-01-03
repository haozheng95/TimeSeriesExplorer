#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:
@software: PyCharm
@file: views.py
@time: 2019-10-25 09:38
"""
import hashlib
import json
import logging
import os

from TimeSeriesExplorer.TimeSeriesAnalyzer.demo import conver_problem_desc, conver_feature_desc, \
    conver_features_rel, \
    conver_features_target_rel, conver_missing_data, phm, conver_dimension_info, conver_feature_info

__mtime__ = '2019-10-25'
logger = logging.getLogger("django")
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

form_file_name = "exampleInputFile"
project_path = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(os.path.dirname(project_path), "static")
save_path = os.path.join(static_path, "data")

FEATURE_LIST = dict(
    # phm 16
    phm_193cc8e0754ecfbff5c71a2f11d1ac90=['MACHINE_ID', 'MACHINE_DATA', 'TIMESTAMP', 'WAFER_ID', 'STAGE', 'CHAMBER',
                                          'USAGE_OF_BACKING_FILM',
                                          'USAGE_OF_DRESSER', 'USAGE_OF_POLISHING_TABLE', 'USAGE_OF_DRESSER_TABLE',
                                          'PRESSURIZED_CHAMBER_PRESSURE', 'MAIN_OUTER_AIR_BAG_PRESSURE',
                                          'CENTER_AIR_BAG_PRESSURE',
                                          'RETAINER_RING_PRESSURE', 'RIPPLE_AIR_BAG_PRESSURE', 'USAGE_OF_MEMBRANE',
                                          'USAGE_OF_PRESSURIZED_SHEET', 'SLURRY_FLOW_LINE_A', 'SLURRY_FLOW_LINE_B',
                                          'SLURRY_FLOW_LINE_C',
                                          'WAFER_ROTATION', 'STAGE_ROTATION', 'HEAD_ROTATION', 'DRESSING_WATER_STATUS',
                                          'EDGE_AIR_BAG_PRESSURE'],
    # phm 17
    phm_3b115212e873188dce4734b3e8c73616=['f_101', 'f_102', 'f_103', 'f_104', 'f_105', 'f_106', 'f_107', 'f_108',
                                          'f_109', 'f_110', 'f_111',
                                          'f_112', 'f_113', 'f_114', 'f_115', 'f_116', 'f_117', 'f_118', 'f_119',
                                          'f_120', 'f_121', 'f_122',
                                          'f_123', 'f_124', 'f_125', 'f_126', 'f_127', 'f_128', 'f_129', 'f_130',
                                          'f_131', 'f_132', 'f_133',
                                          'f_134', 'f_135', 'f_136', 'f_137', 'f_138', 'f_139', 'f_140', 'f_141',
                                          'f_142', 'f_143', 'f_144',
                                          'f_145', 'f_146', 'f_147', 'f_148', 'f_149', 'f_150', 'f_151', 'f_152',
                                          'f_153', 'f_154', 'f_155',
                                          'f_156', 'f_157', 'f_158', 'f_159', 'f_160', 'f_161', 'f_162', 'f_163',
                                          'f_164', 'f_165', 'f_166',
                                          'f_167', 'f_168', 'f_169', 'f_170', 'f_171', 'f_172', 'f_173', 'f_174',
                                          'f_175', 'f_176', 'f_177',
                                          'f_178', 'f_179', 'f_180', 'f_181', 'f_182', 'f_183', 'f_184', 'f_185',
                                          'f_186', 'f_187', 'f_188',
                                          'f_189', 'f_190'],
)


def upload_view(request):
    if request.method == "GET":
        return render(request, "phm_index.html")

    task_id = upload_file(request)
    return HttpResponseRedirect("/eda-report/" + task_id)


def report_view(request, task_id):
    return render(request, "phm_show_2.html",
                  dict(
                      task_id=task_id
                  ))


def result_view(request, task_id):
    data = handle_storage_file(task_id)
    context = handle_file_data(data)
    return render(request, "result.js", context)


def upload_file(request):
    file_name = request.FILES[form_file_name].name
    hl = hashlib.md5()
    hl.update(file_name.encode(encoding='utf-8'))
    file_name = hl.hexdigest()
    task_path = os.path.join(save_path, file_name)
    handle_uploaded_file(request.FILES[form_file_name].file, task_path)
    return file_name


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f:
            destination.write(chunk)


def handle_storage_file(task_id):
    file = os.path.join(save_path, task_id)
    if "phm_" + task_id in FEATURE_LIST:
        feature_list = FEATURE_LIST["phm_" + task_id]
    else:
        feature_list = handle_feature_list()
    data = phm(file, feature_list)
    return data


def handle_feature_list(n=200, l=3):
    result = []
    for i in range(n):
        temp = str(i)
        if len(temp) < l:
            temp = "0" * (l - len(temp)) + temp
        temp = "f_" + temp
        result.append(temp)
    return result


def handle_file_data(data):
    problem_desc = data["problem_desc"]
    feature_list = data["feature_list"]
    feature_desc = data["feature_desc"]
    features_rel = data["features_rel"]
    features_target_rel = data["features_target_rel"]
    missing_data = conver_missing_data(data["missing_data"])["Total"]

    problem_category = int(data["problem_category"])

    result = dict(
        problem_category=problem_category,
        problem_desc=process_problem_desc(problem_category, problem_desc),  # part_1
        feature_desc_list=process_feature_desc(feature_desc, missing_data),  # part_2_view_list
        features_target_rel=process_features_target_rel(features_target_rel, problem_category),
        features_rel=process_features_rel(features_rel),  # matrix
        feature_list=feature_list,
        dimension_info=conver_dimension_info(data["dimension_info"]),
        feature_info=conver_feature_info(data["feature_info"])
    )
    logger.info("handle_file_data  end")
    if problem_category == 1:
        return result
    logger.info(result["problem_desc"])
    result["problem_desc_histogram_list"] = result["problem_desc"]["histogram_list"]
    result["problem_desc_descriptive_statistics_summary"] = result["problem_desc"]["descriptive_statistics_summary"]
    result["problem_desc_skewness"] = result["problem_desc"]["skewness"]
    result["problem_desc_kurtosis"] = result["problem_desc"]["kurtosis"]
    return result


def process_problem_desc(problem_category, problem_desc):
    if problem_category == 1:
        return [problem_desc.replace('"', "").split(":")]
    return conver_problem_desc(problem_desc)


def process_feature_desc(feature_desc, missing_data):
    feature_desc_list = []
    for k, v in feature_desc.items():
        temp = dict(
            feature=k,
            feature_desc=conver_feature_desc(v),
            missing_data=missing_data[k]
        )
        feature_desc_list.append(temp)
    return json.dumps(feature_desc_list)


def process_features_rel(features_rel):
    features_rel = json.loads(features_rel)
    return conver_features_rel(features_rel)


def process_features_target_rel(features_target_rel, problem_category):
    return conver_features_target_rel(features_target_rel, problem_category)
