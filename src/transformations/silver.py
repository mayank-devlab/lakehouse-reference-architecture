from pyspark import pipelines as dp
from pyspark.sql import functions as F


@dp.table(name="silver.orders", comment="Cleaned, typed orders")
@dp.expect_or_drop("order_id_not_null", "order_id IS NOT NULL")
@dp.expect_or_drop("customer_id_not_null", "customer_id IS NOT NULL")
@dp.expect("purchase_ts_present", "purchase_ts IS NOT NULL")
def silver_orders():
    return (
        spark.readStream.table("bronze.orders")
        .select(
            "order_id",
            "customer_id",
            "order_status",
            F.to_timestamp("order_purchase_timestamp").alias("purchase_ts"),
            F.to_timestamp("order_delivered_customer_date").alias("delivered_ts"),
        )
        .dropDuplicates(["order_id"])
    )


@dp.table(name="silver.order_items", comment="Cleaned, typed order items")
@dp.expect_or_drop("order_id_not_null", "order_id IS NOT NULL")
@dp.expect_or_drop("valid_price", "price IS NOT NULL AND price >= 0")
@dp.expect("valid_freight", "freight_value >= 0")
def silver_order_items():
    return spark.readStream.table("bronze.order_items").select(
        "order_id",
        F.col("order_item_id").cast("int"),
        "product_id",
        "seller_id",
        F.col("price").cast("double"),
        F.col("freight_value").cast("double"),
    )

@dp.table(
    name="silver.customers",
    comment="Cleaned customers; identifiers masked for non-privileged users",
    schema="""
        customer_id STRING,
        customer_unique_id STRING MASK workspace.governance.mask_id,
        zip_prefix STRING MASK workspace.governance.mask_zip,
        city STRING,
        state STRING
    """,
)
@dp.expect_or_drop("customer_id_not_null", "customer_id IS NOT NULL")
@dp.expect("state_is_two_letters", "length(state) = 2")
def silver_customers():
    return (
        spark.readStream.table("bronze.customers")
        .select(
            "customer_id",
            "customer_unique_id",
            F.lpad(F.col("customer_zip_code_prefix").cast("string"), 5, "0").alias("zip_prefix"),
            F.col("customer_city").alias("city"),
            F.col("customer_state").alias("state"),
        )
        .dropDuplicates(["customer_id"])
    )