import pandas as pd


class ResultHandler:
    def __init__(self, results):
        self.r_ = results

    def to_df(self, columns='all'):
        df_columns = [
            'Classifier',
            'Sampler',
            'Accuracy_Mean',
            'Accuracy_Std',
            'Balanced_Accuracy_Mean',
            'Balanced_Accuracy_Std',
            'Sensitivity_Mean',
            'Sensitivity_Std',
            'Specificity_Mean',
            'Specificity_Std',
            'F1_Mean',
            'F1_Std',
            'Precision_Mean',
            'Precision_Std',
            'Recall_Mean',
            'Recall_Std',
            'Order'
        ]

        df = pd.DataFrame(self.r_, columns=df_columns)
        return df[columns]

    def to_latex(self, columns, orientation='vertical'):
        if orientation == 'vertical':
            df_temp = self.to_df(columns)
        else:
            df_temp = self.to_df(columns).transpose()
        latex_code = df_temp.to_latex()

        return latex_code

    def record_results(self, filename):
        pd.set_option("display.precision", 3)
        f = open("C:/Users/Leo/PycharmProjects/swDefect/results/" + filename + ".txt", "w")
        f.write(self.to_latex(columns=['Sampler', 'Accuracy_Mean'], orientation='horizontal'))
        f.write(self.to_latex(columns=['Sampler', 'Balanced_Accuracy_Mean'], orientation='horizontal'))
        f.write(self.to_latex(columns=['Sampler', 'Sensitivity_Mean'], orientation='horizontal'))
        f.write(self.to_latex(columns=['Sampler', 'Specificity_Mean'], orientation='horizontal'))
        f.write(self.to_latex(columns=['Sampler', 'F1_Mean'], orientation='horizontal'))
        f.write(self.to_latex(columns=['Sampler', 'Precision_Mean'], orientation='horizontal'))
        f.write(self.to_latex(columns=['Sampler', 'Recall_Mean'], orientation='horizontal'))
        f.close()
