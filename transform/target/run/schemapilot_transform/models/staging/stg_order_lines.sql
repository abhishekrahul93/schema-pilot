
  
  create view "schemapilot"."main"."stg_order_lines__dbt_tmp" as (
    with source as (
    select * from "schemapilot"."main"."raw_order_lines"
)
select
    line_id,
    order_id,
    product_id,
    coalesce(quantity, 1) as quantity
from source
where line_id is not null and order_id is not null
  );
