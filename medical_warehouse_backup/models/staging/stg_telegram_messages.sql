with raw as (

    select
        message_id,
        channel_name,
        message_date::timestamp as message_date,
        message_text,
        views::int as view_count,
        forwards::int as forward_count,
        case when has_media = 'True' then 1 else 0 end as has_image,
        image_path
    from {{ source('raw', 'telegram_messages') }}

)

select * from raw
where message_id is not null
  and message_text is not null
