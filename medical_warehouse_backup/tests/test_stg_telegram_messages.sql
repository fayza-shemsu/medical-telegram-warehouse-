-- Ensure no null message_id
select *
from {{ ref('stg_telegram_messages') }}
where message_id is null;

-- Ensure no null message_text
select *
from {{ ref('stg_telegram_messages') }}
where message_text is null;
