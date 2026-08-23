
  
    
    

    create  table
      "schemapilot"."main"."fct_orders__dbt_tmp"
  
    as (
      with orders as (
    select * from "schemapilot"."main"."stg_orders"
),

customers as (
    select * from "schemapilot"."main"."stg_customers"
),

order_lines as (
    select * from "schemapilot"."main"."stg_order_lines"
),

products as (
    select * from "schemapilot"."main"."stg_products"
),

line_aggregates as (
    select
        order_id,
        sum(quantity) as total_quantity,
        count(distinct product_id) as distinct_products_count
    from order_lines
    group by order_id
),

final as (
    select
        o.order_id,
        o.customer_id,
        c.customer_name,
        c.country,
        o.order_date,
        o.status,
        coalesce(l.total_quantity, 0) as total_quantity,
        coalesce(l.distinct_products_count, 0) as distinct_products_count
    from orders o
    left join customers c on o.customer_id = c.customer_id
    left join line_aggregates l on o.order_id = l.order_id
)

select * from final
    );
  
  