from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'

    truncate_sql = """
    TRUNCATE TABLE {final_table};
    """
    insert_sql = """
    INSERT INTO {final_table}{columns}
    (
    {query}
    );
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query="",
                 final_table="",
                 columns="",
                 truncate=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query = query
        self.final_table = final_table
        self.columns = columns
        self.truncate = truncate

    def execute(self, context):
        final_query = LoadDimensionOperator.insert_sql

        if self.truncate is True:
            logstring = 'Truncating dimension table: {}'
            self.log.info(logstring.format(self.final_table))
            final_query = LoadDimensionOperator.truncate_sql+final_query

        self.log.info('Loading dimension table: {}'.format(self.final_table))
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        final_query = final_query.format(
            final_table=self.final_table,
            columns=self.columns,
            query=self.query
        )
        redshift.run(final_query)
