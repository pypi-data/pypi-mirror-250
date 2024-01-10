import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import seaborn as sns
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, GRU, LSTM, SimpleRNN

class MachineLearningOperations:
    def __init__(self, excel_path, x, label_column):
        self.excel_path = excel_path
        self.x = x
        self.label_column = label_column
        self.df = pd.read_excel(excel_path)
        # self.data = data

    def knn(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        knn_model = KNeighborsClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            knn_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = knn_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def random_forest(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        rf_model = RandomForestClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            rf_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = rf_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def logistic_regression(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        lr_model = LogisticRegression()

        for epoch in range(1, e+1):
            start_time = time.time()
            lr_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = lr_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def decision_tree(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        dt_model = DecisionTreeClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            dt_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = dt_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def linear_regression(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        lr_model = LinearRegression()

        start_time = time.time()
        lr_model.fit(X_train, y_train)
        end_time = time.time()
        elapsed_time = end_time - start_time

        y_pred = lr_model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        print(f'Time: {elapsed_time:.2f}s - Mean Squared Error: {mse}')

        return y_test, y_pred, mse

    def naive_bayes(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        nb_model = GaussianNB()

        start_time = time.time()
        nb_model.fit(X_train, y_train)
        end_time = time.time()
        elapsed_time = end_time - start_time

        y_pred = nb_model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def adaboost(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        adaboost_model = AdaBoostClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            adaboost_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = adaboost_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def bagging(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        bagging_model = BaggingClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            bagging_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = bagging_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy
# ... (previous code)

    def neural_network(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        model = Sequential()
        model.add(Dense(50, input_dim=X_train.shape[1], activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        for epoch in range(1, e+1):
            start_time = time.time()
            model.fit(X_train, y_train, epochs=1, batch_size=32, validation_data=(X_test, y_test))
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred_prob = model.predict(X_test)
            y_pred = (y_pred_prob > 0.5).astype(int)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def decision_tree(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        dt_model = DecisionTreeClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            dt_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = dt_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def rnn(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        # Assuming numerical_features is a 2D array [samples, features]
        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        # Reshape data for SimpleRNN
        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)
        X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

        model = Sequential()
        model.add(SimpleRNN(units=50, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        for epoch in range(1, e+1):
            start_time = time.time()
            model.fit(X_train, y_train, epochs=1, batch_size=32, validation_data=(X_test, y_test))
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred_prob = model.predict(X_test)
            y_pred = (y_pred_prob > 0.5).astype(int)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy



    def lstm(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        # Assuming numerical_features is a 2D array [samples, features]
        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        # Reshape data for LSTM
        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)
        X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

        model = Sequential()
        model.add(LSTM(units=50, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        for epoch in range(1, e+1):
            start_time = time.time()
            model.fit(X_train, y_train, epochs=1, batch_size=32, validation_data=(X_test, y_test))
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred_prob = model.predict(X_test)
            y_pred = (y_pred_prob > 0.5).astype(int)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def random_forest(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        rf_model = RandomForestClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            rf_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = rf_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def logistic_regression(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        lr_model = LogisticRegression()

        for epoch in range(1, e+1):
            start_time = time.time()
            lr_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = lr_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def linear_regression(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        lr_model = LinearRegression()

        start_time = time.time()
        lr_model.fit(X_train, y_train)
        end_time = time.time()
        elapsed_time = end_time - start_time

        y_pred = lr_model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        print(f'Time: {elapsed_time:.2f}s - Mean Squared Error: {mse}')

        return y_test, y_pred, mse

    def naive_bayes(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        nb_model = GaussianNB()

        start_time = time.time()
        nb_model.fit(X_train, y_train)
        end_time = time.time()
        elapsed_time = end_time - start_time

        y_pred = nb_model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f'Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def adaboost(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        adaboost_model = AdaBoostClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            adaboost_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = adaboost_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def bagging(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        bagging_model = BaggingClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            bagging_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = bagging_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def extra_trees(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        extra_trees_model = ExtraTreesClassifier()

        for epoch in range(1, e+1):
            start_time = time.time()
            extra_trees_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = extra_trees_model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy

    def mlp_regressor(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        mlp_regressor_model = MLPRegressor()

        for epoch in range(1, e+1):
            start_time = time.time()
            mlp_regressor_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = mlp_regressor_model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Mean Squared Error: {mse}')

        return y_test, y_pred, mse

    def decision_tree_regressor(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        dt_regressor_model = DecisionTreeRegressor()

        for epoch in range(1, e+1):
            start_time = time.time()
            dt_regressor_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = dt_regressor_model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Mean Squared Error: {mse}')

        return y_test, y_pred, mse

    def random_forest_regressor(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        rf_regressor_model = RandomForestRegressor()

        for epoch in range(1, e+1):
            start_time = time.time()
            rf_regressor_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = rf_regressor_model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Mean Squared Error: {mse}')

        return y_test, y_pred, mse

    def svm_regressor(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=1)

        svm_regressor_model = SVR()

        for epoch in range(1, e+1):
            start_time = time.time()
            svm_regressor_model.fit(X_train, y_train)
            end_time = time.time()
            elapsed_time = end_time - start_time

            y_pred = svm_regressor_model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Mean Squared Error: {mse}')

        return y_test, y_pred, mse

    def plotter(self, y_test, y_pred):
        x = np.arange(y_pred.shape[0])
        plt.plot(y_test)
        plt.plot(y_pred, color='red')
        plt.show()
        plt.scatter(x, y_test, marker='.')
        plt.scatter(x, y_pred, marker='.')
        plt.show()
        plt.plot(y_test)
        plt.plot(y_pred, color='red')
        plt.show()

        plt.figure(figsize=(12, 6))
        plt.plot(y_test, label='Actual Values', color='blue')
        plt.plot(y_pred, label='Predicted Values', color='red')
        plt.title('Actual vs Predicted Values')
        plt.legend()
        plt.show()

        # Seasonal decomposition of the predicted values
        decomposition = seasonal_decompose(y_pred.flatten(), period=10)  # Set the appropriate seasonal period
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid

        # Plot the components of the decomposition
        plt.figure(figsize=(12, 8))
        plt.subplot(411)
        plt.plot(y_pred.flatten(), label='Original')
        plt.legend(loc='upper left')
        plt.subplot(412)
        plt.plot(trend, label='Trend')
        plt.legend(loc='upper left')
        plt.subplot(413)
        plt.plot(seasonal, label='Seasonal')
        plt.legend(loc='upper left')
        plt.subplot(414)
        plt.plot(residual, label='Residual')
        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()
        y_predt = y_pred.reshape(y_pred.shape[0])
        avg = np.mean(y_predt)
        for i in range(y_predt.shape[0]):
            if y_predt[i] >= avg:
                y_predt[i] = 1
            else:
                y_predt[i] = 0

        plt.plot(y_test)
        plt.plot(y_predt, color='red')
        plt.show()
        plt.scatter(x, y_test, marker='.')
        plt.scatter(x, y_predt, marker='.')
        plt.show()
        plt.plot(y_test)
        plt.plot(y_predt, color='red')
        plt.show()

        plt.figure(figsize=(12, 6))
        plt.plot(y_test, label='Actual Values', color='blue')
        plt.plot(y_predt, label='Predicted Values', color='red')
        plt.title('Actual vs Predicted Values')
        plt.legend()
        plt.show()

        # =======================
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy = {accuracy}")
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1score = f1_score(y_test, y_pred)

        print(f"Precision = {precision}")
        print(f"Recall = {recall}")
        print(f"F1 Score = {f1score}")

        conf_matrix = confusion_matrix(y_test, y_pred)
        print("conf_matrix")
        plt.figure(figsize=(8, 8))
        sns.set(font_scale=1.5)

        ax = sns.heatmap(
            conf_matrix,  # confusion matrix 2D array
            annot=True,  # show numbers in the cells
            fmt='d',  # show numbers as integers
            cbar=False,  # don't show the color bar
            cmap='flag',  # customize color map
            # vmax=175 # to get better color contrast
        )

        ax.set_xlabel("Predicted", labelpad=20)
        ax.set_ylabel("Actual", labelpad=20)
        plt.show()
        print(f"Accuracy = {accuracy.round(4)}")
        print(f"Precision = {precision.round(4)}")
        print(f"Recall = {recall.round(4)}")
        print(f"F1 Score = {f1score.round(4)}")

    def plotter2(self, y_test, y_pred):
        x = np.arange(y_pred.shape[0])

        # Create a single subplot for all the plots
        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 20))

        # Plot y_test and y_pred
        axes[0, 0].plot(y_test, label='Actual Values', color='blue')
        axes[0, 0].plot(y_pred, label='Predicted Values', color='red')
        axes[0, 0].set_title('Actual vs Predicted Values')
        axes[0, 0].legend()

        # Scatter plots
        axes[0, 1].scatter(x, y_test, marker='.', label='Actual Values')
        axes[0, 1].scatter(x, y_pred, marker='.', label='Predicted Values')
        axes[0, 1].legend()

        # Seasonal decomposition
        decomposition = seasonal_decompose(y_pred.flatten(), period=10)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid

        axes[1, 0].plot(y_pred.flatten(), label='Original')
        axes[1, 0].legend(loc='upper left')
        axes[1, 1].plot(trend, label='Trend')
        axes[1, 1].legend(loc='upper left')
        axes[2, 0].plot(seasonal, label='Seasonal')
        axes[2, 0].legend(loc='upper left')
        axes[2, 1].plot(residual, label='Residual')
        axes[2, 1].legend(loc='upper left')

        # Binary classification based on average
        y_predt = y_pred.reshape(y_pred.shape[0])
        avg = np.mean(y_predt)
        for i in range(y_predt.shape[0]):
            if y_predt[i] >= avg:
                y_predt[i] = 1
            else:
                y_predt[i] = 0

        axes[3, 0].plot(y_test, label='Actual Values', color='blue')
        axes[3, 0].plot(y_predt, label='Predicted Values', color='red')
        axes[3, 0].set_title('Binary Classification Based on Average')
        axes[3, 0].legend()

        axes[3, 1].scatter(x, y_test, marker='.', label='Actual Values')
        axes[3, 1].scatter(x, y_predt, marker='.', label='Predicted Values')
        axes[3, 1].legend()

        # Confusion matrix heatmap
        conf_matrix = confusion_matrix(y_test, y_pred)
        sns.set(font_scale=1.5)
        ax = sns.heatmap(
            conf_matrix,
            annot=True,
            fmt='d',
            cbar=False,
            cmap='flag',
            ax=axes[4, 0]
        )
        ax.set_xlabel("Predicted", labelpad=20)
        ax.set_ylabel("Actual", labelpad=20)

        # Metrics
        axes[4, 1].text(0.5, 0.5, f"Accuracy = {accuracy_score(y_test, y_pred):.4f}\n"
                                   f"Precision = {precision_score(y_test, y_pred):.4f}\n"
                                   f"Recall = {recall_score(y_test, y_pred):.4f}\n"
                                   f"F1 Score = {f1_score(y_test, y_pred):.4f}",
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=axes[4, 1].transAxes)
        axes[4, 1].axis('off')

        plt.tight_layout()
        plt.show()

    def preprocess_data(self):
        # Your data preprocessing logic here
        pass

    def split_data(self):
        # Split your data into features and labels
        X = self.data.drop('target_column', axis=1)
        y = self.data['target_column']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test

    def train_random_forest(self, X_train, y_train):
        # Train Random Forest classifier
        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)
        return clf

    def train_logistic_regression(self, X_train, y_train):
        # Train Logistic Regression classifier
        clf = LogisticRegression()
        clf.fit(X_train, y_train)
        return clf

    def train_svm(self, X_train, y_train):
        # Train Support Vector Machine classifier
        clf = SVC()
        clf.fit(X_train, y_train)
        return clf

    # Add methods for other algorithms as needed

    def evaluate_model(self, clf, X_test, y_test):
        # Make predictions
        y_pred = clf.predict(X_test)

        # Call the plotter method or any other evaluation method
        self.plotter(y_test, y_pred)

    def test_all_algorithms(self):
        # Preprocess data
        self.preprocess_data()

        # Split data
        X_train, X_test, y_train, y_test = self.split_data()

        # Train and evaluate Random Forest
        clf_rf = self.train_random_forest(X_train, y_train)
        self.evaluate_model(clf_rf, X_test, y_test)

        # Train and evaluate Logistic Regression
        clf_lr = self.train_logistic_regression(X_train, y_train)
        self.evaluate_model(clf_lr, X_test, y_test)

        # Train and evaluate SVM
        clf_svm = self.train_svm(X_train, y_train)
        self.evaluate_model(clf_svm, X_test, y_test)

        # Add training and evaluation for other algorithms as needed
    # def gru(self, e):
    #     # Load the dataset from Excel
    #     df = pd.read_excel(excel_path)

    #     # Assuming your Excel file has columns 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', and 'label'
    #     numerical_features = df[['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']].values
    #     labels = df['label'].values

    #     # Standardize numerical features
    #     numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

    #     # Split the dataset
    #     X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=42)

    #     # Build the GRU model
    #     model = Sequential()
    #     model.add(GRU(units=100, input_shape=(X_train.shape[1], 1)))  # Adjust input shape based on the number of features
    #     model.add(Dense(units=1, activation='sigmoid'))

    #     # Compile the model
    #     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    #     # Reshape input data for GRU layer
    #     X_train_reshaped = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    #     X_test_reshaped = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    #     # Train the model
    #     history = model.fit(X_train_reshaped, y_train, epochs=5, batch_size=64, validation_data=(X_test_reshaped, y_test))

    #     # Get the predicted values for the test set
    #     y_pred = model.predict(X_test_reshaped)

    #     # Evaluate the model
    #     loss, accuracy = model.evaluate(X_test_reshaped, y_test)
    #     print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

    #     return y_test, y_pred, accuracy

    def gru(self, e):
        numerical_features = self.df[self.x].values
        labels = self.df[self.label_column].values

        numerical_features_standardized = StandardScaler().fit_transform(numerical_features)

        X_train, X_test, y_train, y_test = train_test_split(numerical_features_standardized, labels, test_size=0.3, random_state=42)

        # Build the GRU model
        model = Sequential()
        model.add(GRU(units=100, input_shape=(X_train.shape[1], 1)))  # Adjust input shape based on the number of features
        model.add(Dense(units=1, activation='sigmoid'))

        # Compile the model
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        for epoch in range(1, e + 1):
            start_time = time.time()
            # Reshape input data for GRU layer
            X_train_reshaped = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
            X_test_reshaped = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

            # Train the model
            history = model.fit(X_train_reshaped, y_train, epochs=1, batch_size=64, validation_data=(X_test_reshaped, y_test), verbose=0)

            # Get the predicted values for the test set
            y_pred = model.predict(X_test_reshaped)

            # Evaluate the model
            loss, accuracy = model.evaluate(X_test_reshaped, y_test, verbose=0)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f'Epoch {epoch} - Time: {elapsed_time:.2f}s - Test Loss: {loss}, Test Accuracy: {accuracy}')

        return y_test, y_pred, accuracy
