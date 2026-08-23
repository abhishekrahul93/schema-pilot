with source as (
    select * from "schemapilot"."main"."raw_products"
)
select
    product_id,
    trim(product_name) as product_name,
    coalesce(category, 'Uncategorized') as category,
    try_cast(price as decimal(10,2)) as price,
    try_cast(cost as decimal(10,2)) as cost
from source
where product_id is not null