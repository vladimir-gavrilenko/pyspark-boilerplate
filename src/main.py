#!/usr/bin/env python

import argparse
import logging
import sys
from typing import List

import requests  # to ensure that libraries are available
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

# to ensure that packages are available
from helpers.helper import WORDS_SEPARATOR


def extract(spark: SparkSession, path: str) -> DataFrame:
    return spark \
        .read \
        .text(path)


def transform(lines: DataFrame) -> DataFrame:
    words = lines \
        .select(F.split(F.col("value"), WORDS_SEPARATOR).alias("value")) \
        .select(F.explode("value").alias("value")) \
        .filter(F.col("value") != "")
    return words \
        .groupBy("value") \
        .count() \
        .sort("count", ascending=False)


def load(df: DataFrame, path: str) -> None:
    df \
        .write \
        .option("header", "true") \
        .csv(path)


def main(args: List[str]) -> None:
    log = logging.getLogger("main")
    log.info(requests.status_codes.codes)

    parser = argparse.ArgumentParser(
        description="Simple job for counting words in a text file"
    )
    parser.add_argument("--in-path", help="input file path")
    parser.add_argument("--out-path", help="path to write results")
    parsed_args = vars(parser.parse_args(args))

    spark = SparkSession \
        .builder \
        .getOrCreate()

    text_lines = extract(spark, parsed_args["in_path"])
    word_count = transform(text_lines)
    load(word_count, parsed_args["out_path"])


if __name__ == "__main__":
    main(sys.argv[1:])
