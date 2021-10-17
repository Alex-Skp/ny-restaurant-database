from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    template_fields = ['s3_bucket']

    staging_sql_template = """
    TRUNCATE {table};
    COPY {table}
    FROM '{s3_bucket}'
    ACCESS_KEY_ID '{key_id}'
    SECRET_ACCESS_KEY '{secret_key}'
    REGION '{region}'
    {extra_params};
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_conn_id="",
                 table="",
                 s3_bucket="",
                 region="",
                 extra_params="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.region = region
        self.extra_params = extra_params

    def execute(self, context):
        aws_hook = AwsHook(aws_conn_id=self.aws_conn_id)
        aws_credentials = aws_hook.get_credentials()

        logstring = 'Staging to redshift {} from {}'
        self.log.info(logstring.format(self.table, self.s3_bucket))
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        s3_path = self.s3_bucket.format(**context)

        staging_sql = StageToRedshiftOperator.staging_sql_template.format(
            table=self.table,
            s3_bucket=s3_path,
            key_id=aws_credentials.access_key,
            secret_key=aws_credentials.secret_key,
            region=self.region,
            extra_params=self.extra_params
        )
        redshift.run(staging_sql)
