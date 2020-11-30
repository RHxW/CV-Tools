def get_measurements(TP, FN, FP, TN, alpha:int=None):
    P = TP + FN
    N = FP + TN
    if P == 0 or N == 0:
        if P == 0:
            print("P(TP + FN) is 0!")
        else:
            print("N(FP + TN) is 0!")
        return {
            "TP": TP,
            "FN": FN,
            "FP": FP,
            "TN": TN
        }
    P_ = TP + FP
    N_ = FN + TN
    # Accuracy
    acc = (TP + TN) / (TP + TN + FP + FN)

    # Error rate (err = 1 - acc)
    err = (FP + FN) / (TP + TN + FP + FN)

    # sensitive
    sens = TP / P

    # specificity
    spec = TN / N

    # Precision
    prec = TP / (TP + FP)

    # recall (==sensitive)
    recall = TP / (TP + FN)

    # F-measure
    # F1
    F1 = (2 * prec * recall) / (prec + recall)

    # F-alpha
    if alpha is None or type(alpha) is not int:
        Fa = None
    else:
        Fa = ((alpha ** 2 + 1) * prec * recall) / (alpha ** 2 * (prec + recall))

    ret = {
        "accuracy": acc,
        "error_rate": err,
        # "sensitive": sens,
        "specificity": spec,
        "precision": prec,
        "recall": recall,
        "F1": F1,
        "Fa": Fa,
        "alpha": alpha
    }
    return ret
