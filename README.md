
# Motivated Reasoning: Causal Inference on Court Cases

This project aims to answer the question posed by the DE JURE: Motivated Reasoning project: how do district courtjudges appointed by Democrat presidents differ from judges appointed by Republican presidents?  In particular, we look at how Democrat and Republican district court judges rule on cases and when they tend to favor the plaintiff. We are particularly interested in whether the “treatment” of a judge’s political party seems to have an effect on whether they tend to rule in favor of the plaintiff. We perform CATE estimation using a variety of learners to estimate the treatment effect of each case. Finally, we inspect feature importances and SHAP values of a model fit to classify cases in favor of the plaintiff vs the defendant and infer the types of cases where Republican judges tend to favor the plaintiff vs the defendant, and similarly for Democrat judges.


## Project Structure

The main files of the project are described as below: 

    .
    ├── artifacts                           Artifacts (sample data, metadata, sample case structure)
    ├── notebooks
    |   ├── cate-3.ipynb                    CATE estimation (casualml package from Uber)
    |   ├── cate-4-X-by-party.ipynb         Draw inferences from cases where judges favor the plaintiffs or the defendants
    |   ├── cate-dowhy.ipynb                CATE estimation (dowhy package from Microsoft)
    |   ├── feature-engg.ipynb              Feature engineering from raw files
    |   └── randomization-test-fe.ipynb     Randomization test for random treatment assignment with fixed effects
    ├── results
    |   ├── cate-1M.png                     Distribution of CATE estimates on 1M samples
    |   ├── cate-50k.png                    Distribution of CATE estimates on 50k samples
    |   ├── shap-democrats.png              SHAP values for democrats favoring plaintiff vs defendant
    |   ├── shap-republicans.png            SHAP values for republican favoring plaintiff vs defendant
    |   ├── xgb-imp-democrats.png           XG-Boost feature importances for democrat model
    |   └── xgb-imp-republicans.png         XG-Boost feature importances for republican model
    ├── utils                               Parsing utils
    └── README.md


