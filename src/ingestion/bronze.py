from pyspark import pipelines as dp
from pyspark.sql import functions as F

LANDING = "/Volumes/workspace/landing/raw"


def _autoloader(folder: str):
    """Incrementally read CSV files from a landing folder."""
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(f"{LANDING}/{folder}/")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
    )


@dp.table(name="bronze.orders", comment="Raw orders, append-only")
def bronze_orders():
    return _autoloader("orders")


@dp.table(name="bronze.order_items", comment="Raw order items, append-only")
def bronze_order_items():
    return _autoloader("order_items")