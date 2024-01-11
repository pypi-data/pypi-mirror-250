import math
from collections import defaultdict
from typing import Optional, Sequence, Any

import numpy as np
import pandas
from sklearn.metrics import ConfusionMatrixDisplay


class ClickableConfusionMatrix:
    def __init__(self, y_true, y_pred, feature_data: Optional[pandas.DataFrame] = None, feature_headers: Sequence[str] = None, feature_rows: Optional[Sequence[Any]] = None, *args, **kwargs):
        if feature_data is not None:
            self.feature_data = feature_data
        else:
            self.feature_data = pandas.DataFrame.from_records(feature_rows, columns=feature_headers)
        self.indices_by_combo = defaultdict(list)
        for i, (true, pred) in enumerate(zip(y_true, y_pred)):
            self.indices_by_combo[(true, pred)].append(i)
        for combo, indices in self.indices_by_combo.items():
            self.indices_by_combo[combo] = np.array(indices)

        def on_click(ax, event):
            if event.inaxes == ax:
                x = math.floor(event.xdata + 0.5)
                y = math.floor(event.ydata + 0.5)
                true_label = self.confusion_matrix_display.display_labels[y]
                pred_label = self.confusion_matrix_display.display_labels[x]
                print(f"\n{true_label=} {pred_label=}")
                print(self.feature_data.iloc[self.indices_by_combo[(y, x)]])

        self.confusion_matrix_display = ConfusionMatrixDisplay.from_predictions(y_true, y_pred, *args, **kwargs)
        self.confusion_matrix_display.ax_.figure.canvas.mpl_connect('button_press_event', lambda event: on_click(self.confusion_matrix_display.ax_, event))


if __name__ == "__main__":
    """Demo confusion matrix"""
    from matplotlib import pyplot as plt
    ClickableConfusionMatrix(
        [0, 0, 0, 1, 1, 1, 1],
        [0, 1, 0, 1, 1, 0, 1],
        labels=list(range(3)),
        display_labels=["negative", "positive", "neutral"],
        feature_rows=np.array([[message] for message in ["This movie sucked!", "It was not very good",
                               "I want my money back", "I was on the edge of my seat!",
                               "The twist at the end was mind-blowing",
                               "Well worth the price of admission",
                               "A thrilling comedy for the whole family"]])
    )
    plt.show()

