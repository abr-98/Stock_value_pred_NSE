from utilities.explaination.create_final_dataframe import create_final_dataframe
from utilities.explaination.linear_explaination import linear_explaination
from utilities.explaination.split_data import get_split_data
from utilities.explaination.decision_explaination import decision_explaination

def get_final_explanation(df):

    df_final = create_final_dataframe(df)
    X, y = get_split_data(df_final)
    linear_exp = linear_explaination(X, y)
    decision_exp = decision_explaination(X, y)

    return {
        "linear_explanation": linear_exp,
        "decision_tree_explanation": decision_exp
    }
    