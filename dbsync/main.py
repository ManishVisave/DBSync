from DBHelper import DBHelper
from ConfigParserHelper import ConfigParserHelper
from QueryConstants import QueryConstants
from RedashHelper import RedashHelper
import pandas as pd
import argparse


def save_redash_to_local(query, table_name):
    required_tables = ['tenant', 'schema_table', 'schema_column', 'tenant_property']
    print(f'\n\nProcessing table : [{table_name}]')
    data = redash_helper.get_records_from_table(query)
    if len(data) != 0:
        df = pd.DataFrame(data=data)
        if table_name == 'execution_step':
            df.to_csv(f"{table_name}_{args['tenant_id']}.csv", index=False)
            print(f"Saved {table_name}_{args['tenant_id']}.csv file in project root")
        else:
            db_helper.save_data_to_DB(df, table_name)
    elif len(data) == 0 and table_name in required_tables:
        raise RuntimeError(f'{table_name} table should not have 0 records')


def get_formatted_query(query):
    return query.replace(':tenant_id', args['tenant_id'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Db Sync Tool')
    parser.add_argument('-c', '--config-file-name', help='Name of the config file', required=True)
    parser.add_argument('-t', '--tenant-id', help='Tenant Id for db sync', required=True)
    parser.add_argument('-s', '--source', choices=['EU_PROD', 'GCP_PROD', 'GREEN_PROD'],
                        help='PROD Env where tenant data is stored', required=True)
    parser.add_argument('-l', "--table-list", nargs="+",
                        default=["tenant", "schema_table", "schema_column", "tenant_property", "execution_buckets",
                                 "execution_summary_group", "execution_summarycustomization", "execution_step"])
    args = vars(parser.parse_args())
    print(f"Tables: {len(args['table_list'])}")
    config_helper = ConfigParserHelper(args['config_file_name'])
    db_helper = DBHelper(config_helper)
    redash_helper = RedashHelper(config_helper, args['source'])

    save_redash_to_local(get_formatted_query(QueryConstants.TENANT_FETCH_QUERY), 'tenant')
    save_redash_to_local(get_formatted_query(QueryConstants.SCHEMA_TABLE_QUERY), 'schema_table')
    save_redash_to_local(get_formatted_query(QueryConstants.SCHEMA_COLUMN_QUERY), 'schema_column')
    save_redash_to_local(get_formatted_query(QueryConstants.TENANT_PROPERTY_QUERY), 'tenant_property')
    save_redash_to_local(get_formatted_query(QueryConstants.EXECUTION_BUCKET_QUERY), 'execution_buckets')
    save_redash_to_local(get_formatted_query(QueryConstants.EXECUTION_SUMMARY_GROUP_QUERY), 'execution_summary_group')
    save_redash_to_local(get_formatted_query(QueryConstants.EXECUTION_SUMMARY_CUSTOMIZATION_QUERY), 'execution_summarycustomization')
    save_redash_to_local(get_formatted_query(QueryConstants.EXECUTION_STEP_QUERY), 'execution_step')

    print(f'\n\nAll tables processed')