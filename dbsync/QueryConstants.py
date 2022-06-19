class QueryConstants:
    TENANT_FETCH_QUERY = "select mapper_pod, tenant_name, mapper_memory, tenant_id,  1 as active, mapper_cores from " \
                         "tenant where active = 1 and tenant_id in (0, :tenant_id) ; "
    SCHEMA_TABLE_QUERY = "select table_id,active ,display_name,cast(immutable as UNSIGNED) as immutable,name," \
                         "partition_type,step,visible,tenant_id,display_resource_key,availability from schema_table t " \
                         "where t.tenant_id in (0,:tenant_id) and active = 1; "
    SCHEMA_COLUMN_QUERY = "select * from schema_column where tenant_id in (0, :tenant_id);"
    TENANT_PROPERTY_QUERY = "select * from tenant_property where tenant_id in (0, :tenant_id)"
    EXECUTION_BUCKET_QUERY = "select * from execution_buckets where tenant_id in (0, :tenant_id);"
    EXECUTION_SUMMARY_GROUP_QUERY = "select * from execution_summary_group where tenant_id in (0, :tenant_id);"
    EXECUTION_SUMMARY_CUSTOMIZATION_QUERY = "select * from execution_summarycustomization where tenant_id in" \
                                            " (0, :tenant_id);"
    EXECUTION_STEP_QUERY = "select * from execution_step where revision = 0 and tenant_id = :tenant_id and active = 1 " \
                           "and step_id like 'bi_%'; "
