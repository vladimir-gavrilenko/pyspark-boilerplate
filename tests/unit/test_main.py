from pathlib import Path

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StringType

import main


def test_extract(spark_session: SparkSession) -> None:
    in_path = "tests/unit/some_text_file.txt"
    expected_df = spark_session.createDataFrame([
        "hello world world",
        "hello world",
        "",
        "test",
    ], schema=StringType())
    df = main.extract(spark_session, in_path)
    assert df.collect() == expected_df.collect()


def test_transform(spark_session: SparkSession) -> None:
    df = spark_session.createDataFrame([
        "a b cc", " a b ", "a", ""
    ], schema=StringType())
    expected_transformed_df = spark_session.createDataFrame([
        ("a", 3),
        ("b", 2),
        ("cc", 1)
    ], schema=["value", "count"])
    transformed_df = main.transform(df)
    assert transformed_df.collect() == expected_transformed_df.collect()


def test_load(spark_session: SparkSession, tmp_path: Path) -> None:
    df = spark_session.createDataFrame([
        ("aaa", 100), ("bbb", 10)
    ], schema=["value", "count"])
    out_path = str(tmp_path.absolute() / "load")
    main.load(df, out_path)
    written_df = _read_csv(spark_session, out_path)
    assert written_df.collect() == df.collect()


def test_main(spark_session: SparkSession, tmp_path: Path) -> None:
    expected_df = spark_session.createDataFrame([
        ("world", 3), ("hello", 2), ("test", 1)
    ], schema=["value", "count"])
    in_path = "tests/unit/some_text_file.txt"
    out_path = str(tmp_path.absolute() / "main")
    args = ["--in-path", in_path, "--out-path", out_path]
    main.main(args)
    written_df = _read_csv(spark_session, out_path)
    assert written_df.collect() == expected_df.collect()


def _read_csv(spark: SparkSession, path: str) -> DataFrame:
    return spark \
        .read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(path)
