from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.materialized_view(name="gold.daily_sales", comment="Daily sales for BI")
def gold_daily_sales():
    orders = spark.read.table("silver.orders").where("order_status <> 'canceled'")
    items = spark.read.table("silver.order_items")
    return (
        orders.join(items, "order_id")
        .groupBy(F.to_date("purchase_ts").alias("order_date"))
        .agg(
            F.countDistinct("order_id").alias("orders"),
            F.round(F.sum("price"), 2).alias("revenue"),
            F.round(F.sum("freight_value"), 2).alias("freight"),
        )
    )