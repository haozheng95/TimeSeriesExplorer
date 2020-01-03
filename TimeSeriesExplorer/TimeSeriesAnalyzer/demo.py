#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yinhaozheng
@software: PyCharm
@file: main.py
@time: 2019-10-31 11:23
"""
import json
import os
import random
import pandas as pd

from TimeSeriesExplorer.TimeSeriesAnalyzer.TimeSeries.TimeSeriesAnalyzer import TimeSeriesAnalyzer

__mtime__ = '2019-10-31'


def phm_17():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/phm_17.data")
    feature_list = ['f_101', 'f_102', 'f_103', 'f_104', 'f_105', 'f_106', 'f_107', 'f_108', 'f_109', 'f_110', 'f_111',
                    'f_112', 'f_113', 'f_114', 'f_115', 'f_116', 'f_117', 'f_118', 'f_119', 'f_120', 'f_121', 'f_122',
                    'f_123', 'f_124', 'f_125', 'f_126', 'f_127', 'f_128', 'f_129', 'f_130', 'f_131', 'f_132', 'f_133',
                    'f_134', 'f_135', 'f_136', 'f_137', 'f_138', 'f_139', 'f_140', 'f_141', 'f_142', 'f_143', 'f_144',
                    'f_145', 'f_146', 'f_147', 'f_148', 'f_149', 'f_150', 'f_151', 'f_152', 'f_153', 'f_154', 'f_155',
                    'f_156', 'f_157', 'f_158', 'f_159', 'f_160', 'f_161', 'f_162', 'f_163', 'f_164', 'f_165', 'f_166',
                    'f_167', 'f_168', 'f_169', 'f_170', 'f_171', 'f_172', 'f_173', 'f_174', 'f_175', 'f_176', 'f_177',
                    'f_178', 'f_179', 'f_180', 'f_181', 'f_182', 'f_183', 'f_184', 'f_185', 'f_186', 'f_187', 'f_188',
                    'f_189', 'f_190']
    t = TimeSeriesAnalyzer(feature_list, data_path)
    return dict(
        problem_category=t.get_problem_category(),
        problem_desc=t.get_problem_desc(),
        feature_desc={x: t.get_feature_desc(x) for x in t.feature_list},
        features_rel=t.get_features_rel(),
        missing_data=t.get_missing_data(),
        feature_list=t.feature_list,
        features_target_rel=t.get_features_target_rel(),
        dimension_info=t.get_dimension_info(),
        feature_info=t.get_feature_info()
    )


def phm_16():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/phm_16.data")
    feature_list = ['MACHINE_ID', 'MACHINE_DATA', 'TIMESTAMP', 'WAFER_ID', 'STAGE', 'CHAMBER', 'USAGE_OF_BACKING_FILM',
                    'USAGE_OF_DRESSER', 'USAGE_OF_POLISHING_TABLE', 'USAGE_OF_DRESSER_TABLE',
                    'PRESSURIZED_CHAMBER_PRESSURE', 'MAIN_OUTER_AIR_BAG_PRESSURE', 'CENTER_AIR_BAG_PRESSURE',
                    'RETAINER_RING_PRESSURE', 'RIPPLE_AIR_BAG_PRESSURE', 'USAGE_OF_MEMBRANE',
                    'USAGE_OF_PRESSURIZED_SHEET', 'SLURRY_FLOW_LINE_A', 'SLURRY_FLOW_LINE_B', 'SLURRY_FLOW_LINE_C',
                    'WAFER_ROTATION', 'STAGE_ROTATION', 'HEAD_ROTATION', 'DRESSING_WATER_STATUS',
                    'EDGE_AIR_BAG_PRESSURE']
    t = TimeSeriesAnalyzer(feature_list, data_path)
    return dict(
        problem_category=t.get_problem_category(),
        problem_desc=t.get_problem_desc(),
        feature_desc={x: t.get_feature_desc(x) for x in t.feature_list},
        features_rel=t.get_features_rel(),
        missing_data=t.get_missing_data(),
        feature_list=t.feature_list,
        features_target_rel=t.get_features_target_rel(),
        dimension_info=t.get_dimension_info(),
        feature_info=t.get_feature_info()
    )


def conver_feature_desc(data):
    if isinstance(data, str):
        data = eval(data)
    descriptive_statistics_summary = data["Descriptive statistics summary"]
    descriptive_statistics_summary = eval("{" + descriptive_statistics_summary + "}")
    descriptive_statistics_summary["b25"] = descriptive_statistics_summary["25%"]
    descriptive_statistics_summary["b50"] = descriptive_statistics_summary["50%"]
    descriptive_statistics_summary["b75"] = descriptive_statistics_summary["75%"]

    histogram = data["Histogram"].replace('"', '').split(",")
    histogram_list = []
    for row in histogram:
        t = row.split(":")
        for j in [[str(t[1]), float(t[0].strip())]] * int((t[1])):
            histogram_list.append(j)

    skewness = data["Skewness"]

    kurtosis = data["Kurtosis"]

    rolling_mean = data["Rolling_mean"]
    rolling_mean = rolling_mean.replace('"', '').split(",")
    rolling_mean_list = []
    for row in rolling_mean:
        t = row.split(":")
        rolling_mean_list.append([int(t[0].strip()), float(t[1])])

    rolling_std = data["Rolling_std"]
    rolling_std = rolling_std.replace('"', '').split(",")
    rolling_std_list = []
    for row in rolling_std:
        t = row.split(":")
        rolling_std_list.append([int(t[0].strip()), float(t[1])])

    seasonal = data["Seasonal"]
    seasonal = seasonal.replace('"', '').split(",")
    seasonal_list = []
    i = 0
    for row in seasonal:
        row = float(row.strip())
        seasonal_list.append([i, row])
        i += 1

    trend = data["Trend"]
    trend = trend.replace('"', '').split(",")
    trend_list = []
    i = 0
    for row in trend:
        row = float(row.strip())
        trend_list.append([i, row])
        i += 1

    resid = data["Resid"]
    resid = resid.replace('"', '').split(",")
    resid_list = []
    i = 0
    for row in resid:
        row = float(row.strip())
        resid_list.append([i, row])
        i += 1

    observed = data["Observed"]
    observed = observed.replace('"', '').split(",")
    observed_list = []
    i = 0
    for row in observed:
        row = float(row.strip())
        observed_list.append([i, row])
        i += 1

    # rolling_std_mean_list = []
    # i = 0
    # for row in rolling_std_list:
    #     t = row
    #     t.append(rolling_mean_list[i][1])
    #     rolling_std_mean_list.append(t)
    #     i += 1

    return dict(
        resid_list=resid_list,
        trend_list=trend_list,
        seasonal_list=seasonal_list,
        rolling_std_list=rolling_std_list,
        rolling_mean_list=rolling_mean_list,
        # rolling_std_mean_list=rolling_std_mean_list,
        histogram_list=histogram_list,
        descriptive_statistics_summary=descriptive_statistics_summary,
        skewness=skewness,
        kurtosis=kurtosis,
        observed_list=observed_list
    )


def conver_problem_desc(data):
    descriptive_statistics_summary = data["Descriptive statistics summary"]

    skewness = data["Skewness"]
    kurtosis = data["Kurtosis"]

    descriptive_statistics_summary = eval("{" + descriptive_statistics_summary + "}")

    histogram = data["Histogram"].replace('"', '').split(",")
    histogram_list = []
    for row in histogram:
        t = row.split(":")
        histogram_list.append([t[1], float(t[0])])
    return dict(histogram_list=histogram_list,
                descriptive_statistics_summary=descriptive_statistics_summary,
                skewness=skewness,
                kurtosis=kurtosis
                )


def conver_features_rel(data):
    matrix = []
    for k, v in data.items():
        t = []
        for x in v.values():
            if x is None:
                continue
            else:
                t.append(x)
        if len(t) > 0:
            matrix.append(t)
    return matrix


def conver_features_target_rel(data, problem_category=1):
    if isinstance(data, str):
        data = eval(data)
    if problem_category == 1:
        classification = {}
        classification_list = []
        for row in data:
            if row["class"] in classification:
                classification[row["class"]].append(
                    [row["x"], row["y"], random.randint(10, 99) / 100, random.randint(10, 99) / 100,
                     random.randint(10, 99) / 100])
            else:
                classification[row["class"]] = [
                    [row["x"], row["y"], random.randint(10, 99) / 100, random.randint(10, 99) / 100,
                     random.randint(10, 99) / 100]]
        classification_list = [["x", "healthy", "a", "b", "c"]]
        classification_list += classification["healthy"]
        return classification_list
    # classification_list = [["features", "values", {"role": "'style'"}]]
    classification_list = []
    features = ["features"]
    values = ["feature-value"]
    for k, v in data.items():
        temp = [k, v["target"], "#5286ec"]
        classification_list.append(temp)
    #     features.append(k)
    #     values.append(v["target"])
    # classification_list = [features,values]
    return classification_list


def conver_missing_data(data):
    if isinstance(data, str):
        return json.loads(data)
    return data


def conver_dimension_info(data):
    if isinstance(data, str):
        return eval(data)
    return data


def get_feature_list(path):
    content = set()
    with open(path) as f:
        for line in f:
            text = line
            if text[0] == "\t" or text[0] == "\n":
                continue
            text = text.replace("\n", "")
            content.add(text)
    feature_list = list(content)
    return feature_list


def phm(data_path, feature_list) -> dict:
    t = TimeSeriesAnalyzer(feature_list, data_path)
    return dict(
        problem_category=t.get_problem_category(),
        problem_desc=t.get_problem_desc(),
        feature_desc={x: t.get_feature_desc(x) for x in t.feature_list},
        features_rel=t.get_features_rel(),
        missing_data=t.get_missing_data(),
        features_target_rel=t.get_features_target_rel(),
        dimension_info=t.get_dimension_info(),
        feature_info=t.get_feature_info(),
        feature_list=t.feature_list,
    )


def conver_feature_info(data):
    result = []
    for k, v in data.items():
        v["feature"] = k
        result.append(v)
    return result


if __name__ == '__main__':
    data = phm_17()
    # feature_desc = data["feature_desc"]
    # problem_desc = data["problem_desc"]
    # features_rel = data["features_rel"]
    # missing_data = data["missing_data"]
    # dimension_info = data["dimension_info"]
    # feature_info = data["feature_info"]
    # print(type(dimension_info))
    # print(dimension_info)
    # print(conver_feature_info(feature_info))
    # print(conver_missing_data(missing_data))
    # for k, v in conver_feature_desc(feature_desc).items():
    #     print(k, "--------->>>", v)
    # for k, v in conver_problem_desc(problem_desc).items():
    #     print(k, "--------->>>", v)

    path = "data/timeseries.data"

    # print(get_feature_list(path))
    # phm(path)
