with source as (
    select * from {{ source('raw', 'status')}}
),

flattened as (
    select
    extracted_at,
        'eskom' as region,
        status.eskom.name as region_name,
        status.eskom.stage as stage,
        status.eskom.stage_updated as stage_updated,
        status.eskom.next_stages as next_stages,
    from source

    union all

    select
    extracted_at,
        'capetown' as region,
        status.capetown.name as region_name,
        status.capetown.stage as stage,
        status.capetown.stage_updated as stage_updated,
        status.capetown.next_stages as next_stages,
    from source
)

select * from flattened
