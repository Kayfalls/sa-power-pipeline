select
    extracted_at,
    count(distinct region) as regions
from {{ ref('stg_status') }}
where extracted_at is not null
group by extracted_at
having count(distinct region) != 2