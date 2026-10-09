{{ config(
    materialized = 'incremental',
    unique_key = 'status_key',
    incremental_strategy = 'merge'
    )
}}

with source as (
    select
        safe.parse_timestamp('%Y%m%dT%H%M%SZ', cast(extracted_at as string)) as extracted_ts,
        region,
        region_name,
        stage,
        stage_updated
    from {{ ref('stg_status') }}
    where extracted_at is not null
),

keyed as (
    select
        concat(region, '|', cast(extracted_ts as string)) as status_key,
        extracted_ts,
        region,
        region_name,
        stage,
        stage_updated
    from source
    where extracted_ts is not null
    {% if is_incremental() %}
        and extracted_ts > (select max(extracted_ts) from {{ this }})
    {% endif %}
),

deduped as (
    select 
        *, 
        row_number() over (
            partition by status_key
            order by stage_updated desc
        ) as row_rank
    from keyed
)

select 
    status_key,
    extracted_ts,
    region,
    region_name,
    stage,
    stage_updated
from deduped
where row_rank = 1