# PySpark Boilerplate

A template project for writing PySpark jobs.

## Prerequisites
* python3.7
* make
* zip

## Usage
1. To show available commands, run `make` or `make help`.
1. Prepare dev environment
   ```
   make prepare-dev
   ```
1. Build
   ```
   make build
   ```
1. Submit
    ```
   $SPARK_HOME/bin/spark-submit \
       --name "word-count" \
       --master "local[2]" \
       --py-files dist/packages.zip,dist/libs.zip \
       dist/main.py \
       --in-path file://$(pwd)/tests/unit/some_text_file.txt \
       --out-path file://$(pwd)/build/out
    ```
