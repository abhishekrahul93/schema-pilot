with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

order_lines as (
    select * from {{ ref('stg_order_lines') }}
),

products as (
    select * from {{ ref('stg_products') }}
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
