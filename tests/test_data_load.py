import pandas as pd
import pytest

from src.data import load

CALENDAR_HEADER = (
    "date,wm_yr_wk,weekday,wday,month,year,d,event_name_1,event_type_1,"
    "event_name_2,event_type_2,snap_CA,snap_TX,snap_WI\n"
)


def test_read_calendar_dtypes_and_dates(tmp_path):
    p = tmp_path / "calendar.csv"
    p.write_text(
        CALENDAR_HEADER
        + "2011-01-29,11101,Saturday,1,1,2011,d_1,,,,,0,0,0\n"
        + "2011-01-30,11101,Sunday,2,1,2011,d_2,SuperBowl,Sporting,,,0,0,0\n"
    )
    cal = load.read_calendar(p)
    assert str(cal["date"].dtype).startswith("datetime64")
    assert str(cal["wm_yr_wk"].dtype) == "int16"
    assert cal["event_name_1"].isna().sum() == 1  # missing = "no event", not an error


def test_read_sales_downcasts_to_int16(tmp_path):
    p = tmp_path / "sales.csv"
    p.write_text(
        "id,item_id,dept_id,cat_id,store_id,state_id,d_1,d_2\n"
        "A_CA_1,A,D1,C1,CA_1,CA,0,3\n"
        "B_CA_1,B,D1,C1,CA_1,CA,5,0\n"
    )
    sales = load.read_sales(p)
    assert str(sales["d_1"].dtype) == "int16"
    assert str(sales["store_id"].dtype) == "category"


def test_read_sales_rejects_values_that_overflow_int16(tmp_path):
    p = tmp_path / "sales.csv"
    p.write_text(
        "id,item_id,dept_id,cat_id,store_id,state_id,d_1\n"
        "A_CA_1,A,D1,C1,CA_1,CA,40000\n"
    )
    with pytest.raises(ValueError):
        load.read_sales(p)


def test_quality_report_detects_duplicates_and_missing():
    df = pd.DataFrame({"k": [1, 1, 2], "v": [1.0, 1.0, None]})
    rep = load.quality_report(df, key_cols=["k"])
    assert rep["full_row_duplicates"] == 1
    assert rep["key_duplicates"] == 1
    assert rep["columns_with_missing"] == {"v": 1}