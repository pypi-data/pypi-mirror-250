import json
import logging
import os
from pathlib import Path
from typing import Callable, Dict, List, Optional

import pandas
from fastapi.encoders import jsonable_encoder

from .accuracy import calibration, largest_errors, metrics, roc_curve
from .countplot import countplot
from .dependence import partialdep
from .expectations import condexp
from .importance import varimp
from .shap import ShapExplainer
from .sliceloss import slice_loss
from .t import SliceLoss
from .utils import create_description, df_to_dict

BASE_RESULTS_PATH = os.environ.get("BASE_RESULTS_PATH", "profiling_results")


def mkdir(endpoint_name: str, spec_path: str = "") -> Path:
    folder = Path(BASE_RESULTS_PATH) / endpoint_name / spec_path
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def santize_var_names(var_name: str) -> str:
    """Removing "/" since this leads to errors in file creation."""
    return var_name.replace("/", "")


def create_shapley_schema(
    func: Callable,
    x: pandas.DataFrame,
    endpoint_name: str,
    profile_columns: List[str],
    explain_input_example: List[Dict],
):
    """Create Shapley schema for endpoint"""

    explainer = ShapExplainer(func=func, x=x, profile_columns=profile_columns)
    folder = mkdir(endpoint_name=endpoint_name)

    input_descriptions = [create_description(x[col]) for col in profile_columns]
    logging.info("Shapley - Creating schema")
    file_path = folder / "schema.json"

    example = pandas.DataFrame(explain_input_example).astype(x[profile_columns].dtypes)

    data = create_explainer_schema(
        explainer_schema_example=example,
        explainer=explainer,
        input_descriptions=input_descriptions,
        explain_input_example=explain_input_example,
    )
    with open(file_path, "w") as f:
        json.dump(jsonable_encoder(data), f)


def create_explainer_schema(
    explainer_schema_example: pandas.DataFrame,
    explainer: ShapExplainer,
    input_descriptions: List[Dict],
    explain_input_example: List[Dict],
) -> Dict:
    """Create schema for explainer input"""

    pred = explainer.func(explainer_schema_example)
    baseline, explanation = explainer.explain(explainer_schema_example)

    example = {
        "inputs": explain_input_example,
        "explanations": df_to_dict(explanation),
        "prediction": list(pred),
        "baseline": list(baseline),
    }
    # build schema
    schema = {"input_descriptions": input_descriptions, "example": example}
    return schema


def create_accuracy(
    func: Callable,
    x: pandas.DataFrame,
    y: pandas.Series,
    endpoint_name: str,
    profile_columns: List[str],
    kind: str,
) -> None:
    """Create accuracy profile for endpoint"""

    folder = mkdir(endpoint_name=endpoint_name, spec_path="accuracy")

    logging.info("Accuracy - Creating calibration plot")
    file_path = folder / "calibration.html"
    chart = calibration(func, x, y)
    chart.save(str(file_path))

    logging.info("Accuracy - Creating metrics table")
    file_path = folder / "metrics.json"
    metrics_table = metrics(func, x, y, kind)
    with open(file_path, "w") as f:
        f.write(metrics_table)

    logging.info("Accuracy - Finding largest errors")
    file_path = folder / "errors.json"
    errors_table = largest_errors(func, x, y, profile_columns)
    with open(file_path, "w") as f:
        f.write(errors_table)

    if kind == "binary":
        logging.info("Accuracy - Creating ROC curve")
        file_path = folder / "roc_curve.html"
        chart = roc_curve(func, x, y)
        chart.save(str(file_path))


def create_dependence(
    func: Callable,
    x: pandas.DataFrame,
    endpoint_name: str,
    profile_columns: List[str],
) -> None:
    """Create partial dependence graphs for all variables"""

    x = x.reset_index(drop=True)
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy/partialdep")

    for var in profile_columns:
        logging.info(f"Explanations - Creating partial dependence for {var}")
        var_sanitized = santize_var_names(var_name=var)
        file_path = folder / f"{var_sanitized}.html"
        try:
            chart = partialdep(func=func, x=x, var=var)
            chart.save(str(file_path))
        except AttributeError:
            logging.warning(f"Could not generate valid chart for {var}")


def create_expectations(
    func: Callable,
    x: pandas.DataFrame,
    y: pandas.Series,
    endpoint_name: str,
    profile_columns: List[str],
) -> None:
    """Create conditional expectations graphs for all variables"""

    x, y = x.reset_index(drop=True), y.reset_index(drop=True)
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy/condexp")

    for var in profile_columns:
        logging.info(f"Explanations - Creating conditional expectations for {var}")
        var_sanitized = santize_var_names(var_name=var)
        file_path = folder / f"{var_sanitized}.html"
        try:
            chart = condexp(func, x, y, var)
            chart.save(str(file_path))
        except AttributeError as e:
            logging.warning(f"Could not generate valid chart for {var}: {repr(e)}")
        except TypeError as e:
            # happens when object columns cannot be serialized to JSON
            # https://github.com/altair-viz/altair/issues/1355
            logging.warning(f"Could not generate valid chart for {var}: {repr(e)}")


def create_countplot(
    x: pandas.DataFrame, endpoint_name: str, profile_columns: List[str]
) -> None:
    """
    Create count plot graphs for all variables in profile_columns,
    creates folder structure and saves the plots to named files.
    """

    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy/countplot")

    for var in profile_columns:
        logging.info(f"Explanations - Creating count plot for {var}")
        var_sanitized = santize_var_names(var_name=var)
        file_name = var_sanitized + ".html"
        file_path = Path(folder, file_name)
        chart = countplot(x[var])
        chart.save(str(file_path))


def create_slice_loss(
    func: Callable,
    x: pandas.DataFrame,
    y: pandas.Series,
    endpoint_name: str,
    profile_columns: List[str],
    kind: str,
) -> None:
    """Create slice loss graphs for all variables"""

    if kind == "binary":
        loss = SliceLoss.ACCURACY.value
    elif kind == "regression":
        loss = SliceLoss.RMSE.value
    else:
        loss = None
    assert loss is not None

    x, y = x.reset_index(drop=True), y.reset_index(drop=True)
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy/sliceloss")

    for var in profile_columns:
        logging.info(f"Explanations - Creating slice loss for {var}")
        var_sanitized = santize_var_names(var_name=var)
        file_path = folder / f"{var_sanitized}.html"
        chart = slice_loss(func, x, y, var, loss)
        chart.save(str(file_path))


def create_importance(
    func: Callable,
    x: pandas.DataFrame,
    endpoint_name: str,
    profile_columns: List[str],
    kind: str,
) -> None:

    logging.info("Explanations - Calculating variable importance")
    if kind in ["regression", "binary"]:
        chart, varlist = varimp(func, x, profile_columns=profile_columns)
    else:
        raise NotImplementedError("Unknown endpoint kind:" + kind)

    # Save to disk
    folder = mkdir(endpoint_name=endpoint_name, spec_path="anatomy")

    file_path = folder / "varimp.html"
    chart.save(str(file_path))

    file_path = folder / "varlist.json"
    with open(file_path, "w") as f:
        json.dump(varlist, f)


def create_summary(
    endpoint_name: str,
    input_names: List[str],
    output_names: str,
    kind: str,
    path: Optional[str] = None,
    explain_path: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    position: Optional[int] = None,
) -> None:

    logging.info(f"Summary - creating endpoint summary for endpoint: {endpoint_name}")
    as_json = {
        "name": endpoint_name,
        "kind": kind,
        "inputs": input_names,
        "output": output_names,
        "tags": tags if tags else [],
        "position": position if position else 0,
    }
    if version is not None:
        as_json["version"] = version
    if path is not None:
        as_json["path"] = path
    if explain_path is not None:
        as_json["explain_path"] = explain_path

    # Save to disk
    folder = mkdir(endpoint_name=endpoint_name)
    with open(folder / "summary.json", "w") as summary:
        json.dump(as_json, summary)
