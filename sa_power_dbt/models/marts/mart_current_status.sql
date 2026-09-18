with ranked as (
    select
        extracted_at,
        region,
        region_name,
        stage,
        stage_updated,
        next_stages,
        row_number() over (
            partition by region
            order by extracted_at desc
        ) as row_rank
    from {{ ref('stg_status') }}
    where extracted_at is not null
)

select
    extracted_at,
    region,
    region_name,
    stage,
    stage_updated,
    next_stages
from ranked
where row_rank = 1