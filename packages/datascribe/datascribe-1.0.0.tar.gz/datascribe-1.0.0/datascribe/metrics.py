from sklearn.metrics import (RocCurveDisplay,
                             precision_recall_fscore_support,
                             ConfusionMatrixDisplay,
                             confusion_matrix,
                             r2_score,
                             auc,
                             mean_absolute_error,
                             mean_squared_error,
                             roc_curve)
import os


class Metrics:
    def __init__(self, scribe) -> None:
        '''
        Initiator method for metrics

        Parameters:
        ----------
        scribe: class
            class which holds workflow information

        '''
        # stores metrics methods called
        self.metrics_methods = {}
        # scribe object stored
        self.scribe = scribe
        # text for precision, recall and f1 score if called stored here
        self.prec_rec_f1_text = None

    def mae(self):
        '''
        Calculates mean absolute error and stores in metrics_methods

        Returns:
        -------
        float: score
        '''
        y_true = self.scribe.model.splitted_data['y_test']
        y_pred = self.scribe.model.y_pred
        score = mean_absolute_error(y_true, y_pred)
        self.metrics_methods.update({'mean absolute error': score})
        return score

    def mse(self):
        '''
        Calculates mean squared error and stores in metrics_methods

        Returns:
        -------
        float: score
        '''
        y_true = self.scribe.model.splitted_data['y_test']
        y_pred = self.scribe.model.y_pred

        score = mean_squared_error(y_true, y_pred)
        self.metrics_methods.update({'mean squared error': score})
        return score

    def r2score(self):
        '''
        Calculates the R2 score and stores in metrics_methods

        Returns:
        -------
        float: score
        '''
        y_true = self.scribe.model.splitted_data['y_test']
        y_pred = self.scribe.model.y_pred

        score = r2_score(y_true, y_pred)
        self.metrics_methods.update({'R-squared (R2) score': score})
        return score

    def confusionmatrix(self, labels: list = None):
        '''
        Calculates confusion matrix, provides a summary in the terminal,
        outputs an image (.png) file and adds text to the final write up
        to refer to visual.

        Parameters
        ----------
        labels: list (default: None)
            list of labels to help describe confusion matrix.

        Returns:
        -------
        numpy array: confusion matrix score

        '''
        y_true = self.scribe.model.splitted_data['y_test']
        y_pred = self.scribe.model.y_pred

        score = confusion_matrix(y_true, y_pred, labels=labels)
        self.metrics_methods.update({'confusion matrix': score})

        disp = ConfusionMatrixDisplay(confusion_matrix=score,
                                      display_labels=labels)

        # if no labels passed, use shape of matrix to create
        if labels is None:
            labels = list(range(score.shape[0]))
        labels = [str(label) for label in labels]
        # iterate through score
        for index, label in enumerate(labels):
            print(f"\nThe number of true {label} classifications was"
                  f"{score[index, index]}.")

            for i in range(len(labels)):
                if i == index:
                    continue

                pred_label = labels[i]
                count = score[index, i]

                if count == 0:
                    print(f"There were no {label} classifications "
                          f"incorrectly identified as {pred_label}.")
                else:
                    print(f"The number of {label} classifications incorrectly"
                          f" identified as {pred_label} was {count}.")
        # save image
        img_folder = f"{self.scribe.dir}/images"
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        plot_name = 'confusion matrix'
        output_file = f"{img_folder}/{plot_name}.png"
        disp.plot().figure_.savefig(output_file)
        self.scribe.visuals_loc[plot_name] = output_file
        return score

    def prec_rec_f1_score(self, labels=None, prec_th=0.7,
                          rec_th=[0.5, 0.7, 0.8], f1_th=0.7, zero_div=1.0):
        '''
        Provides the precision, recall and f1 score of the model.

        Parameters:
        ----------
        labels: list (default: None)
            Optional list of labels for outcomes.

        prec_th: float (default: 0.7)
            float to determine threshold for a suitable precision score

        rec_th: list of floats (default: [0.5, 0.7, 0.8])
            list to advise threshold for adequate, good and excellent
            recall scoring

        f1_th: float
            float to determine threshold for a suitable f1 score

        zero_div: float (default: 1.0)
            float to determine how to manage divide zero errors
        '''

        y_true = self.scribe.model.splitted_data['y_test'].values.astype(int)
        y_pred = self.scribe.model.y_pred.astype(int)
        # get scores
        cr = precision_recall_fscore_support(y_true, y_pred, labels=labels,
                                             zero_division=zero_div)
        # variables to store text output
        precision_text = []
        recall_text = []
        fs_text = []
        # if no labels, retrieve from outcomes
        if labels is None:
            labels = sorted(set(y_true) | set(y_pred))
        # iterate through labels for scores
        for index, label in enumerate(labels):
            # precision score
            pr_text = f"The precision score for '{label}' was "\
                      f"{round(cr[0][index], 2)}."
            precision_text.append(pr_text)
            # check if met threshold
            if cr[0][index] == 1:
                pr_text = f"This is considered a perfect score, suggesting "\
                          f"that the model has identified all positive "\
                          f"'{label}' predictions."
                precision_text.append(pr_text)
            elif round(cr[index][0], 2) >= prec_th:
                pr_text = f"This is considered an acceptable score, "\
                          f"suggesting that the model is good at predicting "\
                          f"positive '{label}' predictions."
                precision_text.append(pr_text)
            # recall score
            rec_text = f"The recall score for '{label}' was "\
                       f"{round(cr[1][index], 2)}."
            recall_text.append(rec_text)
            # check which threshold
            if cr[1][index] == 1:
                rec_text = f"This is considered a perfect score, suggesting "\
                           f"that the model has not made any false negatives "\
                           f"when making '{label}' predictions."
            elif round(cr[index][1], 2) > rec_th[2]:
                rec_text = f"This is considered an acceptable score, "\
                           f"suggesting that the model has a low rate of "\
                           f"false negatives when making '{label}'"\
                           f"predictions."
            elif round(cr[index][1], 2) > rec_th[1]:
                rec_text = f"This is considered a good score, suggesting that"\
                           f" the model has a fairly low rate of false "\
                           f"negatives when making '{label}' predictions."
            elif round(cr[index][1], 2) > rec_th[0]:
                rec_text = f"This is a moderate score, suggesting that the "\
                           f"model has a moderate ability to capture positive"\
                           f" instances of '{label}' classification."
            else:
                rec_text = "This is considered a poor score."
            recall_text.append(rec_text)
            # f1 score
            f1_text = f"The f1 score for '{label}' was "\
                      f"{round(cr[2][index], 2)}."
            fs_text.append(f1_text)
            # check if met threshold
            if cr[2][index] == 1:
                f1_text = f"This is considered a perfect score, suggesting "\
                          f"that the model has perfect precision and recall "\
                          f"for '{label}' predictions."
                fs_text.append(f1_text)
            elif round(cr[2][index], 2) >= f1_th:
                f1_text = f"This is considered a good score, suggesting that "\
                          f"the model has good precision and recall for"\
                          f" '{label}' predictions."
                fs_text.append(f1_text)
        # join up text
        precision_text = ' '.join(precision_text)
        recall_text = ' '.join(recall_text)
        fs_text = ' '.join(fs_text)
        all_text = [precision_text, recall_text, fs_text]
        all_text_combined = ' '.join(all_text)
        # store in attributes
        self.prec_rec_f1_text = all_text_combined
        self.metrics_methods.update({'precision, recall, f1 score and support':
                                     cr})
        # show in terminal
        return all_text_combined

    def roc(self):
        '''
        Produces a receiver operating characteristic (ROC) curve from
        the true and predicted values.  Area under the ROC curve (AUROC)
        stored in dictionary of metrics performed.

        '''
        y_true = self.scribe.model.splitted_data['y_test']
        y_pred = self.scribe.model.y_pred

        fpr, tpr, threshold = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc,
                                  estimator_name='logistic regression')
        img_folder = f"{self.scribe.dir}/images"
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        # file name
        filename = 'roc curve'
        output_file = f'{img_folder}/{filename}.png'
        display.plot().figure_.savefig(output_file)
        self.scribe.visuals_loc['roc curve'] = output_file
        self.metrics_methods.update({'roc curve': roc_auc})

    def metrics_commentary(self):
        '''
        Amalgamates the metrics which have been performed and stored in
        metrics_methods attribute into a text summary.

        Returns:
        -------
        str: summary of metrics

        '''
        commentary = []
        for key, value in self.metrics_methods.items():
            if key == 'confusion matrix':
                text = 'The confusion matrix table provides a summary of'\
                        ' the true positive (TP), true negative (TN), '\
                        'false positive (FP) and false negative (FN) values.'
            elif key == "precision, recall, f1 score and support":
                text = self.prec_rec_f1_text
            else:
                val = f"{value:.2f}"
                text = f'The model received a score of {val} for {key}.'
                if key == 'mean absolute error':
                    add = f'This indicated that the predicted values deviate '\
                        f'from the actual values by {value:.2%}.'
                    text = f"{text} {add}"
                elif key == 'R-squared (R2) score':
                    if value < 0:
                        add = "This suggests that the model performs worse "\
                            "than a naive mean-based model."
                    elif value < 0.4:
                        add = "This suggests a low level of correlation."
                    elif value > 0.7:
                        add = "This suggests a high level of correlation."
                    text = f"{text} {add}"
                elif key == 'mean squared error':
                    add = "This indicates the average squared difference "\
                        "between the predicted values and the actual values "\
                        "in the model."
                    text = f"{text} {add}"
                elif key == 'roc curve':
                    text = f'As you can see from the receiver operating '\
                        f'characteristic (ROC) curve, the area under the'\
                        f' curve (AUROC) was {value}.'
            commentary.append(text)
        # join text together
        full_commentary = '\n\n'.join(commentary)
        # return full_commentary
        return full_commentary

    def check_metrics_step(self):
        '''
        Checks whether any metric methods has taken place.

        Returns:
        -------
        boolean
        '''
        # check if dictionary is not empty
        any_non_empty = bool(self.metrics_methods)

        # return result
        return any_non_empty
        return any_non_empty
