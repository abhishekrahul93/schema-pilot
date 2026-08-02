with source as (
    select * from "schemapilot"."main"."raw_orders"
),
cleaned as (
    select
        order_id,
        customer_id,
        try_cast(order_date as timestamp) as order_date,
        lower(trim(status)) as status,
        row_number() over (partition by order_id order by order_date desc) as rn
    from source
    where order_id is not null
)
select
    order_id,
    customer_id,
    order_date,
    status
from cleaned
where rn = 1