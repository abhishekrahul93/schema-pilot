with source as (
    select * from "schemapilot"."main"."raw_customers"
),

cleaned as (
    select
        customer_id,
        trim(name) as customer_name,
        case 
            when email is null or trim(email) = '' then 'unknown@placeholder.com'
            else lower(trim(email))
        end as email,
        case 
            when upper(trim(country)) in ('USA', 'UNITED STATES') then 'United States'
            when country is null or trim(country) = '' then 'Unknown'
            else upper(trim(country))
        end as country,
        try_cast(signup_date as date) as signup_date
    from source
    where customer_id is not null
),

deduped as (
    select *,
           row_number() over (partition by customer_id order by signup_date desc) as rn
    from cleaned
)

select 
    customer_id,
    customer_name,
    email,
    country,
    signup_date
from deduped
where rn = 1