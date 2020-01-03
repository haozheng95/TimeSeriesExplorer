import os
import warnings

from TimeSeriesExplorer.TimeSeriesAnalyzer.TimeSeries.AnomalyDetector import *
from TimeSeriesExplorer.TimeSeriesAnalyzer.TimeSeries.SingleTimeSeries import *
from TimeSeriesExplorer.TimeSeriesAnalyzer.TimeSeries.TimeSeriesRelationship import *
from TimeSeriesExplorer.TimeSeriesAnalyzer.TimeSeries.Utils import *

_logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class TimeSeriesAnalyzerInterface:
    def __init__(self, pd, y, feature_list):
        self.pd = pd
        self.y = y
        self.feature_list = feature_list

    def get_problem_desc(self):
        pass

    def get_feature_desc(self, target_feature):
        pass

    def get_features_rel(self):
        pass

    def get_feature_target_rel(self):
        pass


class TimeSeriesAnalyzerForClassification(TimeSeriesAnalyzerInterface):
    def __init__(self, pd, y, feature_list, target_to_id):
        super(self.__class__, self).__init__(pd, y, feature_list)
        self.target_to_id = target_to_id

    def get_problem_desc(self):
        class_counts = self.y.value_counts().to_json()[1:-1]

        return class_counts

    def get_feature_desc(self, target_feature):
        result = ''
        for target in self.target_to_id.keys():
            pd = self.pd[(self.pd.id == self.target_to_id[target][0])][target_feature]
            ts = SingleTimeSeries(pd)
            result += str(ts.feature_to_dict()) + '\n\n'

        return result

    def get_features_rel(self):
        result = ''
        for target in self.target_to_id.keys():
            ts = self.pd[self.pd.id.isin(self.target_to_id[target])]
            ts = pd.DataFrame(ts, columns=self.feature_list)
            result += TimeSeriesRelationship(
                pd.DataFrame(ts, columns=self.feature_list)).feature_rel_to_string() + '\n\n'

        return result

    def get_feature_target_rel(self):
        return FeatureTargetRelationship(self.pd, self.y).feature_target_pca_to_string()


class TimeSeriesAnalyzerForRegression(TimeSeriesAnalyzerInterface):
    def get_problem_desc(self):
        y = SingleTimeSeries(self.y)

        return y.feature_to_dict(if_series=False)

    def get_feature_desc(self, target_feature):
        pd = self.pd[(self.pd.id == 1)][target_feature]
        ts = SingleTimeSeries(pd)

        return ts.feature_to_dict()

    def get_features_rel(self):
        return TimeSeriesRelationship(pd.DataFrame(self.pd, columns=self.feature_list)).feature_rel_to_string()

    def get_feature_target_rel(self):
        return FeatureTargetRelationship(self.pd, self.y).feature_target_corr_to_string()


class TimeSeriesAnalyzer:
    CONST_CLASSIFICATION = 1
    CONST_REGRESSION = 2

    def __init__(self, feature_list, data_file_name, filter_outliers=True):
        self.data_file_name = data_file_name
        self.feature_list = feature_list
        self.category = self.CONST_CLASSIFICATION
        self.target_to_id = {}

        self.pd, self.y = self._load_time_series()

        if filter_outliers:
            self._remove_outliers()

        self._filter_const_features()

        if self.category == self.CONST_CLASSIFICATION:
            self.solver = TimeSeriesAnalyzerForClassification(self.pd, self.y, self.feature_list, self.target_to_id)
        elif self.category == self.CONST_REGRESSION:
            self.solver = TimeSeriesAnalyzerForRegression(self.pd, self.y, self.feature_list)

    def _load_time_series(self):
        if not os.path.exists(self.data_file_name):
            _logger.warning("The data couldn't be found.")
            return

        id_to_target = {}
        df_rows = []

        with open(self.data_file_name) as f:
            cur_id = -1
            time = 0

            for line in f.readlines():
                # New sample --> increase id, reset time and determine target
                if line[0] not in ['\t', '\n']:
                    cur_id += 1
                    time = 0
                    target = line.strip()
                    id_to_target[cur_id] = target
                    if target not in self.target_to_id.keys():
                        self.target_to_id[target] = [cur_id]
                    else:
                        self.target_to_id[target].append(cur_id)
                # Data row --> split and convert values, create complete df row
                elif line[0] == '\t':
                    values = list(map(float, line.split('\t')[1:]))
                    df_rows.append([cur_id, time] + values)
                    time += 1

        self.feature_list = self.feature_list[:len(df_rows[0]) - 2]
        df = pd.DataFrame(df_rows, columns=['id', 'time'] + self.feature_list)
        y = pd.Series(id_to_target)

        if 2 * len(set(y)) > len(y):
            self.category = self.CONST_REGRESSION

        return df, y

    def _check_solver(self):
        if self.solver is None:
            _logger.warning("Solver is not initialized.")
            return

    def _remove_outliers(self):
        if check_numeric_array(self.y):
            y = self.y.values.astype(float)
            outlier_indices = get_outliers(y)
            normal_indices = [not i for i in outlier_indices]
            normal_ids = np.where(outlier_indices == False)[0]
            self.y = self.y[normal_indices]
            self.pd = self.pd[self.pd.id.isin(normal_ids)]

    def _filter_const_features(self):
        self.const_features = []
        for feature in self.feature_list:
            if np.std(self.pd[feature]) == 0:
                self.const_features.append(feature)
                self.feature_list.remove(feature)
        self.pd = self.pd.drop(self.const_features, axis=1)

    def get_dimension_info(self):
        self.dimension_info = {}
        self.dimension_info['Number_of_observations'] = len(self.y)
        self.dimension_info['Number_of_features'] = len(self.feature_list)

        return self.dimension_info

    def get_feature_info(self):
        self.feature_info = {}
        for f in self.feature_list:
            self.feature_info[f] = {}
            feature = self.pd[f]

            self.feature_info[f]['type'] = get_feature_type(feature.dtypes)
            self.feature_info[f]['missing_count'] = feature.isnull().sum()
            self.feature_info[f]['missing_percent'] = round(feature.isnull().sum() / feature.isnull().count() * 100,
                                                            get_decimals())
            self.feature_info[f]['unique_count'] = feature.nunique()
            self.feature_info[f]['unique_percent'] = round(feature.nunique() / feature.count() * 100, get_decimals())

        return self.feature_info

    def get_const_feature(self):
        return self.const_features

    def get_missing_data(self):
        data = self.pd[self.feature_list]
        total = data.isnull().sum().sort_values(ascending=False)
        percent = (data.isnull().sum() / data.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])

        return missing_data.to_json()

    def get_problem_category(self):
        return self.category

    def get_problem_desc(self):
        self._check_solver()

        return self.solver.get_problem_desc()

    def get_feature_desc(self, target_feature):
        self._check_solver()

        return self.solver.get_feature_desc(target_feature)

    def get_features_rel(self):
        self._check_solver()

        return self.solver.get_features_rel()

    def get_features_target_rel(self):
        self._check_solver()

        return self.solver.get_feature_target_rel()


if __name__ == '__main__':
    data = 'phm_17'

    if data == 'phm_17':
        data_path = "../data/phm_16.data"
        feature_list = ['f_101', 'f_102', 'f_103', 'f_104', 'f_105', 'f_106', 'f_107', 'f_108', 'f_109', 'f_110',
                        'f_111', 'f_112', 'f_113', 'f_114', 'f_115', 'f_116', 'f_117', 'f_118', 'f_119', 'f_120',
                        'f_121', 'f_122', 'f_123', 'f_124', 'f_125', 'f_126', 'f_127', 'f_128', 'f_129', 'f_130',
                        'f_131', 'f_132', 'f_133', 'f_134', 'f_135', 'f_136', 'f_137', 'f_138', 'f_139', 'f_140',
                        'f_141', 'f_142', 'f_143', 'f_144', 'f_145', 'f_146', 'f_147', 'f_148', 'f_149', 'f_150',
                        'f_151', 'f_152', 'f_153', 'f_154', 'f_155', 'f_156', 'f_157', 'f_158', 'f_159', 'f_160',
                        'f_161', 'f_162', 'f_163', 'f_164', 'f_165', 'f_166', 'f_167', 'f_168', 'f_169', 'f_170',
                        'f_171', 'f_172', 'f_173', 'f_174', 'f_175', 'f_176', 'f_177', 'f_178', 'f_179', 'f_180',
                        'f_181', 'f_182', 'f_183', 'f_184', 'f_185', 'f_186', 'f_187', 'f_188', 'f_189', 'f_190']
    elif data == 'phm_16':
        data_path = "../data/phm_16.data"
        feature_list = ['MACHINE_ID', 'MACHINE_DATA', 'TIMESTAMP', 'WAFER_ID', 'STAGE', 'CHAMBER',
                        'USAGE_OF_BACKING_FILM', 'USAGE_OF_DRESSER', 'USAGE_OF_POLISHING_TABLE',
                        'USAGE_OF_DRESSER_TABLE', 'PRESSURIZED_CHAMBER_PRESSURE', 'MAIN_OUTER_AIR_BAG_PRESSURE',
                        'CENTER_AIR_BAG_PRESSURE', 'RETAINER_RING_PRESSURE', 'RIPPLE_AIR_BAG_PRESSURE',
                        'USAGE_OF_MEMBRANE', 'USAGE_OF_PRESSURIZED_SHEET', 'SLURRY_FLOW_LINE_A', 'SLURRY_FLOW_LINE_B',
                        'SLURRY_FLOW_LINE_C', 'WAFER_ROTATION', 'STAGE_ROTATION', 'HEAD_ROTATION',
                        'DRESSING_WATER_STATUS', 'EDGE_AIR_BAG_PRESSURE']
    elif data == 'timeseries':
        data_path = "../data/timeseries.data"
        feature_list = ['F_x', 'F_y', 'F_z', 'P_x', 'P_y', 'P_z']

    t = TimeSeriesAnalyzer(feature_list, data_path)
    print(t.get_dimension_info())
    print(t.get_feature_info())
    print(t.get_const_feature())
    print(t.get_problem_category())
    print(t.get_missing_data())
    print(t.get_problem_desc())
    print(t.get_feature_desc(t.feature_list[2]))
    print(t.get_features_rel())
    print(t.get_features_target_rel())
