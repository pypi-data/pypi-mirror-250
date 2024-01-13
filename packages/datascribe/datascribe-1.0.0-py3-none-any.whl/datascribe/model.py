'''
Contains the Model class for datascribe, which holds information on the
machine learning model used.

'''
from sklearn.model_selection import (train_test_split,
                                     StratifiedKFold,
                                     GridSearchCV)
from sklearn.linear_model import LogisticRegression


class Model:
    def __init__(self):
        '''
        Initiator method for Model.

        '''
        self.model = None
        self.kfold = None
        self.splitted_data = {'X_train': None, 'X_test': None,
                              'y_train': None, 'y_test': None}
        self.k_num = None
        self.split = None
        self.model_type = None
        self.y_pred = None

    def k_fold(self, n_splits=5):
        '''
        Provides train/test indices to split data in train/test sets.

        Parameters:
        --------
        n_splits : int, default=5
            Number of folds. Must be at least 2.

        Returns:
        --------
        cross-validation object with 'n' folds
        '''
        kfold = StratifiedKFold(n_splits=n_splits, shuffle=True,
                                random_state=42)
        self.kfold = kfold
        self.k_num = n_splits

    def regression_model(self, params=None):
        '''
        Train logistic regression model using grid search to get the
        best hyper parameters

        Parameters:
        ----------

        params: dict
            Dictionary of hyperparameters used in logistic regression
            consists of:

            penalty : {'l1', 'l2', 'elasticnet', None}, default='l2'
                Specify the norm of the penalty:

                - `None`: no penalty is added;
                - `'l2'`: add a L2 penalty term and it is the default
                          choice;
                - `'l1'`: add a L1 penalty term;
                - `'elasticnet'`: both L1 and L2 penalty terms are added

            dual : bool, default=False
                Dual or primal formulation. Dual formulation is only
                implemented for l2 penalty with liblinear solver.
                Prefer dual=False when n_samples > n_features.

            tol : float, default=1e-4
                Tolerance for stopping criteria.

            C : float, default=1.0
                Inverse of regularization strength; must be a positive
                float. Like in support vector machines, smaller values
                specify stronger regularization.

            fit_intercept : bool (default=True)
                Specifies if a constant (a.k.a. bias or intercept)
                should be added to the decision function.

            intercept_scaling : float, default=1
                Useful only when the solver 'liblinear' is used
                and self.fit_intercept is set to True.

            random_state : int, RandomState instance, default=None
                Used when ``solver`` == 'sag', 'saga' or 'liblinear'
                to shuffle the data.

            solver : {'lbfgs', 'liblinear', 'newton-cg',
                      'newton-cholesky', 'sag', 'saga'},
                    default='lbfgs'
                    Algorithm to use in the optimization problem.

            class_weight : dict or 'balanced', default=None
                Weights associated with classes in the form
                ``{class_label: weight}``. If not given, all classes are
                supposed to have weight one.

                The "balanced" mode uses the values of y to
                automatically adjust weights inversely proportional to
                class frequencies in the input data as
                ``n_samples / (n_classes * np.bincount(y))``.

            max_iter : int, default=100
                Maximum number of iterations taken for the solvers to
                converge

            multi_class : {'auto', 'ovr', 'multinomial'}, default='auto'

            verbose : int, default=0
            For the liblinear and lbfgs solvers set verbose to any
            positive number for verbosity.

            warm_start : bool, default=False
                When set to True, reuse the solution of the previous
                call to fit as initialization, otherwise, just erase the
                previous solution.

            n_jobs : int, default=None
                Number of CPU cores used when parallelizing over classes
                if multi_class='ovr'"

            l1_ratio : float, default=None
                The Elastic-Net mixing parameter, with
                ``0 <= l1_ratio <= 1``. Only used if
                ``penalty='elasticnet'``

        Returns:
        --------
        logistic regression model

        '''

        # using cross-validated grid-search to define a best logistic
        # regression model with predefined parameters
        if not params:
            params = {}
        logistic_regression = GridSearchCV(LogisticRegression(), params,
                                           cv=self.kfold)
        self.model = logistic_regression
        self.model_type = 'LR_GCV_skf'

    def split_dataset(self, *arrays, test_size=0.25, stratify=None):
        '''
        Split arrays or matrices into random train and test subsets.

        Parameters
        ----------
        *arrays : sequence of indexables with same length / shape[0]
            Allowed inputs are lists, numpy arrays, scipy-sparse
            matrices or pandas dataframes.

        test_size : float or int, (default=0.25)
            If float, should be between 0.0 and 1.0 and represent the
            proportion of the dataset to include in the test split

        stratify : array-like (default:None)
            data is split in a stratified fashion, using this parameter
            as the class labels

        Returns
        -------
        splitting : list, length=2 * len(arrays)
            List containing train-test split of inputs.

        '''
        # split the dataset to train and test
        X_train, X_tst, y_train, y_tst = train_test_split(*arrays,
                                                          test_size=test_size,
                                                          random_state=42,
                                                          stratify=stratify)
        self.splitted_data.update({'X_train': X_train,
                                   'X_test': X_tst,
                                   'y_train': y_train,
                                   'y_test': y_tst})
        self.y_true = y_tst
        self.split = test_size

    def fit(self):
        '''
        Fit the model according to the given training data.

        '''
        # train model
        self.model.fit(self.splitted_data['X_train'],
                       self.splitted_data['y_train'])

    def predict(self):
        '''
        Predict the model according to the given test data

        Returns
        ----------
        y_pred: array-like of shape (n_samples, n_classes)
        '''
        # prediction
        y_pred = self.model.predict(self.splitted_data['X_test'])
        self.y_pred = y_pred

    def check_model_exists(self):
        '''
        Checks whether the class has a model saved in it.

        Returns:
        -------
        boolean
        '''
        if self.model_type is not None:
            return True
        else:
            return False

    def model_commentary(self):
        '''
        Creates a text summary of the model used.

        Returns:
        -------
        str: summary of model
        '''
        # check which model used (if statement would update with more
        # models)
        if self.check_model_exists() is True:
            if self.model_type == 'LR_GCV_skf':
                # convert decimal to whole percentage
                test_split = int(self.split * 100)
                # calculate the complementing percentage
                train_split = 100 - test_split
                # format the string
                split = f"{train_split}%/{test_split}%"
                text = f"A logistic regression model was used with stratified"\
                       f" k fold (k={self.k_num}) and GridCV search used for"\
                       f" feature selection.  The train/test split was "\
                       f"{split}."
                return text
            else:
                print("Model commentary not found.")
                return None
        else:
            return None
