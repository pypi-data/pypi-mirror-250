import numpy as np
from scipy.spatial import distance
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class SurrogateSetImputer:
    __version__ = 'v1.0.2'

    def __init__(self, X, instance_interest, num_neighbours, features_to_impute):
        self.data = np.array(X.copy())
        self.instance_interest = instance_interest
        self.num_neighbours = num_neighbours
        self.features_to_impute = features_to_impute

    def calculate_column_means(self):
        return np.nanmean(self.data, axis=0)

    def set_missing_features_to_mean(self, column_means):
        self.data[self.instance_interest][self.features_to_impute] = column_means[self.features_to_impute]

    def calculate_nearest_complete_neighbours(self):
        complete_instances = np.all(~np.isnan(self.data), axis=1)
        complete_data = self.data[complete_instances]
        dist = distance.cdist([self.data[self.instance_interest]], complete_data)
        nearest_neighbour_indexes = np.argsort(dist)[0, :self.num_neighbours]
        original_indices = np.nonzero(complete_instances)[0][nearest_neighbour_indexes]
        return original_indices

    def generate_synthetic_data(self, num_neighbours_arr):
        synthetic_data = []
        for i in range(len(num_neighbours_arr)):
            nearest_neighbour_indexes = self.data[num_neighbours_arr[i]]
            set_Z = np.random.multivariate_normal(
                mean=nearest_neighbour_indexes,
                cov=np.cov(self.data, rowvar=False, bias=True),
                size=len(self.data)
            )
            synthetic_data.append(set_Z)
        return np.vstack(synthetic_data)

    def calculate_weights(self, synthetic_data):
        kernel_width = 0.75 * np.sqrt(len(synthetic_data))
        distances = np.sum((self.data[self.instance_interest] - synthetic_data), axis=1)
        return np.exp(-(distances) / (kernel_width ** 2))

    def perform_linear_regression(self, synthetic_data, weights):
        y_prime = synthetic_data[:, self.features_to_impute]
        data_copy = np.delete(synthetic_data, self.features_to_impute, 1)

        regressor = LinearRegression()
        regressor.fit(data_copy, y_prime, sample_weight=weights)
        return regressor

    def calculate_shap_values(self, regressor):
        all_features = np.arange(self.data.shape[1])
        features_to_shap = np.setdiff1d(all_features, self.features_to_impute)

        # Calculate the mean of features except those to impute
        mean_except_impute = np.mean(self.data[:, features_to_shap], axis=0)

        # Calculate the original values of features not to impute
        original_values_except_impute = self.data[self.instance_interest, features_to_shap]

        # Calculate SHAP values
        shap_values = regressor.coef_
        shap_values *= (original_values_except_impute - mean_except_impute)

        return shap_values
    
    def impute_missing_features(self):
        column_means = self.calculate_column_means()
        self.set_missing_features_to_mean(column_means)

        nearest_neighbours_arr = self.calculate_nearest_complete_neighbours()[:self.num_neighbours]

        synthetic_data = self.generate_synthetic_data(nearest_neighbours_arr)
        weights = self.calculate_weights(synthetic_data)
        regressor = self.perform_linear_regression(synthetic_data, weights)
        instance_to_predict = np.delete(self.data[self.instance_interest], self.features_to_impute).reshape(1, -1)
        predicted_imputation = regressor.predict(instance_to_predict)
        self.data[self.instance_interest][self.features_to_impute] = predicted_imputation[0]

        # Calculate SHAP values manually
        shap_values = self.calculate_shap_values(regressor)

        return self.data[self.instance_interest], shap_values
    
    def visualise_imputation(self, shap_values):
        num_instances, num_features = shap_values.shape

        for i in range(num_instances):
            fig, ax = plt.subplots(figsize=(8, 4))

            for j in range(num_features):
                value = shap_values[i, j]
                color = 'green' if value >= 0 else 'red'
                ax.bar(j, value, color=color, label=f'Feature {j + 1}')

            ax.set_xticks(range(num_features))
            ax.set_xticklabels([f'Feature {j + 1}' for j in range(num_features)])
            ax.set_title(f'Imputation {i + 1}')
            ax.set_ylabel('Shapley Value')
            ax.set_xlabel('Feature')
            ax.legend()

            plt.tight_layout()
            plt.show()