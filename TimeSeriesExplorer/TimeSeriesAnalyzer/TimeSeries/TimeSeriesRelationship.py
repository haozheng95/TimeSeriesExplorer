from sklearn.decomposition import PCA
from pandas import DataFrame
import json

from TimeSeriesExplorer.TimeSeriesAnalyzer.TimeSeries.Utils import *

class TimeSeriesRelationship:
    def __init__(self, multi_series):
        self.multi_series = multi_series
        self._corr_matrix()

    def _corr_matrix(self):
        self.features_corr_matrix = self.multi_series.corr().fillna(0)

    def feature_rel_to_string(self, zoomed_style = True):
        if zoomed_style:
            c = self.features_corr_matrix.abs()
            s = c.unstack()
            so = s.sort_values(kind="quicksort", ascending=False)

        return self.features_corr_matrix.round(get_decimals()).to_json()


class FeatureTargetRelationship:
    def __init__(self, features, target):
        self.target = target
        if check_numeric_array(target):
            self.target = target.values.astype(float)

        self.features = features.drop(['time'], axis=1)
        self.features = self.features.groupby('id').mean()

    def _corr_matrix(self):
        self.corr = compute_corr(self.features, pd.DataFrame({'target': self.target})).fillna(0)

    def _pca(self):
        pca = PCA(n_components=2)
        pca.fit(self.features)
        self.features_pca = DataFrame(pca.transform(self.features), columns=['x', 'y'])

    def feature_target_corr_to_string(self):
        self._corr_matrix()

        return self.corr.round(get_decimals()).to_json()

    def feature_target_pca_to_string(self):
        self._pca()
        all_info = pd.concat([self.target, self.features_pca], axis=1)
        all_info.columns = ['class', 'x', 'y']

        result = []
        for index, row in all_info.iterrows():
            temp = {}
            temp['x'] = float("{0:.4f}".format(row['x']))
            temp['y'] = float("{0:.4f}".format(row['y']))
            temp['class'] = row['class']
            result.append(temp)

        return json.dumps(result)


