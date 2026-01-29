with messages as (
    select *
    from {{ ref('stg_telegram_messages') }}
),
channels as (
    select *
    from {{ ref('dim_channels') }}
),
dates as (
    select *
    from {{ ref('dim_dates') }}
)

select
    m.message_id,
    c.channel_key,
    d.date_key,
    m.message_text,
    length(m.message_text) as message_length,
    m.view_count,
    m.forward_count,
    m.has_image
from messages m
join channels c on m.channel_name = c.channel_name
join dates d on m.message_date::date = d.full_date
